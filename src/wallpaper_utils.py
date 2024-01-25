from .parser import WallpaperElement, ColorShadingType, PictureOption

from typing import Optional
from pathlib import Path


XDG_DATA = Path('/usr/share')
USER_DATA = Path.home() / '.local/share'
HOST_XDG_DATA = Path('/run/host') / XDG_DATA.relative_to('/')

BACKGROUNDS_PATH = HOST_XDG_DATA / 'backgrounds'
GNOME_BACKGROUND_PROPERTIES_PATH = HOST_XDG_DATA / 'gnome-background-properties'
LANDSCAPES_FILE = USER_DATA / 'gnome-background-properties' / 'landscapes.xml'

LANDSCAPES_FILE.parent.mkdir(parents=True, exist_ok=True)
LANDSCAPES_FILE.touch(exist_ok=True)


def get_thumbnail_path(wallpaper: WallpaperElement) -> Optional[Path]:
    '''Generates a thumbnail for a wallpaper.'''

    if wallpaper.filename is None:
        return None

    return HOST_XDG_DATA / wallpaper.filename.relative_to(XDG_DATA)

def wallpaper_files() -> list[Path]:
    '''Returns a list of all wallpapers.'''

    paths = GNOME_BACKGROUND_PROPERTIES_PATH.glob('*.xml')

    return [path for path in paths if path != LANDSCAPES_FILE]

def new_wallpaper_gradient(
        name: str,
        primary_color: str,
        secondary_color: str
    ) -> WallpaperElement:
    '''Creates a new gradient wallpaper.'''

    return WallpaperElement(
        name=name,
        shade_type=ColorShadingType.VERTICAL,
        primary_color=primary_color,
        secondary_color=secondary_color,
    )

def new_wallpaper_image(name: str, image_path: Path) -> WallpaperElement:
    '''Creates a new image wallpaper.'''

    return WallpaperElement(
        name=name,
        filename=image_path,
        options=[PictureOption.ZOOM],
    )