# Add Music Artwork
The script `AddMusicArtwork.py` automates the process of adding thumbnail cover art images to MP3 files.

## Required installations prior to running the script
* Python 3.8.2
  * Older versions of Python 3 are most likely fine.
* sudo apt install eyed3
  * Version 0.8.10 is good.
* sudo apt install imagemagick
  * Version 6.q16 is good.

## Pre-requisite folder structure
Folder structure:
  Artwork/
  Music/
  Thumbnails/
  AddMusicArtwork.py
  README.md

Within the `Artwork/` and `Music/` folders, you need to have matching file names (excluding file extensions) and a matching number of files. Example:
  Artwork/Somewhere I Belong - Linkin Park.png
  Artwork/Last Stardust - Aimer.png
  Music/Somewhere I Belong - Linkin Park.mp3
  Music/Last Stardust - Aimer.mp3

Also, all image files must be PNG images, and all audio files must be MP3 files.

Your pictures can be their original sizes, but the script resize the original images to a maximum of 300 pixels by 300 pixels while keeping their original dimensions. In other words, a 900x600px image will resize to 300x200px. The newly resized image will be stored in the `Thumbnails/` folder.

#### Edge cases
* Existing files in `Thumbnails/` will be overwitten.
* MP3 files will only store one image file, meaning that this script will not stack the image files on one MP3 file if the script is ran multiple times. This is important because you don't want your MP3 file getting larger with each run!
* Regardless of how you run the script, all of the folders must be exactly named as given.

## Running the script
There are several ways to run this script.

The ensuing command will automate this process:
1) Create equivalent 300x300px thumbnails from PNG files in `Artwork/`
2) Use newly created PNG files in `Thumbnails/` to add as the front cover art image to the equivalent MP3 files in the `Music/` folder
```bash
python3 AddMusicArtwork.py
```

----

The ensuing command will allow you to clear the specified image(s) from the MP3 file(s).
```bash
python3 AddMusicArtwork.py clear "Music/Somewhere I Belong - Linkin Park.mp3" "Music/Last Stardust - Aimer.mp3"
```

----

The ensuing command will allow you to add PNG image(s) to the corresponding MP3 file(s).
```bash
python3 AddMusicArtwork.py add "Music/Somewhere I Belong - Linkin Park.mp3" "Music/Last Stardust - Aimer.mp3"
```

----

The ensuing command will allow you to create 300x300 PNG image(s) from the `Artwork/` folder.
```bash
python3 AddMusicArtwork.py create "Artwork/Somewhere I Belong - Linkin Park.png" "Artwork/Last Stardust - Aimer.png"
```

## Implementation
This script implements the following Ubuntu commands.

#### Resizing artwork to thumbnail files
* convert -resize 300x300 "Artwork/image.png" "Thumbnails/thumbnail.png"
  * The same proportion will be kept.
  * The maximum size of either dimension will be 300px.

#### Adding artwork to audio files
* eyeD3 --add-image "Thumbnails/thumbnail.png:FRONT_COVER" "Music/audio.mp3"

#### Removing artwork from audio files
* eyeD3 --remove-all-images "Music/audio.mp3"

## Changelog
* Version 1.0
  * Everything
* Version 1.0.1
  * README.md updates

## Possible Future Work
* Removal of dependency on Ubuntu packages, thereby enabling Windows and MacOS support
* Enabling of user configuration for folder names and paths
* Creation of an executable file to facilitate the setup process

## Last Remarks
Yeah, I spent a good Sunday evening writing this script and then polishing it thereafter on the ensuing Monday evening. The script suits my current needs, so most likely I won't add any additional support or features.

~ FriskySaga

P.S. My sample files inside the folders are 0 KB ;)

