"""Vulnerability intelligence — correlation, mapping, risk."""

from .correlation import deduplicate_findings, correlate
from .mapping import enrich_finding, CWE_MAP, OWASP_MAP
from .risk import assign_severity, severity_rank

__all__ = [
    "deduplicate_findings",
    "correlate",
    "enrich_finding",
    "CWE_MAP",
    "OWASP_MAP",
    "assign_severity",
    "severity_rank",
]
