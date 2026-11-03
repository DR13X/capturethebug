"""Parser unit tests."""

from pathlib import Path

import pytest

from capturethebug.parsers.nuclei import NucleiParser
from capturethebug.parsers.zap import ZAPParser
from capturethebug.intelligence.correlation import deduplicate_findings
from capturethebug.intelligence.mapping import enrich_finding
from capturethebug.models.enums import Severity

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def test_nuclei_parse():
    parser = NucleiParser()
    result = parser.parse(SAMPLES / "nuclei-sample.jsonl")
    assert result.count >= 4
    assert any(f.severity == Severity.CRITICAL for f in result.findings)
    titles = [f.title for f in result.findings]
    assert any("Log4j" in t or "XSS" in t or "SQL" in t for t in titles)


def test_zap_parse():
    parser = ZAPParser()
    result = parser.parse(SAMPLES / "zap-sample.json")
    assert result.count >= 2
    assert any("Scripting" in f.title or "XSS" in f.title for f in result.findings)


def test_dedupe():
    parser = NucleiParser()
    result = parser.parse(SAMPLES / "nuclei-sample.jsonl")
    findings = result.findings + result.findings  # duplicate set
    deduped = deduplicate_findings(findings)
    assert len(deduped) == len(result.findings)


def test_enrich():
    parser = NucleiParser()
    result = parser.parse(SAMPLES / "nuclei-sample.jsonl")
    for f in result.findings:
        enrich_finding(f)
    xss = next((f for f in result.findings if f.cwe_id and "79" in f.cwe_id), None)
    if xss:
        assert xss.remediation
