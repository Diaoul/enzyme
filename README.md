# Enzyme

Enzyme is a Python module to parse video metadata.

## Usage

Parse a MKV file metadata:

```python
>>> import enzyme
>>> with open('example.mkv', 'rb') as f:
...     mkv = enzyme.MKV(f)
...
>>> mkv.info
<Info [title=None, duration=0:00:01.440000, date=2015-03-14 08:40:16]>
>>> mkv.video_tracks
[<VideoTrack [2, 720x576, V_DIRAC, name=u'Video\x00', language=None]>]
>>> mkv.audio_tracks
[<AudioTrack [1, 2 channel(s), 44100Hz, A_MS/ACM, name=u'Audio\x00', language=None]>]
```

## License

Enzyme is licensed under the MIT license.
