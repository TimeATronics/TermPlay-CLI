# ------------------------------------------------------------
# TermPlay is licensed under the Apache License, Version 2.0.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# A copy of the "License" is also provided with the source
# of this project. Unless required by applicable law or agreed
# to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing
# permissions and limitations under the License.
# ------------------------------------------------------------

# ------------------------------------------------------------
# This project uses components from the
# https://github.com/termux/play-audio project.
# All licenses and copyrights to the aforementioned
# project reside with its author(s) and/or owners.
# ------------------------------------------------------------

import os
import sys
import subprocess
import datetime
import multiprocessing
import readline
import glob
# readline and glob for tab completion
from rich.console import Console
from tinytag import TinyTag
from time import sleep
from awesome_progress_bar import ProgressBar

# Initialise for console output
console = Console()
# Supported extensions
ext = ["mp3", "MP3", "FLAC", "flac", "wav", "WAV", "\
m4a", "M4A", "OGG", "ogg", "wma", "WMA", "aac", "AAC", "\
opus", "OPUS", "aiff", "AIFF"]


class tabCompleter(object):
	""" Taken from another github project for tab completion"""
	# https://gist.github.com/iamatypeofwalrus/5637895

	def pathCompleter(self, text, state):
		try:
			line = readline.get_line_buffer().split()
			return [x for x in glob.glob(text + '*')][state]
		except KeyboardInterrupt:
			print("\n")

	def createListCompleter(self, ll):
		try:
			def listCompleter(text, state):
				line = readline.get_line_buffer()
				if not line:
					return [c + " " for c in ll][state]
				else:
					return [c + " " for c in ll if c.startswith(line)][state]
			self.listCompleter = listCompleter

		except KeyboardInterrupt:
			print("\n")


def folderInput():
	# list of music files
	global file_list
	global userfolder

	try:
		while True:
			console.print("Type :q or :quit to exit\n", style="b green", justify="center")
			console.print("Press TAB to see suggestions\n", style="b green", justify="center")
			console.print("Enter name of directory:\n", style="b magenta")
			console.print(">>> ", style="b red", end="")

			# For autocompletion:
			t = tabCompleter()
			listcomp = [":q", ":quit"] + glob.glob("\
/storage/*/") + glob.glob("/storage/*/*/") + glob.glob("\
/storage/*/*/*/") + glob.glob("/storage/emulated/0/*/") + glob.glob("\
/storage/emulated/0/*/*/")
			t.createListCompleter(listcomp)
			readline.set_completer_delims('\t')
			readline.parse_and_bind("tab: complete")
			readline.set_completer(t.listCompleter)

			userfolder = (input())

			if len(userfolder) != 0 and list(userfolder)[-1] != "/":
				userfolder += "/"  # Add / to end if not present
			userfolder = "/storage/" + userfolder

			if os.path.isdir(userfolder):
				x = os.listdir(userfolder)  # list all files in the folder
				file_list = []
				for i in x:
					name = str(userfolder + i)
					# Check if extension names in filename and then add to file_list
					if os.path.isfile(name) and any(z in name for z in ext):
						file_list.append(i)
				if len(file_list) != 0:
					break

				else:
					console.print("\nDirectory does not contain any music file", style="b red")

			elif userfolder == "/storage/:q/" or userfolder == "/storage/:quit/":
				console.print("\nExiting Now", style="b red")
				sleep(2)
				clearScreen()
				sys.exit()

			else:
				console.print("\nEnter valid directory name", style="b red")
	except PermissionError:
		console.print("\nPrivileges not present to access folder", style="b red")
	except (KeyboardInterrupt, ValueError):
		console.print("\n")


def clearScreen():
	# print("\033c", end="")
	os.system("clear")


def printDir(dir):
	""" Print Directory and Metadata """
	# proc used to get data about play-audio globally
	global proc
	# tag.duration() used by progress bar
	global tag
	# t1 is name of multiprocessing - progress bar process
	global t1
	try:
		console.print("TERMPLAY\n\n", style="b magenta", justify="center")
		console.print("\
To play from a file, choose the corresponding value", style="b green", justify="center")
		console.print("\
To stop playback, but not close the program, type 0.2", style="b green", justify="center")
		console.print("To stop playback and exit, type 0.1\n", style="b green", justify="center")

		# Print directory as [0] file_name and so on
		for i in file_list:
			print("[" + str(file_list.index(i)) + "] ", end="")
			print(i)

		# check if choice is defined (for first execution of program)
		# To differentiate between 1.1 and int input, check if int_choice as float == choice:
		if '\
int_choice' in globals() and 'choice' in globals() and float(str(int_choice) + ".0") == choice:

			# File Metadata
			console.print("\nNow Playing:" + str(file_list[int_choice]), style="b green")
			tag = TinyTag.get(str(userfolder + str(file_list[int_choice])))
			console.print("\n\
Artist:", tag.artist, "\n\
Title:", tag.title, "\n\
Album:", tag.album, "\n\
Duration:", datetime.timedelta(seconds=round(tag.duration)), style="b blue", justify="center")
			console.print("\n")

			proc = subprocess.Popen(["play-audio", str(userfolder + str(file_list[int_choice]))], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			t1 = multiprocessing.Process(target=progress)
			if 'proc' in globals():
				t1.start()
	except TypeError:
		console.print("\nThe file chosen is not of the correct format", style="b red")
		sleep(2)
		clearScreen()

		sys.exit()


def progress():
	""" Print Progress bar (without inbuilt threading) """
	try:
		total = round(tag.duration)  # Total time to print progress
		bar = ProgressBar(total, bar_length=os.get_terminal_size()[0], use_thread=False)
		for x in range(total):
			sleep(1)
			bar.iter()  # iter to update animation
		console.print('\nPlayback finished', style="b cyan")
	except KeyboardInterrupt:
		print("\n")


def killAll():
	if 'proc' in globals():
		# if proc is defined, i.e., input taken at least once,
		# kill it so that no interference occurs
		proc.terminate()

	if 't1' in globals():
		t1.terminate()
		# join to connect parent python process and background process
		t1.join()


def startScreenInput():
	""" Input Prompt """
	# int_choice is used for accessing list index
	global int_choice
	# choice is float and if == 0.1, exit, if 0.2, kill all processes
	global choice

	while True:
		try:
			console.print(">>> ", style="b red", end="")
			choice = float((input()).replace(" ", ""))
			int_choice = int(choice)
			killAll()

		except (ValueError, TypeError):
			console.print("\tPlease enter a valid integer or decimal-point value", style="b red")

		except KeyboardInterrupt:
			console.print("\n")
			pass

		else:
			try:
				# isinstance is for checking data type
				# check if choice is less than actual length of list

				if choice in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9) or (isinstance(int_choice, int) and (int_choice >= len(file_list) or int_choice < 0)):
					console.print("\tPlease enter \
an integer below {} or more than -1".format(len(file_list)), style="b red")
					continue

				elif isinstance(choice, float) and choice == 0.1:
					console.print("\n\tStopping Playback", style="b cyan")
					console.print("\n\tExiting Now\n", style="b red")
					killAll()

					sleep(2)
					clearScreen()
					sys.exit()

				elif isinstance(choice, float) and choice == 0.2:
					console.print("\n\tStopping Playback", style="b cyan")
					killAll()

				else:
					break

			except Exception:
				pass


def main():
	""" Main function"""
	clearScreen()
	folderInput()
	while True:
		try:
			clearScreen()
			printDir(userfolder)
			startScreenInput()
		except KeyboardInterrupt:
			pass
		except NameError:
			sys.exit()


if __name__ == "__main__":
	main()
