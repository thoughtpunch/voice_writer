from mutagen import File as MutagenFile
from mutagen.m4a import M4A
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis


def is_m4a(file) -> bool:
    audio_file_format = file.name.split('.')[-1].upper()
    return isinstance(file, M4A) or audio_file_format == 'M4A'


def is_mp3(file) -> bool:
    audio_file_format = file.name.split('.')[-1].upper()
    return isinstance(file, MP3) or audio_file_format == 'MP3'


def is_ogg_or_flac(file) -> bool:
    audio_file_format = file.name.split('.')[-1].upper()
    instance_bool = isinstance(file, OggVorbis) or isinstance(file, FLAC)
    file_format_bool = audio_file_format == 'OGG' or audio_file_format == 'FLAC'
    return instance_bool or file_format_bool


# Extract audio metadata using the Mutagen library
def extract_audio_metadata_from_file(file) -> dict:
    audio = MutagenFile(file)
    audio_metadata_dict = {}

    # Basic audio file information
    audio_metadata_dict['file_name'] = file.name.split('/')[-1]
    audio_metadata_dict['format'] = file.name.split('.')[-1].upper().strip()
    audio_metadata_dict['file_size'] = file.size

    if audio and audio.info:
        audio_metadata_dict['duration_ms'] = audio.info.length * 1000
        audio_metadata_dict['bitrate_kbps'] = audio.info.bitrate // 1000  # Convert to kbps

        # Extract a human-readable dictionary of audio tags
        if is_m4a(file):
            lookup_dict = M4A_TAGS_DICT
        elif is_mp3(file):
            lookup_dict = MP3_TAGS_DICT
        elif is_ogg_or_flac(file):
            lookup_dict = FLAC_OGG_TAGS_DICT
        else:
            lookup_dict = {}

        # Human-readable Tags for supported formats
        if audio is not None and audio.tags is not None:
            for key, value in audio.tags.items():
                human_readable_key = lookup_dict.get(key, key)
                if isinstance(value, list):
                    audio_metadata_dict[human_readable_key] = list(str(v) for v in value)
                else:
                    audio_metadata_dict[human_readable_key] = str(value)

        # General stats
        for key, value in audio.info.__dict__.items():  # noqa
            audio_metadata_dict[key] = value
    else:
        raise Exception(f"Could not extract metadata from audio file: {str(audio_metadata_dict)}")

    return audio_metadata_dict


# LIST OF POSSIBLE M4A TAGS
M4A_TAGS_DICT = {
    "\xa9nam": "Title",
    "\xa9alb": "Album",
    "\xa9ART": "Artist",
    "\xa9wrt": "Composer",
    "\xa9day": "Release Date",
    "\xa9gen": "Genre",
    "\xa9trk": "Track Number",
    "\xa9too": "Encoder",
    "\xa9cmt": "Comment",
    "\xa9cpy": "Copyright",
    "\xa9lyr": "Lyrics",
    "\xa9grp": "Grouping",
    "\xa9des": "Description",
    "\xa9st3": "Sub-Title",
    "©nam": "Title",
    "©alb": "Album",
    "©ART": "Artist",
    "©wrt": "Composer",
    "©day": "Release Date",
    "©gen": "Genre",
    "©trk": "Track Number",
    "©too": "Encoder",
    "©cmt": "Comment",
    "©cpy": "Copyright",
    "©lyr": "Lyrics",
    "©grp": "Grouping",
    "©des": "Description",
    "©st3": "Sub-Title",
    "aART": "Album Artist",
    "covr": "Cover Art",
    "disk": "Disc Number",
    "cpil": "Compilation",
    "tmpo": "BPM",
    "stik": "Media Type",
    "purd": "Purchase Date",
    "purl": "Purchase URL",
    "pcst": "Podcast",
    "pgap": "Gapless Playback",
    "cnID": "iTunes Catalog ID",
    "atID": "Album/Artist ID",
    "plID": "Playlist ID",
    "geID": "Genre ID",
    "sfID": "Storefront ID",
    "rtng": "Content Rating",
    "egid": "Episode Global Unique ID",
    "tvnn": "TV Network Name",
    "tvsh": "TV Show Name",
    "tven": "TV Episode Number",
    "tvsn": "TV Season Number",
    "tvsp": "TV Episode Number",
    "desc": "Description",
    "ldes": "Long Description",
    "keyw": "Keywords"
}


MP3_TAGS_DICT = {
    "TIT2": "Title",
    "TALB": "Album",
    "TPE1": "Artist",
    "TPE2": "Album Artist",
    "TCON": "Genre",
    "TDRC": "Recording Date",
    "TRCK": "Track Number",
    "TPOS": "Disc Number",
    "COMM": "Comments",
    "TXXX": "User-defined Text",
    "WXXX": "User-defined URL",
    "TENC": "Encoded By",
    "USLT": "Lyrics",
    "APIC": "Cover Art",
    "TCOP": "Copyright",
    "TIT3": "Subtitle",
    "TKEY": "Initial Key",
    "TLEN": "Length (Duration)",
    "TSSE": "Software/Hardware and settings used for encoding",
    "TYER": "Year",  # Older versions of ID3
    "TDRL": "Release Time",
    "TPUB": "Publisher",
    "TIT1": "Content group description",
    "TPE3": "Conductor",
    "TEXT": "Lyricist/Text writer",
    "TORY": "Original release year",
    "TOPE": "Original artist/performer",
    "TOAL": "Original album/movie/show title",
    "TRDA": "Recording dates",
    "TSOP": "Performer sort order",
    "TSOT": "Title sort order"
}


FLAC_OGG_TAGS_DICT = {
    "TITLE": "Title",
    "ALBUM": "Album",
    "ARTIST": "Artist",
    "ALBUMARTIST": "Album Artist",
    "GENRE": "Genre",
    "DATE": "Date",
    "TRACKNUMBER": "Track Number",
    "DISCNUMBER": "Disc Number",
    "COMMENT": "Comment",
    "DESCRIPTION": "Description",
    "LYRICS": "Lyrics",
    "COMPOSER": "Composer",
    "COPYRIGHT": "Copyright",
    "ENCODER": "Encoder",
    "ORGANIZATION": "Organization",
    "PERFORMER": "Performer",
    "PUBLISHER": "Publisher",
    "ISRC": "International Standard Recording Code",
    "LICENSE": "License",
    "LOCATION": "Location",
    "CONTACT": "Contact",
    "REMEDIATION": "Remediation",
    "VENDOR": "Vendor",
    "VERSION": "Version",
    "ISRC": "International Standard Recording Code",
    "REPLAYGAIN_TRACK_GAIN": "ReplayGain Track Gain",
    "REPLAYGAIN_TRACK_PEAK": "ReplayGain Track Peak",
    "REPLAYGAIN_ALBUM_GAIN": "ReplayGain Album Gain",
    "REPLAYGAIN_ALBUM_PEAK": "ReplayGain Album Peak"
}