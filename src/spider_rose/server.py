from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel

from spider_rose.agents import default_agent_markdown, slugify_agent_name
from spider_rose.project import create_agent, find_or_init_project_root, set_default_agent


class AgentCreate(BaseModel):
    name: str


class AgentUpdate(BaseModel):
    markdown: str


class WorkflowLayoutUpdate(BaseModel):
    positions: dict[str, dict[str, float]]


def create_app(project_root: Path | None = None):
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import HTMLResponse

    root = project_root or find_or_init_project_root()
    app = FastAPI(title="Spider Rose Local API")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return AGENTS_HTML

    @app.get("/workflow", response_class=HTMLResponse)
    def workflow() -> str:
        return WORKFLOW_HTML

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
        clean_positions: dict[str, dict[str, float]] = {}
        known_agents = {path.stem for path in (root / "agents").glob("*.md")}
        for name, point in payload.positions.items():
            slug = slugify_agent_name(name)
            if slug not in known_agents:
                continue
            clean_positions[slug] = {
                "x": float(point.get("x", 0)),
                "y": float(point.get("y", 0)),
            }
        path = root / "workflow-layout.json"
        path.write_text(json.dumps({"positions": clean_positions}, indent=2), encoding="utf-8")
        return {"positions": clean_positions, "path": str(path.relative_to(root))}

    return app


def _read_workflow_layout(root: Path) -> dict:
    path = root / "workflow-layout.json"
    if not path.exists():
        return {"positions": {}, "path": str(path.relative_to(root))}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"positions": {}, "path": str(path.relative_to(root)), "warning": "Ignored malformed workflow-layout.json."}
    positions = data.get("positions", {})
    if not isinstance(positions, dict):
        positions = {}
    return {"positions": positions, "path": str(path.relative_to(root))}


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


AGENTS_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Spider Rose</title>
  <style>
