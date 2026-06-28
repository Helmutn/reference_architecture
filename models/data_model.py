#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Project Name: reference_architecture
File Name:    data_model.py
Author:       helmutngawa
Date:         27.06.26
Description:  This file represents a model of data of a youtube video
-------------------------------------------------------------------------------
"""

from dataclasses import dataclass, field

import re
from googleapiclient.discovery import build

# To define how to read appi-key from an external file
API_KEY = "AIzaSyCRdyoYbFNiiXkYrXb9Ku46R2_reIemIn4"


@dataclass
class DataModel:
    url: str = "https://www.youtube.com/watch?v=0tM-l_ZsxjU"
    video_data: dict = field(default_factory=dict)

    def __post_init__(self):
        self.get_video_details()

    def extract_video_id(self):
        """Extrahiert die 11-stellige Video-ID aus verschiedenen YouTube-URL-Formaten."""
        pattern = r"(?:v=|\/v\/|youtu\.be\/|\/embed\/|\/shorts\/)([a-zA-Z0-9_-]{11})"
        match = re.search(pattern, self.url)
        if match:
            return match.group(1)
        return None

    def get_video_details(self):
        """Holt die Statistiken und Details des Videos über die YouTube API."""
        # Verbindung zur API aufbauen
        youtube = build("youtube", "v3", developerKey=API_KEY)

        # API-Anfrage für das spezifische Video starten
        request = youtube.videos().list(part="snippet,statistics", id=self.extract_video_id())
        response = request.execute()

        # Prüfen, ob das Video existiert
        if not response["items"]:
            # To define how to pass data to the container
            print("Video nicht gefunden oder es ist privat.")
            self.video_data = {}

        raw_data = response["items"][0]

        # Daten extrahieren
        title = raw_data["snippet"]["title"]
        published_at = raw_data["snippet"]["publishedAt"]

        # Manche Daten fehlen, wenn sie vom Kanalbesitzer deaktiviert wurden
        stats = raw_data["statistics"]
        views = stats.get("viewCount", "Deaktiviert")
        likes = stats.get("likeCount", "Deaktiviert")
        comments = stats.get("commentCount", "Deaktiviert")

        self.video_data = {
            "title": title,
            "published_at": published_at,
            "views": views,
            "likes": likes,
            "comments": comments
        }
        # To do pass to logger
        print("Video data read.")
