streamInput = data.get('stream_name').lower()
chromecastInput = data.get('media_player')
chromecast = chromecastInput

streams = {
    "overwatchleague": "overwatchleague",
    "overwatch league": "overwatchleague",
    "owl": "overwatchleague",
    "lcs": "riotgames",
    "ninja": "ninja",
    "tim": "timthetatman",
    "gdq": "gamesdonequick",
    "games done quick": "gamesdonequick",
    "shroud": "shroud",
    "seagull": "a_seagull",
    "sneaky": "c9sneaky"
}

if streamInput in streams:
    streamToCast = streams[streamInput]
else:
    streamToCast = streamInput

url = "https://twitch.tv/"+streamToCast

if (chromecast == 1 or chromecast == 'living room tv'):
    mediaPlayer = "living_room_tv"
elif (chromecast == 2 or chromecast == 'bedroom tv'):
    mediaPlayer = "sonas_hot_chromecast"
elif (chromecast == 3):
    mediaPlayer = "dining_room"
elif (chromecast == 4):
    mediaPlayer = "kitchen"
elif (chromecast == 5):
    mediaPlayer = "living_room_speaker"
elif (chromecast == 6):
    mediaPlayer = "music_flow2034"
else:
    mediaPlayer = "living_room_tv"


logger.info("Streaming {} to {}".format(streamInput, mediaPlayer))
hass.services.call("media_extractor", "play_media", {"entity_id": "media_player."+mediaPlayer, "media_content_id": url, "media_content_type": "video"})
