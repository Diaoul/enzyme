from datetime import timedelta, datetime
from enzyme.mkv import MKV, VIDEO_TRACK, AUDIO_TRACK, SUBTITLE_TRACK
import io
import os.path
import requests
import unittest
import zipfile
import pytest


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture(scope="session")
def data_files():
    files = []
    for i in range(1, 9):
        files.append(f"test{i}.mkv")
        files.append(f"test{i}-tag.xml")
    missing_files = [file for file in files if not os.path.exists(os.path.join(DATA_DIR, file))]
    if not missing_files:
        return
    r = requests.get("http://downloads.sourceforge.net/project/matroska/test_files/matroska_test_w1_1.zip")
    with zipfile.ZipFile(io.BytesIO(r.content), "r") as f:
        for missing_file in missing_files:
            f.extract(missing_file, DATA_DIR)


def test_test1(data_files):
    with io.open(os.path.join(DATA_DIR, "test1.mkv"), "rb") as stream:
        mkv = MKV(stream)
    # info
    assert mkv.info.title is None
    assert mkv.info.duration == timedelta(minutes=1, seconds=27, milliseconds=336)
    assert mkv.info.date_utc == datetime(2010, 8, 21, 7, 23, 3)
    assert mkv.info.muxing_app == "libebml2 v0.10.0 + libmatroska2 v0.10.1"
    assert (
        mkv.info.writing_app
        == "mkclean 0.5.5 ru from libebml v1.0.0 + libmatroska v1.0.0 + mkvmerge v4.1.1 ('Bouncin' Back') built on Jul  3 2010 22:54:08"
    )
    # video track
    assert len(mkv.video_tracks) == 1
    assert mkv.video_tracks[0].type == VIDEO_TRACK
    assert mkv.video_tracks[0].number == 1
    assert mkv.video_tracks[0].name is None
    assert mkv.video_tracks[0].language == "und"
    assert mkv.video_tracks[0].enabled == True
    assert mkv.video_tracks[0].default == True
    assert mkv.video_tracks[0].forced == False
    assert mkv.video_tracks[0].lacing == False
    assert mkv.video_tracks[0].codec_id == "V_MS/VFW/FOURCC"
    assert mkv.video_tracks[0].codec_name is None
    assert mkv.video_tracks[0].width == 854
    assert mkv.video_tracks[0].height == 480
    assert mkv.video_tracks[0].interlaced == False
    assert mkv.video_tracks[0].stereo_mode is None
    assert mkv.video_tracks[0].crop == {}
    assert mkv.video_tracks[0].display_width is None
    assert mkv.video_tracks[0].display_height is None
    assert mkv.video_tracks[0].display_unit is None
    assert mkv.video_tracks[0].aspect_ratio_type is None
    # audio track
    assert len(mkv.audio_tracks) == 1
    assert mkv.audio_tracks[0].type == AUDIO_TRACK
    assert mkv.audio_tracks[0].number == 2
    assert mkv.audio_tracks[0].name is None
    assert mkv.audio_tracks[0].language == "und"
    assert mkv.audio_tracks[0].enabled == True
    assert mkv.audio_tracks[0].default == True
    assert mkv.audio_tracks[0].forced == False
    assert mkv.audio_tracks[0].lacing == True
    assert mkv.audio_tracks[0].codec_id == "A_MPEG/L3"
    assert mkv.audio_tracks[0].codec_name is None
    assert mkv.audio_tracks[0].sampling_frequency == 48000.0
    assert mkv.audio_tracks[0].channels == 2
    assert mkv.audio_tracks[0].output_sampling_frequency is None
    assert mkv.audio_tracks[0].bit_depth is None
    # subtitle track
    assert len(mkv.subtitle_tracks) == 0
    # chapters
    assert len(mkv.chapters) == 0
    # tags
    assert len(mkv.tags) == 1
    assert len(mkv.tags[0].simpletags) == 3
    assert mkv.tags[0].simpletags[0].name == "TITLE"
    assert mkv.tags[0].simpletags[0].default == True
    assert mkv.tags[0].simpletags[0].language == "und"
    assert mkv.tags[0].simpletags[0].string == "Big Buck Bunny - test 1"
    assert mkv.tags[0].simpletags[0].binary is None
    assert mkv.tags[0].simpletags[1].name == "DATE_RELEASED"
    assert mkv.tags[0].simpletags[1].default == True
    assert mkv.tags[0].simpletags[1].language == "und"
    assert mkv.tags[0].simpletags[1].string == "2010"
    assert mkv.tags[0].simpletags[1].binary is None
    assert mkv.tags[0].simpletags[2].name == "COMMENT"
    assert mkv.tags[0].simpletags[2].default == True
    assert mkv.tags[0].simpletags[2].language == "und"
    assert mkv.tags[0].simpletags[2].string == "Matroska Validation File1, basic MPEG4.2 and MP3 with only SimpleBlock"
    assert mkv.tags[0].simpletags[2].binary is None


