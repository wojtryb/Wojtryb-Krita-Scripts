# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from krita import Krita, Extension, Window


class WojtrybKritaHelpers(Extension):
    """Krita extension being a collection of scripts used by wojtryb."""

    @staticmethod
    def backup_layer() -> None:
        """
        Creates a hidden backup of the current node.

        When current node is a group, original gets collapsed.
        Node above the backup gets shown and activated. 
        """
        document = Krita.instance().activeDocument()

        # create node duplicate above the original
        original = document.activeNode()
        duplicate = original.duplicate()
        original.parentNode().addChildNode(duplicate, original)

        # Collapse and hide the original, show the duplicate
        if original.type() == "grouplayer":
            original.setCollapsed(True)
        original.setVisible(False)
        duplicate.setVisible(True)

        document.refreshProjection()

    def setup(self) -> None:
        """Obligatory override."""

    def createActions(self, window: Window) -> None:
        """Create every plugin action."""
        def create_action(name: str, callback: Callable[[], None]):
            action = window.createAction(name, name, "tools/scripts")
            action.setAutoRepeat(False)
            action.triggered.connect(callback)
        
        create_action("Backup Layer", self.backup_layer)

