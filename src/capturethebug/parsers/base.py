"""Base parser interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from capturethebug.models.finding import FindingCreate


class ParseResult:
    def __init__(self, findings: list[FindingCreate], source: str, errors: list[str] | None = None):
        self.findings = findings
        self.source = source
        self.errors = errors or []

    @property
    def count(self) -> int:
        return len(self.findings)


class BaseParser(ABC):
    """Abstract parser for scanner exports."""

    source_name: str = "unknown"

    @abstractmethod
    def parse(self, path: Union[str, Path]) -> ParseResult:
        """Parse a file and return normalized FindingCreate objects."""
        ...

    def supports(self, path: Union[str, Path]) -> bool:
        """Heuristic check whether this parser can handle the file."""
        return False
