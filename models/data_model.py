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
from datetime import datetime, timezone

import re
from googleapiclient.discovery import build

# To define how to read appi-key from an external file
API_KEY = "AIzaSyCRdyoYbFNiiXkYrXb9Ku46R2_reIemIn4"


@dataclass
class DataModel:
    def __init__(self, url="https://www.youtube.com/watch?v=0tM-l_ZsxjU"):
        self.url = url
        self.video_data: dict = field(default_factory=dict)

    @staticmethod
    def _parse_date(value):
        if value in (None, ""):
            return None
        if isinstance(value, datetime):
            dt = value
        elif isinstance(value, str):
            normalized = value.replace("Z", "+00:00")
            dt = datetime.fromisoformat(normalized)
        else:
            dt = datetime.fromisoformat(str(value))

        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt

    @staticmethod
    def _to_int(value):
        if value in (None, "", "unknown", "undefined"):
            return 0
        if isinstance(value, (int, float)):
            return int(value)
        return int(str(value).replace(".", "").replace(",", ""))

    def _matches_channel_filters(self, creation_date, subscriber_count, view_count,
                                 min_creation_date=None, max_creation_date=None,
                                 min_subscribers=0, max_subscribers=None,
                                 min_views=0, max_views=None):
        if min_creation_date is not None:
            if creation_date is None or creation_date < self._parse_date(min_creation_date):
                return False

        if max_creation_date is not None:
            if creation_date is None or creation_date > self._parse_date(max_creation_date):
                return False

        if subscriber_count < min_subscribers:
            return False

        if max_subscribers is not None and subscriber_count > max_subscribers:
            return False

        if view_count < min_views:
            return False

        if max_views is not None and view_count > max_views:
            return False

        return True

    def search_youtube_channels(self, query, creation_date=None, min_subscribers=0,
                                max_subscribers=None, min_views=0,
                                max_views=None, max_results=50):
        """Search YouTube channels and filter them by creation date, subscriber count and view count.

        Args:
            query: Search string for YouTube.
            creation_date: Optional exact or minimum creation date (ISO format: YYYY-MM-DD).
            min_subscribers: Minimum subscriber count.
            max_subscribers: Optional maximum subscriber count.
            min_views: Minimum total channel views.
            max_views: Optional maximum total channel views.
            max_results: Maximum number of search results to collect before filtering.
        """
        youtube = build("youtube", "v3", developerKey=API_KEY)

        search_items = []
        next_page_token = None

        while len(search_items) < max_results:
            search_request = youtube.search().list(
                part="snippet",
                type="channel",
                q=query,
                maxResults=min(50, max_results - len(search_items)),
                pageToken=next_page_token,
                order="relevance",
                safeSearch="none"
            )
            search_response = search_request.execute()
            current_items = search_response.get("items", [])
            if not current_items:
                break

            search_items.extend(current_items)

            next_page_token = search_response.get("nextPageToken")
            if not next_page_token:
                break

        if not search_items:
            return []

        channel_ids = ",".join(
            item["id"]["channelId"] for item in search_items if item.get("id", {}).get("channelId")
        )
        if not channel_ids:
            return []

        channel_request = youtube.channels().list(part="snippet,statistics", id=channel_ids)
        channel_response = channel_request.execute()

        matches = []
        for channel in channel_response.get("items", []):
            snippet = channel.get("snippet", {})
            stats = channel.get("statistics", {})

            published_at = snippet.get("publishedAt")
            created_dt = self._parse_date(published_at) if published_at else None
            subscriber_count = self._to_int(stats.get("subscriberCount", 0))
            view_count = self._to_int(stats.get("viewCount", 0))
            video_count = self._to_int(stats.get("videoCount", 0))

            min_creation_date = creation_date
            max_creation_date = None
            if isinstance(creation_date, (tuple, list)) and len(creation_date) == 2:
                min_creation_date, max_creation_date = creation_date

            if self._matches_channel_filters(
                created_dt,
                subscriber_count,
                view_count,
                min_creation_date=min_creation_date,
                max_creation_date=max_creation_date,
                min_subscribers=min_subscribers,
                max_subscribers=max_subscribers,
                min_views=min_views,
                max_views=max_views,
            ):
                matches.append({
                    "channel_id": channel.get("id"),
                    "title": snippet.get("title"),
                    "description": snippet.get("description"),
                    "created_at": published_at,
                    "subscribers": subscriber_count,
                    "views": view_count,
                    "video_count": video_count,
                })

        return matches

    def get_channel_videos(self, channel_id, max_results=10):
        """Return the last videos of a channel with their metadata and stats."""
        youtube = build("youtube", "v3", developerKey=API_KEY)

        channels_response = youtube.channels().list(part="contentDetails", id=channel_id).execute()
        items = channels_response.get("items", [])
        if not items:
            return []

        uploads_playlist_id = items[0].get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
        if not uploads_playlist_id:
            return []

        collected_playlist_items = []
        next_page_token = None
        remaining = max_results if max_results is not None else 50

        while True:
            playlist_items_response = youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=min(50, remaining) if remaining is not None else 50,
                pageToken=next_page_token
            ).execute()

            current_items = playlist_items_response.get("items", [])
            if not current_items:
                break

            collected_playlist_items.extend(current_items)

            if max_results is not None:
                remaining = max_results - len(collected_playlist_items)
                if remaining <= 0:
                    break

            next_page_token = playlist_items_response.get("nextPageToken")
            if not next_page_token:
                break

        if not collected_playlist_items:
            return []

        video_ids = [
            item["snippet"]["resourceId"]["videoId"]
            for item in collected_playlist_items
            if item.get("snippet", {}).get("resourceId", {}).get("videoId")
        ]

        if not video_ids:
            return []

        videos = []
        for index in range(0, len(video_ids), 50):
            chunk = video_ids[index:index + 50]
            stats_response = youtube.videos().list(
                part="snippet,statistics",
                id=",".join(chunk)
            ).execute()

            for video in stats_response.get("items", []):
                snippet = video.get("snippet", {})
                stats = video.get("statistics", {})
                video_id = video.get("id")
                videos.append({
                    "video_id": video_id,
                    "title": snippet.get("title"),
                    "published_at": snippet.get("publishedAt"),
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "views": self._to_int(stats.get("viewCount", 0)),
                    "likes": self._to_int(stats.get("likeCount", 0)),
                    "comments": self._to_int(stats.get("commentCount", 0)),
                })

        return videos

    def extract_video_id(self):
        """Extrahiert die 11-stellige Video-ID aus verschiedenen YouTube-URL-Formaten."""
        pattern = r"(?:v=|\/v\/|youtu\.be\/|\/embed\/|\/shorts\/)([a-zA-Z0-9_-]{11})"
        match = re.search(pattern, self.url)
        if match:
            return match.group(1)
        return None

    def update_video_details(self):
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

    def set_url(self, url):
        self.url = url
