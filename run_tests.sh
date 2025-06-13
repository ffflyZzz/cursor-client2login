#!/bin/bash

# Cursor Client2Login 测试脚本
# 用于在不影响Chrome扩展加载的情况下运行测试

echo "🧪 Cursor Client2Login - 测试脚本"
echo "=================================="

# 清理可能存在的__pycache__目录
echo "🧹 清理Python缓存文件..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -exec rm -f {} + 2>/dev/null || true

# 运行测试
echo "🚀 运行优化功能测试..."
cd tests
python3 test_optimizations.py

# 再次清理，确保Chrome扩展加载不受影响
echo "🧹 清理测试产生的缓存文件..."
cd ..
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -exec rm -f {} + 2>/dev/null || true

echo "✅ 测试完成！现在可以安全地将扩展加载到Chrome中。"
echo "=================================="
