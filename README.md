# TermPlay
*-A Front-End written in Python3 for [play-audio](https://github.com/termux/play-audio) on Android-*

> This project can be used as a packaged application to be used in [Micro-for-Android](https://github.com/TimeATronics/Micro-for-Android) or on [Termux](https://github.com/termux/termux-app)

## Installation:
> Step 1: Download the archive from [Releases](https://github.com/TimeATronics/TermPlay/releases) and unzip into the `/sdcard/` folder.
> Step 2: Open Micro-for-Android (and open a shell) or Termux and `cp` `termplay-exec` from the `/sdcard/TermPlay` folder to your `$HOME`
> Step 3: Make `termplay-exec` executable with the command `termplay-exec`.
> Step 4: Now run `./termplay-exec` in your `$HOME`.
> 
> Note: After Step 4, you can safely delete the `/sdcard/TermPlay` folder.
> 

## Usage:
TermPlay provides a command-line interface to the [play-audio](https://github.com/termux/play-audio) utility.
Upon executing `termplay-exec`, you will be asked to enter the name of a directory containing your musc.
> Note: TermPlay does not support playing music from folders which require root privileges, i.e. it can only access subfolders of the `/storage/` folder.
> 
In the prompt, you can repeatedly press the `TAB` key to get an autocomplete list of a few folders you can choose from. You can also choose others.
> Note: Do not type `/storage/` in front of your input. For eg: `emulated/0/` is a valid input, but not `/storage/emulated/0/`.
> 
If the folder contains any valid file of the formats like .mp3, .flac, .wav etc. you will be able to see a help text and a list of all such music files.
Now, follow the help text as given to proceed further.