def test_test2(data_files):
    with io.open(os.path.join(DATA_DIR, "test2.mkv"), "rb") as stream:
        mkv = MKV(stream)
    # info
    assert mkv.info.title is None
    assert mkv.info.duration == timedelta(seconds=47, milliseconds=509)
    assert mkv.info.date_utc == datetime(2011, 6, 2, 12, 45, 20)
    assert mkv.info.muxing_app == "libebml2 v0.21.0 + libmatroska2 v0.22.1"
    assert (
        mkv.info.writing_app
        == "mkclean 0.8.3 ru from libebml2 v0.10.0 + libmatroska2 v0.10.1 + mkclean 0.5.5 ru from libebml v1.0.0 + libmatroska v1.0.0 + mkvmerge v4.1.1 ('Bouncin' Back') built on Jul  3 2010 22:54:08"
    )
    # video track
    assert len(mkv.video_tracks) == 1
    assert mkv.video_tracks[0].type == VIDEO_TRACK
    assert mkv.video_tracks[0].number == 1
    assert mkv.video_tracks[0].name is None
    assert mkv.video_tracks[0].language == "und"
    assert mkv.video_tracks[0].enabled == True
    assert mkv.video_tracks[0].default == True
    assert mkv.video_tracks[0].forced == False
    assert mkv.video_tracks[0].lacing == False
    assert mkv.video_tracks[0].codec_id == "V_MPEG4/ISO/AVC"
    assert mkv.video_tracks[0].codec_name is None
    assert mkv.video_tracks[0].width == 1024
    assert mkv.video_tracks[0].height == 576
    assert mkv.video_tracks[0].interlaced == False
    assert mkv.video_tracks[0].stereo_mode is None
    assert mkv.video_tracks[0].crop == {}
    assert mkv.video_tracks[0].display_width == 1354
    assert mkv.video_tracks[0].display_height is None
    assert mkv.video_tracks[0].display_unit is None
    assert mkv.video_tracks[0].aspect_ratio_type is None
    # audio track
    assert len(mkv.audio_tracks) == 1
    assert mkv.audio_tracks[0].type == AUDIO_TRACK
    assert mkv.audio_tracks[0].number == 2
    assert mkv.audio_tracks[0].name is None
    assert mkv.audio_tracks[0].language == "und"
    assert mkv.audio_tracks[0].enabled == True
    assert mkv.audio_tracks[0].default == True
    assert mkv.audio_tracks[0].forced == False
    assert mkv.audio_tracks[0].lacing == True
    assert mkv.audio_tracks[0].codec_id == "A_AAC"
    assert mkv.audio_tracks[0].codec_name is None
    assert mkv.audio_tracks[0].sampling_frequency == 48000.0
    assert mkv.audio_tracks[0].channels == 2
    assert mkv.audio_tracks[0].output_sampling_frequency is None
    assert mkv.audio_tracks[0].bit_depth is None
    # subtitle track
    assert len(mkv.subtitle_tracks) == 0
    # chapters
    assert len(mkv.chapters) == 0
    # tags
    assert len(mkv.tags) == 1
    assert len(mkv.tags[0].simpletags) == 3
    assert mkv.tags[0].simpletags[0].name == "TITLE"
    assert mkv.tags[0].simpletags[0].default == True
    assert mkv.tags[0].simpletags[0].language == "und"
    assert mkv.tags[0].simpletags[0].string == "Elephant Dream - test 2"
    assert mkv.tags[0].simpletags[0].binary is None
    assert mkv.tags[0].simpletags[1].name == "DATE_RELEASED"
    assert mkv.tags[0].simpletags[1].default == True
    assert mkv.tags[0].simpletags[1].language == "und"
    assert mkv.tags[0].simpletags[1].string == "2010"
    assert mkv.tags[0].simpletags[1].binary is None
    assert mkv.tags[0].simpletags[2].name == "COMMENT"
    assert mkv.tags[0].simpletags[2].default == True
    assert mkv.tags[0].simpletags[2].language == "und"
    assert (
        mkv.tags[0].simpletags[2].string
        == "Matroska Validation File 2, 100,000 timecode scale, odd aspect ratio, and CRC-32. Codecs are AVC and AAC"
    )
    assert mkv.tags[0].simpletags[2].binary is None


