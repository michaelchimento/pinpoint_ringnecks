#!/bin/sh
# backup_server_launcher.sh
# launches correct python scripts with directory management

cd ~/pinpoint_ringnecks
sleep 10
python3 -u photo_data_analysis.py P1 > logs/logsP1 2>&1 &
python3 -u photo_data_analysis.py P2 > logs/logsP2 2>&1 &
python3 -u photo_data_analysis.py P3 > logs/logsP3 2>&1 &
python3 -u photo_data_analysis.py P4 > logs/logsP4 2>&1 &
exit 0
