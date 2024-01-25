from .parser import WallpaperElement

from pathlib import Path


XDG_DATA = Path('/usr/share')
USER_DATA = Path.home() / '.local/share'
HOST_XDG_DATA = Path('/run/host') / XDG_DATA.relative_to('/')

BACKGROUNDS_PATH = HOST_XDG_DATA / 'backgrounds'
GNOME_BACKGROUND_PROPERTIES_PATH = HOST_XDG_DATA / 'gnome-background-properties'
LANDSCAPES_FILE = USER_DATA / 'gnome-background-properties' / 'landscapes.xml'

LANDSCAPES_FILE.parent.mkdir(parents=True, exist_ok=True)
LANDSCAPES_FILE.touch(exist_ok=True)


def get_thumbnail_path(wallpaper: WallpaperElement) -> Path:
    '''Generates a thumbnail for a wallpaper.'''

    return HOST_XDG_DATA / wallpaper.filename.relative_to(XDG_DATA)

def wallpaper_files() -> list[Path]:
    '''Returns a list of all wallpapers.'''

    paths = GNOME_BACKGROUND_PROPERTIES_PATH.glob('*.xml')

    return [path for path in paths if path != LANDSCAPES_FILE]
