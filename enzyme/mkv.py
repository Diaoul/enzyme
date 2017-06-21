# -*- coding: utf-8 -*-
from .exceptions import ParserError, MalformedMKVError
from .parsers import ebml
from datetime import timedelta
from sys import getsizeof
import xml.etree.ElementTree as xml
import logging


__all__ = ['VIDEO_TRACK', 'AUDIO_TRACK', 'SUBTITLE_TRACK', 'MKV', 'Info', 'Track', 'VideoTrack',
           'AudioTrack', 'SubtitleTrack', 'Tag', 'SimpleTag', 'Chapter', 'Attachment']
logger = logging.getLogger(__name__)


# Track types
VIDEO_TRACK, AUDIO_TRACK, SUBTITLE_TRACK = 0x01, 0x02, 0x11


class MKV(object):
    """Matroska Video file

    :param stream: seekable file-like object

    """
    def __init__(self, stream, recurse_seek_head=False, load_attachments=True):
        # default attributes
        self.info = None
        self.video_tracks = []
        self.audio_tracks = []
        self.subtitle_tracks = []
        self.chapters = []
        self.tags = []
        self.attachments = []
        # keep track of the elements parsed
        self.recurse_seek_head = recurse_seek_head
        self._parsed_positions = set()

        try:
            # get the Segment element
            logger.info('Reading Segment element')
            specs = ebml.get_matroska_specs()
            segments = ebml.parse(stream, specs, ignore_element_names=['EBML'], max_level=0)
            if not segments:
                raise MalformedMKVError('No Segment found')
            if len(segments) > 1:
                logger.warning('%d segments found, using the first one', len(segments))
            segment = segments[0]

            # get and recursively parse the SeekHead element
            logger.info('Reading SeekHead element')
            stream.seek(segment.position)
            seek_head = ebml.parse_element(stream, specs)
            if seek_head.name != 'SeekHead':
                raise MalformedMKVError('No SeekHead found')
            seek_head.load(stream, specs, ignore_element_names=['Void', 'CRC-32'])
            self._parse_seekhead(seek_head, segment, stream, specs, load_attachments)
        except ParserError as e:
            raise MalformedMKVError('Parsing error: %s' % e)

    def _parse_seekhead(self, seek_head, segment, stream, specs, load_attachments):
        for seek in seek_head:
            element_id = ebml.read_element_id(seek['SeekID'].data)
            element_name = specs[element_id][1]
            element_position = seek['SeekPosition'].data + segment.position
            if element_position in self._parsed_positions:
                logger.warning('Skipping already parsed %s element at position %d', element_name, element_position)
                continue
            if element_name == 'Info':
                logger.info('Processing element %s from SeekHead at position %d', element_name, element_position)
                stream.seek(element_position)
                self.info = Info.fromelement(ebml.parse_element(stream, specs, True, ignore_element_names=['Void', 'CRC-32']))
            elif element_name == 'Tracks':
                logger.info('Processing element %s from SeekHead at position %d', element_name, element_position)
                stream.seek(element_position)
                tracks = ebml.parse_element(stream, specs, True, ignore_element_names=['Void', 'CRC-32'])
                self.video_tracks.extend([VideoTrack.fromelement(t) for t in tracks if t['TrackType'].data == VIDEO_TRACK])
                self.audio_tracks.extend([AudioTrack.fromelement(t) for t in tracks if t['TrackType'].data == AUDIO_TRACK])
                self.subtitle_tracks.extend([SubtitleTrack.fromelement(t) for t in tracks if t['TrackType'].data == SUBTITLE_TRACK])
            elif element_name == 'Chapters':
                logger.info('Processing element %s from SeekHead at position %d', element_name, element_position)
                stream.seek(element_position)
                self.chapters.extend([Chapter.fromelement(c) for c in ebml.parse_element(stream, specs, True, ignore_element_names=['Void', 'CRC-32'])[0] if c.name == 'ChapterAtom'])
            elif element_name == 'Tags':
                logger.info('Processing element %s from SeekHead at position %d', element_name, element_position)
                stream.seek(element_position)
                self.tags.extend([Tag.fromelement(t) for t in ebml.parse_element(stream, specs, True, ignore_element_names=['Void', 'CRC-32'])])
            elif element_name == 'Attachments':
                logger.info('Processing element %s from SeekHead at position %d', element_name, element_position)
                stream.seek(element_position)
                self.attachments.extend([Attachment.fromelement(t, load_attachments) for t in ebml.parse_element(stream, specs, True, ignore_element_names=['Void', 'CRC-32'])])
            elif element_name == 'SeekHead' and self.recurse_seek_head:
                logger.info('Processing element %s from SeekHead at position %d', element_name, element_position)
                stream.seek(element_position)
                self._parse_seekhead(ebml.parse_element(stream, specs, True, ignore_element_names=['Void', 'CRC-32']), segment, stream, specs)
            else:
                logger.debug('Element %s ignored', element_name)
            self._parsed_positions.add(element_position)

    def tags_to_xml(self):
        root = xml.Element('Tags')
        root.extend([tag.to_xml() for tag in self.tags])
        return root

    def to_dict(self):
        return {'info': self.info.__dict__, 'video_tracks': [t.__dict__ for t in self.video_tracks],
                'audio_tracks': [t.__dict__ for t in self.audio_tracks], 'subtitle_tracks': [t.__dict__ for t in self.subtitle_tracks],
                'chapters': [c.__dict__ for c in self.chapters], 'tags': [t.to_dict() for t in self.tags], 'attachments':  [a.to_dict() for a in self.attachments]}

    def __getitem__(self, targettype):
        if isinstance(targettype, str):
            return [tag for tag in self.tags if tag.targets.targettype == targettype]
        else:
            return [tag for tag in self.tags if tag.targets.targettypevalue == targettype]

    def __repr__(self):
        return '<%s [%r, %r, %r, %r, %d tags, %d attachments]>' % (self.__class__.__name__, self.info, self.video_tracks, self.audio_tracks, self.subtitle_tracks, len(self.tags), len(self.attachments))


