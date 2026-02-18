#!/bin/bash

echo "========================================"
echo "研时前端开发服务器启动"
echo "========================================"
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "✗ 未检测到 Node.js"
    echo "请先安装 Node.js: https://nodejs.org/"
    exit 1
fi

echo "[1/3] 检查依赖..."
if [ ! -d "node_modules" ]; then
    echo "首次运行，正在安装依赖..."
    npm install
    if [ $? -ne 0 ]; then
        echo "✗ 依赖安装失败"
        exit 1
    fi
fi
echo "✓ 依赖检查完成"
echo ""

echo "[2/3] 启动开发服务器..."
echo ""
echo "开发服务器将启动在: http://localhost:3000"
echo "按 Ctrl+C 停止服务器"
echo ""
echo "========================================"
echo ""

npm run dev
