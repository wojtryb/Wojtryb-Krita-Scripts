# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita


def toggle_layer_collapse() -> None:
    """
    Collapse or expand current group.

    If current node has no children, its parent is toggled instead.
    Collapsing a group activates it.
    Expanding a group activates its topmost child.
    """
    document = Krita.instance().activeDocument()
    active = document.activeNode()
    affected = active if active.childNodes() else active.parentNode()

    if affected == document.rootNode():
        return

    affected.setCollapsed(not affected.collapsed())
    if affected.collapsed():
        document.setActiveNode(affected)
    else:
        document.setActiveNode(affected.childNodes()[-1])

    document.refreshProjection()


# Execute the script only in "Scripter" or "Ten Scripts" plugins
if __name__ in ("__main__", "users_script"):
    toggle_layer_collapse()
