# Spider Rose Ambiguous Product Questions

Version: 0.1.0  
Status: Active queue  
Last updated: 2026-06-04

Purpose: hold unclear product questions until Joel gives enough clarity to move them into `Product-Decisions.md`.

## Queue Rule

Questions in this file are not decisions. Do not implement from this file unless the implementation task is only to investigate, prototype, or clarify.

## Working Vocabulary

Canvas card: a visual block on the workflow canvas that represents an agent or step. In the current model, an agent card points to an underlying Markdown agent file. Moving or duplicating the card changes the visual layout, not the agent file itself.

## Queued

### PQ-006 - Terminal Versus Visual Boundary

Question:

What should stay terminal-first forever, and what should move into the visual app?

Current answer:

Partially clarified: agent creation should work as a chat-style wizard, and the user could use the terminal like this as well. The full terminal-versus-visual boundary is still unresolved.

Why ambiguous:

Spider Rose currently has both a terminal shell and visual app. The right boundary is not clear yet because basic visual agent creation still needs to be defined.

Clarity needed:

- Which actions are faster in terminal?
- Which actions are clearer in the visual app?
- Which actions should be available in both surfaces?
- Which surface should a non-developer use first?

Move to product decision when:

Joel can state the boundary as a product rule.

### PQ-007 - Minimum Useful Workflow Before Execution

Question:

What is the minimum useful agent workflow before workflow execution exists?

Current answer:

Partially clarified on 2026-06-04: the minimum useful workflow should be a visual execution chain, not only a planning diagram. The concrete example is Google Careers web scraping -> stored in RAG/database -> scheduled run -> WhatsApp notification.

Remaining clarity needed:

- What is the smallest storage layer for the first version: local JSON, SQLite, vector DB, or Markdown artifact?
- What should the first scheduler support: manual run, interval, cron-like text, or daily time?
- What should WhatsApp sending use first: manual copy, local gateway, WhatsApp Cloud API, or OpenClaw channel?

### PQ-008 - Connector Edge Meaning

Question:

Should connector edges be only visual planning at first, or should they immediately imply execution logic?

Current answer:

Clarified on 2026-06-04: connectors should represent the active workflow. They are not just explanatory lines. A connector means output/control flows from one executable block into another.

Remaining clarity needed:

- What connector types exist first: data, schedule trigger, message trigger, or all one simple connector?
- How should the UI show whether a connector has run successfully?
- How much validation should happen before a user can run a connected workflow?

### PQ-009 - Markdown Agent Meaning

Question:

What does a "Markdown agent" mean in Spider Rose: prompt file, reusable worker, workflow node, teaching object, or all of these?

Why ambiguous:

The term can mean different things to developers and non-developers. Product language should be clear before UI labels and docs spread.

Clarity needed:

- What word should non-developers see?
- What word should developers see?
- Is an agent primarily a file, a behavior, or a block in a flow?

### PQ-010 - Differentiation

Question:

What makes Spider Rose meaningfully different from Codex, Claude Code, OpenClaw, Hermes, OpenCode, CrewAI, n8n, and LangGraph Studio?

Why ambiguous:

Spider Rose needs a sharper position before public messaging and feature prioritization.

Clarity needed:

- Which products are direct references?
- Which products are not competitors?
- What unique promise should Spider Rose own?

### PQ-011 - Refusal Boundary

Question:

What should Spider Rose deliberately refuse to become?

Why ambiguous:

A clear refusal boundary prevents the product from absorbing every agent, workflow, cloud, marketplace, or automation idea.

Clarity needed:

- What complexity should stay out of the MVP?
- What user requests should be rejected even if technically possible?

### PQ-012 - First Demo

Question:

What is the first demo that would make someone understand the product without explanation?

Why ambiguous:

The demo determines the product story and the order in which features should feel polished.

Clarity needed:

- Is the demo terminal-first, visual-first, or both?
- Does the demo start from an empty folder or a prepared project?
- What is the final visible result?

### PQ-013 - TUI Mastery Gate

Question:

What should Mukthar master in the TUI before he is allowed to invent new interactions?

Why ambiguous:

The mastery direction is clear, but the concrete gate for creative ownership needs a practical evaluation.

Clarity needed:

- What should Mukthar be able to explain?
- What should he be able to implement?
- What should he be able to teach?

### PQ-014 - Reliable Versus Creative Surface

Question:

What part of Spider Rose should be boring and reliable, and what part should be creative and memorable?

Why ambiguous:

The product needs creativity, but not in places where reliability and clarity matter more.

Clarity needed:

- Which interactions must be predictable?
- Where can Spider Rose feel distinctive?

### PQ-015 - Removal Candidate

Question:

Which current feature would we remove if we questioned whether the task needs to be done?

Why ambiguous:

This requires reviewing the current feature set against the new product focus.

Clarity needed:

- Which existing features help simple visual agent creation?
- Which features distract from that goal?

### PQ-016 - Public Readiness

Question:

What should be true before Spider Rose is publicised?

Why ambiguous:

Public readiness could mean install reliability, product clarity, demo quality, or enough differentiated value.

Clarity needed:

- What must work on a clean machine?
- What must the first demo show?
- What docs must be ready?

### PQ-017 - Google SWE-Level Signal

Question:

What would make Spider Rose impressive as a Google SWE-level project without overcomplicating the MVP?

Why ambiguous:

The project should show engineering taste without drifting into overbuilt architecture.

Clarity needed:

- What technical depth matters most?
- What product restraint should be visible?
- What implementation proof should exist?

### PQ-018 - Phase 1 Success Metric

Question:

What is the sharpest Phase 1 success metric: install success, first agent created, first run completed, visual editor opened, canvas saved, or user teaches another person?

Why ambiguous:

The success metric determines what the team should optimize next.

Clarity needed:

- What single event proves Phase 1 worked?
- Is the metric for Joel and Mukthar, developers, or non-developers?
