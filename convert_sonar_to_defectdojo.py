import json

with open("reports/sonarqube-issues.json") as f:
    data = json.load(f)

findings = []
for issue in data.get("issues", []):
    finding = {
        "title": issue.get("message", "SonarQube Issue"),
        "severity": {
            "BLOCKER": "Critical",
            "CRITICAL": "High",
            "MAJOR": "Medium",
            "MINOR": "Low",
            "INFO": "Info"
        }.get(issue.get("severity", "INFO").upper(), "Info"),
        "description": issue.get("message", ""),
        "file_path": issue.get("component", "").split(":")[-1],
        "line": issue.get("line", 1)
    }
    findings.append(finding)

output = {
    "scan_type": "Generic Findings Import",
    "findings": findings
}

with open("converted-report.json", "w") as out:
    json.dump(output, out, indent=2)
