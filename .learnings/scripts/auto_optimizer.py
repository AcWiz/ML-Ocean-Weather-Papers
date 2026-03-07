#!/usr/bin/env python3
"""
自动优化机制
基于历史表现自动调整行为策略
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"

class AutoOptimizer:
    """自动优化引擎"""
    
    def __init__(self):
        self.config_file = WORKSPACE / ".learnings" / "optimizer_config.json"
        self.load_config()
        
    def load_config(self):
        """加载配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = self.get_default_config()
            self.save_config()
    
    def get_default_config(self) -> dict:
        """默认配置"""
        return {
            "version": "1.0",
            "strategies": {
                "research_depth": "medium",  # low/medium/high
                "backup_frequency": "auto",   # manual/auto
                "reflection_enabled": True,
                "pattern_learning": True
            },
            "performance": {
                "tasks_completed": 0,
                "success_rate": 1.0,
                "avg_response_time": 0
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def record_success(self, task_type: str):
        """记录成功"""
        self.config["performance"]["tasks_completed"] += 1
        self.config["last_updated"] = datetime.now().isoformat()
        self.save_config()
        print(f"✅ 记录成功: {task_type}")
    
    def should_deepen_research(self) -> bool:
        """判断是否需要深化研究"""
        success_rate = self.config["performance"].get("success_rate", 1.0)
        return success_rate < 0.8
    
    def adjust_strategy(self, area: str, new_value: str):
        """调整策略"""
        if area in self.config["strategies"]:
            old_value = self.config["strategies"][area]
            self.config["strategies"][area] = new_value
            self.save_config()
            print(f"✅ 策略调整: {area} {old_value} -> {new_value}")
    
    def get_recommendations(self) -> list:
        """获取优化建议"""
        recommendations = []
        
        # 检查是否需要深化研究
        if self.should_deepen_research():
            recommendations.append("建议加深研究深度")
        
        # 检查备份频率
        if self.config["strategies"]["backup_frequency"] == "manual":
            recommendations.append("建议开启自动备份")
        
        return recommendations

if __name__ == "__main__":
    optimizer = AutoOptimizer()
    print("=== 自动优化机制 ===\n")
    
    # 测试
    optimizer.record_success("research")
    optimizer.record_success("documentation")
    
    print("\n当前策略:")
    for k, v in optimizer.config["strategies"].items():
        print(f"  {k}: {v}")
    
    print("\n优化建议:")
    for r in optimizer.get_recommendations():
        print(f"  - {r}")
