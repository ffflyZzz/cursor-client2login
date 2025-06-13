#!/usr/bin/env python3
"""
Cursor Client2Login 测试管理器
解决__pycache__导致Chrome扩展加载失败的问题
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

class TestManager:
    """测试管理器类"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.tests_dir = self.project_root / "tests"
        
    def clean_pycache(self):
        """清理所有__pycache__目录和.pyc文件"""
        print("🧹 清理Python缓存文件...")
        
        # 清理__pycache__目录
        for pycache_dir in self.project_root.rglob("__pycache__"):
            if pycache_dir.is_dir():
                print(f"   删除: {pycache_dir}")
                shutil.rmtree(pycache_dir, ignore_errors=True)
        
        # 清理.pyc文件
        for pyc_file in self.project_root.rglob("*.pyc"):
            if pyc_file.is_file():
                print(f"   删除: {pyc_file}")
                pyc_file.unlink(missing_ok=True)
                
        print("✅ 缓存清理完成")
    
    def run_tests(self):
        """运行测试"""
        print("🚀 运行优化功能测试...")
        
        # 确保tests目录存在
        self.tests_dir.mkdir(exist_ok=True)
        
        # 运行测试脚本
        test_script = self.tests_dir / "test_optimizations.py"
        if test_script.exists():
            try:
                # 设置PYTHONDONTWRITEBYTECODE环境变量，防止生成.pyc文件
                env = os.environ.copy()
                env['PYTHONDONTWRITEBYTECODE'] = '1'
                
                result = subprocess.run([
                    sys.executable, str(test_script)
                ], cwd=str(self.tests_dir), env=env, capture_output=True, text=True)
                
                print(result.stdout)
                if result.stderr:
                    print("错误输出:", result.stderr)
                    
                return result.returncode == 0
            except Exception as e:
                print(f"❌ 测试运行失败: {e}")
                return False
        else:
            print(f"❌ 测试脚本不存在: {test_script}")
            return False
    
    def check_chrome_compatibility(self):
        """检查Chrome扩展兼容性"""
        print("🔍 检查Chrome扩展兼容性...")
        
        # 检查是否存在可能导致Chrome加载失败的文件/目录
        problematic_items = []
        
        for item in self.project_root.iterdir():
            if item.name.startswith('_') and item.name != '.gitignore':
                problematic_items.append(item)
        
        if problematic_items:
            print("⚠️  发现可能导致Chrome加载失败的文件/目录:")
            for item in problematic_items:
                print(f"   - {item}")
            return False
        else:
            print("✅ Chrome扩展兼容性检查通过")
            return True
    
    def setup_test_environment(self):
        """设置测试环境"""
        print("⚙️  设置测试环境...")
        
        # 设置环境变量防止生成.pyc文件
        os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
        
        # 确保tests目录存在且在.gitignore中
        self.tests_dir.mkdir(exist_ok=True)
        
        gitignore_path = self.project_root / ".gitignore"
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if "tests/" not in content:
                with gitignore_path.open("a") as f:
                    f.write("\n# 测试目录（避免Chrome扩展加载时的__pycache__问题）\ntests/\n")
                print("✅ 已更新.gitignore文件")
        
        print("✅ 测试环境设置完成")
    
    def run_full_test_cycle(self):
        """运行完整的测试周期"""
        print("🎯 Cursor Client2Login - 测试管理器")
        print("=" * 50)
        
        # 1. 清理缓存
        self.clean_pycache()
        
        # 2. 设置测试环境
        self.setup_test_environment()
        
        # 3. 运行测试
        test_success = self.run_tests()
        
        # 4. 再次清理缓存
        self.clean_pycache()
        
        # 5. 检查Chrome兼容性
        chrome_compatible = self.check_chrome_compatibility()
        
        print("=" * 50)
        if test_success and chrome_compatible:
            print("🎉 所有测试通过！现在可以安全地将扩展加载到Chrome中。")
            return True
        else:
            print("❌ 测试或兼容性检查失败，请检查上述错误信息。")
            return False

def main():
    """主函数"""
    manager = TestManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "clean":
            manager.clean_pycache()
        elif command == "test":
            manager.run_tests()
        elif command == "check":
            manager.check_chrome_compatibility()
        elif command == "setup":
            manager.setup_test_environment()
        else:
            print("用法: python3 test_manager.py [clean|test|check|setup]")
            print("或直接运行进行完整测试周期")
            manager.run_full_test_cycle()
    else:
        manager.run_full_test_cycle()

if __name__ == "__main__":
    main()
