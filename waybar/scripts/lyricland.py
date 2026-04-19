#!/usr/bin/env python3

import asyncio
import json
import sys
import websockets

WS_URL = "ws://localhost:25885"
API_URL = "http://localhost:25884"

async def get_current_lyric():
    try:
        import urllib.request
        req = urllib.request.Request(f"{API_URL}/api/control/song-info")
        response = urllib.request.urlopen(req, timeout=2)
        data = json.loads(response.read().decode())
        if data.get("code") == 200:
            return data.get("data", {})
    except:
        pass
    return None

def format_lyric(lyric_data):
    if not lyric_data:
        return ""
    
    current_time = lyric_data.get("currentTime", 0)
    lrc_data = lyric_data.get("lrcData", [])
    
    current_line = ""
    for line in lrc_data:
        start = line.get("startTime", 0)
        end = line.get("endTime", 0)
        if start <= current_time <= end:
            words = line.get("words", [])
            if words:
                current_line = "".join(w.get("word", "") for w in words)
                break
    
    if not current_line:
        for line in lrc_data:
            if line.get("startTime", 0) <= current_time:
                words = line.get("words", [])
                if words:
                    current_line = "".join(w.get("word", "") for w in words)
    
    if current_line:
        return current_line[:25]
    return ""

async def main():
    lyric_data = await get_current_lyric()
    lyric = format_lyric(lyric_data)
    
    if lyric:
        output = lyric
    else:
        output = "♪"
    
    print(output)
    sys.stdout.flush()

    try:
        async with websockets.connect(WS_URL) as ws:
            await ws.send(json.dumps({"type": "get-song-info"}))
            
            async for message in ws:
                try:
                    msg = json.loads(message)
                except:
                    continue
                
                msg_type = msg.get("type")
                
                if msg_type in ["lyric-change", "song-change", "progress-change"]:
                    lyric_data = await get_current_lyric()
                    lyric = format_lyric(lyric_data)
                    
                    if lyric:
                        output = lyric
                    else:
                        output = "♪"
                    
                    print(output)
                    sys.stdout.flush()
                    
                elif msg_type == "welcome":
                    pass
                    
    except Exception as e:
        pass

if __name__ == "__main__":
    asyncio.run(main())
