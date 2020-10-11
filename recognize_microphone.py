#!/usr/bin/python
import os
import sys
import libs
import libs.fingerprint as fingerprint
import argparse

from argparse import RawTextHelpFormatter
# from itertools import izip_longest
try:
    # Python 3
    from itertools import zip_longest
except ImportError:
    # Python 2
    from itertools import izip_longest as zip_longest

from termcolor import colored
from libs.config import get_config
from libs.reader_microphone import MicrophoneReader
from libs.visualiser_console import VisualiserConsole as visual_peak
from libs.visualiser_plot import VisualiserPlot as visual_plot
from libs.db_sqlite import SqliteDatabase
# from libs.db_mongo import MongoDatabase
# python -c 'from myfile import hello; hello()'
# if __name__ == '__main__':

config = get_config()

db = SqliteDatabase()

def run():
  parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
  parser.add_argument('-s', '--seconds', nargs='?')
  args = parser.parse_args()

  if not args.seconds:
    # parser.print_help()
    # sys.exit(0)
    seconds = int(5)
    args.seconds = seconds
  # seconds = int(args.seconds)

  chunksize = 2**12  # 4096
  channels = 2#int(config['channels']) # 1=mono, 2=stereo

  record_forever = False
  visualise_console = bool(config['mic.visualise_console'])
  visualise_plot = bool(config['mic.visualise_plot'])

  reader = MicrophoneReader(None)

  reader.start_recording(seconds=seconds,
    chunksize=chunksize,
    channels=channels)

  msg = ' * started recording..'
  print(colored(msg, attrs=['dark']))

  while True:
    bufferSize = int(reader.rate / reader.chunksize * seconds)

    for i in range(0, bufferSize):
      nums = reader.process_recording()

      if visualise_console:
        msg = colored('%05d', attrs=['dark']) + colored(' %s', 'green')
        print(msg  % visual_peak.calc(nums))
      else:
        msg = 'processing %d of %d..' % (i, bufferSize)
        print(colored(msg, attrs=['dark']))

    if not record_forever: break

  if visualise_plot:
    data = reader.get_recorded_data()[0]
    visual_plot.show(data)

  reader.stop_recording()

  msg = ' * recording has been stopped'
  print(colored(msg, attrs=['dark']))



  def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    liste = [list(filter(None, values)) for values in zip_longest(fillvalue=fillvalue, *args)]
    # print('liste :', liste)
    return liste

  data = reader.get_recorded_data()

  msg = ' * recorded %d samples'
  print(colored(msg, attrs=['dark']) % len(data[0]))

  # reader.save_recorded('test.wav')


  Fs = fingerprint.DEFAULT_FS
  channel_amount = len(data)

  result = set()
  matches = []
  # print("matches :", matches)
  
  def find_matches(samples, Fs=fingerprint.DEFAULT_FS):
    hashes = fingerprint.fingerprint(samples, Fs=Fs)
    return return_matches(hashes)

  def return_matches(hashes):
    mapper = {}
    for hash, offset in hashes:
      mapper[hash.upper()] = offset
      
    values = mapper.keys()

    for split_values in grouper(values, 1000):
      # @todo move to db related files
      query = """
        SELECT upper(hash), song_fk, offset
        FROM fingerprints
        WHERE upper(hash) IN (%s)
      """
      query = query % ','.join('?' * len(split_values))
      # print('query:', query)
      # print('split_values', split_values)
      x = db.executeAll(query, split_values)
      # print('X', x)
      matches_found = len(x)

      if matches_found > 0:
        msg = '** found %d hash matches (step %d/%d)'
        print(colored(msg, 'green') % (
          matches_found,
          len(split_values),
          len(values)
        ))
      else:
        msg = '** not matches found (step %d/%d)'
        print(colored(msg, 'red') % (
          len(split_values),
          len(values)
        ))

      for hash, sid, offset in x:
        # (sid, db_offset - song_sampled_offset)
        # print('hash', hash)
        # print('sid', sid)
        # print('offset', offset)
        # print(' mapper[hash]', mapper[hash])
        # yield (sid, offset - mapper[hash])
        yield (sid, mapper[hash])

  for channeln, channel in enumerate(data):
    # TODO: Remove prints or change them into optional logging.
    msg = 'fingerprinting channel %d/%d'
    print(colored(msg, attrs=['dark']) % (channeln+1, channel_amount))

    matches.extend(find_matches(channel))

    msg = 'finished channel %d/%d, got %d hashes'
    print(colored(msg, attrs=['dark']) % (
      channeln+1, channel_amount, len(matches)
    ))

  def align_matches(matches):
    diff_counter = {}
    largest = 0
    largest_count = 0
    song_id = -1

    for tup in matches:
      sid, diff = tup

      if diff not in diff_counter:
        diff_counter[diff] = {}

      if sid not in diff_counter[diff]:
        diff_counter[diff][sid] = 0

      diff_counter[diff][sid] += 1

      if diff_counter[diff][sid] > largest_count:
        largest = diff
        largest_count = diff_counter[diff][sid]
        song_id = sid

    songM = db.get_song_by_id(song_id)

    nseconds = round(float(largest) / fingerprint.DEFAULT_FS *
                     fingerprint.DEFAULT_WINDOW_SIZE *
                     fingerprint.DEFAULT_OVERLAP_RATIO, 5)

    return {
        "SONG_ID" : song_id,
        "SONG_NAME" : songM[1],
        "CONFIDENCE" : largest_count,
        "OFFSET" : int(largest),
        "OFFSET_SECS" : nseconds
    }

  total_matches_found = len(matches)

  print('')

  if total_matches_found > 0:
    msg = ' ** totally found %d hash matches'
    print(colored(msg, 'green') % total_matches_found)

    song = align_matches(matches)
    #print(song['SONG_NAME'])

    msg = ' => song: %s (id=%d)\n'
    msg += 'offset: %d (%d secs)\n'
    msg += 'confidence: %d'

    print(colored(msg, 'green') % (
      song['SONG_NAME'], song['SONG_ID'],
      song['OFFSET'], song['OFFSET_SECS'],
      song['CONFIDENCE']
    ))
    return song
  else:
    msg = {'error':' ** not matches found at all'}
    print(colored(msg['error'], 'red'))
    return msg
#if __name__ == '__main__':
#  run()