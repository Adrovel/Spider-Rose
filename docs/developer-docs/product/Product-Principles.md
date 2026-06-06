# Spider Rose Product Principles

Version: 0.1.0  
Status: Active product guardrails  
Last updated: 2026-06-04

Purpose: keep Spider Rose from becoming overbuilt before users prove what matters.

## Core Principles

### 1. Simple To Use

Spider Rose should be understandable from one command:

```bash
spiderrose
```

The user should not need to understand orchestration theory, LangGraph internals, workflow engines, or config files before creating and connecting useful blocks.

Default behavior should be useful:

- new projects preload the `google-careers-scraper` demo agent while the two-block demo is the immediate priority
- users can type natural tasks
- slash commands are reserved for app actions
- generated files are visible and editable
- errors should say what to do next

### Resource Use Must Stay Cheap

Every feature should be cheap enough for a developer installing the Spider Rose SDK/CLI in a Linux terminal.

Before implementing a feature, Joel should see the expected resource cost so he can make the product decision.

Resource review should include:

- network requests
- runtime duration
- disk writes
- stored file size
- dependency cost
- retry behavior
- expected limits

This resource-use review is for Joel's planning and approval. The app UI should stay understandable for laymen and should not expose technical cost details unless that is explicitly approved.

### 2. Fundamental Blocks First

Spider Rose should avoid one-off blocks for every site or scenario.

Prefer reusable fundamental blocks:

- Input
- Website Source
- Web Scraper
- Extractor
- Store/RAG
- Scheduler
- Formatter
- WhatsApp Sender
- Agent

Specific targets such as Google Careers, Instagram, or a company career page should usually be inputs/configuration for reusable blocks.

### Non-Technical Labels

Spider Rose can use technical internal contracts, but normal user-facing words should stay simple.

Examples:

- show `Jobs found`, not `job_results`
- show `Matched by: job link`, not `dedupe_key: url`
- show `Already seen`, not `duplicate_count`

Developer/internal details can exist in an inspector or advanced view later.

### Question Mock Data

Mock data should be questioned before it is used in Spider Rose workflows.

Joel is skeptical of mock data because it can drift away from actual problem solving. The product should not assume mock data is the right starting point.

Mock data may still be useful when it is explicitly approved for a narrow purpose, such as validating visual flow, run states, connector meaning, or inspector layout before a real integration is ready.

Mock data is risky because it can:

- drift away from actual problem solving
- make the product feel more complete than it is
- hide source, parsing, storage, and error-handling problems
- delay the real workflow that users actually need

For small workflows, ask whether real data is feasible before choosing mock data.

When mock data is used:

- label it as mock/demo data
- do not let it define final scraper or block behavior
- replace it with real data as soon as the workflow shape is validated
- keep the real problem visible in the atomic plan

### 3. Simple UI

The UI should stay quiet, black-themed, and functional.

Phase 1 UI rules:

- show agents
- create agents
- edit agent Markdown
- show where the agent is stored
- make the visual grid understandable before adding execution complexity
- avoid dashboards, charts, marketing panels, and decorative layouts

Simple does not mean unfinished. It means the user can immediately see what exists, edit it, and keep moving.

## Implementation Guardrail

No actual code changes should happen without Joel and Mukthar overlooking the work.

No feature addition should happen until it goes through the atomic-plan phase and is approved.

Default flow:

1. Capture the product scenario or requirement.
2. Add or update the atomic-plan item.
3. Review with Joel and Mukthar.
4. Implement only after approval.
5. Run the relevant local check before any commit/push decision.

## Complexity Gate

Do not add major abstractions before there is user pressure.

Examples of gated complexity:

- workflow canvas
- executable workflow runtime
- authentication
- cloud accounts
- billing
- marketplace
- team permissions
- distributed runtime
- heavy local databases

The question before adding complexity:

```text
Would this help the next 10 users, or is it architecture vanity?
```

If the answer is unclear, document it in `Future-Features.md` instead of building it.
