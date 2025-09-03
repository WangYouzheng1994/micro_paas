#!/bin/bash
source /opt/micro-paas/venv/bin/activate
exec monitor /opt/micro-paas/config/config.yaml >> /opt/micro-paas/logs/monitor.log 2>&1