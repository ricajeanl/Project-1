import random
from Data_Storage import DataStorage

class Queue:
    def __init__(self):
        self.list = []
        self.current = None
        self.shuffle = False
        self.repeat = False
        self.pagination = 10
        self.total_duration = 0
        self.originalOrder = []
        self.current_index = None  # Initialize current_index

    def play(self):
        if not self.list:
            print("The queue is empty. Nothing to play.")
            return
        
        if self.shuffle:
            if not self.current_index:
                self.current_index = 0
            print(f"Playing: {self.list[self.current_index]}")
        elif self.current_index is None:
            self.current_index = 0
            print(f"Playing: {self.list[self.current_index]}")
        else:
            print(f"Playing: {self.list[self.current_index]}")

    def skip(self):
        if not self.list:
            print("The queue is empty. Nothing to skip.")
            return
        
        if self.repeat:
            self.current_index = (self.current_index + 1) % len(self.list)
            print(f"Playing: {self.list[self.current_index]}")
        else:
            if self.current_index is None or self.current_index + 1 >= len(self.list):
                print("End of the queue. No more tracks to skip to.")
            else:
                self.current_index += 1
                print(f"Playing: {self.list[self.current_index]}")


    def previous(self):
        if self.current is None:
            print("No track is currently playing.")
            return
        
        if self.current.prev is None:
            print("No previous track. You are at the start of the queue.")
            return
        
        self.current = self.current.prev.track
        print(f"Playing: {self.current}")

    def toggle_shuffle(self):
        if not self.list:
            print("The queue is empty. Cannot shuffle.")
            return

        self.shuffle = not self.shuffle
        if self.shuffle:
            self.originalOrder = self.list[:]
            random.shuffle(self.list)
            print("Shuffle is On. Queue is shuffled.")
        else:
            self.list = self.originalOrder
            self.originalOrder = []
            print("Shuffle is Off. Queue is back to its original order.")


    def toggle_repeat(self):
        self.repeat = not self.repeat
        print(f"Repeat mode is now {'enabled' if self.repeat else 'disabled'}.")

    def add_tracks(self, new_tracks):
        added_count = 0
        for track in new_tracks:
            if track not in self.list:
                self.list.append(track)
                added_count += 1
        
        if not self.current and self.list:
            self.current_index = 0
            self.current = self.list[0]
        
        self.update_duration()
        print(f"Added {added_count} new tracks to the queue.")

    def get_total_duration(self):
        return f"{self.total_duration // 3600} hr {self.total_duration % 3600 // 60} min"

    def display_queue(self):
        if not self.list:
            print("The queue is empty.")
            return

        total_pages = (len(self.list) + self.pagination - 1) // self.pagination
        current_page = (self.current_index // self.pagination + 1) if self.current_index is not None else 1

        print(f"Total Duration: {self.get_total_duration()}")
        print(f"Shuffle: {'On' if self.shuffle else 'Off'} | Repeat: {'On' if self.repeat else 'Off'}")
        print(f"Page {current_page} of {total_pages}")
        print("Tracks:")

        start = (current_page - 1) * self.pagination
        end = min(start + self.pagination, len(self.list))
        for i in range(start, end):
            prefix = "(Currently Playing)" if self.current_index == i else f"({i + 1})"
            track = self.list[i]
            print(f"{prefix} {track.title} - {track.artist} ({track.duration})")


    def exit(self):
        self.save_queue()
        print("Queues saved.")



