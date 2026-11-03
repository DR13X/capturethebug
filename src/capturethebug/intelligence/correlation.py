"""Finding correlation and deduplication."""

from __future__ import annotations

from collections import defaultdict

from capturethebug.models.finding import FindingCreate


def _merge_evidence(a, b):
    """Merge evidence lists without requiring hashability."""
    seen = set()
    merged = []
    for ev in list(a or []) + list(b or []):
        key = (ev.request, ev.response, ev.notes, ev.screenshot_path)
        if key not in seen:
            seen.add(key)
            merged.append(ev)
    return merged


def deduplicate_findings(findings: list[FindingCreate]) -> list[FindingCreate]:
    """
    Deduplicate by fingerprint. When duplicates exist, keep the highest-severity
    instance and merge evidence / references.
    """
    by_fp: dict[str, FindingCreate] = {}
    no_fp: list[FindingCreate] = []

    for f in findings:
        if not f.fingerprint:
            no_fp.append(f)
            continue
        if f.fingerprint not in by_fp:
            by_fp[f.fingerprint] = f
        else:
            existing = by_fp[f.fingerprint]
            from .risk import severity_rank

            if severity_rank(f.severity) > severity_rank(existing.severity):
                f.evidence = _merge_evidence(existing.evidence, f.evidence)
                f.references = list(dict.fromkeys((existing.references or []) + (f.references or [])))
                by_fp[f.fingerprint] = f
            else:
                existing.evidence = _merge_evidence(existing.evidence, f.evidence)
                existing.references = list(
                    dict.fromkeys((existing.references or []) + (f.references or []))
                )

    return list(by_fp.values()) + no_fp


def correlate(findings: list[FindingCreate]) -> dict[str, list[FindingCreate]]:
    """Group related findings by CWE or title similarity for reporting."""
    groups: dict[str, list[FindingCreate]] = defaultdict(list)
    for f in findings:
        key = f.cwe_id or f.title[:40]
        groups[key].append(f)
    return dict(groups)
