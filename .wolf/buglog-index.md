# Buglog Index

> Search this file before opening bug JSONL sources. Active Spider Rose bugs live in `.wolf/buglog.jsonl`; archived bugs live under `.wolf/archive/`.

Use examples:

```bash
rg -n "visualise|agent|runtime|packaging" .wolf/buglog-index.md
rg -n "bug-001" .wolf/buglog-index.md .wolf/buglog.jsonl .wolf/archive
```

JSONL shape:

```json
{"id":"bug-001","timestamp":"2026-06-01T00:00:00.000Z","error_message":"Short failure name","file":"path/to/file","root_cause":"Why it happened","fix":"What changed","tags":["manual","runtime"],"related_bugs":[],"occurrences":1,"last_seen":"2026-06-01T00:00:00.000Z"}
```

| ID | Last Seen | Tags | Source:Line | File | Error | Fix |
|---|---|---|---|---|---|---|
