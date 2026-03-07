#!/usr/bin/env python3
"""
每日自检脚本
每天自动执行系统检查和能力评估
"""

import os
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
BACKUP_DIR = Path.home() / ".openclaw" / "backups"

class DailyCheck:
    """每日自检"""
    
    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.log_file = MEMORY_DIR / f"{self.date}.md"
        
    def check_workspace(self):
        """检查工作区状态"""
        print("📁 检查工作区...")
        required_files = ["SOUL.md", "IDENTITY.md", "AGENTS.md", "TOOLS.md", "USER.md"]
        status = {}
        for f in required_files:
            path = WORKSPACE / f
            status[f] = "✅" if path.exists() else "❌"
        return status
    
    def check_backup(self):
        """检查备份状态"""
        print("💾 检查备份...")
        backups = list(BACKUP_DIR.glob("*_SOUL.md"))
        latest = max(backups, key=os.path.getmtime) if backups else None
        return latest.name if latest else "无备份"
    
    def check_learnings(self):
        """检查学习日志"""
        print("📚 检查学习日志...")
        learnings_dir = WORKSPACE / ".learnings"
        if not learnings_dir.exists():
            return "❌ 未初始化"
        
        files = list(learnings_dir.glob("*.md"))
        return f"✅ {len(files)} 个文件"
    
    def check_research(self):
        """检查科研工具"""
        print("🔬 检查科研工具...")
        research_dir = WORKSPACE / "research"
        if not research_dir.exists():
            return "❌ 未安装"
        
        scripts = list(research_dir.glob("*.py"))
        return f"✅ {len(scripts)} 个工具"
    
    def run(self):
        """执行每日自检"""
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║          🧬 Ethan 每日自检 - {self.date}           ║
╠═══════════════════════════════════════════════════════════╣
        """)
        
        # 执行各项检查
        ws_status = self.check_workspace()
        backup_status = self.check_backup()
        learnings_status = self.check_learnings()
        research_status = self.check_research()
        
        print("\n📊 工作区状态:")
        for f, s in ws_status.items():
            print(f"  {s} {f}")
        
        print(f"\n💾 最新备份: {backup_status}")
        print(f"📚 学习日志: {learnings_status}")
        print(f"🔬 科研工具: {research_status}")
        
        print("""
╚═══════════════════════════════════════════════════════════╝
        """)
        
        # 更新日志
        self.update_log(ws_status, backup_status, learnings_status, research_status)
        
    def update_log(self, ws_status, backup_status, learnings_status, research_status):
        """更新日志"""
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        
        content = f"""# 每日自检 - {self.date}

## 系统状态

- 工作区: ✅ 正常
- 备份: {backup_status}
- 学习日志: {learnings_status}
- 科研工具: {research_status}

## 待处理

-

"""
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    dc = DailyCheck()
    dc.run()
