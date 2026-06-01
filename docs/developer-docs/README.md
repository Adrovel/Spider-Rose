# Spider Rose Developer Docs

Version: 0.1.0  
Status: Working developer docs  
Last updated: 2026-06-01

This folder is the working map for Spider Rose development. Start here, then open the smallest doc that matches the work.

## Start Here

- [Product description](./product/Description.md)
- [Current features](./product/Features.md)
- [Architecture](./implementation/Architecture.md)
- [Implementation plan](./planning/Plan.md)

## Product

Product docs explain what Spider Rose is, who it is for, and what promises the app should keep.

- [Description](./product/Description.md)
- [Features](./product/Features.md)
- [Product Principles](./product/Product-Principles.md)

## Implementation

Implementation docs describe the current code shape, file model, command surface, and UI behavior.

- [Architecture](./implementation/Architecture.md)
- [Agents](./implementation/Agents.md)
- [Stacks and Tools](./implementation/Stacks-and-Tools.md)
- [Terminal UX Plan](./implementation/Terminal-UX-Plan.md)
- [UI Plan Layer](./implementation/UI-Plan-Layer.md)

## Planning

Planning docs track phased work, atomic tasks, and features intentionally pushed out of the current MVP.

- [Plan](./planning/Plan.md)
- [Atomic Plan](./planning/Atomic-Plan.md)
- [Future Features](./planning/Future-Features.md)

## Team

- [Team](./team/Team.md)
- [Design Choices](./team/Design-Choices.md)

## Related Docs

- [Research Docs](../research-docs/README.md)
- [GitHub Workflow Standards](../engineering-standards/GitHub-Workflow.md)

## Component Review

Storybook is used for UI component review.

```bash
npm run storybook
npm run build-storybook
```

## Organization Rule

Keep docs short and decision-oriented. If a doc starts mixing product description, architecture, roadmap, task tracking, and research, split it before implementation continues.
