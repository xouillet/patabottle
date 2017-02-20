# Patabottle

Patabottle is a simple web server written in Python 3 with [Bottle](https://bottlepy.org/) framework
to allow simple [Patacrep](https://github.com/patacrep/patacrep) songbook generation

## Requirements

 - Python 3
 - Bottle (`pip install bottle`)
 - [Patacrep](https://github.com/patacrep/patacrep) (`pip install patacrep`)
 - [Patadata](https://github.com/patacrep/patadata) repository for songs
 
## Usage
 
Edit `patabottle.py` to set path to patadata directory (defaults to '../patadata'), then just run it
 
```
$ python patabottle.py
INFO:root:Discovering all songs...
INFO:root:958 songs discovered
Bottle v0.12.12 server starting up (using WSGIRefServer())...
Listening on http://0.0.0.0:7654/
Hit Ctrl-C to quit.

```

You can now access patabottle on port 7654
