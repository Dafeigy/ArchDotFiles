#!/bin/bash

MODE_FILE="/tmp/lyricland_mode"
SCRIPT_NAME="lyricland.py"

if [ -f "$MODE_FILE" ]; then
    mode=$(cat "$MODE_FILE")
    if [ "$mode" = "lyric" ]; then
        echo "time" > "$MODE_FILE"
    else
        echo "lyric" > "$MODE_FILE"
    fi
else
    echo "lyric" > "$MODE_FILE"
fi

pid=$(pgrep -n -f "$SCRIPT_NAME")
if [ -n "$pid" ]; then
    kill -10 "$pid"
fi
