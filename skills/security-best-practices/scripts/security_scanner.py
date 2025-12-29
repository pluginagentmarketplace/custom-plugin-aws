#!/usr/bin/env python3
"""
Security Scanner Utility
Checks for common security vulnerabilities and misconfigurations.
"""

import re
import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple


class SecurityScanner:
    """Scan codebase for security issues."""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.findings: List[Dict] = []

    # Secret patterns to detect
    SECRET_PATTERNS = [
        (r'(?i)api[_-]?key\s*[=:]\s*["\']?([a-zA-Z0-9]{20,})["\']?', "API Key"),
        (r'(?i)secret[_-]?key\s*[=:]\s*["\']?([a-zA-Z0-9]{20,})["\']?', "Secret Key"),
        (r'(?i)password\s*[=:]\s*["\']([^"\']+)["\']', "Hardcoded Password"),
        (r'(?i)aws_access_key_id\s*[=:]\s*["\']?(AKIA[A-Z0-9]{16})["\']?', "AWS Access Key"),
        (r'(?i)aws_secret_access_key\s*[=:]\s*["\']?([a-zA-Z0-9/+=]{40})["\']?', "AWS Secret Key"),
        (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token"),
        (r'sk-[a-zA-Z0-9]{48}', "OpenAI API Key"),
        (r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*', "JWT Token"),
        (r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----', "Private Key"),
    ]

    # SQL injection patterns
    SQL_PATTERNS = [
        (r'execute\s*\(\s*["\'].*%s.*["\']\s*%', "SQL Injection (string formatting)"),
        (r'\.format\s*\(.*\).*(?:SELECT|INSERT|UPDATE|DELETE)', "SQL Injection (format)"),
        (r'f["\'].*{.*}.*(?:SELECT|INSERT|UPDATE|DELETE)', "SQL Injection (f-string)"),
    ]

    # XSS patterns
    XSS_PATTERNS = [
        (r'innerHTML\s*=\s*[^"\']*(?:user|input|data)', "Potential XSS (innerHTML)"),
        (r'document\.write\s*\(', "Potential XSS (document.write)"),
        (r'\.html\s*\([^)]*(?:user|input|data)', "Potential XSS (jQuery .html())"),
    ]

    def scan_file(self, file_path: Path) -> List[Dict]:
        """Scan a single file for security issues."""
        findings = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

            # Check for secrets
            for pattern, secret_type in self.SECRET_PATTERNS:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line):
                        findings.append({
                            "type": "SECRET",
                            "severity": "CRITICAL",
                            "file": str(file_path),
                            "line": i,
                            "description": f"Potential {secret_type} detected",
                            "snippet": line.strip()[:100]
                        })

            # Check for SQL injection
            for pattern, issue_type in self.SQL_PATTERNS:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append({
                            "type": "SQL_INJECTION",
                            "severity": "HIGH",
                            "file": str(file_path),
                            "line": i,
                            "description": issue_type,
                            "snippet": line.strip()[:100]
                        })

            # Check for XSS
            for pattern, issue_type in self.XSS_PATTERNS:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append({
                            "type": "XSS",
                            "severity": "HIGH",
                            "file": str(file_path),
                            "line": i,
                            "description": issue_type,
                            "snippet": line.strip()[:100]
                        })

        except Exception as e:
            findings.append({
                "type": "SCAN_ERROR",
                "severity": "INFO",
                "file": str(file_path),
                "description": f"Could not scan file: {str(e)}"
            })

        return findings

    def scan_directory(self, extensions: List[str] = None) -> List[Dict]:
        """Scan directory for security issues."""
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.java', '.go', '.rb', '.php', '.yaml', '.yml', '.json', '.env']

        all_findings = []

        for ext in extensions:
            for file_path in self.base_path.rglob(f"*{ext}"):
                # Skip common non-source directories
                if any(part.startswith('.') or part in ['node_modules', 'venv', '__pycache__', 'dist', 'build']
                       for part in file_path.parts):
                    continue

                findings = self.scan_file(file_path)
                all_findings.extend(findings)

        self.findings = all_findings
        return all_findings

    def check_dependencies(self, package_file: str) -> List[Dict]:
        """Check for known vulnerable dependencies."""
        findings = []
        file_path = self.base_path / package_file

        if not file_path.exists():
            return findings

        # This is a simplified check - use tools like safety, npm audit, etc. for real scanning
        vulnerable_packages = {
            "lodash": ["<4.17.21", "Prototype Pollution"],
            "minimist": ["<1.2.6", "Prototype Pollution"],
            "node-fetch": ["<2.6.7", "Information Exposure"],
            "django": ["<3.2.4", "SQL Injection"],
            "flask": ["<2.0.0", "Cookie Parsing Issue"],
        }

        try:
            with open(file_path, 'r') as f:
                content = f.read()

            for pkg, (version, vuln) in vulnerable_packages.items():
                if pkg in content.lower():
                    findings.append({
                        "type": "VULNERABLE_DEPENDENCY",
                        "severity": "MEDIUM",
                        "file": str(file_path),
                        "description": f"Potentially vulnerable package: {pkg} ({vuln})",
                        "recommendation": f"Upgrade {pkg} to version {version.replace('<', '>=')} or later"
                    })

        except Exception:
            pass

        return findings

    def generate_report(self) -> Dict:
        """Generate security scan report."""
        report = {
            "scan_path": str(self.base_path),
            "total_findings": len(self.findings),
            "by_severity": {},
            "by_type": {},
            "findings": self.findings
        }

        for finding in self.findings:
            severity = finding.get("severity", "UNKNOWN")
            finding_type = finding.get("type", "UNKNOWN")

            report["by_severity"][severity] = report["by_severity"].get(severity, 0) + 1
            report["by_type"][finding_type] = report["by_type"].get(finding_type, 0) + 1

        return report


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Security Scanner")
    parser.add_argument("--path", default=".", help="Path to scan")
    parser.add_argument("--output", choices=["json", "text"], default="text")
    parser.add_argument("--severity", choices=["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"],
                        help="Minimum severity to report")

    args = parser.parse_args()

    scanner = SecurityScanner(args.path)
    scanner.scan_directory()

    # Check common dependency files
    for pkg_file in ["package.json", "requirements.txt", "Gemfile", "go.mod"]:
        scanner.findings.extend(scanner.check_dependencies(pkg_file))

    if args.severity:
        severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
        min_idx = severity_order.index(args.severity)
        scanner.findings = [f for f in scanner.findings
                          if severity_order.index(f.get("severity", "INFO")) <= min_idx]

    report = scanner.generate_report()

    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print(f"\nSecurity Scan Report")
        print(f"{'=' * 50}")
        print(f"Path: {report['scan_path']}")
        print(f"Total Findings: {report['total_findings']}")
        print(f"\nBy Severity: {report['by_severity']}")
        print(f"By Type: {report['by_type']}")
        print(f"\n{'=' * 50}")

        for finding in report['findings']:
            print(f"\n[{finding['severity']}] {finding['type']}")
            print(f"  File: {finding.get('file', 'N/A')}")
            if 'line' in finding:
                print(f"  Line: {finding['line']}")
            print(f"  Description: {finding['description']}")


if __name__ == "__main__":
    main()
