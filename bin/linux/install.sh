#!/bin/bash
set -e

APP_NAME="micro-paas"
APP_USER="micro-paas"
APP_DIR="/opt/${APP_NAME}"
WHL_FILE="/tmp/micro-paas-0.1.0-py3-none-any.whl"
PYTHON_BIN="python3.12"


echo "开始部署 ${APP_NAME} ..."

# 1. 创建系统用户
if ! id -u "$APP_USER" >/dev/null 2>&1; then
    echo " 创建用户: $APP_USER"
    sudo useradd -r -s /bin/false $APP_USER
fi

# 2. 创建目录结构
echo " 创建目录: $APP_DIR"
sudo mkdir -p ${APP_DIR}/{app,venv,config,logs}
sudo chown -R $APP_USER:$APP_USER $APP_DIR

# 3. 创建虚拟环境
if [ ! -d "${APP_DIR}/venv" ]; then
    echo " 创建虚拟环境..."
    $PYTHON_BIN -m venv ${APP_DIR}/venv
    source ${APP_DIR}/venv/bin/activate
    pip install --upgrade pip wheel setuptools
else
    echo "  已存在虚拟环境，跳过"
    source ${APP_DIR}/venv/bin/activate
fi

# 4. 安装 .whl 包
echo " 安装应用: ${WHL_FILE}"
pip install $WHL_FILE

# 5. 写配置文件（如不存在）
CONFIG_FILE="${APP_DIR}/config/config.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "创建配置文件 ${CONFIG_FILE}"
    cat <<EOF | sudo tee $CONFIG_FILE
monitor:
  mysql:
    - name: "mysql_master"
      host: "127.0.0.1"
      port: 3306
      user: "root"
      password: "123456"
      thresholds:
        threads_connected: 200
        qps: 500
        slow_queries: 10
        disk_usage: 85
        io_wait: 30
EOF
    sudo chown $APP_USER:$APP_USER $CONFIG_FILE
fi

# 6. 写启动脚本
RUN_SCRIPT="${APP_DIR}/run.sh"
echo "创建启动脚本 ${RUN_SCRIPT}"
cat <<'EOF' | sudo tee $RUN_SCRIPT
#!/bin/bash
source /opt/micro-paas/venv/bin/activate
exec monitor /opt/micro-paas/config/config.yaml >> /opt/micro-paas/logs/monitor.log 2>&1
EOF
sudo chmod +x $RUN_SCRIPT
sudo chown $APP_USER:$APP_USER $RUN_SCRIPT

# 7. 配置 systemd 服务
SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"
echo " 创建 systemd 服务 ${SERVICE_FILE}"
cat <<EOF | sudo tee $SERVICE_FILE
[Unit]
Description=Micro-PaaS Monitoring Service
After=network.target

[Service]
User=${APP_USER}
Group=${APP_USER}
ExecStart=${APP_DIR}/run.sh
Restart=always
WorkingDirectory=${APP_DIR}
# 不启用数据缓冲，及时的输出日志
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF


# 8. 配置 systemd timer
TIMER_FILE="/etc/systemd/system/${APP_NAME}.timer"
echo "⏲️ 创建 systemd Timer ${TIMER_FILE}"
cat <<EOF | sudo tee $TIMER_FILE
[Unit]
Description=Run Micro-PaaS monitoring every 5 minutes

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Unit=${APP_NAME}.service

[Install]
WantedBy=timers.target
EOF

# 8. 启动服务
echo "启动服务 ${APP_NAME}"
sudo systemctl daemon-reload
sudo systemctl enable ${APP_NAME}
sudo systemctl restart ${APP_NAME}

echo "部署完成！使用以下命令查看日志："
echo "journalctl -u ${APP_NAME} -f"
echo "或   tail -f ${APP_DIR}/logs/monitor.log"