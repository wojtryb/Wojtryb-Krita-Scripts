# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from krita import Extension, Window

from .scripts import (
    backup_layer,
    project_to_layers_below,
    remove_hidden_layers,
    toggle_layer_collapse)


class WojtrybKritaScripts(Extension):
    """Krita extension being a collection of scripts used by wojtryb."""

    def setup(self) -> None:
        """Obligatory override."""

    def createActions(self, window: Window) -> None:
        """Create every plugin action."""
        def create_action(name: str, callback: Callable[[], None]):
            action = window.createAction(name, name, "tools/scripts")
            action.setAutoRepeat(False)
            action.triggered.connect(callback)

        create_action("Backup Layer", backup_layer)
        create_action("Project To Layers Below", project_to_layers_below)
        create_action("Remove Hidden Layers", remove_hidden_layers)
        create_action("Toggle Layer Collapse", toggle_layer_collapse)
