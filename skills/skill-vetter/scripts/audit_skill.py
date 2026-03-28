#!/usr/bin/env python3
"""
Skill Security Auditor

Audits AgentSkills for security vulnerabilities and potential risks.
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict

@dataclass
class SecurityIssue:
    """Represents a security issue found during audit."""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # Command Execution, Data Exfiltration, etc.
    location: str  # filepath:line
    finding: str   # Description of the issue
    code_snippet: str | None = None
    recommendation: str = ""

class SkillSecurityAuditor:
    """Audits skills for security vulnerabilities."""

    # Dangerous command patterns
    DANGEROUS_COMMANDS = [
        r'rm\s+-rf\s+/?',           # Recursive deletion
        r'rmdir\s+/?\*',             # Recursive directory removal
        r'del\s+/?[a-z]',            # Windows delete
        r'format\s+/',               # Disk formatting
        r'>\s*/dev/(sd|vd|hd)[a-z]', # Disk destruction
        r'dd\s+if=/dev/(zero|random|urandom)', # Disk wiping
        r'sudo\s+',                  # Privilege escalation
        r'su\s+',                    # Switch user
        r'runas\s+',                 # Windows runas
        r'doas\s+',                  # BSD doas
        r"sh\s+-c",                  # Shell execution
        r"bash\s+-c",                # Bash execution
        r'eval\s+\$',                # Eval with variable
        r'exec\s+\$',                # Exec with variable
        r'__import__\(.+subprocess', # subprocess import
        r'os\.system\(',            # os.system
        r'os\.popen\(',             # os.popen
        r'commands\.\w+\s*\(',      # commands module
    ]

    # Data exfiltration patterns
    EXFILTRATION_PATTERNS = [
        r'requests\.(post|get)\s*\(["\']http[s]?://[^"\']+["\']', # HTTP requests
        r'urllib\.(request|fetch)\s*\(', # urllib usage
        r'open\(/etc/passwd\)',         # Read system files
        r'open\(/etc/shadow\)',         # Shadow file
        r'open\(/root/.*\)',            # Read root files
        r'ssh\s+',                      # SSH connections
        r'nc\s+-[lL]',                 # Netcat listener
        r'nc\s+[a-z0-9\.]+',            # Netcat connection
        r'curl\s+.*\|\s*(sh|bash|python)', # Pipe to shell
        r'wget\s+.*\|\s*(sh|bash|python)', # Wget pipe to shell
    ]

    # Sensitive data patterns
    SENSITIVE_PATTERNS = [
        r'api[_-]?key\s*=\s*["\'][a-zA-Z0-9_-]{20,}["\']', # API keys
        r'password\s*=\s*["\'][\w@#$%^&]+["\']', # Passwords
        r'secret\s*=\s*["\[a-zA-Z0-9_-]{20,}["\']', # Secrets
        r'token\s*=\s*["\']Bearer\s+[A-Za-z0-9._-]+["\']', # Bearer tokens
        r'auth[_-]?token\s*=\s*["\'][A-Za-z0-9_-]{20,}["\']', # Auth tokens
        r'private[_-]?key\s*=\s*["\']-----BEGIN', # Private keys
        r'aws[_-]?access[_-]?key\s*=\s*["\'][A-Z0-9]{20}["\']', # AWS keys
        r'client[_-]?secret\s*=\s*["\'][\w/+=]{20,}["\']', # Client secrets
    ]

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.issues: List[SecurityIssue] = []

    def audit(self) -> Dict:
        """Run full security audit."""
        if not self.skill_path.exists():
            return {"error": f"Skill path not found: {self.skill_path}"}

        print(f"Auditing skill: {self.skill_path}")

        # Audit SKILL.md
        self.audit_skill_md()

        # Audit Python scripts
        self.audit_python_scripts()

        # Audit Bash scripts
        self.audit_bash_scripts()

        # Generate report
        return self.generate_report()

    def audit_skill_md(self):
        """Audit SKILL.md for security issues."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return

        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for dangerous instructions
        if 'rm -rf' in content:
            self.add_issue(
                severity="HIGH",
                category="Command Execution",
                location=f"{skill_md}:1",
                finding="SKILL.md contains instruction to use rm -rf",
                code_snippet="rm -rf",
                recommendation="Verify this is intentional and safe. Consider alternative approaches."
            )

        # Check for sudo instructions
        if 'sudo ' in content or 'sudo\n' in content:
            self.add_issue(
                severity="HIGH",
                category="Unauthorized Access",
                location=f"{skill_md}:1",
                finding="SKILL.md contains sudo instructions",
                code_snippet="sudo",
                recommendation="Avoid sudo. Use least privilege necessary."
            )

        # Check for exfiltration instructions
        if re.search(r'(requests\.post|curl.*http)', content):
            self.add_issue(
                severity="MEDIUM",
                category="Data Exfiltration",
                location=f"{skill_md}:1",
                finding="SKILL.md mentions external HTTP requests",
                code_snippet="requests.post / curl",
                recommendation="Verify all external domains are trusted and necessary."
            )

    def audit_python_scripts(self):
        """Audit Python scripts in scripts/ directory."""
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return

        for py_file in scripts_dir.glob("*.py"):
            self._check_file_dangerous_patterns(py_file)

    def audit_bash_scripts(self):
        """Audit Bash scripts in scripts/ directory."""
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return

        for sh_file in scripts_dir.glob("*.sh"):
            self._check_file_dangerous_patterns(sh_file)

    def _check_file_dangerous_patterns(self, filepath: Path):
        """Check a file for dangerous security patterns."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            self.add_issue(
                severity="LOW",
                category="File Access",
                location=str(filepath),
                finding=f"Could not read file: {e}",
                recommendation="Check file permissions and encoding."
            )
            return

        file_content = ''.join(lines)

        # Check for dangerous commands
        for pattern in self.DANGEROUS_COMMANDS:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    self.add_issue(
                        severity="HIGH",
                        category="Command Execution",
                        location=f"{filepath}:{i}",
                        finding=f"Dangerous command pattern detected",
                        code_snippet=line.strip(),
                        recommendation="Remove or safely replace this command."
                    )

        # Check for exfiltration
        for pattern in self.EXFILTRATION_PATTERNS:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    self.add_issue(
                        severity="HIGH",
                        category="Data Exfiltration",
                        location=f"{filepath}:{i}",
                        finding=f"Potential data exfiltration pattern",
                        code_snippet=line.strip(),
                        recommendation="Verify external domain and data being sent."
                    )

        # Check for sensitive data
        for pattern in self.SENSITIVE_PATTERNS:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    self.add_issue(
                        severity="CRITICAL",
                        category="Sensitive Information",
                        location=f"{filepath}:{i}",
                        finding=f"Hardcoded sensitive data detected",
                        code_snippet=line.strip()[:100],
                        recommendation="Remove hardcoded credentials. Use environment variables or secure config."
                    )

    def add_issue(self, severity: str, category: str, location: str,
                  finding: str, code_snippet: str | None = None,
                  recommendation: str = ""):
        """Add a security issue to the audit results."""
        self.issues.append(SecurityIssue(
            severity=severity,
            category=category,
            location=location,
            finding=finding,
            code_snippet=code_snippet,
            recommendation=recommendation
        ))

    def generate_report(self) -> Dict:
        """Generate security audit report."""
        # Count issues by severity
        severity_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }

        for issue in self.issues:
            severity_counts[issue.severity] += 1

        # Determine overall risk level
        if severity_counts["CRITICAL"] > 0:
            risk_level = "CRITICAL"
        elif severity_counts["HIGH"] > 0:
            risk_level = "HIGH"
        elif severity_counts["MEDIUM"] > 2:
            risk_level = "HIGH"
        elif severity_counts["MEDIUM"] > 0:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Format issues for report
        formatted_issues = [asdict(issue) for issue in self.issues]

        return {
            "skill_path": str(self.skill_path),
            "executive_summary": {
                "risk_level": risk_level,
                "total_issues": len(self.issues),
                "severity_breakdown": severity_counts
            },
            "issues": formatted_issues
        }

def print_report(report: Dict):
    """Print human-readable security report."""
    print("\n" + "="*70)
    print("SECURITY AUDIT REPORT")
    print("="*70)

    summary = report.get("executive_summary", {})
    print(f"\nSkill: {report.get('skill_path', 'Unknown')}")
    print(f"Risk Level: {summary.get('risk_level', 'N/A')}")
    print(f"Total Issues: {summary.get('total_issues', 0)}")

    print("\nSeverity Breakdown:")
    for severity, count in summary.get('severity_breakdown', {}).items():
        if count > 0:
            print(f"  {severity}: {count}")

    print("\n" + "="*70)
    print("DETAILED FINDINGS")
    print("="*70)

    for i, issue in enumerate(report.get("issues", []), 1):
        print(f"\n### Issue #{i}")
        print(f"Severity: {issue['severity']}")
        print(f"Category: {issue['category']}")
        print(f"Location: {issue['location']}")
        print(f"Finding: {issue['finding']}")
        if issue.get('code_snippet'):
            print(f"Code: {issue['code_snippet']}")
        if issue.get('recommendation'):
            print(f"Recommendation: {issue['recommendation']}")

    print("\n" + "="*70)

def main():
    parser = argparse.ArgumentParser(description="Audit AgentSkills for security vulnerabilities")
    parser.add_argument("skill_path", help="Path to the skill directory to audit")
    parser.add_argument("--json", action="store_true", help="Output report in JSON format")
    args = parser.parse_args()

    auditor = SkillSecurityAuditor(args.skill_path)
    report = auditor.audit()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)

if __name__ == "__main__":
    main()
