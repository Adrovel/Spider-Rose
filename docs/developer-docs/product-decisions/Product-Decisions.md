# Spider Rose Product Decisions

Version: 0.1.0  
Status: Active decisions  
Last updated: 2026-06-04

Purpose: record clarified product decisions so requirements are not optimized or implemented before the product direction is understood.

## QNA-001 - First Product Focus

Question:

What painful job should Spider Rose solve first?

Answer:

Create agents. It should be simple. Any non-developer should be able to use it. It should be customisable and easy to use as a visual tool.

Decision:

Spider Rose should optimize first for simple, visual, customizable agent creation. The product should not assume the first successful user is a developer who understands agent frameworks or terminal jargon.

Follow-up:

- Define the simplest possible visual agent creation flow.
- Decide which fields a non-developer must understand to create a useful agent.
- Keep terminal power available, but do not make terminal knowledge required for basic agent creation.

## QNA-002 - First Real User

Question:

Who is the first real user?

Answer:

The first real users are Joel and Mukthar, then developers.

Decision:

Spider Rose should first be useful to Joel and Mukthar as the founding users. After that, it should expand toward developers.

Follow-up:

- Validate the product against Joel and Mukthar's real agent-creation workflow before generalizing.
- Avoid optimizing too early for broad AI-builder personas.

## QNA-003 - First Painful Jobs

Question:

What painful jobs should Spider Rose solve first?

Answer:

Creating agents, arranging agents, and understanding flows.

Decision:

Spider Rose should prioritize agent creation, visual arrangement, and flow understanding before deeper execution complexity.

Follow-up:

- Keep the visual canvas focused on making agent structure and flow understandable.
- Treat workflow execution as secondary until creation and arrangement are simple.

## QNA-004 - First-Run Feeling

Question:

When someone runs `spiderrose` for the first time, what should they feel within the first 30 seconds?

Answer:

Simplicity.

Decision:

The first-run experience should feel simple before it feels powerful.

Follow-up:

- Remove or hide anything in the first-run path that makes the product feel complex too early.
- Make the first successful action obvious.

## QNA-005 - Product Feel

Question:

Should Spider Rose feel more like a coding agent, a local workflow builder, a terminal notebook, or an agent IDE?

Answer:

Local workflow builder and agent IDE.

Decision:

Spider Rose should combine a local workflow builder feel with agent IDE capabilities.

Follow-up:

- Use workflow-builder language for arranging and understanding flows.
- Use agent-IDE language for creating, editing, and customizing agents.

## QNA-006 - Agent Creation Interaction

Question:

Should agent creation feel like a simple form, a chat-style wizard, a canvas card you fill in, or a mix of form and canvas card?

Answer:

A chat-style wizard, not a form. The user could use the terminal like this as well.

Decision:

Spider Rose agent creation should start as a guided chat-style wizard. The same interaction model should be possible in the terminal and in the visual app. The product should avoid making first-time users fill a static form before they understand what the agent is.

Follow-up:

- Define the wizard questions for creating the first useful agent.
- Make the visual app feel conversational rather than form-heavy.
- Explore a terminal wizard flow for `/new agent` that asks one question at a time.
- Keep the generated result editable after the wizard finishes.

## QNA-007 - Agent Creation Wizard Content

Question:

What should the chat-style agent creation wizard ask, show after completion, and do before saving?

Answer:

The wizard should begin with "Create your own agents." It should ask what the agent should do, what it should know, what outputs it should produce, and what tools it should use. After completion, it should show "agent created" and an agent summary, with some possibility to edit the agent. A review step before saving is preferred.

Decision:

The first agent creation wizard should be short, conversational, and review-based. It should gather only the minimum information needed to create a useful first agent, then show a summary and let the user review or edit before the agent is finalized.

Follow-up:

- Use "Create your own agents" as the starting wizard message.
- Ask these wizard questions first: what should this agent do, what should it know, what outputs should it produce, and what tools should it use.
- Show an agent-created state and agent summary after the wizard completes.
- Include an edit/review step before saving the final agent.
- Make the same question flow usable in the terminal wizard and visual app wizard.

## QNA-008 - Terminal Agent Wizard Behavior

Question:

How should `/new agent` behave in the terminal wizard?

Answer:

`/new agent google-careers-scraper` should open the wizard with the agent name prefilled. Spider Rose should be able to extract details from the user's natural language paragraph instead of forcing the user to paste structured fields. At the review step, the options should be Save agent, Edit answer, Start over, and Cancel.

Decision:

