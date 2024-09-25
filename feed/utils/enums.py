from enum import Enum


class FeedContentTypes(Enum):
    TEXT_HTML = 'text/html'
    TEXT_XML = 'text/xml'
    APPLICATION_XML = 'application/xml'
    APPLICATION_XML_RSS = 'application/rss+xml'
    APPLICATION_XML_ATOM = 'application/atom+xml'


class AudioMimeTypes(Enum):
    AUDIO_MPEG = 'audio/mpeg'
    AUDIO_MP3 = 'audio/mp3'
    AUDIO_X_M4A = 'audio/x-m4a'


class VideoMimeTypes(Enum):
    VIDEO_MP4 = 'video/mp4'


class FeedMediaContentMediums(Enum):
    VIDEO = 'video'