class Info(object):
    """Object for the Info EBML element"""
    def __init__(self, title=None, duration=None, date_utc=None, timecode_scale=None, muxing_app=None, writing_app=None):
        self.title = title
        self.duration = timedelta(microseconds=duration * (timecode_scale or 1000000) // 1000) if duration else None
        self.date_utc = date_utc
        self.muxing_app = muxing_app
        self.writing_app = writing_app

    @classmethod
    def fromelement(cls, element):
        """Load the :class:`Info` from an :class:`~enzyme.parsers.ebml.Element`

        :param element: the Info element
        :type element: :class:`~enzyme.parsers.ebml.Element`

        """
        title = element.get('Title')
        duration = element.get('Duration')
        date_utc = element.get('DateUTC')
        timecode_scale = element.get('TimecodeScale')
        muxing_app = element.get('MuxingApp')
        writing_app = element.get('WritingApp')
        return cls(title, duration, date_utc, timecode_scale, muxing_app, writing_app)

    def __repr__(self):
        return '<%s [title=%r, duration=%s, date=%s]>' % (self.__class__.__name__, self.title, self.duration, self.date_utc)

    def __str__(self):
        return repr(self.__dict__)


class Track(object):
    """Base object for the Tracks EBML element"""
    def __init__(self, type=None, number=None, name=None, language=None, enabled=None, default=None, forced=None, lacing=None,  # @ReservedAssignment
                 codec_id=None, codec_name=None, uid=None):
        self.type = type
        self.number = number
        self.name = name
        self.language = language
        self.enabled = enabled
        self.default = default
        self.forced = forced
        self.lacing = lacing
        self.codec_id = codec_id
        self.codec_name = codec_name
        self.uid = uid

    @classmethod
    def fromelement(cls, element):
        """Load the :class:`Track` from an :class:`~enzyme.parsers.ebml.Element`

        :param element: the Track element
        :type element: :class:`~enzyme.parsers.ebml.Element`

        """
        type = element.get('TrackType')  # @ReservedAssignment
        number = element.get('TrackNumber', 0)
        name = element.get('Name')
        language = element.get('Language')
        enabled = bool(element.get('FlagEnabled', 1))
        default = bool(element.get('FlagDefault', 1))
        forced = bool(element.get('FlagForced', 0))
        lacing = bool(element.get('FlagLacing', 1))
        codec_id = element.get('CodecID')
        codec_name = element.get('CodecName')
        uid = element.get('TrackUID', 0)

        return cls(type=type, number=number, name=name, language=language, enabled=enabled, default=default,
                   forced=forced, lacing=lacing, codec_id=codec_id, codec_name=codec_name, uid=uid)

    def __repr__(self):
        return '<%s [%d, name=%r, language=%s]>' % (self.__class__.__name__, self.number, self.name, self.language)

    def __str__(self):
        return str(self.__dict__)


class VideoTrack(Track):
    """Object for the Tracks EBML element with :data:`VIDEO_TRACK` TrackType"""
    def __init__(self, width=0, height=0, interlaced=False, stereo_mode=None, crop=None,
                 display_width=None, display_height=None, display_unit=None, aspect_ratio_type=None, **kwargs):
        super(VideoTrack, self).__init__(**kwargs)
        self.width = width
        self.height = height
        self.interlaced = interlaced
        self.stereo_mode = stereo_mode
        self.crop = crop
        self.display_width = display_width
        self.display_height = display_height
        self.display_unit = display_unit
        self.aspect_ratio_type = aspect_ratio_type

    @classmethod
    def fromelement(cls, element):
        """Load the :class:`VideoTrack` from an :class:`~enzyme.parsers.ebml.Element`

        :param element: the Track element with :data:`VIDEO_TRACK` TrackType
        :type element: :class:`~enzyme.parsers.ebml.Element`

        """
        videotrack = super(VideoTrack, cls).fromelement(element)
        videotrack.width = element['Video'].get('PixelWidth', 0)
        videotrack.height = element['Video'].get('PixelHeight', 0)
        videotrack.interlaced = bool(element['Video'].get('FlagInterlaced', False))
        videotrack.stereo_mode = element['Video'].get('StereoMode')
        videotrack.crop = {}
        if 'PixelCropTop' in element['Video']:
            videotrack.crop['top'] = element['Video']['PixelCropTop']
        if 'PixelCropBottom' in element['Video']:
            videotrack.crop['bottom'] = element['Video']['PixelCropBottom']
        if 'PixelCropLeft' in element['Video']:
            videotrack.crop['left'] = element['Video']['PixelCropLeft']
        if 'PixelCropRight' in element['Video']:
            videotrack.crop['right'] = element['Video']['PixelCropRight']
        videotrack.display_width = element['Video'].get('DisplayWidth')
        videotrack.display_height = element['Video'].get('DisplayHeight')
        videotrack.display_unit = element['Video'].get('DisplayUnit')
        videotrack.aspect_ratio_type = element['Video'].get('AspectRatioType')
        return videotrack

    def __repr__(self):
        return '<%s [%d, %dx%d, %s, name=%r, language=%s]>' % (self.__class__.__name__, self.number, self.width, self.height,
                                                               self.codec_id, self.name, self.language)

    def __str__(self):
        return str(self.__dict__)


class AudioTrack(Track):
    """Object for the Tracks EBML element with :data:`AUDIO_TRACK` TrackType"""
    def __init__(self, sampling_frequency=None, channels=None, output_sampling_frequency=None, bit_depth=None, **kwargs):
        super(AudioTrack, self).__init__(**kwargs)
        self.sampling_frequency = sampling_frequency
        self.channels = channels
        self.output_sampling_frequency = output_sampling_frequency
        self.bit_depth = bit_depth

    @classmethod
    def fromelement(cls, element):
        """Load the :class:`AudioTrack` from an :class:`~enzyme.parsers.ebml.Element`

        :param element: the Track element with :data:`AUDIO_TRACK` TrackType
        :type element: :class:`~enzyme.parsers.ebml.Element`

        """
        audiotrack = super(AudioTrack, cls).fromelement(element)
        audiotrack.sampling_frequency = element['Audio'].get('SamplingFrequency', 8000.0)
        audiotrack.channels = element['Audio'].get('Channels', 1)
        audiotrack.output_sampling_frequency = element['Audio'].get('OutputSamplingFrequency')
        audiotrack.bit_depth = element['Audio'].get('BitDepth')
        return audiotrack

    def __repr__(self):
        return '<%s [%d, %d channel(s), %.0fHz, %s, name=%r, language=%s]>' % (self.__class__.__name__, self.number, self.channels,
                                                                               self.sampling_frequency, self.codec_id, self.name, self.language)


class SubtitleTrack(Track):
    """Object for the Tracks EBML element with :data:`SUBTITLE_TRACK` TrackType"""
    pass


class Tag(object):
    """Object for the Tag EBML element"""
    def __init__(self, targets=None, simpletags=None):
        self.targets = targets
        self.simpletags = simpletags if simpletags is not None else []

    @classmethod
    def fromelement(cls, element):
        """Load the :class:`Tag` from an :class:`~enzyme.parsers.ebml.Element`

        :param element: the Tag element
        :type element: :class:`~enzyme.parsers.ebml.Element`

        """
        targets = Targets.fromelement(element['Targets']) if 'Targets' in element else Targets()
        simpletags = [SimpleTag.fromelement(s) for s in element if s.name == 'SimpleTag']
        return cls(targets, simpletags)

    def __getitem__(self, tagName):
        return [st for st in self.simpletags if st.name == tagName]

    def to_xml(self):
        root = xml.Element('Tag')
        root.append(self.targets.to_xml())
        root.extend([simtag.to_xml() for simtag in self.simpletags])
        return root

    def to_dict(self):
        return {'targets':self.targets.__dict__, 'simpletags':[st.to_dict() for st in self.simpletags]}

    def __truediv__(self, other):
        if isinstance(other, SimpleTag):
            self.simpletags.append(other)
        return other

    def __repr__(self):
        return '<%s [targets=%r, simpletags=%r]>' % (self.__class__.__name__, self.targets, self.simpletags)


class Targets(object):
    """Object for the Targets EBML element"""
    def __init__(self, targettypevalue=50, targettype=None, trackUIDs=None, chapterUIDs=None, attachmentUIDs=None, editionUIDs=None):
        self.targettypevalue = targettypevalue
        self.targettype = targettype
        self.trackUIDs = trackUIDs if trackUIDs is not None else []
        self.chapterUIDs = chapterUIDs if chapterUIDs is not None else []
        self.attachmentUIDs = attachmentUIDs if attachmentUIDs is not None else []
        self.editionUIDs = editionUIDs if editionUIDs is not None else []

    @classmethod
    def fromelement(cls, element):
        """Load the :class:`Targets` from an :class:`~enzyme.parsers.ebml.Element`

        :param element: the Targets element
        :type element: :class:`~enzyme.parsers.ebml.Element`

        """
        targettype = element.get('TargetType')
        targettypevalue = element.get('TargetTypeValue', 50)
        trackUIDs = element.get_all('TagTrackUID')
        chapterUIDS = element.get_all('TagChapterUID')
        attachmentUIDs = element.get_all('TagAttachmentUID')
        editionUIDs = element.get_all('TagEditionUID')
        return cls(targettypevalue, targettype, trackUIDs, chapterUIDS, attachmentUIDs, editionUIDs)

    def to_xml(self):
        root = xml.Element('Targets')
        if self.targettypevalue is not None:
            xml.SubElement(root, 'TargetTypeValue').text = str(self.targettypevalue)
        if self.targettype is not None:
            xml.Subelement(root, 'TargetType').text = self.targettype
        for uids in self.trackUIDs:
            xml.SubElement(root, 'TrackUID').text = str(uids)
        for uids in self.chapterUIDs:
            xml.SubElement(root, 'ChapterUID').text = str(uids)
        for uids in self.attachmentUIDs:
            xml.SubElement(root, 'AttachmentUID').text = str(uids)
        for uids in self.editionUIDs:
            xml.SubElement(root, 'EditionUID').text = str(uids)
        return root

    def __repr__(self):
        return '<%s [%s, targettype=%s, %d target UIDs]>' % (self.__class__.__name__, str(self.targettypevalue), self.targettype,
                                                             sum([len(t) for t in [self.chapterUIDs, self.trackUIDs, self.editionUIDs, self.attachmentUIDs]]))


class SimpleTag(Tag):
    """Object for the SimpleTag EBML element"""
    def __init__(self, name, language='und', default=True, string=None, binary=None, simpletags=None):
        self.name = name
        self.language = language
        self.default = default
        self.string = string
        self.binary = binary
        self.simpletags = simpletags if simpletags is not None else []

    @classmethod
    def fromelement(cls, element):
        """Load the :class:`SimpleTag` from an :class:`~enzyme.parsers.ebml.Element`

        :param element: the SimpleTag element
        :type element: :class:`~enzyme.parsers.ebml.Element`

        """
        name = element.get('TagName')
        language = element.get('TagLanguage', 'und')
        default = element.get('TagDefault', True)
        string = element.get('TagString')
        binary = element.get('TagBinary')
        simpletags = [SimpleTag.fromelement(t) for t in element.get_master_elements()]
        return cls(name, language, default, string, binary, simpletags)

    def to_xml(self):
        root = xml.Element('Simple')
        xml.SubElement(root, 'Name').text = self.name
        if self.language != 'und' : xml.SubElement(root, 'TagLanguage').text = self.language
        if not self.default: xml.SubElement(root, 'DefaultLanguage').text = str(int(self.default))
        if self.string is not None:
            xml.SubElement(root, 'String').text = self.string
        if self.binary is not None:
            xml.SubElement(root, 'Binary').text = str(int(self.binary))
        root.extend([simtag.to_xml() for simtag in self.simpletags])
        return root

    def to_dict(self):
        stag_dict = self.__dict__.copy()
        stag_dict['simpletags'] = [st.to_dict() for st in self.simpletags]
        return stag_dict

    def __repr__(self):
        if len(self.simpletags) == 0:
            return '<%s [%s, language=%s, default=%s, string=%s]>' % (self.__class__.__name__, self.name, self.language, self.default, self.string)
        else:
            return '<%s [%s, language=%s, default=%s, string=%s, simpletags=%r]>' % (self.__class__.__name__, self.name, self.language, self.default, self.string, self.simpletags)


class Chapter(object):
    """Object for the ChapterAtom and ChapterDisplay EBML element

    .. note::
        For the sake of simplicity, it is assumed that the ChapterAtom element
        has no more than 1 ChapterDisplay child element and informations it contains
        are merged into the :class:`Chapter`

    """
    def __init__(self, start, hidden=False, enabled=False, end=None, uid=None, string=None, language=None):
        self.start = start
        self.hidden = hidden
        self.enabled = enabled
        self.end = end
        self.string = string
        self.language = language
        self.uid = uid

    @classmethod
    def fromelement(cls, element):
        """Load the :class:`Chapter` from a :class:`~enzyme.parsers.ebml.Element`

        :param element: the ChapterAtom element
        :type element: :class:`~enzyme.parsers.ebml.Element`

        """
        start = timedelta(microseconds=element.get('ChapterTimeStart') // 1000)
        hidden = element.get('ChapterFlagHidden', False)
        enabled = element.get('ChapterFlagEnabled', True)
        end = element.get('ChapterTimeEnd')
        uid = element.get('ChapterUID')
        chapterdisplays = [c for c in element if c.name == 'ChapterDisplay']
        if len(chapterdisplays) > 1:
            logger.warning('More than 1 (%d) ChapterDisplay element in the ChapterAtom, using the first one', len(chapterdisplays))
        if chapterdisplays:
            string = chapterdisplays[0].get('ChapString')
            language = chapterdisplays[0].get('ChapLanguage')
            return cls(start, hidden, enabled, end, uid, string, language)
        return cls(start, hidden, enabled, end, uid)

    def __repr__(self):
        return '<%s [%s, enabled=%s]>' % (self.__class__.__name__, self.start, self.enabled)


class Attachment(object):
    """Object for the Attachedfile EBML element"""
    def __init__(self, description=None, name=None, mime_type=None, uid=None, data=None):
        self.description = description
        self.name = name
        self.mime_type = mime_type
        self.uid = uid
        self.data = data

    @classmethod
    def fromelement(cls, element, load_attachment=True):
        """Load the :class:`Attachment` from a :class:`~enzyme.parsers.ebml.Element`

        :param element: the Attachedfile element element
        :type element: :class:`~enzyme.parsers.ebml.Element`
        :param load_attachment: whether to load the attachment data or not (Default : true)
        :type load_attachment: :class:str
        """
        description = element.get('FileDescription')
        name = element.get('FileName')
        mime_type = element.get('FileMimeType')
        uid = element.get('FileUID')
        if load_attachment:
            data = element.get('FileData', None)
        else:
            data = None
        return cls(description, name, mime_type, uid, data)

    def to_dict(self):
        att_dict = self.__dict__.copy()
        att_dict['data'] = None if self.data is None else self.data.read()
        return att_dict

    def __repr__(self):
        return '<%s [%s, type=%s, %d KB]>' % (self.__class__.__name__, self.description if not self.description == '' else self.name, self.mime_type, getsizeof(self.data)/1000)
