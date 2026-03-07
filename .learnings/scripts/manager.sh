#!/bin/bash
LEARNINGS_DIR=~/.openclaw/workspace/.learnings
case "$1" in
    analyze) python3 $LEARNINGS_DIR/scripts/pattern_detector.py ;;
    search) shift; python3 $LEARNINGS_DIR/scripts/hybrid_search.py "$@" ;;
    classify) python3 $LEARNINGS_DIR/scripts/auto_classifier.py ;;
    *) echo "用法: learn-mgr {analyze|search|classify}" ;;
esac
