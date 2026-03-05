import re
from typing import List, Dict

class SecurityScanner:
    def __init__(self):
        # We use regex named groups to identify the specific risk type
        self.signatures: Dict[str, str] = {
            "AWS Access Key": r"AKIA[0-9A-Z]{16}",
            "Stripe Secret Key": r"sk_live_[0-9a-zA-Z]{24}",
            "Google API Key": r"AIza[0-9A-Za-z\\-_]{35}",
            "Postgres Connection String": r"postgres(ql)?://[a-zA-Z0-9_]+:[a-zA-Z0-9_]+@[\w\.-]+(:\d+)?/\w+",
            "Generic Private Key": r"-----BEGIN [A-Z ]+ PRIVATE KEY-----",
            "Hardcoded Password/Secret": r"(?i)(password|secret|api_key|token|access_token|auth_token)\s*[:=]\s*['\"][^'\"]+['\"]"
        }

    def scan_content(self, content: str) -> List[str]:
        """
        Performs a multi-pass regex scan of the provided code content.
        Returns a list of high-severity security findings.
        """
        findings = []

        for label, pattern in self.signatures.items():
            # Using re.MULTILINE in case secrets span lines or are in comments
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                # We redact the actual secret in the log for safety
                findings.append(f"🔴 CRITICAL: Potential {label} detected. Do not commit secrets to version control.")

        return findings

    def audit_risk_level(self, findings: List[str]) -> str:
        """Determines if the file should be blocked from deployment."""
        if any("CRITICAL" in f for f in findings):
            return "HIGH RISK"
        return "CLEAR"