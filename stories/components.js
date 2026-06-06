export function SidebarTabs({ active = "agents" } = {}) {
  return html(`
    <aside class="sr-sidebar" style="max-width: 320px;">
      <h1>Spider Rose</h1>
      <div class="sr-muted">Two-block web demo.</div>
      <div class="sr-tabs">
        ${tab("Agents", active === "agents")}
        ${tab("Workflow", active === "workflow")}
      </div>
    </aside>
  `);
}

export function AgentEditor() {
  return html(`
    <section class="sr-sidebar" style="max-width: 420px;">
      <h1>Agents</h1>
      <div class="sr-row">
        <input class="sr-input" value="google-careers-scraper" />
        <button class="sr-button">Create</button>
      </div>
      <button class="sr-agent-list-button sr-agent-list-button-active">google-careers-scraper</button>
      <p class="sr-muted">Stored at agents/google-careers-scraper.md</p>
      <textarea class="sr-editor"># Google Careers Scraper Agent

Goal:
Scrape Google Careers search results and return a small, readable list of matching jobs.

Instructions:
- Use the user's task as the search query.
- Return job title, location, level, and minimum qualifications.

Tools:
- google_careers_scraper

Output:
google_careers_jobs</textarea>
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
      ${AgentCard({ name: "google-careers-scraper", description: "Scrape Google Careers search results and return matching jobs.", x: 80, y: 90 })}
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

export function AgentPicker() {
  return html(`
    <div class="sr-picker">
      <p class="sr-muted">Select an agent</p>
      <button class="sr-agent-list-button">google-careers-scraper</button>
      <button class="sr-agent-list-button">linkedin-search</button>
      <button class="sr-agent-list-button">youtube-poster</button>
    </div>
  `);
}

export function AgentDetailsPopover() {
  return `
    <section class="sr-detail-popover">
      <div class="sr-detail-header">
        <strong>google-careers-scraper</strong>
        <div class="sr-row">
          <button class="sr-button-secondary">Duplicate</button>
          <button class="sr-button-secondary">Close</button>
        </div>
      </div>
      <div class="sr-detail-tabs">
        <button class="sr-tab sr-tab-active">Markdown</button>
        <button class="sr-tab">LangGraph</button>
      </div>
      <pre class="sr-detail-body"># Google Careers Scraper Agent

Goal:
Scrape Google Careers search results and return matching jobs.

Tools:
- google_careers_scraper</pre>
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
