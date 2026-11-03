"""Scanner result parsers."""

from .base import BaseParser, ParseResult
from .zap import ZAPParser
from .nuclei import NucleiParser
from .nmap import NmapParser

PARSERS = {
    "zap": ZAPParser,
    "nuclei": NucleiParser,
    "nmap": NmapParser,
}

__all__ = ["BaseParser", "ParseResult", "ZAPParser", "NucleiParser", "NmapParser", "PARSERS"]
