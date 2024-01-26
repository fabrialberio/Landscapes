from .parser import WallpaperElement

from gi.repository import Adw, Gtk


class WallpaperPage(Gtk.Box):
    __gtype_name__ = 'WallpaperPage'

    wallpaper: WallpaperElement

    def __init__(self, wallpaper: WallpaperElement):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
        )

        self.wallpaper = wallpaper

        status_page = Adw.StatusPage(
            title=self.wallpaper.name,
            vexpand=True,
        )
        self.append(status_page)
