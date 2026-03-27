#!/bin/sh

SCRIPT="/nct11af/script/uid_manager.py"

# python 경로 (환경 따라 다름)
PYTHON="/usr/bin/python"

if [ ! -f "$SCRIPT" ]; then
    echo "Error: uid_manager.py not found"
    exit 1
fi

if [ ! -x "$PYTHON" ]; then
    echo "Error: python not found"
    exit 1
fi

echo "Running UID Manager..."
$PYTHON $SCRIPT

exit 0