def test_test3(data_files):
    with io.open(os.path.join(DATA_DIR, "test3.mkv"), "rb") as stream:
        mkv = MKV(stream)
    # info
    assert mkv.info.title is None
    assert mkv.info.duration == timedelta(seconds=49, milliseconds=64)
    assert mkv.info.date_utc == datetime(2010, 8, 21, 21, 43, 25)
    assert mkv.info.muxing_app == "libebml2 v0.11.0 + libmatroska2 v0.10.1"
    assert (
        mkv.info.writing_app
        == "mkclean 0.5.5 ro from libebml v1.0.0 + libmatroska v1.0.0 + mkvmerge v4.1.1 ('Bouncin' Back') built on Jul  3 2010 22:54:08"
    )
    # video track
    assert len(mkv.video_tracks) == 1
    assert mkv.video_tracks[0].type == VIDEO_TRACK
    assert mkv.video_tracks[0].number == 1
    assert mkv.video_tracks[0].name is None
    assert mkv.video_tracks[0].language == "und"
    assert mkv.video_tracks[0].enabled == True
    assert mkv.video_tracks[0].default == True
    assert mkv.video_tracks[0].forced == False
    assert mkv.video_tracks[0].lacing == False
    assert mkv.video_tracks[0].codec_id == "V_MPEG4/ISO/AVC"
    assert mkv.video_tracks[0].codec_name is None
    assert mkv.video_tracks[0].width == 1024
    assert mkv.video_tracks[0].height == 576
    assert mkv.video_tracks[0].interlaced == False
    assert mkv.video_tracks[0].stereo_mode is None
    assert mkv.video_tracks[0].crop == {}
    assert mkv.video_tracks[0].display_width is None
    assert mkv.video_tracks[0].display_height is None
    assert mkv.video_tracks[0].display_unit is None
    assert mkv.video_tracks[0].aspect_ratio_type is None
    # audio track
    assert len(mkv.audio_tracks) == 1
    assert mkv.audio_tracks[0].type == AUDIO_TRACK
    assert mkv.audio_tracks[0].number == 2
    assert mkv.audio_tracks[0].name is None
    assert mkv.audio_tracks[0].language is None
    assert mkv.audio_tracks[0].enabled == True
    assert mkv.audio_tracks[0].default == True
    assert mkv.audio_tracks[0].forced == False
    assert mkv.audio_tracks[0].lacing == True
    assert mkv.audio_tracks[0].codec_id == "A_MPEG/L3"
    assert mkv.audio_tracks[0].codec_name is None
    assert mkv.audio_tracks[0].sampling_frequency == 48000.0
    assert mkv.audio_tracks[0].channels == 2
    assert mkv.audio_tracks[0].output_sampling_frequency is None
    assert mkv.audio_tracks[0].bit_depth is None
    # subtitle track
    assert len(mkv.subtitle_tracks) == 0
    # chapters
    assert len(mkv.chapters) == 0
    # tags
    assert len(mkv.tags) == 1
    assert len(mkv.tags[0].simpletags) == 3
    assert mkv.tags[0].simpletags[0].name == "TITLE"
    assert mkv.tags[0].simpletags[0].default == True
    assert mkv.tags[0].simpletags[0].language == "und"
    assert mkv.tags[0].simpletags[0].string == "Elephant Dream - test 3"
    assert mkv.tags[0].simpletags[0].binary is None
    assert mkv.tags[0].simpletags[1].name == "DATE_RELEASED"
    assert mkv.tags[0].simpletags[1].default == True
    assert mkv.tags[0].simpletags[1].language == "und"
    assert mkv.tags[0].simpletags[1].string == "2010"
    assert mkv.tags[0].simpletags[1].binary is None
    assert mkv.tags[0].simpletags[2].name == "COMMENT"
    assert mkv.tags[0].simpletags[2].default == True
    assert mkv.tags[0].simpletags[2].language == "und"
    assert (
        mkv.tags[0].simpletags[2].string
        == "Matroska Validation File 3, header stripping on the video track and no SimpleBlock"
    )
    assert mkv.tags[0].simpletags[2].binary is None


