from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from spider_rose.agents import default_agent_markdown, slugify_agent_name
from spider_rose.google_careers import scrape_google_careers_jobs, store_google_careers_jobs
from spider_rose.project import create_agent, find_or_init_project_root, set_default_agent


class AgentCreate(BaseModel):
    name: str


class AgentUpdate(BaseModel):
    markdown: str


class WorkflowCard(BaseModel):
    id: str
    agent: str
    x: float = 0
    y: float = 0


class WorkflowLayoutUpdate(BaseModel):
    cards: list[WorkflowCard] = Field(default_factory=list)
    positions: dict[str, dict[str, float]] = Field(default_factory=dict)


def create_app(project_root: Path | None = None):
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import HTMLResponse

    root = project_root or find_or_init_project_root()
    app = FastAPI(title="Spider Rose Local API")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return APP_HTML

    @app.get("/workflow", response_class=HTMLResponse)
    def workflow() -> str:
        return APP_HTML

    @app.get("/api/project")
    def project() -> dict:
        return {"name": "Spider Rose", "root": str(root)}

    @app.get("/api/agents")
    def agents() -> list[dict]:
        return [
            {"name": path.stem, "path": str(path.relative_to(root)), "markdown": path.read_text(encoding="utf-8")}
            for path in sorted((root / "agents").glob("*.md"))
        ]

    @app.post("/api/agents")
    def create(payload: AgentCreate) -> dict:
        try:
            path = create_agent(root, payload.name)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {"name": path.stem, "path": str(path.relative_to(root)), "markdown": path.read_text(encoding="utf-8")}

    @app.put("/api/agents/{name}")
    def update(name: str, payload: AgentUpdate) -> dict:
        try:
            slug = slugify_agent_name(name)
            path = root / "agents" / f"{slug}.md"
            if not path.exists():
                raise HTTPException(status_code=404, detail=f"Agent not found: agents/{slug}.md")
            if not payload.markdown.strip():
                raise HTTPException(status_code=400, detail="Agent Markdown cannot be empty.")
            path.write_text(payload.markdown, encoding="utf-8")
            return {"name": slug, "path": str(path.relative_to(root)), "markdown": payload.markdown}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Could not save agent `{name}`: {exc}") from exc

    @app.post("/api/agents/{name}/default")
    def make_default(name: str) -> dict:
        try:
            set_default_agent(root, name)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {"default_agent": slugify_agent_name(name)}

    @app.get("/api/templates/agent")
    def agent_template(name: str = "new-agent") -> dict:
        return {"markdown": default_agent_markdown(name)}

    @app.get("/api/workflow-layout")
    def workflow_layout() -> dict:
        return _read_workflow_layout(root)

    @app.put("/api/workflow-layout")
    def save_workflow_layout(payload: WorkflowLayoutUpdate) -> dict:
        known_agents = {path.stem for path in (root / "agents").glob("*.md")}
        clean_cards: list[dict] = []
        seen_ids: set[str] = set()

        if payload.cards:
            for card in payload.cards:
                agent = slugify_agent_name(card.agent)
                card_id = _clean_card_id(card.id)
                if agent not in known_agents or card_id in seen_ids:
                    continue
                seen_ids.add(card_id)
                clean_cards.append({"id": card_id, "agent": agent, "x": float(card.x), "y": float(card.y)})
        else:
            for name, point in payload.positions.items():
                agent = slugify_agent_name(name)
                card_id = f"{agent}-1"
                if agent not in known_agents or card_id in seen_ids:
                    continue
                seen_ids.add(card_id)
                clean_cards.append(
                    {
                        "id": card_id,
                        "agent": agent,
                        "x": float(point.get("x", 0)),
                        "y": float(point.get("y", 0)),
                    }
                )

        path = root / "workflow-layout.json"
        path.write_text(json.dumps({"cards": clean_cards}, indent=2), encoding="utf-8")
        return {"cards": clean_cards, "positions": _cards_to_positions(clean_cards), "path": str(path.relative_to(root))}

    @app.post("/api/demo/google-careers/run")
    def run_google_careers_demo() -> dict:
        try:
            scrape_result = scrape_google_careers_jobs(query="software engineer", location="India", limit=5)
            if not scrape_result.jobs:
                return {
                    "ok": False,
                    "error": "No Google Careers jobs were found in the fetched page.",
                    "resource_use": {
                        "network_requests": scrape_result.network_requests,
                        "duration_ms": scrape_result.duration_ms,
                        "stored_file_size_bytes": 0,
                    },
                }
            store_result = store_google_careers_jobs(root, scrape_result.jobs)
            stored_path = root / store_result.storage_path
            return {
                "ok": True,
                "store_result": store_result.__dict__,
                "resource_use": {
                    "network_requests": scrape_result.network_requests,
                    "duration_ms": scrape_result.duration_ms,
                    "stored_file_size_bytes": stored_path.stat().st_size if stored_path.exists() else 0,
                },
            }
        except Exception as exc:
            return {
                "ok": False,
                "error": f"Could not scrape Google Careers: {exc}",
                "resource_use": {"network_requests": 1, "duration_ms": 0, "stored_file_size_bytes": 0},
            }

    return app


