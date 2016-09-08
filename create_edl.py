#!/usr/bin/env python

import os, sys, shutil
import process_edl

# where are the comskip configurations kept
comskip_directory='/Users/james/bin/comskip'
library_directories = [
  '/Users/james/Downloads/torrents/tv',
  '/Volumes/4TB/TV/TV-14',
  '/Volumes/4TB/TV/TV-G',
  '/Volumes/4TB/TV/TV-PG',
]
file_extensions = {
  'mkv' : True,
  'mp4' : True,
  'm4v' : True,
  'avi' : True,
}
processed_count = 0

def process_file(file_name):
  print "file_name: %s" % file_name
  if os.path.isfile(file_name):
    
    # look for comskip config file
    # check to see if there is a comskip.ini in the file's directory, if not copy the found config
    file_dir = os.path.dirname(file_name)
    comskip_config = '%s/comskip.ini' % comskip_directory
    comskip_ini_file = '%s/comskip.ini' % file_dir
    if  not os.path.isfile(comskip_ini_file):
      series_name = file_name.split('.')[0]
      possible_comskip_config = '%s/%s.ini' % (comskip_directory, series_name)
      print "possible_conskip_config: %s" % (possible_comskip_config)
      if os.path.isfile(possible_comskip_config):
        comskip_config = possible_comskip_config

      series_name = file_name.split(' - ')[0]
      possible_comskip_config = '%s/%s.ini' % (comskip_directory, series_name)
      print "possible_conskip_config: %s" % (possible_comskip_config)
      if os.path.isfile(possible_comskip_config):
        comskip_config = possible_comskip_config
      
      print "copying file %s to %s" % (comskip_config, comskip_ini_file)
      shutil.copyfile(comskip_config, comskip_ini_file)

    os.chdir(file_dir)
    comskip_command = 'comskip --csvout -t -n  "%s"' % (file_name)
    comskip_command = 'comskip -n "%s"' % (file_name)
    print "comskip_command: %s" % comskip_command
    print "running comskip..."
    os.system(comskip_command)

    # cleanup temporary directory
    
def recurse_directory(top_dir):
  global processed_count
  dir_list = os.listdir(top_dir)
  for file in dir_list:
    if file[0] == '.':
      # skip hidden files, they are hidden for a reason
      continue
    file = "%s/%s" % (top_dir, file)
    if os.path.isdir(file):
      recurse_directory(file)
    else:
      # this is a file, see if it matches the file_extensions requirements
      extension = file.split('.')[-1]
      # check to see if the extension matches
      if extension in file_extensions:
        # we have a file with a good extension, check to see if there is already an EDL file
        edl_filename = file.replace(extension, 'edl')
        if not os.path.isfile(edl_filename):
          processed_count += 1
          if (processed_count <= 10):
            process_file(file)
          else:
            return;
      else:
        #print 'non-matching file: %s' % file
        pass


if __name__=='__main__':
  pwd = os.getcwd();
  # list the files in the original_directory

  for dir in library_directories:
    recurse_directory(dir)
    
  os.chdir(pwd)


