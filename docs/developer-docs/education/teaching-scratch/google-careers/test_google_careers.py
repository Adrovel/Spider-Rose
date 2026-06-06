from __future__ import annotations

from spider_rose.google_careers import format_google_careers_jobs, parse_google_careers_jobs
from spider_rose.tool_runner import _parse_google_task


HTML = """
<main>
<h2>Jobs search results</h2>
<ul>
<li>
<h3>Software Engineer III, AI Infrastructure</h3>
<span>Mid</span>
<div>Google | Bengaluru, Karnataka, India</div>
<h4>Minimum qualifications</h4>
<p>Bachelor's degree or equivalent practical experience.</p>
<p>2 years of experience with software development.</p>
</li>
<li>
<h3>Product Manager II, Google Cloud</h3>
<span>Mid</span>
<div>Google | Sunnyvale, CA, USA</div>
<h4>Minimum qualifications</h4>
<p>Bachelor's degree or equivalent practical experience.</p>
</li>
</ul>
</main>
"""


def test_parse_google_careers_jobs_extracts_job_cards():
    jobs = parse_google_careers_jobs(HTML)

    assert len(jobs) == 2
    assert jobs[0].title == "Software Engineer III, AI Infrastructure"
    assert jobs[0].location == "Bengaluru, Karnataka, India"
    assert jobs[0].level == "Mid"
    assert jobs[0].minimum_qualifications[0] == "Bachelor's degree or equivalent practical experience."


def test_format_google_careers_jobs_is_readable():
    jobs = parse_google_careers_jobs(HTML, limit=1)

    output = format_google_careers_jobs(jobs)

    assert "1. Software Engineer III, AI Infrastructure" in output
    assert "Location: Bengaluru, Karnataka, India" in output
    assert "Minimum qualifications:" in output


def test_parse_google_task_splits_query_and_location():
    assert _parse_google_task("software engineer in India") == ("software engineer", "India")
    assert _parse_google_task("product manager") == ("product manager", "")
