export function SidebarTabs({ active = "agents" } = {}) {
  return html(`
    <aside class="sr-sidebar" style="max-width: 320px;">
      <h1>Spider Rose</h1>
      <div class="sr-muted">Simple agents. Movable canvas.</div>
      <div class="sr-tabs">
        ${tab("Agents", active === "agents")}
        ${tab("Workflow", active === "workflow")}
        ${tab("Tools", active === "tools")}
      </div>
    </aside>
  `);
}

export function AgentEditor() {
  return html(`
    <section class="sr-sidebar" style="max-width: 420px;">
      <h1>Agents</h1>
      <div class="sr-row">
        <input class="sr-input" value="researcher" />
        <button class="sr-button">Create</button>
      </div>
      <button class="sr-agent-list-button sr-agent-list-button-active">researcher</button>
      <p class="sr-muted">Stored at agents/researcher.md</p>
      <textarea class="sr-editor"># Researcher Agent

Goal:
Find accurate information.

Instructions:
- Identify the user task.
- Return concise output.

Tools:
- web_search

Output:
research_summary</textarea>
      <div class="sr-row" style="margin-top: 10px;">
        <button class="sr-button-secondary">Set Default</button>
        <button class="sr-button">Save</button>
      </div>
    </section>
  `);
}

export function WorkflowCanvas() {
  return html(`
    <main class="sr-stage">
      ${FloatingAddButton()}
      ${ZoomControls()}
      ${AgentCard({ name: "researcher", description: "Find accurate information from reliable sources.", x: 80, y: 90 })}
      ${AgentCard({ name: "researcher", description: "Duplicate canvas block using the same Markdown agent.", x: 340, y: 210 })}
      ${AgentDetailsPopover()}
    </main>
  `);
}

export function AgentCard({ name, description, x = 80, y = 80 }) {
  return `
    <article class="sr-agent-card" style="transform: translate(${x}px, ${y}px);">
      <strong>${name}</strong>
      <div class="sr-description">${description}</div>
    </article>
  `;
}

export function FloatingAddButton() {
  return `
    <div class="sr-floating sr-floating-left">
      <button class="sr-button sr-icon-button" title="Add agent">+</button>
    </div>
  `;
}

export function ZoomControls() {
  return `
    <div class="sr-floating sr-floating-right">
      <button class="sr-button-secondary sr-icon-button" title="Zoom in">+</button>
      <div class="sr-zoom-label">100%</div>
      <button class="sr-button-secondary sr-icon-button" title="Zoom out">-</button>
    </div>
  `;
}

export function AgentPicker() {
  return html(`
    <div class="sr-picker">
      <p class="sr-muted">Select an agent</p>
      <button class="sr-agent-list-button">researcher</button>
      <button class="sr-agent-list-button">linkedin-search</button>
      <button class="sr-agent-list-button">youtube-poster</button>
    </div>
  `);
}

export function ToolsPanel() {
  return html(`
    <section class="sr-sidebar" style="max-width: 320px;">
      <h1>Tools</h1>
      <p class="sr-muted">Tools are planned but not active yet.</p>
      <div class="sr-tool-card">web_search<br><span class="sr-muted">Planned</span></div>
      <div class="sr-tool-card">file_reader<br><span class="sr-muted">Planned</span></div>
    </section>
  `);
}

export function AgentDetailsPopover() {
  return `
    <section class="sr-detail-popover">
      <div class="sr-detail-header">
        <strong>researcher</strong>
        <div class="sr-row">
          <button class="sr-button-secondary">Duplicate</button>
          <button class="sr-button-secondary">Close</button>
        </div>
      </div>
      <div class="sr-detail-tabs">
        <button class="sr-tab sr-tab-active">Markdown</button>
        <button class="sr-tab">LangGraph</button>
        <button class="sr-tab">Tools</button>
      </div>
      <pre class="sr-detail-body"># Researcher Agent

Goal:
Find accurate information.

Tools:
- web_search</pre>
    </section>
  `;
}

function tab(label, active) {
  return `<button class="sr-tab ${active ? "sr-tab-active" : ""}">${label}</button>`;
}

function html(markup) {
  const wrapper = document.createElement("div");
  wrapper.innerHTML = markup.trim();
  return wrapper.firstElementChild;
}
