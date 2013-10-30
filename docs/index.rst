.. enzyme documentation master file, created by
   sphinx-quickstart on Fri May 10 01:11:03 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Enzyme
======
Release v\ |version|

Enzyme is a Python module to parse video metadata.


Usage
-----
Parse a MKV file::

    >>> with open('How.I.Met.Your.Mother.S08E21.720p.HDTV.X264-DIMENSION.mkv', 'rb') as f:
    ...    mkv = enzyme.MKV(f)
    ... 
    >>> mkv.info
    <Info [title=None, duration=0:20:56.005000, date=2013-04-15 14:06:50]>
    >>> mkv.video_tracks
    [<VideoTrack [1, 1280x720, V_MPEG4/ISO/AVC, name=None, language=eng]>]
    >>> mkv.audio_tracks
    [<AudioTrack [2, 6 channel(s), 48000Hz, A_AC3, name=None, language=und]>]


License
-------
Apache2


API Documentation
-----------------

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api/mkv
   api/parsers