def test_test5(data_files):
    with io.open(os.path.join(DATA_DIR, "test5.mkv"), "rb") as stream:
        mkv = MKV(stream)
    # info
    assert mkv.info.title is None
    assert mkv.info.duration == timedelta(seconds=46, milliseconds=665)
    assert mkv.info.date_utc == datetime(2010, 8, 21, 18, 6, 43)
    assert mkv.info.muxing_app == "libebml v1.0.0 + libmatroska v1.0.0"
    assert mkv.info.writing_app == "mkvmerge v4.0.0 ('The Stars were mine') built on Jun  6 2010 16:18:42"
    # video track
    assert len(mkv.video_tracks) == 1
    assert mkv.video_tracks[0].type == VIDEO_TRACK
    assert mkv.video_tracks[0].number == 1
    assert mkv.video_tracks[0].name is None
    assert mkv.video_tracks[0].language == "und"
    assert mkv.video_tracks[0].enabled == True
    assert mkv.video_tracks[0].default == True
    assert mkv.video_tracks[0].forced == False
    assert mkv.video_tracks[0].lacing == False
    assert mkv.video_tracks[0].codec_id == "V_MPEG4/ISO/AVC"
    assert mkv.video_tracks[0].codec_name is None
    assert mkv.video_tracks[0].width == 1024
    assert mkv.video_tracks[0].height == 576
    assert mkv.video_tracks[0].interlaced == False
    assert mkv.video_tracks[0].stereo_mode is None
    assert mkv.video_tracks[0].crop == {}
    assert mkv.video_tracks[0].display_width == 1024
    assert mkv.video_tracks[0].display_height == 576
    assert mkv.video_tracks[0].display_unit is None
    assert mkv.video_tracks[0].aspect_ratio_type is None
    # audio tracks
    assert len(mkv.audio_tracks) == 2
    assert mkv.audio_tracks[0].type == AUDIO_TRACK
    assert mkv.audio_tracks[0].number == 2
    assert mkv.audio_tracks[0].name is None
    assert mkv.audio_tracks[0].language == "und"
    assert mkv.audio_tracks[0].enabled == True
    assert mkv.audio_tracks[0].default == True
    assert mkv.audio_tracks[0].forced == False
    assert mkv.audio_tracks[0].lacing == True
    assert mkv.audio_tracks[0].codec_id == "A_AAC"
    assert mkv.audio_tracks[0].codec_name is None
    assert mkv.audio_tracks[0].sampling_frequency == 48000.0
    assert mkv.audio_tracks[0].channels == 2
    assert mkv.audio_tracks[0].output_sampling_frequency is None
    assert mkv.audio_tracks[0].bit_depth is None
    assert mkv.audio_tracks[1].type == AUDIO_TRACK
    assert mkv.audio_tracks[1].number == 10
    assert mkv.audio_tracks[1].name == "Commentary"
    assert mkv.audio_tracks[1].language is None
    assert mkv.audio_tracks[1].enabled == True
    assert mkv.audio_tracks[1].default == False
    assert mkv.audio_tracks[1].forced == False
    assert mkv.audio_tracks[1].lacing == True
    assert mkv.audio_tracks[1].codec_id == "A_AAC"
    assert mkv.audio_tracks[1].codec_name is None
    assert mkv.audio_tracks[1].sampling_frequency == 22050.0
    assert mkv.audio_tracks[1].channels == 1
    assert mkv.audio_tracks[1].output_sampling_frequency == 44100.0
    assert mkv.audio_tracks[1].bit_depth is None
    # subtitle track
    assert len(mkv.subtitle_tracks) == 8
    assert mkv.subtitle_tracks[0].type == SUBTITLE_TRACK
    assert mkv.subtitle_tracks[0].number == 3
    assert mkv.subtitle_tracks[0].name is None
    assert mkv.subtitle_tracks[0].language is None
    assert mkv.subtitle_tracks[0].enabled == True
    assert mkv.subtitle_tracks[0].default == True
    assert mkv.subtitle_tracks[0].forced == False
    assert mkv.subtitle_tracks[0].lacing == False
    assert mkv.subtitle_tracks[0].codec_id == "S_TEXT/UTF8"
    assert mkv.subtitle_tracks[0].codec_name is None
    assert mkv.subtitle_tracks[1].type == SUBTITLE_TRACK
    assert mkv.subtitle_tracks[1].number == 4
    assert mkv.subtitle_tracks[1].name is None
    assert mkv.subtitle_tracks[1].language == "hun"
    assert mkv.subtitle_tracks[1].enabled == True
    assert mkv.subtitle_tracks[1].default == False
    assert mkv.subtitle_tracks[1].forced == False
    assert mkv.subtitle_tracks[1].lacing == False
    assert mkv.subtitle_tracks[1].codec_id == "S_TEXT/UTF8"
    assert mkv.subtitle_tracks[1].codec_name is None
    assert mkv.subtitle_tracks[2].type == SUBTITLE_TRACK
    assert mkv.subtitle_tracks[2].number == 5
    assert mkv.subtitle_tracks[2].name is None
    assert mkv.subtitle_tracks[2].language == "ger"
    assert mkv.subtitle_tracks[2].enabled == True
    assert mkv.subtitle_tracks[2].default == False
    assert mkv.subtitle_tracks[2].forced == False
    assert mkv.subtitle_tracks[2].lacing == False
    assert mkv.subtitle_tracks[2].codec_id == "S_TEXT/UTF8"
    assert mkv.subtitle_tracks[2].codec_name is None
    assert mkv.subtitle_tracks[3].type == SUBTITLE_TRACK
    assert mkv.subtitle_tracks[3].number == 6
    assert mkv.subtitle_tracks[3].name is None
    assert mkv.subtitle_tracks[3].language == "fre"
    assert mkv.subtitle_tracks[3].enabled == True
    assert mkv.subtitle_tracks[3].default == False
    assert mkv.subtitle_tracks[3].forced == False
    assert mkv.subtitle_tracks[3].lacing == False
    assert mkv.subtitle_tracks[3].codec_id == "S_TEXT/UTF8"
    assert mkv.subtitle_tracks[3].codec_name is None
    assert mkv.subtitle_tracks[4].type == SUBTITLE_TRACK
    assert mkv.subtitle_tracks[4].number == 8
    assert mkv.subtitle_tracks[4].name is None
    assert mkv.subtitle_tracks[4].language == "spa"
    assert mkv.subtitle_tracks[4].enabled == True
    assert mkv.subtitle_tracks[4].default == False
    assert mkv.subtitle_tracks[4].forced == False
    assert mkv.subtitle_tracks[4].lacing == False
    assert mkv.subtitle_tracks[4].codec_id == "S_TEXT/UTF8"
    assert mkv.subtitle_tracks[4].codec_name is None
    assert mkv.subtitle_tracks[5].type == SUBTITLE_TRACK
    assert mkv.subtitle_tracks[5].number == 9
    assert mkv.subtitle_tracks[5].name is None
    assert mkv.subtitle_tracks[5].language == "ita"
    assert mkv.subtitle_tracks[5].enabled == True
    assert mkv.subtitle_tracks[5].default == False
    assert mkv.subtitle_tracks[5].forced == False
    assert mkv.subtitle_tracks[5].lacing == False
    assert mkv.subtitle_tracks[5].codec_id == "S_TEXT/UTF8"
    assert mkv.subtitle_tracks[5].codec_name is None
    assert mkv.subtitle_tracks[6].type == SUBTITLE_TRACK
    assert mkv.subtitle_tracks[6].number == 11
    assert mkv.subtitle_tracks[6].name is None
    assert mkv.subtitle_tracks[6].language == "jpn"
    assert mkv.subtitle_tracks[6].enabled == True
    assert mkv.subtitle_tracks[6].default == False
    assert mkv.subtitle_tracks[6].forced == False
    assert mkv.subtitle_tracks[6].lacing == False
    assert mkv.subtitle_tracks[6].codec_id == "S_TEXT/UTF8"
    assert mkv.subtitle_tracks[6].codec_name is None
    assert mkv.subtitle_tracks[7].type == SUBTITLE_TRACK
    assert mkv.subtitle_tracks[7].number == 7
    assert mkv.subtitle_tracks[7].name is None
    assert mkv.subtitle_tracks[7].language == "und"
    assert mkv.subtitle_tracks[7].enabled == True
    assert mkv.subtitle_tracks[7].default == False
    assert mkv.subtitle_tracks[7].forced == False
    assert mkv.subtitle_tracks[7].lacing == False
    assert mkv.subtitle_tracks[7].codec_id == "S_TEXT/UTF8"
    assert mkv.subtitle_tracks[7].codec_name is None
    # chapters
    assert len(mkv.chapters) == 0
    # tags
    assert len(mkv.tags) == 1
    assert len(mkv.tags[0].simpletags) == 3
    assert mkv.tags[0].simpletags[0].name == "TITLE"
    assert mkv.tags[0].simpletags[0].default == True
    assert mkv.tags[0].simpletags[0].language == "und"
    assert mkv.tags[0].simpletags[0].string == "Big Buck Bunny - test 8"
    assert mkv.tags[0].simpletags[0].binary is None
    assert mkv.tags[0].simpletags[1].name == "DATE_RELEASED"
    assert mkv.tags[0].simpletags[1].default == True
    assert mkv.tags[0].simpletags[1].language == "und"
    assert mkv.tags[0].simpletags[1].string == "2010"
    assert mkv.tags[0].simpletags[1].binary is None
    assert mkv.tags[0].simpletags[2].name == "COMMENT"
    assert mkv.tags[0].simpletags[2].default == True
    assert mkv.tags[0].simpletags[2].language == "und"
    assert (
        mkv.tags[0].simpletags[2].string
        == "Matroska Validation File 8, secondary audio commentary track, misc subtitle tracks"
    )
    assert mkv.tags[0].simpletags[2].binary is None


