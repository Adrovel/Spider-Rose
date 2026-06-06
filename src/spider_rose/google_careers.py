from __future__ import annotations

from dataclasses import asdict, dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
import time
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen


GOOGLE_CAREERS_URL = "https://www.google.com/about/careers/applications/jobs/results/"


@dataclass(frozen=True)
class GoogleCareerJob:
    title: str
    location: str
    url: str
    level: str
    minimum_qualifications: list[str]
    source: str = "google_careers"


@dataclass(frozen=True)
class ScrapeResult:
    jobs: list[GoogleCareerJob]
    fetched_url: str
    duration_ms: int
    network_requests: int


@dataclass(frozen=True)
class StoreResult:
    type: str
    storage_path: str
    stored_count: int
    new_count: int
    duplicate_count: int
    dedupe_key: str
    sample_records: list[dict]


@dataclass(frozen=True)
class _TextToken:
    value: str
    href: str


class _GoogleCareersParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tokens: list[_TextToken] = []
        self._href_stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href") or ""
        self._href_stack.append(urljoin(GOOGLE_CAREERS_URL, href) if "/jobs/results/" in href else "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href_stack:
            self._href_stack.pop()

    def handle_data(self, data: str) -> None:
        value = " ".join(data.split())
        if value:
            self.tokens.append(_TextToken(value=value, href=self._href_stack[-1] if self._href_stack else ""))


def scrape_google_careers_jobs(query: str = "software engineer", location: str = "India", limit: int = 5) -> ScrapeResult:
    start = time.perf_counter()
    fetched_url = google_careers_url(query=query, location=location)
    html = fetch_google_careers_html(fetched_url)
    jobs = parse_google_careers_jobs(html, limit=limit)
    duration_ms = int((time.perf_counter() - start) * 1000)
    return ScrapeResult(jobs=jobs, fetched_url=fetched_url, duration_ms=duration_ms, network_requests=1)


def google_careers_url(query: str = "", location: str = "") -> str:
    params = {"hl": "en_US"}
    if query.strip():
        params["q"] = query.strip()
    if location.strip():
        params["location"] = location.strip()
    return f"{GOOGLE_CAREERS_URL}?{urlencode(params)}"


def fetch_google_careers_html(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 SpiderRose/0.1",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urlopen(request, timeout=12) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_google_careers_jobs(html: str, limit: int = 5) -> list[GoogleCareerJob]:
    parser = _GoogleCareersParser()
    parser.feed(html)
    tokens = _relevant_tokens(parser.tokens)
    jobs: list[GoogleCareerJob] = []
    index = _jobs_start(tokens)

    while index < len(tokens) and len(jobs) < limit:
        title = tokens[index]
        company_line_index = _find_company_line(tokens, index + 1)
        if not _looks_like_title(title.value) or company_line_index is None:
            index += 1
            continue

        level = _find_level(tokens, index + 1, company_line_index)
        location = _clean_location(tokens[company_line_index].value)
        qualifications, next_index = _collect_qualifications(tokens, company_line_index + 1)
        jobs.append(
            GoogleCareerJob(
                title=title.value,
                location=location,
                url=title.href,
                level=level,
                minimum_qualifications=qualifications[:4],
            )
        )
        index = next_index

    return [job for job in jobs if job.url]


def store_google_careers_jobs(root: Path, jobs: list[GoogleCareerJob]) -> StoreResult:
    path = root / "artifacts" / "google-careers" / "job-results.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_urls = _existing_urls(path)
    new_jobs = [job for job in jobs if job.url not in existing_urls]
    with path.open("a", encoding="utf-8") as handle:
        for job in new_jobs:
            handle.write(json.dumps(asdict(job), sort_keys=True) + "\n")

    stored_count = len(existing_urls) + len(new_jobs)
    return StoreResult(
        type="store_result",
        storage_path=str(path.relative_to(root)),
        stored_count=stored_count,
        new_count=len(new_jobs),
        duplicate_count=len(jobs) - len(new_jobs),
        dedupe_key="url",
        sample_records=[asdict(job) for job in jobs[:3]],
    )


def _existing_urls(path: Path) -> set[str]:
    if not path.exists():
        return set()
    urls: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            url = json.loads(line).get("url", "")
        except json.JSONDecodeError:
            continue
        if url:
            urls.add(url)
    return urls


def _relevant_tokens(tokens: list[_TextToken]) -> list[_TextToken]:
    ignored = {"share", "Learn more", "link Copy link", "email Email a friend"}
    return [token for token in tokens if token.value not in ignored]


def _jobs_start(tokens: list[_TextToken]) -> int:
    for index, token in enumerate(tokens):
        if token.value == "Jobs search results":
            return index + 1
    return 0


def _find_company_line(tokens: list[_TextToken], start: int) -> int | None:
    for index in range(start, min(start + 12, len(tokens))):
        if tokens[index].value.startswith("Google |"):
            return index
    return None


def _looks_like_title(value: str) -> bool:
    blocked = {"Jobs search results", "Search Jobs", "Minimum qualifications"}
    return value not in blocked and len(value.split()) >= 2


def _find_level(tokens: list[_TextToken], start: int, stop: int) -> str:
    known_levels = {"Early", "Mid", "Advanced", "Director+"}
    for index in range(start, stop):
        if tokens[index].value in known_levels:
            return tokens[index].value
    return ""


def _clean_location(company_line: str) -> str:
    return company_line.replace("Google |", "", 1).strip()


def _collect_qualifications(tokens: list[_TextToken], start: int) -> tuple[list[str], int]:
    qualifications: list[str] = []
    index = start
    while index < len(tokens):
        value = tokens[index].value
        if value == "Minimum qualifications":
            index += 1
            continue
        company_index = _find_company_line(tokens, index + 1)
        if company_index is not None and (company_index - index <= 2) and _looks_like_title(value):
            break
        if value and value not in {"Early", "Mid", "Advanced", "Director+"}:
            qualifications.append(value)
        index += 1
    return qualifications, index
