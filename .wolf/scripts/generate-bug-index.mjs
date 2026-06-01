import fs from "fs";
import path from "path";

const sources = [
  { file: ".wolf/buglog.jsonl", source: "active" },
  ...archiveSources(),
];

function archiveSources() {
  const archiveDir = ".wolf/archive";
  if (!fs.existsSync(archiveDir)) return [];
  return fs.readdirSync(archiveDir)
    .filter((name) => /^buglog-.+\.jsonl$/.test(name))
    .sort()
    .map((name) => ({
      file: path.join(archiveDir, name),
      source: name.replace(/\.jsonl$/, ""),
    }));
}

function readJsonl(file, source) {
  if (!fs.existsSync(file)) return [];
  return fs.readFileSync(file, "utf8")
    .split(/\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line, index) => {
      try {
        return { ...JSON.parse(line), _source: source, _line: index + 1 };
      } catch (error) {
        throw new Error(`${file}:${index + 1}: ${error.message}`);
      }
    });
}

function cell(value) {
  return String(value || "")
    .replace(/\s+/g, " ")
    .replace(/\|/g, "\\|")
    .trim();
}

const bugs = sources.flatMap(({ file, source }) => readJsonl(file, source));
bugs.sort((a, b) => {
  const aNumber = Number(String(a.id || "").replace(/^bug-/, ""));
  const bNumber = Number(String(b.id || "").replace(/^bug-/, ""));
  return aNumber - bNumber;
});

const rows = bugs.map((bug) => {
  const tags = Array.isArray(bug.tags) ? bug.tags.join(", ") : "";
  const location = `${bug._source}:${bug._line}`;
  return `| ${cell(bug.id)} | ${cell(bug.last_seen || bug.timestamp)} | ${cell(tags)} | ${cell(location)} | ${cell(bug.file)} | ${cell(bug.error_message)} | ${cell(bug.fix)} |`;
});

const output = [
  "# Buglog Index",
  "",
  "> Search this file before opening bug JSONL sources. Active Spider Rose bugs live in `.wolf/buglog.jsonl`; archived bugs live under `.wolf/archive/`.",
  "",
  "Use examples:",
  "",
  "```bash",
  "rg -n \"visualise|agent|runtime|packaging\" .wolf/buglog-index.md",
  "rg -n \"bug-001\" .wolf/buglog-index.md .wolf/buglog.jsonl .wolf/archive",
  "```",
  "",
  "JSONL shape:",
  "",
  "```json",
  "{\"id\":\"bug-001\",\"timestamp\":\"2026-06-01T00:00:00.000Z\",\"error_message\":\"Short failure name\",\"file\":\"path/to/file\",\"root_cause\":\"Why it happened\",\"fix\":\"What changed\",\"tags\":[\"manual\",\"runtime\"],\"related_bugs\":[],\"occurrences\":1,\"last_seen\":\"2026-06-01T00:00:00.000Z\"}",
  "```",
  "",
  "| ID | Last Seen | Tags | Source:Line | File | Error | Fix |",
  "|---|---|---|---|---|---|---|",
  ...rows,
  "",
].join("\n");

fs.writeFileSync(".wolf/buglog-index.md", output);
console.log(`indexed ${bugs.length} bugs from ${sources.length} JSONL sources`);
