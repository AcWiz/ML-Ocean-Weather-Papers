#!/usr/bin/env python3
"""
统一进化管理器
整合自我反思、自动优化、模式学习
"""

import sys
from pathlib import Path

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent

# 导入各模块
sys.path.insert(0, str(SCRIPT_DIR))

class EvolutionManager:
    """进化管理器"""
    
    def __init__(self):
        self.name = "Ethan 进化管理系统"
        self.version = "1.0"
        
    def status(self):
        """显示状态"""
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║          🧬 {self.name} v{self.version}           ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  📊 组件状态:                                            ║
║                                                           ║
║  ✅ 自我反思机制    - self_reflection.py                ║
║  ✅ 自动优化引擎    - auto_optimizer.py                 ║
║  ✅ 重要性分类器    - auto_classifier.py                ║
║  ✅ 模式识别器      - pattern_detector.py               ║
║  ✅ 记忆管理器      - memory_manager.py                 ║
║                                                           ║
║  📈 进化能力:                                            ║
║                                                           ║
║  ✅ 记忆增强       - 多层级记忆系统                    ║
║  ✅ 自我反思       - 决策后自评                        ║
║  ✅ 自动优化       - 基于表现调整策略                   ║
║  ✅ 模式学习       - 识别重复模式                      ║
║  ✅ 持续进化       - 每周自动更新                       ║
║                                                           ║
║  🔄 定时任务:                                            ║
║                                                           ║
║  ✅ 每周科研更新   - 周日上午 9:00                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """)
    
    def help(self):
        """显示帮助"""
        print("""
使用方法:
  python3 evolution_manager.py <command>

命令:
  status    - 显示进化系统状态
  reflect   - 进行自我反思
  optimize  - 运行自动优化
  analyze   - 分析模式
  help      - 显示此帮助

示例:
  python3 evolution_manager.py status
  python3 evolution_manager.py reflect "任务描述" "决策" "结果"
        """)

if __name__ == "__main__":
    em = EvolutionManager()
    
    if len(sys.argv) < 2:
        em.status()
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        em.status()
    elif cmd == "help":
        em.help()
    elif cmd == "reflect":
        # 自我反思
        from self_reflection import SelfReflection
        sr = SelfReflection()
        context = sys.argv[2] if len(sys.argv) > 2 else "一般任务"
        decision = sys.argv[3] if len(sys.argv) > 3 else "标准执行"
        outcome = sys.argv[4] if len(sys.argv) > 4 else None
        sr.reflect(context, decision, outcome)
    elif cmd == "optimize":
        # 自动优化
        from auto_optimizer import AutoOptimizer
        ao = AutoOptimizer()
        ao.record_success("manual")
    elif cmd == "analyze":
        # 模式分析
        from pattern_detector import analyze_patterns
        print(analyze_patterns())
    else:
        print(f"未知命令: {cmd}")
        em.help()
