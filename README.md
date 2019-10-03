# Utano
Simple but powerful music player written (by the guy who doesn't speak English) in Python (3.7).
#### Please keep in mind program is still in beta and lots of things are going to be changed a lot. ( => This documentation may not be up-today)
## What does it do
- Automatically starts playing music from the given folder.
- Automatically shuffles your playlist.
- Quick and easy controls.
- No complex settings, just click and play. (If you don't want them to be complex)
- Possible lyrics and some basic music visualization.
- And it has achievements.

# Install
- Install [vlc player](https://www.videolan.org/vlc/index.cs.html)
- Add vlc to your system path
- Go to [releases](https://github.com/TheNovi/Utano/releases) and download the latest version
- Write your full path to the folder with music, to `home/config.json` (for more info about config file read further).
#### From source
- Install python (3.7 or newer)
- Install [vlc player](https://www.videolan.org/vlc/index.cs.html)
- Add vlc to your system path
- Get this repo
- Install pipfile (or install all packages in requirements.txt)
- Write your full path to the folder with music, to `home/config.json` (for more info about config file read further).
- Run `main.py`
- If there was any issue while following these steps, or program doesn't run at all. Please don't hesitate to write a [issue](https://github.com/TheNovi/Utano/issues) (I'm too lazy to properly test this)

# Song files name format
Better and more ways to personalize this coming soon. Until then:<br>
`artist - song_name.format`
- `artist` - name of artist
- ` - ` - Must be surrounded by spaces
- `song_name` - name of the song
- `format` - `.mp3`, `.wav`, etc.

# Controls
### Controls are under heavy development right now, but here is some summary at least:
- Control songs by area with song name and artist:
    - Left-click for next song.
    - Right-click for the previous song.
        - Can be switched in `conf.json`
    - Press mouse wheel to pause/resume.
    - Move your mouse into the window and scroll the mouse wheel to change the volume
    - Start typing to search
    - Left/Right (This is going to be changed a lot) to show stats from there:
        - Left/Right to show achievements
- Press `Escape` anywhere to get back to the main scene  
- Catalog mode
    - press `Down arrow` to access it.
    - start writing for search
    - hit `Enter` or `Down/Up arrow` for access list
    - (press `i` or `Backspace` to search again)
    - select one song (with `mouse` or `arrows`) and hit `mouse` or `enter` for play it.

# Conf files
- You can delete any option to use it's default
#### Conf file (`conf.json`)
- `path`: path to songs folder. (default: './')
- `theme_path`: path to theme.json (default: "./theme.json")
- `stats_path`: path to theme.json (default: "./stats.json")
- `volume`: starting volume (default: 50)
- `switch_controls`: switch song switching controls (only mouse buttons) (default: False)
- `reverse_title`: reverse full song name ("artist - name") in the title (default: False)
- `reverse_in_list`: ^^^ but in the catalog (default: False)
#### Theme file (`theme.json`)
- `bg`: Background color (default: "Black")
- `fg`: Foreground/Font color (default: "Red")
- `font`: Font name (default: "segoe print")
- `lrc`: fg of lrc (default: "#ffdddd")

# Lrc files
### There is no proper way to make lrc files yet.<br>
This program does NOT use normal `.lrc` files.<br>
- ## .lc files
    -  Quick way to disable some features:
        - `!lrcs` - Disable texts
        - `!drops` - Disable drops
        - `!all` - Disable everything (same as deleting whole file but it's quicker)
    - main commands:
        - `[ time ] text` - at `time` (in milliseconds) show `text` (`[ 49570 ] la la la`)
        - `[ time ] !drop duration name_offset artist_offset sm` - for drop (`[100] !drop 17 2 1 s`)
            - `duration` - duration of drop
            - `offset` - How much will text (`song_name`/`song_artist`) move from site to site (counted in chars)
            - `sm`
                - type `s` - for disabling shuffling
                - type `m` - for disabling moving/twitching
                - or both
    - Lines starting with `#`, `/` will be ignored.
    
# (not really) FAQ 
#### Why `not really` FAQ?
Because I don't get any questions.
#### Why do I need to install vlc player?
The program plays music using `python-vlc` module. Which requires installed vlc on the local machine. Also, vlc is one of the best media players
#### What are supported music formats
This Program uses vlc.MediaPlayer, you can find this information in their documentation. (I'm too lazy to read it. Sorry)
But so far I know it's supporting these formats: `.mp3`, `.wav` ... (also I didn't find any which aren't supported)
#### Why, if I press the stop button (multimedia button on the keyboard), program crash?
Yeah, stop button closes the program (its quick and elegant way to stop the program). And you can simulate stop button by pressing (mouse buttons) `wheel` `right` and `left`.
#### What program does when it gets to the last song?
After the program gets on the end (of the playlist), he shuffles the music. And start over again.
#### In `What does it do` you said it doesn't have complex settings, but this is a way too complicated.
Yeah if you want to use this program with it's all features right away, it may get a little complicated.<br>
But after you get little use to it, it's not that hard.
Also, if you don't want to use lyrics, drops, etc. You don't have to. Just ignore them.
