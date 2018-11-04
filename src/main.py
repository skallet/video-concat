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

   print_short_licence()

   try:
      opts, args = getopt.getopt(
         argv,
         "hf:o:c:t:",
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

   if codec is not None and not codecs.has_key(codec):
      print('Unknown codec, use -h or --help to show help message.')
      sys.exit(2)

   if not outputFile:
      print('Output folder is not found, use -h or --help to show help message.')
      sys.exit(2)

   fileList = []

   try:
      fileList = os.listdir(inputFolder)
   except:
      print('Input folder not found, use -h or --help to show help message.')
      sys.exit(2)

   videos = []
   for f in fileList:
      videos.append(VideoFileClip(os.path.join(inputFolder, f)))

   if (len(videos) <= 0):
      print('No input video found, use -h or --help to show help message.')
      sys.exit(2)

   shuffle(videos)

   if (take is not None):
      videos = videos[:take]

   result = concatenate_videoclips(videos)
   result.write_videofile(outputFile, codec=codec)

if __name__ == "__main__":
   main(sys.argv[1:])