# Spider Rose Product Decisions

Version: 0.1.0  
Status: Active decisions  
Last updated: 2026-06-03

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
