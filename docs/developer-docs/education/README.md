# Spider Rose Education

Version: 0.1.0  
Status: Learning workspace  
Last updated: 2026-06-04

Purpose: help Joel and Mukthar understand Spider Rose by walking through concrete workflows before implementation starts.

## Product Model

Spider Rose should be understood as a visual workflow grid made from reusable fundamental blocks.

The first teaching workflow is:

```text
[Web Scraper: Google Careers]
  -> [Store: Job Results]
```

Google Careers is the first site used for product clarity. It is an input/configuration inside the Web Scraper block, not automatically a permanent one-off block.

Scheduler and WhatsApp blocks are intentionally removed from the first walkthrough. They can return after Joel and Mukthar understand the smaller scraping-and-storage workflow.

## Learning Rule

Education docs are for product clarity and shared understanding. They do not approve code changes by themselves.

Implementation still requires:

- an atomic-plan item
- Joel product approval
- Mukthar technical review when available
- explicit approval before code changes

## Files

- [Google Careers Workflow Learning](./Google-Careers-Workflow-Learning.md)
- [Fundamental Blocks Primer](./Fundamental-Blocks-Primer.md)
- [Google Careers Teaching Scratch](./teaching-scratch/google-careers/README.md)
