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

        # Start searching for the hidden layers in current scope
        groups: list[GroupLayer] = [document.activeNode().parentNode()]

        def remove_in_group(group: GroupLayer) -> None:
            for node in group.childNodes():
                if not node.visible():
                    node.remove()
                elif isinstance(node, GroupLayer):
                    # Visible group must be searched for hidden layers 
                    groups.append(node)

        while groups:
            remove_in_group(groups.pop())

        document.refreshProjection()

    @staticmethod
    def collapse_all_groups() -> None:
        document = Krita.instance().activeDocument()

        # start searching for groups in the top level
        groups: list[GroupLayer] = [document.rootNode()]

        def collapse_in_group(group: GroupLayer) -> None:
            for node in group.childNodes():
                if isinstance(node, GroupLayer):
                    node.setCollapsed(True)
                    groups.append(node)

        while groups:
            collapse_in_group(groups.pop())

    @staticmethod
    def project_to_layers_below():
        DUPLICATE_NAME = "_projection_to_merge"

        document = Krita.instance().activeDocument()
        root = document.activeNode().parentNode()
        nodes = root.childNodes()

        def duplicate(node):
            copy = node.duplicate()
            copy.setName(DUPLICATE_NAME)
            return copy

        projection = nodes[-1]
        projection_copy = duplicate(projection)

        def do_it(top, middle, bottom):
            document.setActiveNode(middle)
            Krita.instance().action('selectopaque_add').trigger()
            document.setActiveNode(top)
            Krita.instance().action('clear').trigger()
            Krita.instance().action('deselect').trigger()

            copy = duplicate(top)
            root.addChildNode(copy, bottom)

        Krita.instance().action('deselect').trigger()
        for i in range(2):
            do_it(nodes[-1], nodes[-2-i], nodes[-3-i])

        root.addChildNode(projection_copy, projection)
        projection.remove()

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
        create_action("Collapse All Groups", self.collapse_all_groups)
        create_action("Project To Layers Below", self.project_to_layers_below)

