# main.py
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

from .window import Window

from gi.repository import Adw, Gio, Gtk
from gi import require_version

from sys import argv

require_version('Gtk', '4.0')
require_version('Adw', '1')


class Landscapes(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='io.github.fabrialberio.landscapes',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )

        self._create_action('quit', self._quit_action, ['<primary>q'])
        self._create_action('about', self._about_action)

    def do_activate(self):
        window = Window(application=self)
        window.present()

    def _about_action(self, action: Gio.SimpleAction, param: None):
        builder = Gtk.Builder.new_from_resource(
            '/io/github/fabrialberio/landscapes/ui/about-window.ui')

        about_window: Adw.AboutWindow = builder.get_object('about-window')
        about_window.set_transient_for(self.get_active_window())
        about_window.present()

    def _quit_action(self, action: Gio.SimpleAction, param: None):
        self.quit()

    def _create_action(self, name: str, callback, shortcuts=None, param=None):
        action = Gio.SimpleAction.new(name, param)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    app = Landscapes()
    return app.run(argv)
