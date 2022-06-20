#!/usr/bin/python

from cmath import log
from distutils import extension
import sys
import ffmpeg
import os
import exiftool
import logging

def print_l(message):
  # logging.info(message)
  pass

def human_readable_size(size, decimal_places=1):
    for unit in ['B','KiB','MiB','GiB','TiB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f}{unit}"
    
def get_keywords(filename):
    with  exiftool.ExifToolHelper() as exif:
      meta = exif.get_tags(filename,tags=["Keywords"])[0]
      print_l("exif")
      print_l(meta)
      if "IPTC:Keywords" in meta: 
        print_l(meta["IPTC:Keywords"])
        return meta["IPTC:Keywords"]

def set_keyword(filename,value):
  with exiftool.ExifToolHelper() as et:
    et.set_tags(
        [filename],
        tags={"Keywords": [value]}
    )

def media_convert_base(filename_in):
    """
    COnvert file via ffmpeg to {filename_in}.min.{ext}
    Returns file path of converted file
    """
    ext = os.path.splitext(filename_in)[1]
    filename_out =  filename_in + ".min"+ext
    print_l (f"filename:{filename_in}")
    (
        ffmpeg
        .input(filename_in)
        .output(filename_out)
        .run(quiet=True,overwrite_output=True)
    )
    
    return filename_out


def media_convert(filename_in):
   keyword =  get_keywords(filename_in)
   if  "reduced-" in keyword:
      print(f"File has keyword '{keyword}'. Skipping this file.")
      return
   
   filesize_in = os.path.getsize(filename_in)
   print(f"Converting {filename_in} ... {human_readable_size(filesize_in)}")
   filename_out = media_convert_base(filename_in)
   filesize_out = os.path.getsize(filename_out)
   ratio = round(filesize_in/filesize_out,1)
   k1 = get_keywords(filename_out)
   k2 = get_keywords(filename_in)
   print(f"Converting {filename_in} ... done  {human_readable_size(filesize_in)}->{human_readable_size(filesize_out)}, reduced {ratio} times.")
   if ratio>1.5:
     with exiftool.ExifToolHelper() as et:
        # exiftool -overwrite_original -TagsFromFile "$f" -All:All "reduced.$f" 1> /dev/null 2> /dev/null
        et.execute(*["-overwrite_original", "-TagsFromFile", filename_in,"-All:All", filename_out])
        et.set_tags(
            [filename_out],
            tags={"Keywords": [f"reduced-{ratio}-times"]},
            params=[ "-overwrite_original"]
        )
        os.remove(filename_in)
        os.rename(filename_out,filename_in)
   else:
       print(f"Converting {filename_in} ... done  The reducing was weak. The reduced file is not use ...")

       with exiftool.ExifToolHelper() as et:
         et.set_tags(
            [filename_in],
            tags={"Keywords": [f"reduced-{0}-times"]}
        )




def main(argv):
    media_convert(argv[1])
    pass

main(sys.argv)
