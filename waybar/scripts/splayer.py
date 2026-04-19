#!/usr/bin/env python3

import asyncio
import json
import sys
import websockets

WS_URL = "ws://localhost:25885"
API_URL = "http://localhost:25884"

async def get_song_info():
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

def format_output(song_info):
    play_status = song_info.get("playStatus", False) if song_info else False
    
    if play_status:
        icon = "▶"
        status_icon = "⏸"
    else:
        icon = "⏸"
        status_icon = "▶"
    
    if song_info:
        name = song_info.get("playName", "")
        artist = song_info.get("artistName", "")
        if name:
            tooltip = f"{status_icon} {name} - {artist}"
        else:
            tooltip = f"{status_icon}"
    else:
        tooltip = f"{status_icon}"
    
    print(icon)
    print(tooltip)
    sys.stdout.flush()

async def main():
    song_info = await get_song_info()
    format_output(song_info)

    try:
        async with websockets.connect(WS_URL) as ws:
            await ws.send(json.dumps({"type": "get-song-info"}))
            
            async for message in ws:
                try:
                    msg = json.loads(message)
                except:
                    continue
                
                msg_type = msg.get("type")
                
                if msg_type in ["status-change", "song-change", "progress-change"]:
                    song_info = await get_song_info()
                    format_output(song_info)
                    
                elif msg_type == "welcome":
                    pass
                    
    except Exception as e:
        pass

if __name__ == "__main__":
    asyncio.run(main())
