import json
import os
import sys

import keyboard
from nui.gui.v1 import Stage, Style

from core import Utano
from scenes.catalog import Catalog
from scenes.home import Home
from scenes.volume import Volume

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
	s.after(10, queue)


DEBUG = [x for x in sys.argv if x.lower() in ['-d', '--debug']]

if __name__ == '__main__':
	s: Stage = Stage(Style.from_dict(theme), __file__)
	conf = load(s.path(os.path.join('nudes' if DEBUG else 'home', 'conf.json')), conf)
	conf['path'] = os.path.realpath(conf['path'])
	conf['theme_path'] = os.path.realpath(s.path(conf['theme_path']))
	conf['stats_path'] = os.path.realpath(s.path(conf['stats_path']))
	conf['lrc_path'] = os.path.realpath(s.path(conf['lrc_path']))
	theme = load(conf['theme_path'], theme)
	s.style = Style.from_dict(theme)
	ut = Utano(conf)
	s.master.title('Utano')
	s.master.iconbitmap(default=s.path('icon.ico'))
	s.master.resizable(width=False, height=False)
	s.master.wm_minsize(width=200, height=0)
	s.master.bind("<Button-2>", lambda e: ut.pause())
	s.add('', Home, ut)
	s.add('v', Volume, ut)
	s.add('c', Catalog, ut)

	# noinspection PyTypeChecker
	h: Home = s['']
	ut.set_callbacks(next_song_call=h.next_song_call, lrc_call=h.lrc_call, achieve_call=h.achieve_call)  # TODO Move these lines to some ut.init() method
	ut.next_song(init=True)
	ut.stats.program_started.add()

	# noinspection PyBroadException
	try:
		keyboard.add_hotkey(-179, lambda: ut.pause())  # play/pause media
		keyboard.add_hotkey(-176, lambda: ut.next_song())  # next track
		keyboard.add_hotkey(-177, lambda: ut.next_song(-1))  # previous track
		keyboard.add_hotkey(-178, lambda: conf['disable_stop_button'] or s.quit())  # stop media
	except:  # NOSONAR
		pass

	s.after(1, queue)
	s.run('')
	ut.end()
