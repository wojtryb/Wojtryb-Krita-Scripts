# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita


def change_collapse_state() -> None:
    """(Un)collapse current node, or its parent when node has no children."""
    document = Krita.instance().activeDocument()
    active_node = document.activeNode()

    if active_node.childNodes():
        active_node.setCollapsed(not active_node.collapsed())
        return

    parent = active_node.parentNode()
    parent.setCollapsed(not parent.collapsed())

    document.refreshProjection()


# Execute the script only in "Scripter" or "Ten Scripts" plugins
if __name__ in ("__main__", "users_script"):
    change_collapse_state()
