import json
import os
import sys

import keyboard
from nui.gui.v2 import Stage, Style

from core import Utano
from core.conf import Conf
from scenes.achievements import Achievements
from scenes.catalog import Catalog
from scenes.home import Home
from scenes.options import Options
from scenes.stats import Stats
from scenes.volume import Volume

theme = {
	"bg": "Black",
	"fg": "Red",
	"font_family": "segoe print",
	# "lrc": "#ffdddd"  # TODO As child
}


def load(path: str, default: dict) -> dict:
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


if __name__ == '__main__':
	s: Stage = Stage(Style.from_dict(theme), __file__)
	conf = Conf(s.path()).load(''.join(sys.argv[1:]) if len(sys.argv) > 1 else os.path.join('home', 'conf.json'))
	s.style = Style.from_dict(load(conf.theme_path, theme))
	ut = Utano(conf)
	s.master.title('Utano')
	s.master.iconbitmap(default=s.path('icon.ico'))
	s.master.resizable(width=False, height=False)
	s.master.wm_minsize(width=200, height=0)
	s.master.bind("<Button-2>", lambda e: ut.pause())
	s.args(ut=ut) \
		.add_all([Home, Catalog, Volume, Stats, Achievements, Options])

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
		keyboard.add_hotkey(-178, lambda: conf.disable_stop_button or s.quit())  # stop media
	except:  # NOSONAR
		pass

	s.after(1, queue)
	s.run('')
	ut.end()
