#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Project Name: reference_architecture
File Name:    youtube_tracker_tab.py
Author:       helmutngawa
Date:         27.06.26
Description:  [Enter a brief description of the script's purpose]
-------------------------------------------------------------------------------
"""
import webbrowser
import tkinter as tk
from tkinter import messagebox

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
except ImportError:
    matplotlib = None
    plt = None

from controllers.main_controller import MainController
from infrastructure.event_bus import EventBus
from ui.widgets.primary_widgets import PrimaryLabel, PrimaryButton, PrimaryEntry, PrimaryTreeview
from ui.tabs.base_tab import BaseTab


class YoutubeTrackerTab(BaseTab):
    def __init__(self, parent, controller: MainController, event_bus: EventBus):
        super().__init__(parent, event_bus)

        self.model = controller.model
        self.data_service = controller.data_service
        self.result_lookup = {}

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)
        self.configure(height=700)
        self.pack_propagate(False)

        self.canvas = tk.Canvas(self, highlightthickness=0, height=700)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.x_scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.x_scrollbar.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(yscrollcommand=self.scrollbar.set, xscrollcommand=self.x_scrollbar.set)
        self.content_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.content_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=2)
        self.content_frame.rowconfigure(7, weight=1)

        PrimaryLabel(self.content_frame, text="Search query: ").grid(column=0, row=0, sticky="w", padx=(10, 5), pady=(10, 5))
        self.entry_query = PrimaryEntry(self.content_frame)
        self.entry_query.insert(0, "python tutorials")
        self.entry_query.grid(column=1, row=0, sticky="ew", padx=(0, 10), pady=(10, 5))

        PrimaryLabel(self.content_frame, text="Creation date: ").grid(column=0, row=1, sticky="w", padx=(10, 5), pady=5)
        self.entry_creation_date = PrimaryEntry(self.content_frame)
        self.entry_creation_date.insert(0, "2020-01-01")
        self.entry_creation_date.grid(column=1, row=1, sticky="ew", padx=(0, 10), pady=5)

        PrimaryLabel(self.content_frame, text="Min subscribers: ").grid(column=0, row=2, sticky="w", padx=(10, 5), pady=5)
        self.entry_min_subscribers = PrimaryEntry(self.content_frame)
        self.entry_min_subscribers.insert(0, "1")
        self.entry_min_subscribers.grid(column=1, row=2, sticky="ew", padx=(0, 10), pady=5)

        PrimaryLabel(self.content_frame, text="Max subscribers: ").grid(column=0, row=3, sticky="w", padx=(10, 5), pady=5)
        self.entry_max_subscribers = PrimaryEntry(self.content_frame)
        self.entry_max_subscribers.insert(0, "2000000")
        self.entry_max_subscribers.grid(column=1, row=3, sticky="ew", padx=(0, 10), pady=5)

        PrimaryLabel(self.content_frame, text="Min views: ").grid(column=0, row=4, sticky="w", padx=(10, 5), pady=5)
        self.entry_min_views = PrimaryEntry(self.content_frame)
        self.entry_min_views.insert(0, "1")
        self.entry_min_views.grid(column=1, row=4, sticky="ew", padx=(0, 10), pady=5)

        PrimaryLabel(self.content_frame, text="Max views: ").grid(column=0, row=5, sticky="w", padx=(10, 5), pady=5)
        self.entry_max_views = PrimaryEntry(self.content_frame)
        self.entry_max_views.insert(0, "50000000")
        self.entry_max_views.grid(column=1, row=5, sticky="ew", padx=(0, 10), pady=5)

        self.btn_search = PrimaryButton(self.content_frame, text="Search channels", command=self.on_search_btn_clicked)
        self.btn_search.grid(column=0, row=6, columnspan=2, sticky="ew", padx=10, pady=(10, 10))

        self.results_tree = PrimaryTreeview(
            self.content_frame,
            columns=("title", "created_at", "subscribers", "views", "video_count", "link"),
            show="headings"
        )
        self.results_tree.heading("title", text="Title")
        self.results_tree.heading("created_at", text="Created")
        self.results_tree.heading("subscribers", text="Subscribers")
        self.results_tree.heading("views", text="Views")
        self.results_tree.heading("video_count", text="Videos")
        self.results_tree.heading("link", text="Link")
        self.results_tree.column("title", width=260, anchor="w")
        self.results_tree.column("created_at", width=120, anchor="center")
        self.results_tree.column("subscribers", width=130, anchor="center")
        self.results_tree.column("views", width=130, anchor="center")
        self.results_tree.column("video_count", width=90, anchor="center")
        self.results_tree.column("link", width=220, anchor="center")
        self.results_tree.tag_configure("link", foreground="blue")
        self.results_tree.configure(cursor="hand2")
        self.results_tree.bind("<Double-1>", self.on_results_tree_click)
        self.results_tree.bind("<Button-3>", self.on_results_tree_right_click)

        self.results_tree_scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree_x_scrollbar = tk.Scrollbar(self.content_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=self.results_tree_scrollbar.set, xscrollcommand=self.results_tree_x_scrollbar.set)
        self.results_tree.grid(column=0, row=7, columnspan=2, sticky="nsew", padx=10, pady=(0, 10))
        self.results_tree_scrollbar.grid(column=2, row=7, sticky="ns", pady=(0, 10))
        self.results_tree_x_scrollbar.grid(column=0, row=8, columnspan=3, sticky="ew", padx=(10, 0), pady=(0, 10))

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Show videos", command=self.show_selected_channel_videos)
        self.context_menu.add_command(label="Plot video statistics", command=self.plot_selected_channel_videos)

        PrimaryLabel(self.content_frame, text="Title: ").grid(column=0, row=9, sticky="w", padx=(10, 5), pady=(10, 5))
        self.label_title = PrimaryLabel(self.content_frame, text="")
        self.label_title.grid(column=1, row=9, sticky="w", padx=(0, 10), pady=(10, 5))

        PrimaryLabel(self.content_frame, text="Published at: ").grid(column=0, row=10, sticky="w", padx=(10, 5), pady=5)
        self.label_published = PrimaryLabel(self.content_frame, text="")
        self.label_published.grid(column=1, row=10, sticky="w", padx=(0, 10), pady=5)

        PrimaryLabel(self.content_frame, text="Number of views: ").grid(column=0, row=11, sticky="w", padx=(10, 5), pady=5)
        self.label_views = PrimaryLabel(self.content_frame, text="")
        self.label_views.grid(column=1, row=11, sticky="w", padx=(0, 10), pady=5)

        PrimaryLabel(self.content_frame, text="Number of likes: ").grid(column=0, row=12, sticky="w", padx=(10, 5), pady=5)
        self.label_likes = PrimaryLabel(self.content_frame, text="")
        self.label_likes.grid(column=1, row=12, sticky="w", padx=(0, 10), pady=5)

        PrimaryLabel(self.content_frame, text="Comments: ").grid(column=0, row=13, sticky="w", padx=(10, 5), pady=(5, 10))
        self.label_comments = PrimaryLabel(self.content_frame, text="")
        self.label_comments.grid(column=1, row=13, sticky="w", padx=(0, 10), pady=(5, 10))

        self.btn_update = PrimaryButton(self.content_frame, text="Update", command=self.on_update_btn_clicked, state="disabled")
        self.btn_update.grid(column=0, row=14, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        self.content_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    @staticmethod
    def _parse_creation_date(raw_value):
        if raw_value is None or raw_value.strip() == "":
            return None
        parts = [part.strip() for part in raw_value.split(",") if part.strip()]
        if len(parts) == 2:
            return tuple(parts)
        return raw_value

    def update_tracker_data(self, data):
        self.label_title.configure(text=data.get("title", ""))
        self.label_published.configure(text=data.get("published_at", ""))
        self.label_views.configure(text=data.get("views", ""))
        self.label_likes.configure(text=data.get("likes", ""))
        self.label_comments.configure(text=data.get("comments", ""))

    def _get_selected_result(self, event=None):
        if event is not None:
            item_id = self.results_tree.identify_row(event.y)
        else:
            selected_items = self.results_tree.selection()
            item_id = selected_items[0] if selected_items else None

        if item_id is None:
            return None
        return self.result_lookup.get(item_id)

    def on_update_btn_clicked(self):
        self.print_logger("Updating tracker")
        self.model.set_url(self.data_service.get_url())
        self.model.update_video_details()
        self.update_tracker_data(self.model.video_data)

    def on_results_tree_click(self, event):
        region = self.results_tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column_id = self.results_tree.identify_column(event.x)
        if column_id != "#6":
            return

        selected_item = self.results_tree.identify_row(event.y)
        if not selected_item:
            return

        values = self.results_tree.item(selected_item, "values")
        if not values or len(values) < 6:
            return

        channel_url = values[5]
        if channel_url:
            webbrowser.open(channel_url)
            self.print_logger(f"Opening channel: {channel_url}")

    def on_results_tree_right_click(self, event):
        item_id = self.results_tree.identify_row(event.y)
        if item_id is None:
            return

        self.results_tree.selection_set(item_id)
        self.context_menu.post(event.x_root, event.y_root)

    def _update_results_tree_height(self, total_results):
        visible_rows = min(12, max(5, total_results))
        self.results_tree.configure(height=visible_rows)

    def plot_selected_channel_videos(self):
        result = self._get_selected_result()
        if result is None:
            return

        channel_id = result.get("channel_id")
        if not channel_id:
            return

        if plt is None:
            messagebox.showinfo("Plot unavailable", "Matplotlib is not available in the current environment.")
            return

        videos = self.data_service.get_channel_videos(channel_id, max_results=50)
        if not videos:
            messagebox.showinfo("No videos", "No videos were found for this channel.")
            return

        videos = sorted(videos, key=lambda video: video.get("views", 0), reverse=True)[:10]

        labels = [video.get("title", "")[:20] for video in videos]
        views = [int(video.get("views", 0) or 0) for video in videos]
        likes = [int(video.get("likes", 0) or 0) for video in videos]

        fig, ax = plt.subplots(figsize=(12, 6))
        x_positions = list(range(len(videos)))

        bars = ax.bar(x_positions, views, width=0.8, alpha=0.7, color="tab:blue", label="Views")
        ax.set_xticks(x_positions)
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_ylabel("Views")
        ax.set_title(f"Top videos for {result.get('title', '')}")
        ax.legend(loc="upper left")

        ax2 = ax.twinx()
        ax2.plot(x_positions, likes, color="tab:orange", marker="o", linewidth=2, label="Likes")
        ax2.set_ylabel("Likes")
        ax2.legend(loc="upper right")

        for bar, value in zip(bars, views):
            ax.text(bar.get_x() + bar.get_width() / 2, value, f"{value:,}", ha="center", va="bottom", fontsize=8)

        fig.tight_layout()
        plt.show()

    def show_selected_channel_videos(self):
        result = self._get_selected_result()
        if result is None:
            return

        channel_id = result.get("channel_id")
        if not channel_id:
            return

        videos = self.data_service.get_channel_videos(channel_id, max_results=200)
        if not videos:
            messagebox.showinfo("No videos", "No videos were found for this channel.")
            return

        videos = sorted(videos, key=lambda video: video.get("views", 0), reverse=True)

        window = tk.Toplevel(self)
        window.title(f"Videos for {result.get('title', '')}")
        window.geometry("1200x500")

        container = tk.Frame(window, padx=10, pady=10)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        v_scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        v_scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=v_scrollbar.set)

        tree_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=tree_frame, anchor="nw")
        tree_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        tree = PrimaryTreeview(tree_frame, columns=("title", "link", "views", "likes", "comments"), show="headings")
        tree.heading("title", text="Title")
        tree.heading("link", text="Link")
        tree.heading("views", text="Views")
        tree.heading("likes", text="Likes")
        tree.heading("comments", text="Comments")
        tree.column("title", width=340, anchor="w")
        tree.column("link", width=280, anchor="center")
        tree.column("views", width=110, anchor="center")
        tree.column("likes", width=110, anchor="center")
        tree.column("comments", width=130, anchor="center")
        tree.pack(fill="both", expand=True)

        h_scrollbar = tk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side="bottom", fill="x")

        for video in videos:
            tree.insert(
                "",
                "end",
                values=(
                    video.get("title", ""),
                    video.get("url", ""),
                    video.get("views", 0),
                    video.get("likes", 0),
                    video.get("comments", 0),
                )
            )

        def open_selected_video(event):
            if tree.identify("region", event.x, event.y) != "cell":
                return
            column_id = tree.identify_column(event.x)
            if column_id != "#2":
                return
            selected = tree.identify_row(event.y)
            if not selected:
                return
            url = tree.item(selected, "values")[1]
            if url:
                webbrowser.open(url)

        tree.bind("<Double-1>", open_selected_video)

    def _populate_results(self, results):
        self.result_lookup = {}
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        self._update_results_tree_height(len(results))

        for result in results:
            channel_id = result.get("channel_id")
            channel_url = f"https://www.youtube.com/channel/{channel_id}" if channel_id else ""
            item_id = self.results_tree.insert(
                "",
                "end",
                values=(
                    result.get("title", ""),
                    result.get("created_at", ""),
                    result.get("subscribers", 0),
                    result.get("views", 0),
                    result.get("video_count", 0),
                    channel_url,
                ),
                tags=("link",)
            )
            self.result_lookup[item_id] = result

    def on_search_btn_clicked(self):
        query = self.entry_query.get().strip()
        if not query:
            self.print_logger("Please enter a search query for YouTube channels.")
            return

        raw_creation_date = self.entry_creation_date.get().strip()
        min_subscribers = self.entry_min_subscribers.get().strip()
        max_subscribers = self.entry_max_subscribers.get().strip()
        min_views = self.entry_min_views.get().strip()
        max_views = self.entry_max_views.get().strip()

        creation_date = self._parse_creation_date(raw_creation_date)

        try:
            results = self.data_service.search_youtube_channels(
                query=query,
                creation_date=creation_date,
                min_subscribers=int(min_subscribers) if min_subscribers else 0,
                max_subscribers=int(max_subscribers) if max_subscribers else None,
                min_views=int(min_views) if min_views else 0,
                max_views=int(max_views) if max_views else None,
            )
        except ValueError as exc:
            self.print_logger(f"Invalid search input: {exc}")
            return
        except Exception as exc:
            self.print_logger(f"Channel search failed: {exc}")
            return

        self._populate_results(results)
        self.print_logger(f"Found {len(results)} channels matching the filters")