def _read_workflow_layout(root: Path) -> dict:
    path = root / "workflow-layout.json"
    if not path.exists():
        return {"positions": {}, "path": str(path.relative_to(root))}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"positions": {}, "path": str(path.relative_to(root)), "warning": "Ignored malformed workflow-layout.json."}
    cards = data.get("cards", [])
    if not isinstance(cards, list):
        cards = []
    clean_cards = []
    for card in cards:
        if not isinstance(card, dict):
            continue
        clean_cards.append(
            {
                "id": _clean_card_id(str(card.get("id", ""))),
                "agent": slugify_agent_name(str(card.get("agent", ""))),
                "x": float(card.get("x", 0)),
                "y": float(card.get("y", 0)),
            }
        )
    if not clean_cards:
        positions = data.get("positions", {})
        if not isinstance(positions, dict):
            positions = {}
        clean_cards = [
            {"id": f"{slugify_agent_name(name)}-1", "agent": slugify_agent_name(name), "x": float(point.get("x", 0)), "y": float(point.get("y", 0))}
            for name, point in positions.items()
            if isinstance(point, dict)
        ]
    return {"cards": clean_cards, "positions": _cards_to_positions(clean_cards), "path": str(path.relative_to(root))}


def _clean_card_id(value: str) -> str:
    clean = "".join(char for char in value if char.isalnum() or char in "-_")
    return clean[:80] or "card"


def _cards_to_positions(cards: list[dict]) -> dict[str, dict[str, float]]:
    positions: dict[str, dict[str, float]] = {}
    for card in cards:
        positions.setdefault(card["agent"], {"x": card["x"], "y": card["y"]})
    return positions


BASE_STYLE = """
    :root { color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    body { margin: 0; background: #080808; color: #f5f5f5; }
    button, input, textarea { font: inherit; }
    a { color: inherit; text-decoration: none; }
    button { border: 1px solid #f5f5f5; border-radius: 6px; padding: 9px 11px; background: #f5f5f5; color: #080808; cursor: pointer; white-space: nowrap; }
    button:hover { background: #e5e5e5; }
    button.secondary, a.nav-link { background: #151515; color: #e5e5e5; border: 1px solid #3a3a3a; border-radius: 6px; padding: 9px 11px; }
    button.secondary:hover, a.nav-link:hover { border-color: #5a5a5a; color: #ffffff; background: #1b1b1b; }
    .muted { color: #a3a3a3; font-size: 13px; }
    .row { display: flex; gap: 8px; }
    .topnav { display: flex; align-items: center; gap: 8px; margin-bottom: 18px; }
    .topnav strong { margin-right: auto; }
"""


APP_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Spider Rose</title>
  <style>
