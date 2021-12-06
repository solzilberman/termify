
import py_cui
import os
import logging
from spotify import Spotify
import threading
import time
class Player:

    def __init__(self, master: py_cui.PyCUI, Spotify):

        self.master = master
        self.master.set_refresh_timeout(1)
        self.sp = Spotify
        # currently playing display
        self.currently_playing_song_str = self.sp.getCurrentlyPlaying()
        self.currently_playing_label = self.master.add_button(f'Currently Playing: {self.currently_playing_song_str}',0, 0, row_span=1,column_span=5)
        self.currently_playing_label.set_color(py_cui.GREEN_ON_WHITE)
        self.currently_playing_label.set_border_color(py_cui.GREEN_ON_WHITE)
        # search functionality
        self.searchResults = []
        self.search_scroll_cell = self.master.add_scroll_menu('Search Results',         1, 0, row_span=5, column_span=5)
        self.search_scroll_cell.add_key_command(py_cui.keys.KEY_ENTER, self.playSong)
        self.search_scroll_cell.add_key_command(py_cui.keys.KEY_Q_LOWER, self.qSong)
        self.search_scroll_cell.add_key_command(py_cui.keys.KEY_Q_UPPER, self.qSong)
        self.search_text_box = self.master.add_text_box('Search', 6, 0, row_span=1,column_span=5)
        self.search_text_box.add_key_command(py_cui.keys.KEY_ENTER, self.search)
        # queue functionality
        self.qList = []
        self.qu_scroll_cell = self.master.add_scroll_menu('Current Queue', 1, 5, row_span=5, column_span=2)

        self.pauseButton = self.master.add_button(f'PAUSE',0, 5, row_span=1,column_span=1, command=self.pause)
        self.playButton = self.master.add_button(f'PLAY',0, 6, row_span=1,column_span=1,command=self.play)
        self.nextButton = self.master.add_button(f'SKIP',0, 7, row_span=1,column_span=1,command=self.skip)
        self.pauseButton.set_color(py_cui.WHITE_ON_GREEN)
        self.playButton.set_color(py_cui.WHITE_ON_GREEN)
        self.nextButton.set_color(py_cui.WHITE_ON_GREEN)

        # state management daemon
        thread = threading.Thread(target=self.thread_update, args=())
        thread.daemon = True
        thread.start()

    def thread_update(self):
        try:
            while 1:
                self.currently_playing_song_str = self.sp.getCurrentlyPlaying()    
                if self.currently_playing_song_str == "None": pass
                # need to update queue
                lst = self.currently_playing_song_str.split(' ')
                ind = lst.index('-')
                curr = ' '.join(lst[0:ind])
                self.qList = list(filter(lambda x: x != curr, self.qList))
                self.qu_scroll_cell.clear()
                for q in self.qList:
                    self.qu_scroll_cell.add_item(q)
                self.currently_playing_label.set_title(f"Currently Playing: {self.currently_playing_song_str}")
                time.sleep(.5)
        except:
            print('error on getting currently playing song')

    def getCurrentlyPlaying(self):
        self.sp.getCurrentlyPlaying()
        
    def search(self):
        search_param = self.search_text_box.get()
        self.searchResults = self.sp.search(search_param)
        self.search_scroll_cell.clear()
        for r in self.searchResults:
            self.search_scroll_cell.add_item(r[0])
        self.search_text_box.clear()
        self.master.move_focus(self.search_scroll_cell)
    
    def playSong(self):
        selected = self.search_scroll_cell.get()
        song_id = [song[1] for song in self.searchResults if song[0] == selected]
        self.sp.playSong(song_id)
        self.currently_playing_song_str = selected
        self.currently_playing_label.set_title(f"Currently Playing: {self.currently_playing_song_str}")

    def qSong(self):
        selected = self.search_scroll_cell.get()
        song_id = [song[1] for song in self.searchResults if song[0] == selected]
        self.qList.append(selected)
        self.qu_scroll_cell.add_item(selected)
        if len(song_id): self.sp.qSong(song_id[0])

    def pause(self):
        self.sp.pause()
    def play(self):
        self.sp.play()
    def skip(self):
        self.sp.skip()

    

root = py_cui.PyCUI(8, 8)
root.set_title('Termify - Spotify in your Terminal')
root.enable_logging(logging_level=logging.ERROR)
sp = Spotify()
s = Player(root,sp)
root.start()