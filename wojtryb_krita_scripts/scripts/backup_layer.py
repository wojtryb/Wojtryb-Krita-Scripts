# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita


def backup_layer() -> None:
    """
    Creates a hidden copy of the active layer below it.

    When duplicated node is a group, backup gets collapsed.
    Node above the backup gets shown and remains activated.

    NOTE: it is not possible to affect multiple layers at once by
    selecting them with `ctrl` or `shift` in the layer stack.
    It can be achieved only by running the script on the group.
    """
    document = Krita.instance().activeDocument()

    original = document.activeNode()

    # Make sure the original is not visible
    if original.visible():
        Krita.instance().action("toggle_layer_visibility").trigger()
        document.waitForDone()

    # Create node duplicate above the original
    Krita.instance().action("duplicatelayer").trigger()
    document.waitForDone()

    # Find the duplicate created by action call
    parent = original.parentNode()
    children = parent.childNodes()
    index = children.index(original)
    duplicate = children[index+1]

    # Make the duplicate visible and rename it
    duplicate.setVisible(True)
    duplicate.setName(original.name())

    # Collapse the original
    if original.childNodes():
        original.setCollapsed(True)

    document.refreshProjection()


# Execute the script only in "Scripter" or "Ten Scripts" plugins
if __name__ in ("__main__", "users_script"):
    backup_layer()
