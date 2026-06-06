# Demo And Outreach Plan

Status: Active immediate plan  
Created: 2026-06-05

Spider Rose has shifted toward making the current two-block workflow demoable.

The first demo should use what already exists: the Web Scraper block, the Store block, and the visual connection between them.

## Current Demo Focus

Make one small web feel clear.

Resource use should stay cheap for every feature.

Resource-use visibility is for Joel's planning and approval, not for the app's layman-facing UI. Before implementing a feature, Joel should know the cost of each resource used: network requests, runtime duration, disk writes, stored file size, dependency cost, retry behavior, and expected limits.

In product language:

- agents can be called **spiders**
- workflows can be called **webs**
- a web is made of connected spiders/blocks

The first demo web:

```text
Web Scraper: Google Careers -> Store: Job Results
```

## Immediate Product Direction

Iterate over the current two-block demo in this order:

1. Functionality: scrape real Google Careers jobs.
2. Honest failure state when scraping cannot work.
3. Progress chips.
4. Block behavior.
5. Connector behavior.
6. Right sidebar behavior.
7. Demo story.

## Demo Audience

Planned demo audience:

- Fahim
- Alfeen
- Don
- Christie
- Prithvi
- Mubaris
- Pranav
- Joel Sam
- Gowri
- Athul
- Mevit
- Varsha
- Reshma
- Nithin Noushad
- Joel
- others

## GitHub Plan

Goal: make the repository understandable to technical reviewers.

Focus:

- README should explain the two-block demo clearly.
- Screenshots or GIF should show the web visually.
- The repo should show that Spider Rose is local-first.
- Avoid claiming real scraping until it exists.
- Show the current demo as a product direction, not a finished automation platform.

## LinkedIn Plan

Goal: share progress without overclaiming.

Focus:

- Frame Spider Rose as a local visual way to connect small agents/spiders.
- Show the Google Careers demo as the first tiny web.
- Say it is early and being shaped through demos.
- Ask for feedback on clarity, not adoption.

## Content Creator Outreach

Goal: find people who can react to the product idea and visual clarity.

Focus:

- Send a short demo clip or screenshot.
- Explain the idea in one line: connect small spiders into webs that run useful workflows.
- Ask whether the visual flow is understandable.
- Do not pitch it as a mature tool yet.

## Current Non-Goals

- Do not add back the Tools feature surface for this demo.
- Do not add more blocks before the two-block web is demoable.
- Do not show `hello` or `researcher` agents in the current demo.
- Do not show zoom controls or infinite-canvas behavior in the current demo.
- Do not call mock data real scraping.
- Do not make queued UI notes into atomic-plan tasks without Joel approval.
