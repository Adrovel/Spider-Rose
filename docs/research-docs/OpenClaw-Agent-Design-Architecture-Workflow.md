# OpenClaw Agent Design, Architecture, Workflow

## What It Is

OpenClaw is a self-hosted gateway for connecting messaging channels, web control surfaces, and AI coding agents. Its core product idea is a single local gateway that routes messages from many surfaces to isolated agent sessions.

## Core Product Shape

- Local-first gateway process.
- Messaging channels connect to the gateway.
- Control UI, CLI, and channel integrations are different surfaces over the same gateway.
- Plugins and skills extend available channels and agent behavior.
- Sessions isolate context by agent, channel, account, and peer.

## Workflow Model

OpenClaw's workflow is message-driven:

1. A message arrives from a channel or UI surface.
2. The gateway receives and authenticates it.
3. The router chooses the correct agent/session.
4. The agent processes the message with configured tools and workspace access.
5. Output streams back to the original surface.

The architecture docs identify Gateway, Channels, Sessions, Agents, and Router as core concepts. The CLI also exposes gateway, agents, channels, plugins, skills, tasks, messages, sessions, and logs as distinct commands.

## Architecture Notes

- The Gateway is the control plane.
- A lock file prevents multiple gateway instances.
- Sessions use structured routing keys to isolate context.
- Channels are pluggable and lifecycle-managed.
- Agents can be routed by channel/account/peer.

## Lessons For Spider Rose

- "Only one local server" is a real product requirement, not just a dev convenience.
- Spider Rose should keep one local visualization server at a time and avoid port/process duplication.
- Session identity and routing become important once agents can run through multiple surfaces.
- A future Spider Rose runtime can learn from OpenClaw's separation of gateway, channels, routing, sessions, and agent execution.

## What To Avoid

- Bringing channel/gateway complexity into Phase 1.
- Treating every user as a messaging-platform power user.
- Adding plugin systems before the base agent file model is stable.

## Sources

- OpenClaw overview docs: https://docs.openclaw.ai/
- OpenClaw architecture docs: https://openclaw-openclaw.mintlify.app/concepts/architecture
- Local command reference captured with `openclaw --help` on 2026-06-01.
