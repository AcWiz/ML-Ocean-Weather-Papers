#!/bin/bash
LOG_DIR=~/.openclaw/workspace/research/logs
mkdir -p $LOG_DIR
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE=$LOG_DIR/weekly_update_$(date +%Y%m%d).log
echo "=== Weekly Research Update ===" > $LOG_FILE
date >> $LOG_FILE
python3 ~/.openclaw/workspace/research/literature_search.py "data assimilation" >> $LOG_FILE 2>&1
python3 ~/.openclaw/workspace/research/literature_search.py "agent framework" >> $LOG_FILE 2>&1
echo "Done" >> $LOG_FILE
cp $LOG_FILE ~/.openclaw/workspace/research/notes/latest_update.md
