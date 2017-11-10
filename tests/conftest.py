from pytest import fixture
from unittest import mock

import logging
import os
import urllib.request
from hashlib import md5
from io import BytesIO
from urllib.request import urlopen as orig_urlopen


logging.raiseExceptions = False


cache_dir = os.path.join(os.path.dirname(__file__), '.cache')
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)


def mock_urlopen(url):
    key = md5(url.encode('utf-8')).hexdigest()
    cache_file = os.path.join(cache_dir, key)
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            content = f.read()
    else:
        content = orig_urlopen(url).read()
        with open(cache_file, 'wb') as f:
            f.write(content)
    return BytesIO(content)


urllib.request.urlopen = mock.Mock(wraps=mock_urlopen)


BASE_URL = 'http://akas.imdb.com'

MOVIES = {
    '0043338': 'ace in the hole',           # multiple languages, single sound mix with note
    '3629794': 'aslan',                     # no cover URL
    '1863157': 'ates parcasi',              # no rating, no votes, no rank, no plot, no mpaa, no aspect ratio, no sound mix
    '0185906': 'band of brothers',          # TV mini-series, ended series years
    '1247467': 'band of brothers ep 4',     # episode in mini-series
    '0436992': 'dr who',                    # TV series, continuing series years
    '1000252': 'dr who ep blink',           # TV episode
    '0412142': 'house md',                  # multiple seasons
    '0606035': 'house md ep first',         # first episode
    '2121964': 'house md ep middle',        # intermediate episode
    '2121965': 'house md ep last',          # last episode
    '0063850': 'if....',                    # one genre, multiple color info with notes,
                                            # single sound mix without notes
    '0060666': 'manos',                     # bottom 100, single color info with notes
    '0133093': 'matrix',                    # top 250, aspect ratio, multiple sound mix with notes
    '2971344': 'matrix short',              # short movie, language "None"
    '0389150': 'matrix tv',                 # TV movie, no color info
    '0274085': 'matrix tv short',           # TV short movie
    '0390244': 'matrix vg',                 # video game
    '0109151': 'matrix video',              # video movie
    '3698420': 'mothers day iv',            # IMDb index
    '0120789': 'pleasantville',             # multiple color info, multiple sound mix without notes
    '1985970': 'roast of charlie sheen',    # TV special
    '0081505': 'shining',                   # multiple runtimes, multiple countries
    '0076786': 'suspiria'                   # multiple country runtimes
}

PEOPLE = {
    '0000001': 'fred astaire',      # name with dates
    '0000206': 'keanu reeves',      # no IMDb index
    '0000210': 'julia roberts',     # IMDb index
    '0330139': 'deni gordon'        # no headshot
}


@fixture(scope='session')
def movies():
    """Base addresses of all test movies."""
    return {v: '%(base)s/title/tt%(key)s' % {'base': BASE_URL, 'key': k}
            for k, v in MOVIES.items()}


@fixture(scope='session')
def people():
    """Base addresses of all test people."""
    return {v: '%(base)s/name/nm%(key)s' % {'base': BASE_URL, 'key': k}
            for k, v in PEOPLE.items()}


@fixture(scope='session')
def search():
    """Base address for search pages."""
    return '%(base)s/find' % {'base': BASE_URL}
