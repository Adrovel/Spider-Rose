# Spider Rose Idea Questions

Last updated: 2026-06-03

Purpose: capture product questions Joel should answer before Spider Rose requirements are optimized, implemented, or treated as fixed.

## Open Product Questions For Joel

1. What is the one sentence promise of Spider Rose to a developer who has never heard of it?
2. Who is the first real user: Joel, Mukthar, AI engineers, LangGraph users, open-source agent builders, or a narrower group?
3. What painful job should Spider Rose solve first: creating agents, running agents, arranging agents, understanding flows, teaching agents, or debugging agents?
4. When someone runs `spiderrose` for the first time, what should they feel within the first 30 seconds?
5. Should Spider Rose feel more like a coding agent, a local workflow builder, a terminal notebook, or an agent IDE?
6. What should stay terminal-first forever, and what should move into the visual app?
7. What is the minimum useful agent workflow before workflow execution exists?
8. Should connector edges be only visual planning at first, or should they immediately imply execution logic?
9. What does a "Markdown agent" mean in Spider Rose: prompt file, reusable worker, workflow node, teaching object, or all of these?
10. What makes Spider Rose meaningfully different from Codex, Claude Code, OpenClaw, Hermes, OpenCode, CrewAI, n8n, and LangGraph Studio?
11. What should Spider Rose deliberately refuse to become?
12. What is the first demo that would make someone understand the product without explanation?
13. What should Mukthar master in the TUI before he is allowed to invent new interactions?
14. What part of Spider Rose should be boring and reliable, and what part should be creative and memorable?
15. Which current feature would we remove if we questioned whether the task needs to be done?
16. What should be true before Spider Rose is publicised?
17. What would make Spider Rose impressive as a Google SWE-level project without overcomplicating the MVP?
18. What is the sharpest Phase 1 success metric: install success, first agent created, first run completed, visual editor opened, canvas saved, or user teaches another person?

## Answer Format

For each answer, use:

```text
Question:
Answer:
Decision:
Follow-up:
```

## Joel Answers

### JA-001 - First product focus

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

### JA-002 - First real user

Question:

Who is the first real user?

Answer:

The first real users are Joel and Mukthar, then developers.

Decision:

Spider Rose should first be useful to Joel and Mukthar as the founding users. After that, it should expand toward developers.

Follow-up:

- Validate the product against Joel and Mukthar's real agent-creation workflow before generalizing.
- Avoid optimizing too early for broad AI-builder personas.

### JA-003 - First painful jobs

Question:

What painful job should Spider Rose solve first?

Answer:

Creating agents, arranging agents, and understanding flows.

Decision:

Spider Rose should prioritize agent creation, visual arrangement, and flow understanding before deeper execution complexity.

Follow-up:

- Keep the visual canvas focused on making agent structure and flow understandable.
- Treat workflow execution as secondary until creation and arrangement are simple.

### JA-004 - First-run feeling

Question:

When someone runs `spiderrose` for the first time, what should they feel within the first 30 seconds?

Answer:

Simplicity.

Decision:

The first-run experience should feel simple before it feels powerful.

Follow-up:

- Remove or hide anything in the first-run path that makes the product feel complex too early.
- Make the first successful action obvious.

### JA-005 - Product feel

Question:

Should Spider Rose feel more like a coding agent, a local workflow builder, a terminal notebook, or an agent IDE?

Answer:

Local workflow builder and agent IDE.

Decision:

Spider Rose should combine a local workflow builder feel with agent IDE capabilities.

Follow-up:

- Use workflow-builder language for arranging and understanding flows.
- Use agent-IDE language for creating, editing, and customizing agents.

### JA-006 - Terminal versus visual boundary

Question:

What should stay terminal-first forever, and what should move into the visual app?

Answer:

Not sure.

Decision:

This boundary is unresolved.

Follow-up:

- Revisit after the simplest visual agent creation flow is defined.
- Compare which actions feel faster in terminal versus clearer in the visual app.