def test_test6(data_files):
    with io.open(os.path.join(DATA_DIR, "test6.mkv"), "rb") as stream:
        mkv = MKV(stream)
    # info
    assert mkv.info.title is None
    assert mkv.info.duration == timedelta(seconds=87, milliseconds=336)
    assert mkv.info.date_utc == datetime(2010, 8, 21, 16, 31, 55)
    assert mkv.info.muxing_app == "libebml2 v0.10.1 + libmatroska2 v0.10.1"
    assert (
        mkv.info.writing_app
        == "mkclean 0.5.5 r from libebml v1.0.0 + libmatroska v1.0.0 + mkvmerge v4.0.0 ('The Stars were mine') built on Jun  6 2010 16:18:42"
    )
    # video track
    assert len(mkv.video_tracks) == 1
    assert mkv.video_tracks[0].type == VIDEO_TRACK
    assert mkv.video_tracks[0].number == 1
    assert mkv.video_tracks[0].name is None
    assert mkv.video_tracks[0].language == "und"
    assert mkv.video_tracks[0].enabled == True
    assert mkv.video_tracks[0].default == False
    assert mkv.video_tracks[0].forced == False
    assert mkv.video_tracks[0].lacing == False
    assert mkv.video_tracks[0].codec_id == "V_MS/VFW/FOURCC"
    assert mkv.video_tracks[0].codec_name is None
    assert mkv.video_tracks[0].width == 854
    assert mkv.video_tracks[0].height == 480
    assert mkv.video_tracks[0].interlaced == False
    assert mkv.video_tracks[0].stereo_mode is None
    assert mkv.video_tracks[0].crop == {}
    assert mkv.video_tracks[0].display_width is None
    assert mkv.video_tracks[0].display_height is None
    assert mkv.video_tracks[0].display_unit is None
    assert mkv.video_tracks[0].aspect_ratio_type is None
    # audio track
    assert len(mkv.audio_tracks) == 1
    assert mkv.audio_tracks[0].type == AUDIO_TRACK
    assert mkv.audio_tracks[0].number == 2
    assert mkv.audio_tracks[0].name is None
    assert mkv.audio_tracks[0].language == "und"
    assert mkv.audio_tracks[0].enabled == True
    assert mkv.audio_tracks[0].default == False
    assert mkv.audio_tracks[0].forced == False
    assert mkv.audio_tracks[0].lacing == True
    assert mkv.audio_tracks[0].codec_id == "A_MPEG/L3"
    assert mkv.audio_tracks[0].codec_name is None
    assert mkv.audio_tracks[0].sampling_frequency == 48000.0
    assert mkv.audio_tracks[0].channels == 2
    assert mkv.audio_tracks[0].output_sampling_frequency is None
    assert mkv.audio_tracks[0].bit_depth is None
    # subtitle track
    assert len(mkv.subtitle_tracks) == 0
    # chapters
    assert len(mkv.chapters) == 0
    # tags
    assert len(mkv.tags) == 1
    assert len(mkv.tags[0].simpletags) == 3
    assert mkv.tags[0].simpletags[0].name == "TITLE"
    assert mkv.tags[0].simpletags[0].default == True
    assert mkv.tags[0].simpletags[0].language == "und"
    assert mkv.tags[0].simpletags[0].string == "Big Buck Bunny - test 6"
    assert mkv.tags[0].simpletags[0].binary is None
    assert mkv.tags[0].simpletags[1].name == "DATE_RELEASED"
    assert mkv.tags[0].simpletags[1].default == True
    assert mkv.tags[0].simpletags[1].language == "und"
    assert mkv.tags[0].simpletags[1].string == "2010"
    assert mkv.tags[0].simpletags[1].binary is None
    assert mkv.tags[0].simpletags[2].name == "COMMENT"
    assert mkv.tags[0].simpletags[2].default == True
    assert mkv.tags[0].simpletags[2].language == "und"
    assert (
        mkv.tags[0].simpletags[2].string
        == "Matroska Validation File 6, random length to code the size of Clusters and Blocks, no Cues for seeking"
    )
    assert mkv.tags[0].simpletags[2].binary is None


