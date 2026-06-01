from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from spider_rose.agents import default_agent_markdown, slugify_agent_name
from spider_rose.project import create_agent, find_or_init_project_root, set_default_agent


def create_app(project_root: Path | None = None):
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import HTMLResponse

    root = project_root or find_or_init_project_root()
    app = FastAPI(title="Spider Rose Local API")

    class AgentCreate(BaseModel):
        name: str

    class AgentUpdate(BaseModel):
        markdown: str

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return HTML

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
        slug = slugify_agent_name(name)
        path = root / "agents" / f"{slug}.md"
        if not path.exists():
            raise HTTPException(status_code=404, detail="Agent not found.")
        path.write_text(payload.markdown, encoding="utf-8")
        return {"name": slug, "path": str(path.relative_to(root)), "markdown": payload.markdown}

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

    return app


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Spider Rose</title>
  <style>
    :root { color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    body { margin: 0; background: #080808; color: #f5f5f5; }
    button, input, textarea { font: inherit; }
    .shell { min-height: 100vh; display: grid; grid-template-columns: 300px 1fr; }
    aside { border-right: 1px solid #2a2a2a; padding: 18px; background: #111111; }
    main { padding: 22px; }
    h1 { font-size: 22px; margin: 0 0 4px; }
    h2 { font-size: 15px; margin: 24px 0 10px; }
    .muted { color: #a3a3a3; font-size: 13px; }
    .row { display: flex; gap: 8px; }
    input { width: 100%; box-sizing: border-box; border: 1px solid #3a3a3a; border-radius: 6px; padding: 9px 10px; background: #0f0f0f; color: #f5f5f5; outline: none; }
    input:focus { border-color: #777777; }
    button { border: 1px solid #f5f5f5; border-radius: 6px; padding: 9px 11px; background: #f5f5f5; color: #080808; cursor: pointer; white-space: nowrap; }
    button:hover { background: #e5e5e5; }
    button.secondary { background: #151515; color: #e5e5e5; border-color: #3a3a3a; }
    button.secondary:hover { border-color: #5a5a5a; color: #ffffff; background: #1b1b1b; }
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
      agents = await fetch('/api/agents').then((res) => res.json());
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
        $('status').textContent = (await res.json()).detail || 'Could not create agent.';
        return;
      }
      const created = await res.json();
      $('agentName').value = '';
      await loadAgents();
      selectAgent(created.name);
    }

    async function saveAgent() {
      if (!current) return;
      const res = await fetch(`/api/agents/${current}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ markdown: $('editor').value })
      });
      $('status').textContent = res.ok ? 'Saved.' : 'Save failed.';
      await loadAgents();
      selectAgent(current);
    }

    async function setDefault() {
      if (!current) return;
      const res = await fetch(`/api/agents/${current}/default`, { method: 'POST' });
      $('status').textContent = res.ok ? `${current} is now the default agent.` : 'Could not set default.';
    }

    $('createBtn').addEventListener('click', createAgent);
    $('saveBtn').addEventListener('click', saveAgent);
    $('defaultBtn').addEventListener('click', setDefault);
    $('agentName').addEventListener('keydown', (event) => { if (event.key === 'Enter') createAgent(); });
    loadAgents();
  </script>
</body>
</html>"""
