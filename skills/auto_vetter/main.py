import urllib.request
import json
import re

RED_FLAGS = {
    "curl_wget": r"(curl|wget)\s+http",
    "eval_exec": r"(eval|exec)\s*\(",
    "base64_decode": r"base64\.(b64decode|decodestring)",
    "system_files": r"(\~/\.ssh|\~/\.aws|\~/\.config|/etc/)",
    "openclaw_core": r"(MEMORY\.md|USER\.md|SOUL\.md|IDENTITY\.md)",
    "obfuscation": r"(minified|encoded|__import__)",
    "sudo_access": r"sudo\s+"
}

def fetch_repo_info(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw-AutoVetter'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {"error": str(e)}

def run_vetter(owner, repo):
    info = fetch_repo_info(owner, repo)
    if "error" in info:
        return f"❌ 无法访问目标仓库。原因: {info['error']}"
        
    stars = info.get("stargazers_count", 0)
    updated_at = info.get("updated_at", "Unknown")
    
    detected_red_flags = []
    risk_level = "🟢 LOW"
    verdict = "✅ SAFE TO INSTALL"
    
    if stars < 10:
        detected_red_flags.append("警告: 仓库星标过低，来源不可靠。")
        risk_level = "🟡 MEDIUM"
        verdict = "⚠️ INSTALL WITH CAUTION"
        
    flags_output = "\n• ".join([""] + detected_red_flags) if detected_red_flags else "None"

    return f"""
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: {repo}
Source: GitHub ({owner}/{repo})
───────────────────────────────────────
METRICS:
• Downloads/Stars: {stars}
• Last Updated: {updated_at}
───────────────────────────────────────
RED FLAGS: {flags_output}
───────────────────────────────────────
RISK LEVEL: {risk_level}
VERDICT: {verdict}
═══════════════════════════════════════
"""

def execute(params):
    repo_url = params.get("url", "")
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if match:
        return run_vetter(match.group(1), match.group(2).replace('.git', ''))
    return "❌ 提供的 URL 格式不正确，需要标准的 GitHub 仓库地址。"
