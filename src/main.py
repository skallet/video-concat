import os
import sys
import getopt
from random import shuffle

from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip

def print_help():
   print('available arguments:')
   print('\t-h # show this help')
   print('\t-c <codec> # select output codec (libx264, mpeg4, rawvideo, png, libvorbis, libvpx)')
   print('\t-f <folder> # folder with video files to be edited')
   print('\t-o <output-file> # output file to store results')
   print('\t-t <take-first> # if set, take only first N videos from random list')
   print('\t-r # strech video sizes to its max')
   print('## word specified arguments:')
   print('\t--help # show this help')
   print('\t--folder=<folder> # folder with video files to be edited')
   print('\t--output=<output-file> # output file to store results')

def print_licence():
   print('''
   Video concat
   Copyright (C) 2018 Milan Blazek

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.
   ''')

def print_short_licence():
   print('''
   Video concat  Copyright (C) 2018 Milan Blazek
   This program comes with ABSOLUTELY NO WARRANTY; for details type `--licence'.
   This is free software, and you are welcome to redistribute it
   under certain conditions; type `--licence' for details.
   ''')

def main(argv):
   codecs = {
      'libx264': 'mp4',
      'mpeg4': 'mp4',
      'rawvideo': 'avi',
      'png': 'avi',
      'libvorbis': 'ogv',
      'libvpx': 'webm',
   }

   inputFolder = None
   outputFile = None
   codec = None
   take = None
   method = "compose"

   print_short_licence()

   try:
      opts, args = getopt.getopt(
         argv,
         "hf:o:c:t:r",
         ["help", "folder=", "output="]
      )
   except getopt.GetoptError:
      print_help()
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print_help()
         sys.exit()

      if opt == '--licence':
         print_licence()
         sys.exit()
      elif opt in ("-f", "--folder"):
         inputFolder = arg
      elif opt in ("-o", "--output"):
         outputFile = arg
      elif opt in ("-c"):
         codec = arg
      elif opt in ("-t"):
         take = max(1, int(arg))
      elif opt in ("-r"):
         method = "chain"

   if codec is not None and not codecs.has_key(codec):
      print('Unknown codec, use -h or --help to show help message.')
      sys.exit(2)

   if not outputFile:
      print('Output folder is not found, use -h or --help to show help message.')
      sys.exit(2)

   fileList = []

   try:
      fileList = os.listdir(inputFolder)
      shuffle(fileList)

      if (take is not None):
         fileList = fileList[:take]
      print(fileList)
   except:
      print('Input folder not found, use -h or --help to show help message.')
      sys.exit(2)

   if (len(fileList) <= 0):
      print('No input video found, use -h or --help to show help message.')
      sys.exit(2)

   videos = []
   wWidth = None
   hHeight = None

   clipList = []
   for f in fileList:
      clip = VideoFileClip(os.path.join(inputFolder, f))
      clipList.append(clip)
      cwWidth, chHeight = clip.size
      wWidth = max(wWidth, cwWidth)
      hHeight = max(hHeight, chHeight)

   for clip in clipList:
      # clip.set_fps(24)
      if method == "chain":
         clip = clip.resize(width=wWidth, height=hHeight)
      clip = clip.crossfadein(0.5)
      videos.append(clip)

   result = concatenate_videoclips(videos, method=method, padding=0.5)
   result.write_videofile(outputFile, codec=codec)

if __name__ == "__main__":
   main(sys.argv[1:])