def test_test7(data_files):
    with io.open(os.path.join(DATA_DIR, "test7.mkv"), "rb") as stream:
        mkv = MKV(stream)
    # info
    assert mkv.info.title is None
    assert mkv.info.duration == timedelta(seconds=37, milliseconds=43)
    assert mkv.info.date_utc == datetime(2010, 8, 21, 17, 0, 23)
    assert mkv.info.muxing_app == "libebml2 v0.10.1 + libmatroska2 v0.10.1"
    assert (
        mkv.info.writing_app
        == "mkclean 0.5.5 r from libebml v1.0.0 + libmatroska v1.0.0 + mkvmerge v4.0.0 ('The Stars were mine') built on Jun  6 2010 16:18:42"
    )
    # video track
    assert len(mkv.video_tracks) == 1
    assert mkv.video_tracks[0].type == VIDEO_TRACK
    assert mkv.video_tracks[0].number == 1
    assert mkv.video_tracks[0].name is None
    assert mkv.video_tracks[0].language == "und"
    assert mkv.video_tracks[0].enabled == True
    assert mkv.video_tracks[0].default == False
    assert mkv.video_tracks[0].forced == False
    assert mkv.video_tracks[0].lacing == False
    assert mkv.video_tracks[0].codec_id == "V_MPEG4/ISO/AVC"
    assert mkv.video_tracks[0].codec_name is None
    assert mkv.video_tracks[0].width == 1024
    assert mkv.video_tracks[0].height == 576
    assert mkv.video_tracks[0].interlaced == False
    assert mkv.video_tracks[0].stereo_mode is None
    assert mkv.video_tracks[0].crop == {}
    assert mkv.video_tracks[0].display_width is None
    assert mkv.video_tracks[0].display_height is None
    assert mkv.video_tracks[0].display_unit is None
    assert mkv.video_tracks[0].aspect_ratio_type is None
    # audio track
    assert len(mkv.audio_tracks) == 1
    assert mkv.audio_tracks[0].type == AUDIO_TRACK
    assert mkv.audio_tracks[0].number == 2
    assert mkv.audio_tracks[0].name is None
    assert mkv.audio_tracks[0].language == "und"
    assert mkv.audio_tracks[0].enabled == True
    assert mkv.audio_tracks[0].default == False
    assert mkv.audio_tracks[0].forced == False
    assert mkv.audio_tracks[0].lacing == True
    assert mkv.audio_tracks[0].codec_id == "A_AAC"
    assert mkv.audio_tracks[0].codec_name is None
    assert mkv.audio_tracks[0].sampling_frequency == 48000.0
    assert mkv.audio_tracks[0].channels == 2
    assert mkv.audio_tracks[0].output_sampling_frequency is None
    assert mkv.audio_tracks[0].bit_depth is None
    # subtitle track
    assert len(mkv.subtitle_tracks) == 0
    # chapters
    assert len(mkv.chapters) == 0
    # tags
    assert len(mkv.tags) == 1
    assert len(mkv.tags[0].simpletags) == 3
    assert mkv.tags[0].simpletags[0].name == "TITLE"
    assert mkv.tags[0].simpletags[0].default == True
    assert mkv.tags[0].simpletags[0].language == "und"
    assert mkv.tags[0].simpletags[0].string == "Big Buck Bunny - test 7"
    assert mkv.tags[0].simpletags[0].binary is None
    assert mkv.tags[0].simpletags[1].name == "DATE_RELEASED"
    assert mkv.tags[0].simpletags[1].default == True
    assert mkv.tags[0].simpletags[1].language == "und"
    assert mkv.tags[0].simpletags[1].string == "2010"
    assert mkv.tags[0].simpletags[1].binary is None
    assert mkv.tags[0].simpletags[2].name == "COMMENT"
    assert mkv.tags[0].simpletags[2].default == True
    assert mkv.tags[0].simpletags[2].language == "und"
    assert (
        mkv.tags[0].simpletags[2].string
        == "Matroska Validation File 7, junk elements are present at the beggining or end of clusters, the parser should skip it. There is also a damaged element at 451418"
    )
    assert mkv.tags[0].simpletags[2].binary is None


