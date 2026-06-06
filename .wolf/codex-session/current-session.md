# Current Codex Session

Date: 2026-06-05  
Scope: Spider Rose session with Codex

## Active Guardrails

- No actual Spider Rose feature code changes without atomic-plan approval.
- Joel is the final product owner.
- Mukthar's technical review is useful, but Joel usually overrides product direction.
- Product and implementation decisions should be captured locally in Spider Rose docs or local `.wolf` before relying on global workspace memory.

## Current Product Direction

- The visual grid is the active execution surface.
- Blocks should feel Lego-like and executable.
- Connectors represent output or control flow between blocks.
- Fundamental blocks should be reused instead of creating a new block for every site or scenario.
- Example: Web Scraper is a fundamental block; Google Careers is input/configuration.

## Current Approved Demo Slice

- Google Careers visual demo is approved as a visual-only slice.
- Demo uses mock job data for now.
- Mock data remains questionable, not a default future principle.
- Current working storage/artifact direction is still debatable.
- The Store block should show saved path, counts, dedupe key, and sample links after execution.

## Current Codex Review Rule

When Codex changes meaningful code in a Spider Rose session, Joel should see:

- high-level changed areas
- small plain-English chunk explanations
- one-line summaries for simple functions
- more observability for critical logic
- what to visually inspect
- tests or checks that were run

This is a Spider Rose session-with-Codex rule, not a Spider Rose product feature unless Joel explicitly promotes it.

## Local Bug Logging

Spider Rose scoped bugs must be logged in this repo's `.wolf/buglog.jsonl`.

Global duplicate entries are allowed, but local logging must always happen.
