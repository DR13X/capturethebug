"""Report generation smoke tests."""

from pathlib import Path

from capturethebug.models.enums import FindingStatus, ScannerSource, Severity
from capturethebug.models.finding import Assessment, Finding, ReportConfig
from capturethebug.reporting.generator import ReportGenerator


def test_html_report(tmp_path: Path):
    assessment = Assessment(name="Demo App", client="ACME Corp", target_urls=["https://example.com"])
    findings = [
        Finding(
            assessment_id=assessment.id,
            title="Broken Access Control",
            description="Unauthorized access to protected resources.",
            severity=Severity.HIGH,
            status=FindingStatus.NEEDS_VALIDATION,
            cwe_id="CWE-862",
            affected_endpoint="/api/example/resource",
            scanner=ScannerSource.NUCLEI,
            impact="Unauthorized access to protected resources.",
            remediation="Enforce server-side authorization checks for every protected resource.",
        ),
        Finding(
            assessment_id=assessment.id,
            title="Missing Security Headers",
            severity=Severity.INFORMATIONAL,
            status=FindingStatus.CONFIRMED,
            scanner=ScannerSource.ZAP,
        ),
    ]
    gen = ReportGenerator()
    out = tmp_path / "report.html"
    gen.generate_html(assessment, findings, ReportConfig(), out)
    assert out.exists()
    text = out.read_text()
    assert "Broken Access Control" in text
    assert "Executive Summary" in text or "executive" in text.lower() or "Critical" in text


def test_json_report(tmp_path: Path):
    assessment = Assessment(name="Demo")
    findings = [
        Finding(
            assessment_id=assessment.id,
            title="Test Finding",
            severity=Severity.MEDIUM,
            status=FindingStatus.CONFIRMED,
            scanner=ScannerSource.MANUAL,
        )
    ]
    gen = ReportGenerator()
    out = tmp_path / "report.json"
    gen.generate_json(assessment, findings, ReportConfig(), out)
    assert out.exists()
    import json

    data = json.loads(out.read_text())
    assert data["findings"][0]["title"] == "Test Finding"
