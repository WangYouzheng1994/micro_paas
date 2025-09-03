# 创建专用用户
sudo useradd -r -s /bin/false micro-paas
sudo mkdir -p /opt/micro-paas/{app,venv,config,logs}
sudo chown -R micro-paas:micro-paas /opt/micro-paas

# 给执行脚本赋权
chmod +x /opt/micro-paas/run.sh

# 设置自启动
