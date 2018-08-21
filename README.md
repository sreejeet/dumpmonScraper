# dumpmonScraper (python 3.6.x)
A python script to get dumpmon links from twitter.

This script does the following:
  1. Find links from last 20 tweets by @dumpmon
  2. Saves files locally.
  3. Searches these files for keywords.
  4. Logs snippets of keyword found in the files.
  5. Removes log if there were no keywords found. (This is to reduce 
      making too many useless log files.) 

Usage:
```sh
$ python3 dumpmonScraper.py
```
    Runs ONE time.

```sh
$ python3 dumpmonScraper.py 200
```
    Runs indefinitely with a delay of 200 seconds between each round.
