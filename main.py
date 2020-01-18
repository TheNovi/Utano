import json
import tkinter
from sys import argv

import keyboard

from scenes import ScenesManager
from utano import *

conf = {
	"path": "home/music/",
	"theme_path": "home/theme.json",
	"stats_path": "home/stats.json",
	"lrc_path": "home/lrc/",
	"volume": 50,
	"start_paused": False,
	"auto_play": False,
	"replay_when_progress": 0,
	"disable_stop_button": True,
	"switch_controls": False,
	"reverse_title": True,
	"reverse_in_list": False
}

theme = {
	"bg": "Black",
	"fg": "Red",
	"font": "segoe print",
	"lrc": "#ffdddd"
}


def load(path: str, default: dict) -> dict:
	print(path)
	c = {}
	try:
		with open(path, 'r') as f:
			c = json.load(f)
	except Exception as e:
		print(e)
	for k in default:
		if k not in c:
			c[k] = default[k]
	return c


def queue():
	ut.tick()
	s_manager.tick()
	root.after(10, queue)


DEBUG = [x for x in argv if x.lower() in ['-d', '--debug']]

if __name__ == '__main__':
	conf = load(f'{"nudes/" if DEBUG else "home/"}conf.json', conf)
	if not conf['path'].endswith('/'):
		conf['path'] += '/'
	if not conf['lrc_path'].endswith('/'):
		conf['lrc_path'] += '/'
	theme = load(conf['theme_path'], theme)
	ut = Utano(conf)
	root = tkinter.Tk()
	root.config(bg=theme["bg"])
	root.title('Utano Beta')
	root.iconbitmap(default="icon.ico")
	root.resizable(width=False, height=False)
	root.bind("<Button-2>", lambda e: ut.pause())

	s_manager = ScenesManager(root, ut, theme)
	ut.set_callbacks(next_song_call=s_manager.next_song_call, lrc_call=s_manager.s_main.lrc_call, achieve_call=s_manager.achieve_call)
	ut.next_song(stat=False)
	ut.stats.add(ut.stats.events.program_started)

	# noinspection PyBroadException
	try:
		keyboard.add_hotkey(-179, lambda: ut.pause())  # play/pause media
		keyboard.add_hotkey(-176, lambda: ut.next_song())  # next track
		keyboard.add_hotkey(-177, lambda: ut.next_song(-1))  # previous track
		keyboard.add_hotkey(-178, lambda: conf['disable_stop_button'] or root.quit())  # stop media
	except:
		pass

	root.after(1, queue)
	root.mainloop()
	ut.end()
