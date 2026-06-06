# Antigravity Agent IDE Competitor Research

Version: 0.1.0  
Status: Competitor research note  
Last updated: 2026-06-04

Purpose: understand what Spider Rose should learn from Google Antigravity without copying the wrong product shape.

Sources:

- Google Antigravity docs: https://www.antigravity.google/docs/home
- Antigravity IDE product page: https://www.antigravity.google/product/antigravity-ide
- Antigravity 2 product page: https://www.antigravity.google/product/antigravity-2

## Competitor Summary

Antigravity is an agent-first software development product. Its center is the developer workspace: editor, codebase, tasks, autonomous agents, browser control, and verification.

The product direction is:

```text
Developer task
  -> agent plans
  -> agent edits code / uses tools
  -> agent verifies work
  -> developer reviews
```

Spider Rose should not compete as another AI coding IDE.

Spider Rose's stronger direction is:

```text
Local visual workflow
  -> reusable blocks pass JSON
  -> outputs are stored as artifacts
  -> user inspects and composes the workflow
```

## What Spider Rose Should Learn

### 1. Make Agent Work Visible

Antigravity treats agent work as something the user can supervise, not a hidden chatbot answer.

Spider Rose should do the same through workflow blocks:

- show each block's input
- show each block's output
- show the connector payload
- show where artifacts are stored
- show what failed and why

For the Google Careers workflow, the user should be able to inspect:

```text
Web Scraper input:
Site: Google Careers
Description: Find software engineering jobs in India.

Web Scraper output:
JSON job_results

Store output:
artifacts/google-careers/job-results.jsonl
```

### 2. Keep A Review Layer

Antigravity's agent-first direction assumes users need to review autonomous work.

Spider Rose should make review a normal part of workflows:

- preview block output before storing
- show record count before save
- show duplicate count after store
- let user approve a workflow before scheduler/WhatsApp are added

This matters because Spider Rose will handle scraped data, external websites, and messaging channels.

### 3. Separate Builder From Runner

Antigravity is strong because the product has a clear work surface for building and supervising agent tasks.

Spider Rose should distinguish:

- Build mode: arrange blocks, configure fields, connect outputs
- Run mode: execute a selected workflow and show block-by-block results
- Review mode: inspect artifacts, duplicates, errors, and stored records

This avoids making the visual grid only decorative.

### 4. Use Artifacts As Trust Anchors

Coding agents gain trust when they show diffs, tests, logs, and browser results.

Spider Rose should gain trust through workflow artifacts:

- scraped JSON result
- saved JSONL record
- job URL
- run timestamp
- source URL
- error message when scraping fails

For v0, the trust anchor is a real job link saved in `artifacts/google-careers/job-results.jsonl`.

### 5. Avoid Becoming An IDE

Antigravity's core product is code work. Spider Rose should stay away from editor competition.

Do not optimize Spider Rose around:

- code autocomplete
- repo-wide code editing
- autonomous programming agents
- IDE command palettes
- coding benchmark performance

Optimize Spider Rose around:

- block composition
- local workflow files
- inspectable data passing
- artifacts
- simple automation workflows

## Product Difference

| Question | Antigravity | Spider Rose |
|---|---|---|
| Main surface | AI IDE / agent manager | visual workflow grid |
| Primary job | build and modify software | compose local agent/automation workflows |
| Main user action | assign a coding task to an agent | connect reusable blocks |
| Trust object | code diff, test result, browser result | JSON message, JSONL artifact, source link |
| Best proof | code works | workflow output is saved and inspectable |
| Risk to avoid | agent edits too much autonomously | blocks become hidden magic |

## How To Make Spider Rose Better

### Improve The Canvas

Make the canvas show execution truth, not only arrangement:

- each block has status: idle, running, success, failed
- each connector can be clicked to inspect JSON payload
- each block has an output preview
- each run creates a saved artifact

### Improve Block Design

Blocks should have small, visible contracts:

```text
Inputs
Outputs
Artifacts
Errors
```

For the Web Scraper block:

```text
Inputs:
- site
- scrape description

Output:
- JSON job_results

Artifact:
- raw fetch snapshot, optional later

Errors:
- site unreachable
- no results found
- parse failed
```

### Improve Safety

Antigravity's autonomy makes safety and review important. Spider Rose should avoid hidden external actions.

Rules:

- scraping writes to local artifacts first
- WhatsApp sending is not automatic in v0
- scheduler is not added until manual runs are clear
- block output must be inspectable before it flows to external messaging

### Improve Positioning

Use this distinction:

```text
Antigravity is an agentic IDE for building software.
Spider Rose is a local visual workflow builder for composing reusable agent and automation blocks.
```

## Concrete Takeaways For The Google Careers Workflow

The first workflow should stay small:

```text
[Web Scraper: Google Careers]
  -> [Store: Job Results]
```

Recommended behavior:

- Web Scraper accepts `site` and `scrape_description`.
- Web Scraper outputs JSON.
- Store saves JSONL.
- User inspects saved job links.
- Scheduler and WhatsApp wait until this manual workflow is trusted.

## Open Questions

- Should a connector be clickable to show the JSON payload?
- Should every block show its latest output preview?
- Should raw scraped HTML be stored as an artifact, or only extracted records?
- Should Store deduplicate by URL by default?
- Should failed runs create error artifacts?

## Follow-Up Todo

Add a "grill me" teaching/review skill for Spider Rose planning.

Purpose:

- challenge weak assumptions before implementation
- ask Antigravity-style review questions about visibility, artifacts, trust, and user control
- help Joel and Mukthar catch product confusion before code changes

This should be a planning/education tool first, not runtime behavior.
