# Fingerprint audio files & identify what's playing

- conference [PaceMaker: BackEnd-2016 conference](http://www.pacemaker.in.ua/BackEnd-2016/about)
- slides are on [slideshare.net/rodomansky/ok-shazam-la-lalalaa](http://www.slideshare.net/rodomansky/ok-shazam-la-lalalaa)

![](http://new.tinygrab.com/7020c0e8b010392da4053fa90ab8e0c8419bded864.png)

## How to set up 

1. Run `$ make clean reset` to clean & init database struct
1. Run `$ make tests` to make sure that everything is properly configurated
1. Copy some `.mp3` audio files into `mp3/` directory
1. Run `$ make fingerprint-songs` to analyze audio files & fill your db with hashes
1. Start play any of audio file (from any source) from `mp3/` directory, and run (parallely) `$ make recognize-listen seconds=5`