The terminal agent creation flow should be conversational and extraction-based. The command should not force users into a rigid form. If the user provides an agent name in the command, Spider Rose should keep that name and continue the wizard from there. The user can describe the agent naturally, and Spider Rose should extract what the agent should do, what it should know, expected outputs, and tools. Before saving, Spider Rose should show a review screen with Save agent, Edit answer, Start over, and Cancel.

Rejected alternative:

The main alternative was a strict step-by-step wizard that asks one field at a time and requires structured answers. That is not the preferred default because Spider Rose should feel simple and intelligent enough to understand a natural description.

Follow-up:

- Define the exact terminal copy for `/new agent`.
- Support `/new agent <name>` as a wizard start with the name prefilled.
- Let users describe the agent naturally and extract agent details from that description.
- Show a review state before saving.
- Review actions: Save agent, Edit answer, Start over, Cancel.

## QNA-009 - Visual Workflow Execution Model

Question:

What does the visual element do in Spider Rose?

Answer:

The app should work like Lego-style blocks on a grid. Each block is a functional unit in the workflow. A web scraper block connects to a website such as Google Careers, scrapes jobs, and creates an output. That output can connect to a RAG/database block that stores the result. Another block can be a scheduler that decides how frequently the workflow runs. Another block can be a WhatsApp block that sends scheduled messages. The blocks connect visually, and the visual flow is the active execution model.

Decision:

Spider Rose's visual canvas should become the primary workflow execution surface. Blocks are not only diagrams. A block represents an executable capability, data store, scheduler, communication channel, or agent. Connectors define how output moves from one block to the next.

Follow-up:

- Rename product language from only "agent cards" toward workflow blocks where needed.
- Define first block types: Web Scraper, Website Source, RAG/DB Store, Scheduler, WhatsApp Sender, and Agent.
- Define connector meaning as data/control flow between executable blocks.
- Keep the first working workflow concrete: Google Careers scraper -> RAG/DB store -> scheduler -> WhatsApp message.
- Design the canvas as a grid where connected blocks show the actual running workflow.

## QNA-010 - Implementation Approval Gate And Product Ownership

Question:

When should Spider Rose code changes happen?

Answer:

No actual code changes should happen without the work going through the atomic-plan phase. Mukthar may review and challenge implementation details, but Joel owns final product decisions and can override Mukthar on product direction.

Decision:

Spider Rose implementation must be plan-gated. Product scenarios and feature ideas should first become atomic-plan items. Joel is the final approval owner for product direction. Mukthar's review is important for implementation quality, technical concerns, and TUI work, but Mukthar product decisions may need Joel approval and Joel usually overrides on product calls.

Follow-up:

- Treat future scenario walkthroughs as product discovery, not implementation permission.
- Add proposed features to the atomic plan before touching runtime, UI, tests, or agent files.
- Keep unapproved experiments out of the tracked implementation unless explicitly approved.
- Record whether a slice is Joel-approved, Mukthar-reviewed, or still pending technical review.

## QNA-011 - Fundamental Block Library

Question:

Should every workflow block be a new custom block?

Answer:

No. Spider Rose should have fundamental blocks. A Web Scraper block can be a fundamental reusable block, with sites such as Google Careers provided as inputs.

Decision:

Spider Rose should build around reusable fundamental block types instead of creating a new block type for every specific site or scenario. Specific workflows should configure these blocks through inputs, connectors, and saved settings.

Follow-up:

- Define a first fundamental block library.
- Treat Google Careers as an input/configuration for a Web Scraper block, not necessarily a separate permanent block type.
- Use scenario walkthroughs to decide which block types are fundamental and which details are inputs.

## QNA-012 - Mock Data Boundary

Question:

Should the first Google Careers workflow demo use mock data?

Answer:

Joel is conflicted. Mock data has two problems: it deviates from actual problem solving, and the actual task is small enough that mocking can feel unnecessary. Ultimately Spider Rose needs to scrape realistically. Joel is okay with mock data for this first demo, but this should not become the default approach. Later demos may skip mock data and go directly to real integrations.

Decision:

Mock data is acceptable for the first Google Careers visual demo only as a fast way to validate the block flow, run states, connector meaning, and right-side inspector. It should not become a general product habit or a substitute for solving the real workflow.

Follow-up:

- Keep the mock demo clearly labeled as a visual/product demo.
- Do not let mock data define scraper behavior.
- Move to real Google Careers scraping as soon as the visual workflow shape is validated.
- For small workflows, consider real data earlier instead of mocking by default.
- Product principle added: question mock data before using it; Joel is skeptical because it can drift away from actual problem solving.
