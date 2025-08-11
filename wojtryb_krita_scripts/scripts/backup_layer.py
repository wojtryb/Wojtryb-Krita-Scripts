# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita


def backup_layer() -> None:
    """
    Creates a hidden copy of the active layer below it.

    When current node is a group, original gets collapsed.
    Node above the backup gets shown and activated.
    """
    document = Krita.instance().activeDocument()

    # create node duplicate above the original
    original = document.activeNode()
    duplicate = original.duplicate()
    original.parentNode().addChildNode(duplicate, original)

    # Collapse and hide the original, show the duplicate
    if original.childNodes():
        original.setCollapsed(True)
    original.setVisible(False)
    duplicate.setVisible(True)

    document.refreshProjection()


# Execute the script only in "Scripter" or "Ten Scripts" plugins
if __name__ in ("__main__", "users_script"):
    backup_layer()
