#!/bin/bash
# 阿里云服务器网络检查脚本

echo "🔍 阿里云服务器网络配置检查"
echo "=================================="

# 1. 获取内网IP
echo "📍 内网IP地址:"
hostname -I | awk '{print "  " $1}'

# 2. 获取公网IP
echo "🌍 公网IP地址:"
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || echo "获取失败")
echo "  $PUBLIC_IP"

# 3. 检查端口监听状态
echo "🔌 端口监听状态:"
if netstat -tulpn 2>/dev/null | grep -q ":3000 "; then
    echo "  ✅ 端口 3000 (前端) - 正在监听"
else
    echo "  ❌ 端口 3000 (前端) - 未监听"
fi

if netstat -tulpn 2>/dev/null | grep -q ":8080 "; then
    echo "  ✅ 端口 8080 (后端) - 正在监听"
else
    echo "  ❌ 端口 8080 (后端) - 未监听"
fi

# 4. 防火墙检查
echo "🛡️  防火墙状态:"
if command -v ufw >/dev/null 2>&1; then
    if ufw status 2>/dev/null | grep -q "Status: active"; then
        echo "  🔥 UFW防火墙已启用"
        if ufw status 2>/dev/null | grep -q "3000"; then
            echo "  ✅ 端口 3000 已开放"
        else
            echo "  ❌ 端口 3000 未开放"
            echo "      执行: sudo ufw allow 3000"
        fi
        if ufw status 2>/dev/null | grep -q "8080"; then
            echo "  ✅ 端口 8080 已开放"
        else
            echo "  ❌ 端口 8080 未开放"
            echo "      执行: sudo ufw allow 8080"
        fi
    else
        echo "  ✅ UFW防火墙未启用"
    fi
elif command -v firewall-cmd >/dev/null 2>&1; then
    if systemctl is-active firewalld >/dev/null 2>&1; then
        echo "  🔥 Firewalld已启用"
        if firewall-cmd --list-ports 2>/dev/null | grep -q "3000"; then
            echo "  ✅ 端口 3000 已开放"
        else
            echo "  ❌ 端口 3000 未开放"
            echo "      执行: sudo firewall-cmd --add-port=3000/tcp --permanent && sudo firewall-cmd --reload"
        fi
        if firewall-cmd --list-ports 2>/dev/null | grep -q "8080"; then
            echo "  ✅ 端口 8080 已开放"
        else
            echo "  ❌ 端口 8080 未开放"
            echo "      执行: sudo firewall-cmd --add-port=8080/tcp --permanent && sudo firewall-cmd --reload"
        fi
    else
        echo "  ✅ Firewalld未启用"
    fi
else
    echo "  ✅ 未检测到系统防火墙"
fi

echo ""
echo "🎯 访问地址:"
if [ "$PUBLIC_IP" != "获取失败" ]; then
    echo "  🌍 外网访问: http://$PUBLIC_IP:3000"
    echo "  🔧 API接口: http://$PUBLIC_IP:8080"
    echo "  📚 API文档: http://$PUBLIC_IP:8080/docs"
else
    echo "  ❌ 无法获取公网IP，请检查网络连接"
fi

echo ""
echo "💡 重要提醒:"
echo "  1. 确保阿里云安全组已开放 3000 和 8080 端口"
echo "  2. 服务必须绑定到 0.0.0.0 而不是 localhost"
echo "  3. 如需HTTPS，请配置SSL证书和nginx"
