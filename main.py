import time
import json
import os
from kickapi import KickAPI
import requests

STREAMER = "adinross"          # ← CHANGE THIS
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1487180223349919847/vFyLvnWXYhZa9N3NeoRGwhG96h82HtG6XKLrBJokVGXOH0KQB7VSUDbDokBK_Z-xVW4J"  # ← CHANGE THIS
CHECK_INTERVAL = 120                     # 2 minutes
SEEN_FILE = "seen_clips.json"

kick_api = KickAPI()

def load_seen_clips():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen_clips(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def send_to_discord(clip):
    embed = {
        "title": getattr(clip, 'title', "New Kick Clip!"),
        "url": f"https://kick.com/{STREAMER}/clip/{getattr(clip, 'id', '')}",
        "description": f"New clip from {STREAMER}!",
        "color": 0x00ff00,
        "thumbnail": {"url": getattr(clip, 'thumbnail', '')},
        "footer": {"text": "Kick Clip Notifier"}
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]})
        print(f"Sent: {getattr(clip, 'title', 'Clip')}")
    except Exception as e:
        print(f"Discord error: {e}")

seen_clips = load_seen_clips()
print(f"🚀 Starting Kick clip notifier for {STREAMER}...")

while True:
    try:
        channel = kick_api.channel(STREAMER)
        new_clips = [clip for clip in channel.clips if getattr(clip, 'id', None) not in seen_clips]
        
        for clip in reversed(new_clips):
            send_to_discord(clip)
            seen_clips.add(getattr(clip, 'id', None))
        
        if new_clips:
            save_seen_clips(seen_clips)
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(CHECK_INTERVAL)
