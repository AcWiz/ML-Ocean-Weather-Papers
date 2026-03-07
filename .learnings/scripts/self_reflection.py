#!/usr/bin/env python3
"""
自我反思机制
让系统在每次重要操作后进行自我评估和改进
"""

import json
from datetime import datetime
from pathlib import Path

LEARNINGS_DIR = Path.home() / ".openclaw" / "workspace" / ".learnings"

class SelfReflection:
    """自我反思引擎"""
    
    def __init__(self):
        self.reflection_log = LEARNINGS_DIR / "reflections.md"
        self.init_log()
        
    def init_log(self):
        """初始化反思日志"""
        if not self.reflection_log.exists():
            with open(self.reflection_log, 'w', encoding='utf-8') as f:
                f.write("# 自我反思日志\n\n")
                f.write("*每次重大决策后的自我评估*\n\n")
    
    def reflect(self, context: str, decision: str, outcome: str = None):
        """记录反思"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        entry = f"""## {timestamp} - 反思

**场景**: {context}
**决策**: {decision}
**结果**: {outcome or '待评估'}

### 自我评估

- 决策质量: ⭐⭐⭐⭐⭐
- 可改进点: 

"""
        with open(self.reflection_log, 'a', encoding='utf-8') as f:
            f.write(entry)
        
        print(f"✅ 反思已记录: {timestamp}")
    
    def get_recent_reflections(self, count: int = 5) -> list:
        """获取最近反思"""
        if not self.reflection_log.exists():
            return []
        
        with open(self.reflection_log, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = content.split("## ")[-count:]
        return [e.strip() for e in entries if e.strip()]
    
    def analyze_patterns(self) -> dict:
        """分析反思模式"""
        if not self.reflection_log.exists():
            return {"total": 0, "patterns": []}
        
        with open(self.reflection_log, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单统计
        entries = content.split("## ")
        return {
            "total": len([e for e in entries if e.strip()]),
            "patterns": []  # 可扩展模式识别
        }

if __name__ == "__main__":
    sr = SelfReflection()
    print("=== 自我反思机制 ===\n")
    
    # 测试
    sr.reflect(
        context="决定是否接受用户的进化任务",
        decision="接受并分阶段执行",
        outcome="用户满意"
    )
    
    print("\n最近反思:")
    for r in sr.get_recent_reflections(3):
        print(f"- {r[:80]}...")
