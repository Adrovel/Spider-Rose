from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urlencode
from urllib.request import Request, urlopen


GOOGLE_CAREERS_URL = "https://www.google.com/about/careers/applications/jobs/results/"


@dataclass(frozen=True)
class GoogleCareerJob:
    title: str
    location: str
    level: str
    minimum_qualifications: list[str]


class TextCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []

    def handle_data(self, data: str) -> None:
        value = " ".join(data.split())
        if value:
            self.values.append(value)


def scrape_google_careers_jobs(query: str = "", location: str = "", limit: int = 5) -> list[GoogleCareerJob]:
    html = fetch_google_careers_html(query=query, location=location)
    return parse_google_careers_jobs(html, limit=limit)


def fetch_google_careers_html(query: str = "", location: str = "") -> str:
    params = {}
    if query.strip():
        params["q"] = query.strip()
    if location.strip():
        params["location"] = location.strip()
    url = GOOGLE_CAREERS_URL
    if params:
        url = f"{url}?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": "SpiderRose/0.1"})
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_google_careers_jobs(html: str, limit: int = 5) -> list[GoogleCareerJob]:
    parser = TextCollector()
    parser.feed(html)
    lines = _relevant_lines(parser.values)
    jobs: list[GoogleCareerJob] = []
    index = _jobs_start(lines)

    while index < len(lines) and len(jobs) < limit:
        title = lines[index]
        company_line_index = _find_company_line(lines, index + 1)
        if not _looks_like_title(title) or company_line_index is None:
            index += 1
            continue

        level = _find_level(lines, index + 1, company_line_index)
        location = _clean_location(lines[company_line_index])
        qualifications, next_index = _collect_qualifications(lines, company_line_index + 1)
        jobs.append(
            GoogleCareerJob(
                title=title,
                location=location,
                level=level,
                minimum_qualifications=qualifications[:4],
            )
        )
        index = next_index

    return jobs


def format_google_careers_jobs(jobs: list[GoogleCareerJob]) -> str:
    if not jobs:
        return "No Google Careers jobs were found in the fetched page."

    blocks = []
    for number, job in enumerate(jobs, start=1):
        qualifications = "\n".join(f"  - {item}" for item in job.minimum_qualifications) or "  - Not listed"
        blocks.append(
            f"{number}. {job.title}\n"
            f"Location: {job.location}\n"
            f"Level: {job.level or 'Not listed'}\n"
            f"Minimum qualifications:\n{qualifications}"
        )
    return "\n\n".join(blocks)


def _relevant_lines(values: list[str]) -> list[str]:
    ignored = {"share", "Learn more", "link Copy link", "email Email a friend"}
    return [value for value in values if value not in ignored]


def _jobs_start(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        if line == "Jobs search results":
            return index + 1
    return 0


def _find_company_line(lines: list[str], start: int) -> int | None:
    for index in range(start, min(start + 12, len(lines))):
        if lines[index].startswith("Google |"):
            return index
    return None


def _looks_like_title(value: str) -> bool:
    blocked = {"Jobs search results", "Search Jobs", "Minimum qualifications"}
    return value not in blocked and len(value.split()) >= 2


def _find_level(lines: list[str], start: int, stop: int) -> str:
    known_levels = {"Early", "Mid", "Advanced", "Director+"}
    for index in range(start, stop):
        if lines[index] in known_levels:
            return lines[index]
    return ""


def _clean_location(company_line: str) -> str:
    return company_line.replace("Google |", "", 1).strip()


def _collect_qualifications(lines: list[str], start: int) -> tuple[list[str], int]:
    qualifications: list[str] = []
    index = start
    while index < len(lines):
        value = lines[index]
        if value == "Minimum qualifications":
            index += 1
            continue
        comp_index = _find_company_line(lines, index + 1)
        if comp_index is not None and (comp_index - index <= 2) and _looks_like_title(value):
            break
        if value and value not in {"Early", "Mid", "Advanced", "Director+"}:
            qualifications.append(value)
        index += 1
    return qualifications, index
