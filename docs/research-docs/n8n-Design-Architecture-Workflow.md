# n8n Design, Architecture, Workflow

## What It Is

n8n is a visual workflow automation platform. Its core mental model is a workflow made of connected nodes. Each node represents a trigger, integration, transform, action, or control step.

## Core Product Shape

- Visual editor first, CLI second.
- Nodes and connections are the main authoring primitive.
- Executions are first-class debugging objects.
- Credentials are a product surface because workflows often connect to third-party APIs.
- Sticky notes/documentation live near the graph.

## Workflow Model

n8n defines a workflow as a collection of connected nodes that automate a process. Official docs split workflow components into nodes, connections, and sticky notes.

Typical workflow:

1. Trigger node starts the run.
2. Data moves through connected action/logic nodes.
3. Each node receives structured input and produces structured output.
4. Execution history captures what happened for debugging.

## Architecture Notes

- The visual graph is the source of truth for execution order.
- Credentials and environment configuration are operationally critical.
- Execution logs are not a side feature; they are how users debug broken automations.
- Self-hosting creates a different product surface than cloud hosting: backups, encryption keys, worker scaling, and operational safety become visible concerns.

## Lessons For Spider Rose

- Copy the clarity of graph primitives: node, connection, execution.
- Do not copy the full low-code surface for Phase 1.
- Keep credentials/tools explicit and local.
- Make debugging visible only when it exists; do not add fake logs before the runtime is real.
- Sticky-note style annotations may be useful later for explaining agent intent on the canvas.

## What To Avoid

- Too many node types before the agent model is stable.
- Credential-heavy UX in the MVP.
- Building a canvas before terminal actions are smooth.
- Hiding files behind the UI. Spider Rose should always let users inspect Markdown on disk.

## Sources

- n8n Workflows docs: https://docs.n8n.io/workflows/
- n8n Workflow components docs: https://docs.n8n.io/workflows/components/
- n8n Integrations docs: https://docs.n8n.io/integrations/
- n8n Workflow settings docs: https://docs.n8n.io/workflows/settings/
