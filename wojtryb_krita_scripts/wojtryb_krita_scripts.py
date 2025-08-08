# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from krita import Krita, Extension, Window, GroupLayer


class WojtrybKritaScripts(Extension):
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
        if isinstance(original, GroupLayer):
            original.setCollapsed(True)
        original.setVisible(False)
        duplicate.setVisible(True)

        document.refreshProjection()

    @staticmethod
    def remove_hidden_layers() -> None:
        """
        Remove all hidden layers in the group of active layer.

        - Hidden layers inside the subgroups are also removed.         
        - Running the script when active layer is not inside any group,
          results in removing all hidden layers in the document.
        """
        document = Krita.instance().activeDocument()
        parent = document.activeNode().parentNode()

        # Start searching for the hidden layers in current scope
        affected_groups: list[GroupLayer] = [parent]

        def remove_in_group(group: GroupLayer) -> None:
            for node in group.childNodes():
                print(type(node))
                if not node.visible():
                    node.remove()
                elif isinstance(node, GroupLayer):
                    # Visible group must be searched for hidden layers 
                    affected_groups.append(node)

        while affected_groups:
            remove_in_group(affected_groups.pop())

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
        create_action("Remove Hidden Layers", self.remove_hidden_layers)