def test_test8(data_files):
    with io.open(os.path.join(DATA_DIR, "test8.mkv"), "rb") as stream:
        mkv = MKV(stream)
    # info
    assert mkv.info.title is None
    assert mkv.info.duration == timedelta(seconds=47, milliseconds=341)
    assert mkv.info.date_utc == datetime(2010, 8, 21, 17, 22, 14)
    assert mkv.info.muxing_app == "libebml2 v0.10.1 + libmatroska2 v0.10.1"
    assert (
        mkv.info.writing_app
        == "mkclean 0.5.5 r from libebml v1.0.0 + libmatroska v1.0.0 + mkvmerge v4.0.0 ('The Stars were mine') built on Jun  6 2010 16:18:42"
    )
    # video track
    assert len(mkv.video_tracks) == 1
    assert mkv.video_tracks[0].type == VIDEO_TRACK
    assert mkv.video_tracks[0].number == 1
    assert mkv.video_tracks[0].name is None
    assert mkv.video_tracks[0].language == "und"
    assert mkv.video_tracks[0].enabled == True
    assert mkv.video_tracks[0].default == False
    assert mkv.video_tracks[0].forced == False
    assert mkv.video_tracks[0].lacing == False
    assert mkv.video_tracks[0].codec_id == "V_MPEG4/ISO/AVC"
    assert mkv.video_tracks[0].codec_name is None
    assert mkv.video_tracks[0].width == 1024
    assert mkv.video_tracks[0].height == 576
    assert mkv.video_tracks[0].interlaced == False
    assert mkv.video_tracks[0].stereo_mode is None
    assert mkv.video_tracks[0].crop == {}
    assert mkv.video_tracks[0].display_width is None
    assert mkv.video_tracks[0].display_height is None
    assert mkv.video_tracks[0].display_unit is None
    assert mkv.video_tracks[0].aspect_ratio_type is None
    # audio track
    assert len(mkv.audio_tracks) == 1
    assert mkv.audio_tracks[0].type == AUDIO_TRACK
    assert mkv.audio_tracks[0].number == 2
    assert mkv.audio_tracks[0].name is None
    assert mkv.audio_tracks[0].language == "und"
    assert mkv.audio_tracks[0].enabled == True
    assert mkv.audio_tracks[0].default == False
    assert mkv.audio_tracks[0].forced == False
    assert mkv.audio_tracks[0].lacing == True
    assert mkv.audio_tracks[0].codec_id == "A_AAC"
    assert mkv.audio_tracks[0].codec_name is None
    assert mkv.audio_tracks[0].sampling_frequency == 48000.0
    assert mkv.audio_tracks[0].channels == 2
    assert mkv.audio_tracks[0].output_sampling_frequency is None
    assert mkv.audio_tracks[0].bit_depth is None
    # subtitle track
    assert len(mkv.subtitle_tracks) == 0
    # chapters
    assert len(mkv.chapters) == 0
    # tags
    assert len(mkv.tags) == 1
    assert len(mkv.tags[0].simpletags) == 3
    assert mkv.tags[0].simpletags[0].name == "TITLE"
    assert mkv.tags[0].simpletags[0].default == True
    assert mkv.tags[0].simpletags[0].language == "und"
    assert mkv.tags[0].simpletags[0].string == "Big Buck Bunny - test 8"
    assert mkv.tags[0].simpletags[0].binary is None
    assert mkv.tags[0].simpletags[1].name == "DATE_RELEASED"
    assert mkv.tags[0].simpletags[1].default == True
    assert mkv.tags[0].simpletags[1].language == "und"
    assert mkv.tags[0].simpletags[1].string == "2010"
    assert mkv.tags[0].simpletags[1].binary is None
    assert mkv.tags[0].simpletags[2].name == "COMMENT"
    assert mkv.tags[0].simpletags[2].default == True
    assert mkv.tags[0].simpletags[2].language == "und"
    assert (
        mkv.tags[0].simpletags[2].string
        == "Matroska Validation File 8, audio missing between timecodes 6.019s and 6.360s"
    )
    assert mkv.tags[0].simpletags[2].binary is None
