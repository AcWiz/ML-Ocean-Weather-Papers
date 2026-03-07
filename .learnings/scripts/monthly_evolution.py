#!/usr/bin/env python3
"""
每月进化脚本
每月执行系统升级和能力增强
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
BACKUP_DIR = Path.home() / ".openclaw" / "backups"

class MonthlyEvolution:
    """每月进化"""
    
    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m")
        
    def create_snapshot(self):
        """创建月度快照"""
        print("💾 创建月度快照...")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        files = ["SOUL.md", "IDENTITY.md", "AGENTS.md", "TOOLS.md", "USER.md"]
        for f in files:
            src = WORKSPACE / f
            if src.exists():
                dst = BACKUP_DIR / f"{timestamp}_{f}"
                os.system(f"cp {src} {dst}")
        
        print(f"✅ 快照创建完成: {timestamp}")
        return timestamp
    
    def research_update(self):
        """调研更新"""
        print("🔬 执行科研调研...")
        
        # 运行每周更新脚本
        research_dir = WORKSPACE / "research"
        if research_dir.exists():
            os.system(f"cd {research_dir} && ./weekly_update.sh")
        
        print("✅ 调研完成")
    
    def git_commit(self):
        """Git 提交"""
        print("📝 创建月度提交...")
        
        os.system(f"cd {WORKSPACE} && git add -A")
        
        msg = f"chore(monthly): {self.date} 月度进化\n\n- 快照备份\n- 科研更新\n- 系统自检"
        os.system(f'cd {WORKSPACE} && git commit -m "{msg}"')
        
        print("✅ 提交完成")
    
    def run(self):
        """执行每月进化"""
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║          🧬 Ethan 每月进化 - {self.date}             ║
╠═══════════════════════════════════════════════════════════╣
        """)
        
        # 执行进化步骤
        snapshot = self.create_snapshot()
        self.research_update()
        self.git_commit()
        
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║                    ✅ 月度进化完成                        ║
╚═══════════════════════════════════════════════════════════╝
        """)

if __name__ == "__main__":
    me = MonthlyEvolution()
    me.run()
