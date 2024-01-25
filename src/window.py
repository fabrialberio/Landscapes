# window.py
#
# Copyright 2024 Fabrizio
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .parser import WallpaperElement, load_wallpapers
from .wallpaper_utils import LANDSCAPES_FILE, get_thumbnail_path, wallpaper_files

from gi.repository import Adw, Gtk


def update_pref_group(pref_group: Adw.PreferencesGroup, children: list[Gtk.Widget]):
    listbox = pref_group.get_first_child().get_last_child().get_first_child()

    listbox.remove_all()

    for child in children:
        pref_group.add(child)

class WallpaperThumbnail(Gtk.Box):
    '''
    A thumbnail widget for a wallpaper.
    
    Loads the image asynchronously and shows a spinner while loading to avoid
    blocking the UI.
    '''
    __gtype_name__ = 'LandscapeThumbnail'

    def __init__(self, wallpaper: WallpaperElement):
        super().__init__()

        image = Gtk.Image(
            file=get_thumbnail_path(wallpaper),
            pixel_size=96,
        )
        image.add_css_class('icon-dropshadow')

        super().append(image)

class WallapaperTile(Adw.ActionRow):
    __gtype_name__ = 'LandscapeTile'

    def __init__(self, wallpaper: WallpaperElement):
        super().__init__(
            title=wallpaper.name,
        )
        super().add_prefix(WallpaperThumbnail(wallpaper))


@Gtk.Template(resource_path='/io/github/fabrialberio/landscapes/ui/window.ui')
class Window(Adw.ApplicationWindow):
    __gtype_name__ = 'Window'

    pref_group_your_backgrounds = Gtk.Template.Child()
    pref_group_system_backgrounds = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        your_backgrounds = load_wallpapers(LANDSCAPES_FILE)
        system_backgrounds = []

        for file in wallpaper_files():
            system_backgrounds.extend(load_wallpapers(file))

        status_page_no_wallpapers = Adw.StatusPage(
            icon_name='document-open-symbolic',
            title='No backgrounds',
            height_request=200,
        )
        status_page_no_wallpapers.add_css_class('compact')

        if len(your_backgrounds) > 0:
            update_pref_group(self.pref_group_your_backgrounds, [
                WallapaperTile(wallpaper) for wallpaper in your_backgrounds
            ])
        else:
            update_pref_group(self.pref_group_your_backgrounds, [status_page_no_wallpapers])

        update_pref_group(self.pref_group_system_backgrounds, [
            WallapaperTile(wallpaper) for wallpaper in system_backgrounds
        ])
