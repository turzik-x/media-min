#!/usr/bin/python

from distutils import extension
import sys
import ffmpeg
import os



def media_convert(filename):
    ext = os.path.splitext(filename)[1]
    print (f"filename:{filename}")
    import ffmpeg
    (
      ffmpeg
      .input(filename)
      .output( filename + ".min."+ext  )
      .run()
    )


def main(argv):
    media_convert(argv[1])
    pass

main(sys.argv)
