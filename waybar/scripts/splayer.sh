#!/bin/bash

API_URL="http://localhost:25884"

response=$(curl -s "$API_URL/api/control/song-info" 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$response" ]; then
    echo "♫"
    exit 0
fi

play_status=$(echo "$response" | grep -o '"playStatus":[^,}]*' | cut -d':' -f2)
song_name=$(echo "$response" | grep -o '"playName":"[^"]*"' | cut -d'"' -f4)
artist=$(echo "$response" | grep -o '"artistName":"[^"]*"' | cut -d'"' -f4)

if [ "$play_status" = "true" ]; then
    icon="⏸"
else
    icon="▶"
fi

if [ -n "$song_name" ]; then
    echo "$icon"
    echo "♫ $song_name - $artist"
else
    echo "$icon"
fi
