from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from spider_rose.agents import default_agent_markdown, slugify_agent_name
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

    @app.get("/tools", response_class=HTMLResponse)
    def tools() -> str:
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
    .canvas { position: absolute; inset: 0; overflow: hidden; background-color: #080808; background-image: linear-gradient(#1d1d1d 1px, transparent 1px), linear-gradient(90deg, #1d1d1d 1px, transparent 1px), linear-gradient(#111111 1px, transparent 1px), linear-gradient(90deg, #111111 1px, transparent 1px); background-size: calc(120px * var(--zoom, 1)) calc(120px * var(--zoom, 1)), calc(120px * var(--zoom, 1)) calc(120px * var(--zoom, 1)), calc(24px * var(--zoom, 1)) calc(24px * var(--zoom, 1)), calc(24px * var(--zoom, 1)) calc(24px * var(--zoom, 1)); cursor: grab; transform-origin: 0 0; }
    .canvas:active { cursor: grabbing; }
    .canvas-layer { position: absolute; inset: 0; transform-origin: 0 0; transform: scale(var(--zoom, 1)); }
    .agent-card { position: absolute; width: 210px; min-height: 76px; box-sizing: border-box; border: 1px solid #3a3a3a; border-radius: 8px; padding: 12px; background: #111111; color: #f5f5f5; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28); cursor: grab; user-select: none; }
    .agent-card:hover { border-color: #6a6a6a; }
    .agent-card:active { cursor: grabbing; }
    .agent-card strong { display: block; font-size: 15px; margin-bottom: 7px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .agent-card .description { color: #a3a3a3; font-size: 12px; line-height: 1.35; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .floating { position: absolute; z-index: 10; display: flex; gap: 8px; }
    .floating.left { left: 16px; top: 16px; }
    .floating.right { right: 16px; top: 16px; flex-direction: column; }
    .icon-button { width: 40px; height: 40px; display: inline-flex; align-items: center; justify-content: center; border-radius: 8px; padding: 0; font-size: 20px; line-height: 1; }
    .agent-picker { position: absolute; z-index: 11; top: 64px; left: 16px; width: 240px; border: 1px solid #2a2a2a; border-radius: 8px; padding: 10px; background: #111111; box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35); display: none; }
    .agent-picker.open { display: block; }
    .picker-option { width: 100%; margin: 4px 0; text-align: left; background: #151515; color: #e5e5e5; border-color: #2a2a2a; }
    .zoom-label { min-width: 40px; text-align: center; border: 1px solid #2a2a2a; border-radius: 8px; padding: 8px 0; background: #111111; color: #bdbdbd; font-size: 12px; }
    .detail-popover { position: absolute; z-index: 12; right: 16px; bottom: 16px; width: min(520px, calc(100vw - 360px)); max-height: calc(100vh - 120px); overflow: hidden; border: 1px solid #2a2a2a; border-radius: 8px; background: #101010; box-shadow: 0 24px 70px rgba(0, 0, 0, 0.45); display: none; }
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
    @media (max-width: 860px) { .detail-popover { left: 16px; right: 16px; width: auto; max-height: 48vh; } }
  </style>
</head>
<body>
  <div class="app">
    <aside>
      <h1>Spider Rose</h1>
      <div class="muted">Simple agents. Movable canvas.</div>
      <div class="tabs" role="tablist">
        <button class="tab" id="tabAgents" data-tab="agents">Agents</button>
        <button class="tab" id="tabWorkflow" data-tab="workflow">Workflow</button>
        <button class="tab" id="tabTools" data-tab="tools">Tools</button>
      </div>
      <div class="panel" id="panelAgents">
        <h2>New Agent</h2>
        <div class="row">
          <input id="agentName" placeholder="researcher" />
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
        <p class="muted">Drag agent cards on the canvas. Edges and execution come later.</p>
        <p class="muted">Use the plus button on the canvas to add or focus an agent card.</p>
      </div>
      <div class="panel" id="panelTools">
        <h2>Tools</h2>
        <p class="muted">Tools are planned but not active yet.</p>
        <div class="agent">web_search<br><span class="muted">Planned</span></div>
        <div class="agent">file_reader<br><span class="muted">Planned</span></div>
      </div>
    </aside>
    <main>
      <section class="canvas" id="canvas" aria-label="Workflow canvas">
        <div class="canvas-layer" id="canvasLayer"></div>
      </section>
      <div class="floating left">
        <button class="icon-button" id="addCardBtn" title="Add agent to canvas" aria-label="Add agent to canvas">+</button>
      </div>
      <div class="agent-picker" id="agentPicker"></div>
      <div class="floating right">
        <button class="icon-button secondary" id="zoomInBtn" title="Zoom in" aria-label="Zoom in">+</button>
        <div class="zoom-label" id="zoomLabel">100%</div>
        <button class="icon-button secondary" id="zoomOutBtn" title="Zoom out" aria-label="Zoom out">-</button>
      </div>
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
          <button class="detail-tab" data-detail="tools">Tools</button>
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
    let zoom = 1;
    let activeCardId = null;
    let activeDetailTab = 'markdown';
    const $ = (id) => document.getElementById(id);
    const canvasLayer = $('canvasLayer');

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
      canvasLayer.innerHTML = cards.map((card) => {
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
      applyZoom();
      if (activeCardId) renderDetail();
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
      const x = Math.max(0, dragging.originX + (event.clientX - dragging.startX) / zoom);
      const y = Math.max(0, dragging.originY + (event.clientY - dragging.startY) / zoom);
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
      renderDetail();
    }

    function renderDetail() {
      const card = cards.find((item) => item.id === activeCardId);
      const agent = card ? agents.find((item) => item.name === card.agent) : null;
      if (!card || !agent) {
        $('detailPopover').classList.remove('open');
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
      } else {
        $('detailBody').innerHTML = `<pre>${escapeHtml(toolsPreview(agent.markdown))}</pre>`;
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

    function toolsPreview(markdown) {
      const lines = markdown.split('\\n');
      const start = lines.findIndex((line) => line.trim().toLowerCase() === 'tools:');
      if (start < 0) return 'No tools declared yet.';
      const tools = [];
      for (const line of lines.slice(start + 1)) {
        const clean = line.trim();
        if (!clean) continue;
        if (clean.endsWith(':') && !clean.startsWith('-')) break;
        if (clean.startsWith('-')) tools.push(clean.slice(1).trim());
      }
      return tools.length ? tools.map((tool) => `- ${tool}`).join('\\n') : 'No tools declared yet.';
    }

    function setTab(tab) {
      history.replaceState(null, '', tab === 'agents' ? '/' : `/${tab}`);
      document.querySelectorAll('.tab').forEach((button) => button.classList.toggle('active', button.dataset.tab === tab));
      document.querySelectorAll('.panel').forEach((panel) => panel.classList.remove('active'));
      $(`panel${tab[0].toUpperCase()}${tab.slice(1)}`).classList.add('active');
    }

    function initialTab() {
      const route = window.location.pathname.replace('/', '');
      return ['workflow', 'tools'].includes(route) ? route : 'agents';
    }

    function changeZoom(delta) {
      zoom = Math.min(1.8, Math.max(0.5, Number((zoom + delta).toFixed(2))));
      applyZoom();
    }

    function applyZoom() {
      document.documentElement.style.setProperty('--zoom', zoom);
      $('zoomLabel').textContent = `${Math.round(zoom * 100)}%`;
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
    $('zoomInBtn').addEventListener('click', () => changeZoom(0.1));
    $('zoomOutBtn').addEventListener('click', () => changeZoom(-0.1));
    $('duplicateCardBtn').addEventListener('click', duplicateActiveCard);
    $('closeDetailBtn').addEventListener('click', () => $('detailPopover').classList.remove('open'));
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
