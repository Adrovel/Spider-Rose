# Codex Code Review Process

Status: Current session rule  
Scope: Spider Rose sessions with Codex

This process is for how Codex should explain code changes to Joel while working on Spider Rose in this terminal conversation.

It is not a Spider Rose product feature unless Joel explicitly promotes it into product scope.

## Core Rule

When Codex changes a large chunk of code, Joel should be able to see what changed here in the terminal conversation.

The explanation should show a high-level overview first, then explain the implementation in small understandable chunks.

## Review Granularity

Simple functions should be explained in one plain-English line.

Related code blocks should be grouped into review chunks, usually around 5-20 lines of code.

Each chunk explanation should say:

- what the chunk does
- why it exists
- what behavior it affects

## Critical Code

The more critical the code is, the more observability Codex should provide.

Critical code includes:

- workflow execution
- block communication
- scraping logic
- storage
- dedupe behavior
- scheduler behavior
- external integrations
- user-visible inspector behavior

## What Joel Should See

For meaningful code changes, Codex should show:

1. High-level changed areas.
2. Chunk-by-chunk explanation.
3. Critical logic called out separately.
4. What to visually inspect or manually review.
5. What tests or checks were run.

## Change Rule

This process is expected to change during Spider Rose sessions with Codex.

When Joel changes the review preference, update this local `.wolf/codex-session/` process or follow the new session instruction directly.
