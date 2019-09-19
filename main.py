import tkinter
import json
from threading import Thread
from time import sleep

from utano import *
from scenes import main

conf = {
	"path": "./",
	"volume": 100
}

theme = {
	"bg": 'Black',
	"fg": 'Red',
	"font": 'segoe print'
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
	while True:
		sleep(0.01)
		s_main.tick()
		ut.tick()


if __name__ == '__main__':
	conf = load('nudes/conf.json', conf)
	theme = load('nudes/theme.json', theme)
	ut = Utano(conf)
	root = tkinter.Tk()
	root.config(bg=theme["bg"])
	root.title('Utano v1a')
	root.resizable(width=False, height=False)
	root.bind("<Button-2>", lambda e: ut.pause())

	s_main = main.Main(root, ut, theme)

	s_main.pack(fill='both')
	ut.set_callbacks(next_song_call=s_main.next_song_call)

	q = Thread(target=queue)
	q.setDaemon(True)
	q.start()

	ut.next_song()
	root.mainloop()
