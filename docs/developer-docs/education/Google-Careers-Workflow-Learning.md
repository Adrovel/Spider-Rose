# Google Careers Workflow Learning

Version: 0.1.0  
Status: Product clarity walkthrough  
Last updated: 2026-06-04

Purpose: help Joel and Mukthar understand Spider Rose by designing a simple workflow that searches Google Careers and returns job results.

## Scenario

Joel thinks he should build a simple workflow that scrapes the Google Careers site and gets job searches back.

This is not a request to hard-code a one-off Google Careers agent. It is a learning scenario for designing fundamental blocks.

## Current Teaching Workflow

```text
[Web Scraper: Google Careers]
  -> [Store: Job Results]
```

This is the first visible workflow. The goal is not to create many tiny blocks too early.

For now, the Web Scraper block owns:

- the search input
- the website/source setting
- fetching the page
- extracting useful job fields

The Store block owns:

- saving job results
- remembering previous results
- helping the workflow avoid duplicate output later

## Concrete Example

The Web Scraper block is configured with two visible fields:

```text
site: Google Careers
scrape_description: Find software engineering jobs in India and return job links.
```

The flow:

1. Web Scraper block reads the `site` and `scrape_description`.
2. Web Scraper block fetches matching results from Google Careers.
3. Web Scraper block extracts useful fields such as title, location, level, qualifications, and result URL.
4. Store block saves the extracted job records.
5. Store block can later compare new runs against previous runs.

## Data Contract v0

Block-to-block communication should use JSON.

The Web Scraper block should output:

```json
{
  "type": "job_results",
  "source": "google_careers",
  "records": [
    {
      "title": "Software Engineer",
      "location": "Bengaluru, India",
      "url": "https://www.google.com/about/careers/applications/jobs/results/..."
    }
  ]
}
```

The Store block should save records as JSONL:

```jsonl
{"title":"Software Engineer","location":"Bengaluru, India","url":"https://www.google.com/about/careers/applications/jobs/results/...","source":"google_careers","seen_at":"2026-06-04"}
```

The Store block should return a JSON summary after saving:

```json
{
  "type": "store_result",
  "storage_path": "artifacts/google-careers/job-results.jsonl",
  "storage_method": "working_proposal",
  "stored_count": 12,
  "new_count": 3,
  "duplicate_count": 9,
  "dedupe_key": "url",
  "sample_records": [
    {
      "title": "Software Engineer",
      "location": "Bengaluru, India",
      "url": "https://www.google.com/about/careers/applications/jobs/results/..."
    }
  ]
}
```

The visual UI should translate that into human language:

```text
Saved to: artifacts/google-careers/job-results.jsonl
Total saved: 12
New this run: 3
Already seen: 9
Matched by: job link
Sample:
- Software Engineer, Bengaluru
```

`sample_records` is included for v0 so Joel can verify real job links without opening the JSONL file.

Working storage proposal:

```text
artifacts/google-careers/job-results.jsonl
```

The artifact method is still in doubt and debatable. `artifacts/` is the current working proposal because it keeps generated workflow results separate from human-authored docs, agents, and project config.

The first proof that the workflow worked is a real job link saved in the Store block output.

## Visual Proof v0

The first proof should appear in a right-side inspector panel when the Store block is selected.

What appears inside the grid block itself is undecided and should be designed later.

The inspector should show details:

```text
Store: Job Results

Saved to:
artifacts/google-careers/job-results.jsonl

New this run:
3

Already seen:
9

Matched by:
job link

Sample links:
- Software Engineer, Bengaluru
  https://www.google.com/about/careers/applications/jobs/results/...
```

## Run States v0

Each visible workflow block should support four run states:

```text
Idle
Running
Success
Failed
```

Example successful run:

```text
Web Scraper: Success
Store: Success
```

Example failed scrape:

```text
Web Scraper: Failed
Store: Idle
```

This keeps the visual workflow honest. The user can see where the workflow stopped before opening the right-side inspector.

## Connector Meaning v0

The first connector is a data connector.

Internal contract:

```json
{
  "kind": "data",
  "from": "web_scraper",
  "to": "store",
  "payload_type": "job_results"
}
```

Meaning:

```text
Pass the Web Scraper JSON output into the Store block.
```

User-facing labels should be non-technical. The UI should not expose terms like `payload_type` or `job_results` unless the user opens a developer/details view.

Possible user-facing wording:

```text
Jobs found
```

This wording can be redesigned later.

## Mock Data Boundary

The first visual demo may use mock job results to validate the workflow shape quickly.

This is an exception, not a default rule. Joel is concerned that mock data can drift away from real problem-solving, especially for small workflows where the real task should not be too large.

Mock data is acceptable here only to validate:

- the two visible blocks
- run states
- connector meaning
- right-side inspector output
- Store output preview

The product should move to real Google Careers scraping after the visual shape is validated.

## First Implementation Slice

Status: Joel approved for product direction; Mukthar technical review is useful when available, but not a product blocker.

The first implementation slice is a visual-only Google Careers workflow demo:

```text
[Web Scraper: Google Careers]
  -> [Store: Job Results]
```

Scope:

- two visible blocks
- one connector
- four run states
- mock `job_results` JSON for this demo only
- right-side inspector for Store output
- sample job links in the inspector

Out of scope:

- real Google Careers scraping
- scheduler
- WhatsApp
- final storage decision
- deciding what information appears inside each grid block

## What This Teaches

The product should separate visible blocks from internal block responsibilities.

Google Careers is a site input/configuration. Web scraping is the reusable capability.

The first learning goal is to understand:

- what fields the Web Scraper block needs
- what useful job output it should produce
- whether extraction should remain inside Web Scraper for v0
- what the Store block should save
- why the Store block returns counts, a dedupe rule, and `sample_records`
- why JSON is the block message format and JSONL is the stored record format
- whether `artifacts/` is the right storage folder for workflow outputs
- why detailed Store results belong in a right-side inspector panel
- what information, if any, belongs inside the grid block itself
- why blocks need four visible run states: Idle, Running, Success, Failed
- why the first connector passes found jobs from Web Scraper to Store
- how to keep user-facing connector labels non-technical
- how much value exists before scheduler and WhatsApp blocks are added

## Open Questions For Joel And Mukthar

- Are `site` and `scrape_description` enough for the first visible Web Scraper block?
- Should generated workflow records live under `artifacts/`, or should Spider Rose use another storage model?
- What information should appear inside each block on the grid?
- Is `sample_records` enough for the first Store output preview?
- When should extraction become its own visible block, if ever?
- What does Joel want to inspect before WhatsApp and scheduler are added back?

## Atomic Plan Boundary

Before code changes, this scenario needs an approved atomic-plan item.

Suggested item:

```text
Define the Google Careers learning workflow using two visible blocks:
Web Scraper: Google Careers -> Store: Job Results.
```
