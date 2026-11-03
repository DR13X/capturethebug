"""Enumerations used across the platform."""

from enum import Enum


class Severity(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATIONAL = "Informational"
    UNKNOWN = "Unknown"


class FindingStatus(str, Enum):
    NEW = "New"
    NEEDS_VALIDATION = "Needs Validation"
    CONFIRMED = "Confirmed"
    FALSE_POSITIVE = "False Positive"
    FIXED = "Fixed"
    REOPENED = "Reopened"
    ACCEPTED_RISK = "Accepted Risk"


class ScannerSource(str, Enum):
    ZAP = "OWASP ZAP"
    NUCLEI = "Nuclei"
    BURP = "Burp Suite"
    NMAP = "Nmap"
    NESSUS = "Nessus"
    MANUAL = "Manual"


class OWASPCategory(str, Enum):
    A01 = "A01:2021 – Broken Access Control"
    A02 = "A02:2021 – Cryptographic Failures"
    A03 = "A03:2021 – Injection"
    A04 = "A04:2021 – Insecure Design"
    A05 = "A05:2021 – Security Misconfiguration"
    A06 = "A06:2021 – Vulnerable and Outdated Components"
    A07 = "A07:2021 – Identification and Authentication Failures"
    A08 = "A08:2021 – Software and Data Integrity Failures"
    A09 = "A09:2021 – Security Logging and Monitoring Failures"
    A10 = "A10:2021 – Server-Side Request Forgery"
    OTHER = "Other / Uncategorized"