/*BASE_STYLE*/
    body { overflow: hidden; }
    .app { height: 100vh; display: grid; grid-template-columns: 320px 1fr; }
    aside { border-right: 1px solid #2a2a2a; padding: 18px; background: #111111; overflow-y: auto; }
    main { position: relative; overflow: hidden; }
    h1 { font-size: 22px; margin: 0 0 4px; }
    h2 { font-size: 15px; margin: 18px 0 10px; }
    input { width: 100%; box-sizing: border-box; border: 1px solid #3a3a3a; border-radius: 6px; padding: 9px 10px; background: #0f0f0f; color: #f5f5f5; outline: none; }
    input:focus { border-color: #777777; }
    .tabs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 18px 0; }
    .tab { border: 1px solid #2a2a2a; border-radius: 6px; padding: 9px 8px; background: #151515; color: #bdbdbd; cursor: pointer; }
    .tab.active { border-color: #f5f5f5; color: #ffffff; background: #1b1b1b; }
    .panel { display: none; }
    .panel.active { display: block; }
    .agent { width: 100%; text-align: left; margin: 6px 0; background: #151515; color: #e5e5e5; border-color: #2a2a2a; }
    .agent:hover { border-color: #3a3a3a; background: #1b1b1b; }
    .agent.active { border-color: #bdbdbd; box-shadow: inset 3px 0 0 #f5f5f5; color: #ffffff; }
    textarea { width: 100%; min-height: 300px; box-sizing: border-box; resize: vertical; border: 1px solid #2a2a2a; border-radius: 8px; padding: 14px; background: #0f0f0f; color: #f5f5f5; line-height: 1.5; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 14px; outline: none; }
    textarea:focus { border-color: #5a5a5a; }
    .toolbar { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin: 12px 0; }
    .status { min-height: 20px; color: #a3a3a3; font-size: 13px; }
    .canvas { position: absolute; inset: 0; overflow: hidden; background-color: #080808; background-image: linear-gradient(#1d1d1d 1px, transparent 1px), linear-gradient(90deg, #1d1d1d 1px, transparent 1px), linear-gradient(#111111 1px, transparent 1px), linear-gradient(90deg, #111111 1px, transparent 1px); background-size: 120px 120px, 120px 120px, 24px 24px, 24px 24px; }
    .canvas-layer { position: absolute; inset: 0; }
    .agent-card { position: absolute; width: 210px; min-height: 76px; box-sizing: border-box; border: 1px solid #3a3a3a; border-radius: 8px; padding: 12px; background: #111111; color: #f5f5f5; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28); cursor: grab; user-select: none; }
    .agent-card:hover { border-color: #6a6a6a; }
    .agent-card:active { cursor: grabbing; }
    .agent-card strong { display: block; font-size: 15px; margin-bottom: 7px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .agent-card .description { color: #a3a3a3; font-size: 12px; line-height: 1.35; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .workflow-demo { position: absolute; inset: 0; pointer-events: none; }
    .workflow-card { position: absolute; width: 230px; min-height: 92px; box-sizing: border-box; border: 1px solid #3a3a3a; border-radius: 8px; padding: 12px; background: #101010; color: #f5f5f5; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28); cursor: pointer; pointer-events: auto; }
    .workflow-card:hover { border-color: #707070; }
    .workflow-card strong { display: block; font-size: 15px; margin-bottom: 7px; }
    .workflow-card .description { color: #a3a3a3; font-size: 12px; line-height: 1.35; }
    .state-pill { display: inline-flex; align-items: center; margin-top: 10px; border: 1px solid #333333; border-radius: 999px; padding: 4px 8px; color: #bdbdbd; font-size: 12px; }
    .state-pill.running { border-color: #8a7c42; color: #f5df82; background: #211d0d; }
    .state-pill.success { border-color: #3f6f56; color: #96e0b7; background: #0d2017; }
    .state-pill.failed { border-color: #7a3d3d; color: #f0a0a0; background: #241010; }
    .workflow-edge { position: absolute; left: 324px; top: 126px; width: 172px; height: 1px; background: #4a4a4a; pointer-events: none; }
    .workflow-edge::after { content: ""; position: absolute; right: -1px; top: -5px; border-left: 9px solid #4a4a4a; border-top: 5px solid transparent; border-bottom: 5px solid transparent; }
    .workflow-edge-label { position: absolute; left: 376px; top: 96px; border: 1px solid #2f2f2f; border-radius: 999px; padding: 4px 8px; background: #111111; color: #d4d4d4; font-size: 12px; pointer-events: none; }
    .inspector-section { margin-bottom: 14px; }
    .inspector-label { color: #8f8f8f; font-size: 12px; margin-bottom: 5px; }
    .inspector-value { color: #f5f5f5; font-size: 14px; line-height: 1.45; word-break: break-word; }
    .inspector-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; margin-bottom: 14px; }
    .inspector-metric { border: 1px solid #262626; border-radius: 8px; padding: 10px; background: #0d0d0d; }
    .inspector-metric strong { display: block; font-size: 20px; line-height: 1; margin-bottom: 5px; }
    .sample-link { display: block; border: 1px solid #262626; border-radius: 8px; padding: 10px; margin-top: 8px; background: #0d0d0d; }
    .sample-link span { display: block; color: #a3a3a3; font-size: 12px; margin-top: 4px; word-break: break-all; }
    .floating { position: absolute; z-index: 10; display: flex; gap: 8px; }
    .floating.left { left: 16px; top: 16px; }
    .icon-button { width: 40px; height: 40px; display: inline-flex; align-items: center; justify-content: center; border-radius: 8px; padding: 0; font-size: 20px; line-height: 1; }
    .agent-picker { position: absolute; z-index: 11; top: 64px; left: 16px; width: 240px; border: 1px solid #2a2a2a; border-radius: 8px; padding: 10px; background: #111111; box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35); display: none; }
    .agent-picker.open { display: block; }
    .picker-option { width: 100%; margin: 4px 0; text-align: left; background: #151515; color: #e5e5e5; border-color: #2a2a2a; }
    .detail-popover { position: absolute; z-index: 12; top: 72px; right: 16px; bottom: 16px; width: min(520px, calc(100vw - 360px)); overflow: hidden; border: 1px solid #2a2a2a; border-radius: 8px; background: #101010; box-shadow: 0 24px 70px rgba(0, 0, 0, 0.45); display: none; }
    .detail-popover.open { display: grid; grid-template-rows: auto auto 1fr; }
    .detail-header { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding: 12px; border-bottom: 1px solid #242424; }
    .detail-header strong { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .detail-tabs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; padding: 10px 12px; border-bottom: 1px solid #242424; }
    .detail-tab { border: 1px solid #2a2a2a; background: #151515; color: #bdbdbd; }
    .detail-tab.active { border-color: #f5f5f5; color: #ffffff; background: #1b1b1b; }
    .detail-body { padding: 12px; overflow: auto; }
    .detail-body pre { margin: 0; white-space: pre-wrap; word-break: break-word; color: #e5e5e5; font: 13px/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
    .detail-actions { display: flex; gap: 8px; flex-shrink: 0; }
    @media (max-width: 860px) { .app { grid-template-columns: 1fr; grid-template-rows: 44vh 56vh; } aside { border-right: 0; border-bottom: 1px solid #2a2a2a; } textarea { min-height: 180px; } }
    @media (max-width: 860px) { .detail-popover { top: auto; left: 16px; right: 16px; width: auto; max-height: 48vh; } }
  </style>
</head>
<body>
  <div class="app">
    <aside>
      <h1>Spider Rose</h1>
      <div class="muted">Two-block web demo.</div>
      <div class="tabs" role="tablist">
        <button class="tab" id="tabAgents" data-tab="agents">Agents</button>
        <button class="tab" id="tabWorkflow" data-tab="workflow">Workflow</button>
      </div>
      <div class="panel" id="panelAgents">
        <h2>New Agent</h2>
        <div class="row">
          <input id="agentName" placeholder="google-careers-scraper" />
          <button id="createBtn">Create</button>
        </div>
        <h2>Agents</h2>
        <div id="agents"></div>
        <div class="toolbar">
          <div>
            <h2 id="title">Select an agent</h2>
            <div class="muted" id="path">Agents are stored as Markdown files in this project.</div>
          </div>
        </div>
        <textarea id="editor" spellcheck="false" placeholder="Create or select an agent."></textarea>
        <div class="row" style="margin-top: 10px;">
          <button class="secondary" id="defaultBtn">Set Default</button>
          <button id="saveBtn">Save</button>
        </div>
        <div class="status" id="status"></div>
      </div>
      <div class="panel" id="panelWorkflow">
        <h2>Workflow</h2>
        <p class="muted">Google Careers demo. Scrapes current job results and saves job links.</p>
        <button id="runDemoBtn">Run demo</button>
        <div class="status" id="demoStatus"></div>
      </div>
    </aside>
    <main>
      <section class="canvas" id="canvas" aria-label="Workflow canvas">
        <div class="canvas-layer" id="canvasLayer"></div>
        <div class="workflow-demo" id="workflowDemoLayer"></div>
      </section>
      <div class="floating left">
        <button class="icon-button" id="addCardBtn" title="Add agent to canvas" aria-label="Add agent to canvas">+</button>
      </div>
      <div class="agent-picker" id="agentPicker"></div>
      <section class="detail-popover" id="detailPopover" aria-label="Agent details">
        <div class="detail-header">
          <strong id="detailTitle">Agent</strong>
          <div class="detail-actions">
            <button class="secondary" id="duplicateCardBtn">Duplicate</button>
            <button class="secondary" id="closeDetailBtn" aria-label="Close agent details">Close</button>
          </div>
        </div>
        <div class="detail-tabs">
          <button class="detail-tab active" data-detail="markdown">Markdown</button>
          <button class="detail-tab" data-detail="langgraph">LangGraph</button>
        </div>
        <div class="detail-body" id="detailBody"></div>
      </section>
    </main>
  </div>
  <script>
    let agents = [];
    let current = null;
    let cards = [];
    let dragging = null;
    let activeCardId = null;
    let activeDetailTab = 'markdown';
    let activeTab = 'agents';
    let demoRunState = 'Idle';
    let demoStoreResult = null;
    const $ = (id) => document.getElementById(id);
    const canvasLayer = $('canvasLayer');
    const workflowDemoLayer = $('workflowDemoLayer');

    async function loadAgents() {
      const res = await fetch('/api/agents');
      if (!res.ok) {
        $('status').textContent = await readError(res, 'Could not load agents.');
        return;
      }
      agents = await res.json();
      renderAgents();
      await loadLayout();
      if (!current && agents[0]) selectAgent(agents[0].name);
    }

    function renderAgents() {
      $('agents').innerHTML = agents.map((agent) => (
        `<button class="agent ${current === agent.name ? 'active' : ''}" onclick="selectAgent('${agent.name}')">${agent.name}</button>`
      )).join('');
    }

    function selectAgent(name) {
      current = name;
      const agent = agents.find((item) => item.name === name);
      $('title').textContent = agent ? agent.name : 'Select an agent';
      $('path').textContent = agent ? `Stored at ${agent.path}` : 'Agents are stored as Markdown files in this project.';
      $('editor').value = agent ? agent.markdown : '';
      $('status').textContent = '';
      renderAgents();
    }

    async function loadLayout() {
      const res = await fetch('/api/workflow-layout');
      if (!res.ok) return;
      const layout = await res.json();
      cards = Array.isArray(layout.cards) ? layout.cards : cardsFromPositions(layout.positions || {});
      applyDefaultCards();
      renderCanvas();
    }

    function applyDefaultCards() {
      const knownAgents = new Set(agents.map((agent) => agent.name));
      cards = cards.filter((card) => knownAgents.has(card.agent));
      agents.forEach((agent, index) => {
        if (!cards.some((card) => card.agent === agent.name)) {
          cards.push({
            id: nextCardId(agent.name),
            agent: agent.name,
            x: 70 + (index % 3) * 260,
            y: 72 + Math.floor(index / 3) * 150
          });
        }
      });
    }

    function renderCanvas() {
      canvasLayer.innerHTML = activeTab === 'workflow' ? '' : cards.map((card) => {
        const agent = agents.find((item) => item.name === card.agent);
        if (!agent) return '';
        return `<article class="agent-card" data-card-id="${card.id}" data-agent="${agent.name}" style="transform: translate(${card.x}px, ${card.y}px);">
          <strong title="${escapeHtml(agent.name)}">${escapeHtml(agent.name)}</strong>
          <div class="description">${escapeHtml(limitText(agentDescription(agent.markdown), 78))}</div>
        </article>`;
      }).join('');
      document.querySelectorAll('.agent-card').forEach((card) => {
        card.addEventListener('pointerdown', startDrag);
      });
      renderAgentPicker();
      renderWorkflowDemo();
      if (activeCardId) renderDetail();
    }

    function renderWorkflowDemo() {
      if (activeTab !== 'workflow') {
        workflowDemoLayer.innerHTML = '';
        return;
      }
      const scraperState = demoRunState === 'Running' ? 'Running' : demoRunState === 'Success' ? 'Success' : demoRunState === 'Failed' ? 'Failed' : 'Idle';
      const storeState = demoRunState === 'Success' ? 'Success' : demoRunState === 'Running' ? 'Running' : 'Idle';
      workflowDemoLayer.innerHTML = `
        <article class="workflow-card" data-demo-block="scraper" style="transform: translate(70px, 72px);">
          <strong>Web Scraper: Google Careers</strong>
          <div class="description">Find software engineering jobs in India and return job links.</div>
          <span class="state-pill ${stateClass(scraperState)}">${scraperState}</span>
        </article>
        <div class="workflow-edge"></div>
        <div class="workflow-edge-label">Jobs found</div>
        <article class="workflow-card" data-demo-block="store" style="transform: translate(520px, 72px);">
          <strong>Store: Job Results</strong>
          <div class="description">Save found jobs and show what is new.</div>
          <span class="state-pill ${stateClass(storeState)}">${storeState}</span>
        </article>
      `;
      document.querySelectorAll('[data-demo-block]').forEach((block) => {
        block.addEventListener('click', () => openDemoDetail(block.dataset.demoBlock));
      });
    }

    function stateClass(state) {
      return state.toLowerCase();
    }

    async function runGoogleCareersDemo() {
      demoRunState = 'Running';
      demoStoreResult = null;
      $('demoStatus').textContent = 'Scraping Google Careers...';
      renderWorkflowDemo();
      try {
        const res = await fetch('/api/demo/google-careers/run', { method: 'POST' });
        const result = await res.json();
        if (!result.ok) {
          demoRunState = 'Failed';
          $('demoStatus').textContent = result.error || 'Google Careers scrape failed.';
          renderWorkflowDemo();
          openDemoDetail('scraper');
          return;
        }
        demoRunState = 'Success';
        demoStoreResult = result.store_result;
        $('demoStatus').textContent = 'Scrape complete. Select Store to inspect saved job links.';
        renderWorkflowDemo();
        openDemoDetail('store');
      } catch (error) {
        demoRunState = 'Failed';
        $('demoStatus').textContent = `Google Careers scrape failed: ${error}`;
        renderWorkflowDemo();
        openDemoDetail('scraper');
      }
    }

    function openDemoDetail(block) {
      activeCardId = null;
      $('detailPopover').classList.add('open');
      setDetailTabsVisible(false);
      if (block === 'store') {
        $('detailTitle').textContent = 'Store: Job Results';
        $('detailBody').innerHTML = demoStoreResult ? storeInspectorHtml(demoStoreResult) : `
          <div class="inspector-section">
            <div class="inspector-label">Waiting</div>
            <div class="inspector-value">Run demo to inspect saved job links.</div>
          </div>
        `;
      } else {
        $('detailTitle').textContent = 'Web Scraper: Google Careers';
        $('detailBody').innerHTML = `<div class="inspector-section">
          <div class="inspector-label">Site</div>
          <div class="inspector-value">Google Careers</div>
        </div>
        <div class="inspector-section">
          <div class="inspector-label">What to find</div>
          <div class="inspector-value">Find software engineering jobs in India and return job links.</div>
        </div>
        <div class="inspector-section">
          <div class="inspector-label">Demo status</div>
          <div class="inspector-value">${escapeHtml(demoRunState)}</div>
        </div>`;
      }
    }

    function storeInspectorHtml(result) {
      const records = result.sample_records || [];
      return `<div class="inspector-section">
        <div class="inspector-label">Saved to</div>
        <div class="inspector-value">${escapeHtml(result.storage_path)}</div>
      </div>
      <div class="inspector-grid">
        <div class="inspector-metric"><strong>${result.stored_count}</strong><span class="muted">Total saved</span></div>
        <div class="inspector-metric"><strong>${result.new_count}</strong><span class="muted">New this run</span></div>
        <div class="inspector-metric"><strong>${result.duplicate_count}</strong><span class="muted">Already seen</span></div>
        <div class="inspector-metric"><strong>job link</strong><span class="muted">Matched by</span></div>
      </div>
      <div class="inspector-section">
        <div class="inspector-label">Sample links</div>
        ${records.map((record) => `<a class="sample-link" href="${escapeHtml(record.url)}" target="_blank" rel="noreferrer">
          ${escapeHtml(record.title)}, ${escapeHtml(record.location)}
          <span>${escapeHtml(record.url)}</span>
        </a>`).join('')}
      </div>
      <div class="muted">Results are scraped from Google Careers when the demo runs.</div>`;
    }

    function setDetailTabsVisible(visible) {
      document.querySelector('.detail-tabs').style.display = visible ? 'grid' : 'none';
    }

    function startDrag(event) {
      const card = event.currentTarget;
      const cardId = card.dataset.cardId;
      const point = cards.find((item) => item.id === cardId) || { x: 0, y: 0 };
      dragging = {
        id: cardId,
        card,
        startX: event.clientX,
        startY: event.clientY,
        originX: point.x,
        originY: point.y,
        moved: false
      };
      card.setPointerCapture(event.pointerId);
      card.addEventListener('pointermove', drag);
      card.addEventListener('pointerup', endDrag, { once: true });
      card.addEventListener('pointercancel', endDrag, { once: true });
    }

    function drag(event) {
      if (!dragging) return;
      const x = Math.max(0, dragging.originX + event.clientX - dragging.startX);
      const y = Math.max(0, dragging.originY + event.clientY - dragging.startY);
      dragging.moved = dragging.moved || Math.abs(event.clientX - dragging.startX) > 4 || Math.abs(event.clientY - dragging.startY) > 4;
      cards = cards.map((card) => card.id === dragging.id ? { ...card, x, y } : card);
      dragging.card.style.transform = `translate(${x}px, ${y}px)`;
    }

    async function endDrag() {
      if (!dragging) return;
      const finished = dragging;
      dragging.card.removeEventListener('pointermove', drag);
      dragging = null;
      if (!finished.moved) {
        openDetail(finished.id);
        return;
      }
      await saveLayout();
    }

    async function saveLayout() {
      await fetch('/api/workflow-layout', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cards })
      });
    }

    async function createAgent() {
      const name = $('agentName').value.trim();
      if (!name) return;
      const res = await fetch('/api/agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      });
      if (!res.ok) {
        $('status').textContent = await readError(res, 'Could not create agent.');
        return;
      }
      const created = await res.json();
      $('agentName').value = '';
      await loadAgents();
      selectAgent(created.name);
      setTab('agents');
    }

    async function saveAgent() {
      if (!current) return;
      $('status').textContent = 'Saving...';
      const res = await fetch(`/api/agents/${current}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ markdown: $('editor').value })
      });
      if (!res.ok) {
        $('status').textContent = await readError(res, 'Save failed.');
        return;
      }
      const updated = await res.json();
      agents = agents.map((agent) => agent.name === updated.name ? updated : agent);
      $('editor').value = updated.markdown;
      $('status').textContent = `Saved to ${updated.path}.`;
      renderCanvas();
    }

    async function setDefault() {
      if (!current) return;
      const res = await fetch(`/api/agents/${current}/default`, { method: 'POST' });
      $('status').textContent = res.ok ? `${current} is now the default agent.` : await readError(res, 'Could not set default.');
    }

    function renderAgentPicker() {
      $('agentPicker').innerHTML = agents.map((agent) => (
        `<button class="picker-option" data-agent="${agent.name}">${agent.name}</button>`
      )).join('');
      document.querySelectorAll('.picker-option').forEach((button) => {
        button.addEventListener('click', () => {
          const name = button.dataset.agent;
          const card = { id: nextCardId(name), agent: name, x: 80, y: 80 };
          cards.push(card);
          $('agentPicker').classList.remove('open');
          renderCanvas();
          openDetail(card.id);
          saveLayout();
        });
      });
    }

    function openDetail(cardId) {
      activeCardId = cardId;
      activeDetailTab = 'markdown';
      $('detailPopover').classList.add('open');
      setDetailTabsVisible(true);
      renderDetail();
    }

    function renderDetail() {
      const card = cards.find((item) => item.id === activeCardId);
      const agent = card ? agents.find((item) => item.name === card.agent) : null;
      if (!card || !agent) {
        if (activeCardId) $('detailPopover').classList.remove('open');
        activeCardId = null;
        return;
      }
      $('detailTitle').textContent = agent.name;
      document.querySelectorAll('.detail-tab').forEach((button) => {
        button.classList.toggle('active', button.dataset.detail === activeDetailTab);
      });
      if (activeDetailTab === 'markdown') {
        $('detailBody').innerHTML = `<pre>${escapeHtml(agent.markdown)}</pre>`;
      } else if (activeDetailTab === 'langgraph') {
        $('detailBody').innerHTML = `<pre>${escapeHtml(langGraphPreview(agent.name))}</pre>`;
      }
    }

    function duplicateActiveCard() {
      const card = cards.find((item) => item.id === activeCardId);
      if (!card) return;
      const duplicate = {
        id: nextCardId(card.agent),
        agent: card.agent,
        x: card.x + 36,
        y: card.y + 36
      };
      cards.push(duplicate);
      activeCardId = duplicate.id;
      renderCanvas();
      saveLayout();
    }

    function cardsFromPositions(positions) {
      return Object.entries(positions || {}).map(([agent, point]) => ({
        id: `${agent}-1`,
        agent,
        x: Number(point.x || 0),
        y: Number(point.y || 0)
      }));
    }

    function nextCardId(agentName) {
      const base = agentName.replace(/[^a-zA-Z0-9_-]/g, '-') || 'agent';
      let index = 1;
      let id = `${base}-${index}`;
      const existing = new Set(cards.map((card) => card.id));
      while (existing.has(id)) {
        index += 1;
        id = `${base}-${index}`;
      }
      return id;
    }

    function agentDescription(markdown) {
      const lines = markdown.split('\\n');
      const goalIndex = lines.findIndex((line) => line.trim().toLowerCase() === 'goal:');
      if (goalIndex >= 0) {
        const goal = lines.slice(goalIndex + 1).find((line) => line.trim() && !line.trim().endsWith(':'));
        if (goal) return goal.trim().replace(/^-\\s*/, '');
      }
      const firstText = lines.find((line) => {
        const clean = line.trim();
        return clean && !clean.startsWith('#') && !clean.endsWith(':');
      });
      return firstText ? firstText.trim().replace(/^-\\s*/, '') : 'No description yet.';
    }

    function limitText(value, limit) {
      return value.length > limit ? `${value.slice(0, limit - 1)}...` : value;
    }

    function langGraphPreview(name) {
      return `# LangGraph view for ${name}\\n\\nPhase 1 stores this agent as Markdown. LangGraph node editing is planned for a later phase.`;
    }

    function setTab(tab) {
      activeTab = tab;
      history.replaceState(null, '', tab === 'agents' ? '/' : `/${tab}`);
      document.querySelectorAll('.tab').forEach((button) => button.classList.toggle('active', button.dataset.tab === tab));
      document.querySelectorAll('.panel').forEach((panel) => panel.classList.remove('active'));
      $(`panel${tab[0].toUpperCase()}${tab.slice(1)}`).classList.add('active');
      $('agentPicker').classList.remove('open');
      activeCardId = null;
      $('detailPopover').classList.remove('open');
      renderCanvas();
    }

    function initialTab() {
      const route = window.location.pathname.replace('/', '');
      return route === 'workflow' ? route : 'agents';
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, (char) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
      }[char]));
    }

    async function readError(res, fallback) {
      try {
        const body = await res.json();
        return body.detail || fallback;
      } catch {
        return fallback;
      }
    }

    $('createBtn').addEventListener('click', createAgent);
    $('saveBtn').addEventListener('click', saveAgent);
    $('defaultBtn').addEventListener('click', setDefault);
    $('addCardBtn').addEventListener('click', () => $('agentPicker').classList.toggle('open'));
    $('duplicateCardBtn').addEventListener('click', duplicateActiveCard);
    $('closeDetailBtn').addEventListener('click', () => $('detailPopover').classList.remove('open'));
    $('runDemoBtn').addEventListener('click', runGoogleCareersDemo);
    document.querySelectorAll('.detail-tab').forEach((button) => button.addEventListener('click', () => {
      activeDetailTab = button.dataset.detail;
      renderDetail();
    }));
    document.querySelectorAll('.tab').forEach((button) => button.addEventListener('click', () => setTab(button.dataset.tab)));
    $('agentName').addEventListener('keydown', (event) => { if (event.key === 'Enter') createAgent(); });
    setTab(initialTab());
    loadAgents();
  </script>
</body>
</html>""".replace("/*BASE_STYLE*/", BASE_STYLE)
