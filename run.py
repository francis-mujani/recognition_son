#!/usr/bin/python


from recognize_microphone import run

if __name__ == '__main__':
  song = run()
  print("SON TROUVE :",song['SONG_NAME'])