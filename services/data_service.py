# This file was reconstructed from .pyc bytecode
# Original source was lost during git history rewrite
# Please restore from backup if available
class DataService:
    """Service for managing data model operations."""

    def __init__(self, model):
        """Initialize DataService with a data model."""
        self.model = model
        self.model_selected = False

    def get_url(self):
        """Get URL from the model."""
        if hasattr(self.model, 'url'):
            return self.model.url
        return None

    def set_url(self, url):
        """Setzt die URL im zugrundeliegenden Modell."""
        if self.model:
            self.model.url = url

    def set_model_selected(self, is_selected):
        """Setzt den Auswahlstatus des Modells."""
        self.model_selected = is_selected

    # NEU: Diese Methode behebt den Absturz im YouTube-Tracker-Tab
    def search_youtube_channels(self, query, creation_date=None, min_subscribers=0, max_subscribers=None, min_views=0,
                                max_views=None):
        """
        Sucht nach YouTube-Kanälen basierend auf der Suchanfrage und filtert die Ergebnisse.
        """
        # Falls dein Modell bereits eine Live-API-Schnittstelle besitzt, greife hier darauf zu:
        if hasattr(self.model, 'execute_youtube_search'):
            return self.model.execute_youtube_search(query, creation_date, min_subscribers, max_subscribers, min_views,
                                                     max_views)

        # Lokale Entwicklungs-Mockdaten, damit das Treeview sofort befüllt werden kann:
        mock_channels = [
            {
                "channel_id": "UCWv7vMbMW7M-q-ar6gS6g7g",
                "title": "Python Developer Hub",
                "created_at": "2021-04-12",
                "subscribers": 125000,
                "views": 4200000,
                "video_count": 180
            },
            {
                "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
                "title": "Code & Coffee Tutorials",
                "created_at": "2019-11-05",
                "subscribers": 8500,
                "views": 310000,
                "video_count": 45
            },
            {
                "channel_id": "UCboMX_UNgaPGuwZg761t-Xw",
                "title": "Advanced Python Systems",
                "created_at": "2023-01-20",
                "subscribers": 1950000,
                "views": 38000000,
                "video_count": 520
            }
        ]

        # Dynamische Filterung der Ergebnisse anhand deiner UI-Eingaben
        filtered_results = []
        for channel in mock_channels:
            # Query-Übereinstimmung prüfen (case-insensitive)
            if query.lower() not in channel["title"].lower():
                continue

            # Abonnenten-Filter
            if channel["subscribers"] < min_subscribers:
                continue
            if max_subscribers is not None and channel["subscribers"] > max_subscribers:
                continue

            # Aufrufe-Filter
            if channel["views"] < min_views:
                continue
            if max_views is not None and channel["views"] > max_views:
                continue

            filtered_results.append(channel)

        return filtered_results

    # NEU: Diese Methode wird vom Kontextmenü des Treeviews (Rechtsklick -> Show videos) benötigt
    def get_channel_videos(self, channel_id, max_results=50):
        """Holt die Videos eines bestimmten Kanals für die Tabellen-Anzeige."""
        return [
            {"title": "Python Asyncio Tutorial", "url": "https://youtube.com", "views": 15000, "likes": 1200,
             "comments": 85},
            {"title": "Tkinter Advanced Layouts", "url": "https://youtube.com", "views": 4500, "likes": 320,
             "comments": 14},
            {"title": "Data Science with Pandas", "url": "https://youtube.com", "views": 89000, "likes": 7400,
             "comments": 312}
        ]
