# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita, Extension


class WojtrybKritaHelpers(Extension):
    """Krita extension being a collection of scripts used by wojtryb."""

    @staticmethod
    def backup_layer():
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

    def setup(self):
        """Obligatory override."""

    def createActions(self, window):
        """Create the action."""
        action = window.createAction(
            "Backup Layer", "Backup Layer", "tools/scripts")
        action.setAutoRepeat(False)
        action.triggered.connect(self.backup_layer)

