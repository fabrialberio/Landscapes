from xml.etree import ElementTree

from enum import StrEnum
from typing import Optional
from pathlib import Path
from dataclasses import dataclass, field


def load_wallpapers(xml_path: Path) -> list['WallpaperElement']:
    '''Parses an XML file into a list of WallpaperElement objects.'''

    xml = ElementTree.parse(xml_path).getroot()
    return [WallpaperElement.from_xml(e) for e in xml]

def dump_wallpapers(xml_path: Path, wallpapers: list['WallpaperElement']):
    '''Dumps a list of WallpaperElement objects into an XML file.'''

    element = ElementTree.Element('wallpapers')
    for wallpaper in wallpapers:
        element.append(wallpaper.to_xml())

    with open(xml_path, 'wb') as xml_file:
        xml_file.write(b'''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">
''')
        
        ElementTree.indent(element, space='    ')
        ElementTree.ElementTree(element).write(xml_file, xml_declaration=False)


class PictureOption(StrEnum):
    NONE =      'none'
    ZOOM =      'zoom'
    SCALED =    'scaled'
    SPANNED =   'spanned'
    CENTERED =  'centered'
    STRETCHED = 'streched'
    WALLPAPER = 'wallpaper'

class ColorShadingType(StrEnum):
    SOLID =      'solid'
    VERTICAL =   'vertical'
    HORIZONTAL = 'horizontal'


@dataclass
class WallpaperElement:
    name: str
    filename: Path
    filename_dark: Optional[Path] = None
    options: list[PictureOption] = field(default_factory=list)
    shade_type: Optional[ColorShadingType] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    deleted: Optional[bool] = None

    @classmethod
    def from_xml(cls, xml: ElementTree.Element):
        '''
        Parses an XML element into a WallpaperElement object.

        Assumes that if a tag is present, it is not empty
        '''

        name = xml.find('name').text or ''
        filename = Path(xml.find('filename').text)

        element = cls(name, filename)

        if (filename_dark_el := xml.find('filename-dark')) is not None:
            element.filename_dark = Path(filename_dark_el.text)

        for option_el in xml.findall('options'):
            element.options.append(PictureOption(option_el.text))

        if (shade_type_el := xml.find('shade_type')) is not None:
            element.shade_type = ColorShadingType(shade_type_el.text)

        if (primary_color_el := xml.find('pcolor')) is not None:
            element.primary_color = primary_color_el.text

        if (secondary_color_el := xml.find('scolor')) is not None:
            element.secondary_color = secondary_color_el.text

        if (deleted := xml.get('deleted')) is not None:
            element.deleted = deleted == 'true'

        return element

    def to_xml(self) -> ElementTree.Element:
        '''
        Converts a WallpaperElement object into an XML element.
        '''

        xml = ElementTree.Element('wallpaper')

        name_el = ElementTree.Element('name')
        name_el.text = self.name
        xml.append(name_el)

        filename_el = ElementTree.Element('filename')
        filename_el.text = str(self.filename)
        xml.append(filename_el)

        if self.filename_dark is not None:
            filename_dark_el = ElementTree.Element('filename-dark')
            filename_dark_el.text = str(self.filename_dark)
            xml.append(filename_dark_el)

        for option in self.options:
            option_el = ElementTree.Element('options')
            option_el.text = option
            xml.append(option_el)

        if self.shade_type is not None:
            shade_type_el = ElementTree.Element('shade_type')
            shade_type_el.text = self.shade_type
            xml.append(shade_type_el)

        if self.primary_color is not None:
            primary_color_el = ElementTree.Element('pcolor')
            primary_color_el.text = self.primary_color
            xml.append(primary_color_el)

        if self.secondary_color is not None:
            secondary_color_el = ElementTree.Element('scolor')
            secondary_color_el.text = self.secondary_color
            xml.append(secondary_color_el)

        if self.deleted is not None:
            xml.set('deleted', 'true' if self.deleted else 'false')

        return xml
