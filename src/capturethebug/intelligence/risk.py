"""Severity ranking and contextual risk helpers."""

from __future__ import annotations

from capturethebug.models.enums import Severity

_RANK = {
    Severity.CRITICAL: 5,
    Severity.HIGH: 4,
    Severity.MEDIUM: 3,
    Severity.LOW: 2,
    Severity.INFORMATIONAL: 1,
    Severity.UNKNOWN: 0,
}


def severity_rank(sev: Severity | str) -> int:
    if isinstance(sev, str):
        try:
            sev = Severity(sev)
        except ValueError:
            return 0
    return _RANK.get(sev, 0)


def assign_severity(cvss: float | None = None, scanner_severity: Severity | None = None) -> Severity:
    """Derive severity from CVSS when available, else trust scanner."""
    if cvss is not None:
        if cvss >= 9.0:
            return Severity.CRITICAL
        if cvss >= 7.0:
            return Severity.HIGH
        if cvss >= 4.0:
            return Severity.MEDIUM
        if cvss >= 0.1:
            return Severity.LOW
        return Severity.INFORMATIONAL
    return scanner_severity or Severity.UNKNOWN