/*BASE_STYLE*/
    .shell { min-height: 100vh; display: grid; grid-template-columns: 300px 1fr; }
    aside { border-right: 1px solid #2a2a2a; padding: 18px; background: #111111; }
    main { padding: 22px; }
    h1 { font-size: 22px; margin: 0 0 4px; }
    h2 { font-size: 15px; margin: 24px 0 10px; }
    input { width: 100%; box-sizing: border-box; border: 1px solid #3a3a3a; border-radius: 6px; padding: 9px 10px; background: #0f0f0f; color: #f5f5f5; outline: none; }
    input:focus { border-color: #777777; }
    .agent { width: 100%; text-align: left; margin: 6px 0; background: #151515; color: #e5e5e5; border-color: #2a2a2a; }
    .agent:hover { border-color: #3a3a3a; background: #1b1b1b; }
    .agent.active { border-color: #bdbdbd; box-shadow: inset 3px 0 0 #f5f5f5; color: #ffffff; }
    textarea { width: 100%; min-height: calc(100vh - 175px); box-sizing: border-box; resize: vertical; border: 1px solid #2a2a2a; border-radius: 8px; padding: 14px; background: #0f0f0f; color: #f5f5f5; line-height: 1.5; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 14px; outline: none; }
    textarea:focus { border-color: #5a5a5a; }
    .toolbar { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
    .status { min-height: 20px; color: #a3a3a3; font-size: 13px; }
    @media (max-width: 760px) { .shell { grid-template-columns: 1fr; } aside { border-right: 0; border-bottom: 1px solid #2a2a2a; } textarea { min-height: 55vh; } }
  </style>
</head>
<body>
  <div class="shell">
    <aside>
      <h1>Spider Rose</h1>
      <div class="muted">Phase 1 agent editor</div>
      <div class="topnav" style="margin-top: 16px;">
        <a class="nav-link" href="/">Agents</a>
        <a class="nav-link" href="/workflow">Workflow</a>
      </div>
      <h2>New Agent</h2>
      <div class="row">
        <input id="agentName" placeholder="researcher" />
        <button id="createBtn">Create</button>
      </div>
      <h2>Agents</h2>
      <div id="agents"></div>
    </aside>
    <main>
      <div class="toolbar">
        <div>
          <h1 id="title">Select an agent</h1>
          <div class="muted" id="path">Agents are stored as Markdown files in this project.</div>
        </div>
        <div class="row">
          <button class="secondary" id="defaultBtn">Set Default</button>
          <button id="saveBtn">Save</button>
        </div>
      </div>
      <textarea id="editor" spellcheck="false" placeholder="Create or select an agent."></textarea>
      <div class="status" id="status"></div>
    </main>
  </div>
  <script>
    let agents = [];
    let current = null;
    const $ = (id) => document.getElementById(id);

    async function loadAgents() {
      const res = await fetch('/api/agents');
      if (!res.ok) {
        $('status').textContent = await readError(res, 'Could not load agents.');
        return;
      }
      agents = await res.json();
      renderAgents();
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
    }

    async function setDefault() {
      if (!current) return;
      const res = await fetch(`/api/agents/${current}/default`, { method: 'POST' });
      $('status').textContent = res.ok ? `${current} is now the default agent.` : await readError(res, 'Could not set default.');
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
    $('agentName').addEventListener('keydown', (event) => { if (event.key === 'Enter') createAgent(); });
    loadAgents();
  </script>
</body>
</html>""".replace("/*BASE_STYLE*/", BASE_STYLE)


WORKFLOW_HTML = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Spider Rose Workflow</title>
  <style>
{BASE_STYLE}
    body {{ overflow: hidden; }}
    .page {{ height: 100vh; display: flex; flex-direction: column; }}
    header {{ display: flex; align-items: center; gap: 10px; padding: 14px 16px; border-bottom: 1px solid #2a2a2a; background: #111111; }}
    header h1 {{ font-size: 18px; margin: 0; }}
    .canvas {{ position: relative; flex: 1; overflow: hidden; background-color: #080808; background-image: linear-gradient(#1d1d1d 1px, transparent 1px), linear-gradient(90deg, #1d1d1d 1px, transparent 1px), linear-gradient(#111111 1px, transparent 1px), linear-gradient(90deg, #111111 1px, transparent 1px); background-size: 120px 120px, 120px 120px, 24px 24px, 24px 24px; cursor: grab; }}
    .canvas:active {{ cursor: grabbing; }}
    .agent-card {{ position: absolute; width: 220px; min-height: 92px; box-sizing: border-box; border: 1px solid #3a3a3a; border-radius: 8px; padding: 12px; background: #111111; color: #f5f5f5; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28); cursor: move; user-select: none; }}
    .agent-card:hover {{ border-color: #6a6a6a; }}
    .agent-card strong {{ display: block; font-size: 15px; margin-bottom: 8px; }}
    .agent-card code {{ color: #a3a3a3; font-size: 12px; word-break: break-all; }}
    .status {{ min-width: 180px; color: #a3a3a3; font-size: 13px; text-align: right; }}
    @media (max-width: 760px) {{ header {{ flex-wrap: wrap; }} .status {{ text-align: left; width: 100%; }} }}
  </style>
</head>
<body>
  <div class="page">
    <header>
      <h1>Workflow</h1>
      <a class="nav-link" href="/">Agents</a>
      <a class="nav-link" href="/workflow">Workflow</a>
      <div class="muted">Drag agent cards. Execution and edges come later.</div>
      <div class="status" id="status">Loading...</div>
    </header>
    <section class="canvas" id="canvas" aria-label="Workflow canvas"></section>
  </div>
  <script>
    let agents = [];
    let positions = {{}};
    let dragging = null;
    const canvas = document.getElementById('canvas');
    const status = document.getElementById('status');

    async function init() {{
      const [agentsRes, layoutRes] = await Promise.all([
        fetch('/api/agents'),
        fetch('/api/workflow-layout')
      ]);
      if (!agentsRes.ok || !layoutRes.ok) {{
        status.textContent = 'Could not load workflow.';
        return;
      }}
      agents = await agentsRes.json();
      const layout = await layoutRes.json();
      positions = layout.positions || {{}};
      applyDefaultPositions();
      render();
      status.textContent = 'Ready.';
    }}

    function applyDefaultPositions() {{
      agents.forEach((agent, index) => {{
        if (!positions[agent.name]) {{
          positions[agent.name] = {{
            x: 60 + (index % 3) * 260,
            y: 60 + Math.floor(index / 3) * 150
          }};
        }}
      }});
    }}

    function render() {{
      canvas.innerHTML = agents.map((agent) => {{
        const point = positions[agent.name] || {{ x: 60, y: 60 }};
        return `<article class="agent-card" data-agent="${{agent.name}}" style="transform: translate(${{point.x}}px, ${{point.y}}px);">
          <strong>${{escapeHtml(agent.name)}}</strong>
          <code>${{escapeHtml(agent.path)}}</code>
        </article>`;
      }}).join('');
      document.querySelectorAll('.agent-card').forEach((card) => {{
        card.addEventListener('pointerdown', startDrag);
      }});
    }}

    function startDrag(event) {{
      const card = event.currentTarget;
      const name = card.dataset.agent;
      const point = positions[name] || {{ x: 0, y: 0 }};
      dragging = {{
        name,
        card,
        startX: event.clientX,
        startY: event.clientY,
        originX: point.x,
        originY: point.y
      }};
      card.setPointerCapture(event.pointerId);
      card.addEventListener('pointermove', drag);
      card.addEventListener('pointerup', endDrag, {{ once: true }});
      card.addEventListener('pointercancel', endDrag, {{ once: true }});
    }}

    function drag(event) {{
      if (!dragging) return;
      const x = Math.max(0, dragging.originX + event.clientX - dragging.startX);
      const y = Math.max(0, dragging.originY + event.clientY - dragging.startY);
      positions[dragging.name] = {{ x, y }};
      dragging.card.style.transform = `translate(${{x}}px, ${{y}}px)`;
      status.textContent = 'Unsaved position...';
    }}

    async function endDrag(event) {{
      if (!dragging) return;
      dragging.card.removeEventListener('pointermove', drag);
      dragging = null;
      await saveLayout();
    }}

    async function saveLayout() {{
      status.textContent = 'Saving layout...';
      const res = await fetch('/api/workflow-layout', {{
        method: 'PUT',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ positions }})
      }});
      status.textContent = res.ok ? 'Layout saved.' : 'Could not save layout.';
    }}

    function escapeHtml(value) {{
      return String(value).replace(/[&<>"']/g, (char) => ({{
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
      }}[char]));
    }}

    init();
  </script>
</body>
</html>"""
