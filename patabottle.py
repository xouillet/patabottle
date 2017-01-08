#! /usr/bin/env python3

import os
import re
import logging
import tempfile
import shutil
import yaml
from contextlib import contextmanager

from bottle import route, run, template, request, response

from patacrep.songbook import prepare_songbook
from patacrep.build    import DEFAULT_STEPS, SongbookBuilder
from patacrep.latex import parse_song

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

# Path configuration

HERE = os.path.dirname(os.path.realpath(__file__))
PATADATA=os.path.join(HERE, '../patadata')
PATADATA_SONGS=os.path.join(PATADATA, 'songs')

# First parse all songs
logging.info("Discovering all songs...")
songs = []
for path,_,files in os.walk(PATADATA_SONGS):
    for filename in files:
        if re.match(".*\.sg$", filename):
            filepath = os.path.join(path, filename)
            with open(filepath, 'r') as f:
                song = parse_song(f.read(), filepath)
                song['path'] = filepath
                songs.append(song)
logging.info("%d songs discovered", len(songs))

# Sort by artists
artists = {}
for song in songs:
    artist, title, path = song['by'], song['@titles'][0], song['path']
    if artist not in artists: artists[artist] = []
    artists[artist].append((path, title))

# cd definition
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

#
# Bottle stuff
#

@route('/')
def index():
    """ GET route, display template """
    return template('index', artists=artists)

@route('/', method='POST')
def generate():
    """ POST route, generate pdf """
    
    songs = request.forms.getall('songs')
    subtitle = request.forms.get('subtitle')

    # Generate yaml and parse it
    songbook_yaml = template('songbook_yaml', songs=songs, PATADATA=PATADATA, subtitle=subtitle)
    songbook_raw = yaml.load(songbook_yaml)

    # Create temp directory and operate patacrep magic
    outputdir = tempfile.mkdtemp()
    outputname = 'songbook'
    with cd(outputdir):
        songbook = prepare_songbook(songbook_raw, outputdir=outputdir, outputname=outputname, datadir_prefix=PATADATA)
        songbook['_cache'] = False
        songbook['_error'] = "failonbook"
        builder = SongbookBuilder(songbook)
        builder.unsafe = True
        builder.build_steps(DEFAULT_STEPS)

    # Read outputed PDF and delete temp directory
    with open(os.path.join(outputdir, outputname+'.pdf'), 'rb') as f:
        pdf = f.read()
    shutil.rmtree(outputdir)

    # Send pdf
    response.content_type = 'application/pdf'
    return pdf

if __name__ == '__main__':
    run(host='0.0.0.0', port=7654)
