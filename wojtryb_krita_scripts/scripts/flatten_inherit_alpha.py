# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from collections import deque

from krita import Krita, Node, GroupLayer


def _display_popup(message: str) -> None:
    """Display a message in top-left corner of screen."""
    view = Krita.instance().activeWindow().activeView()
    view.showFloatingMessage(
        message, Krita.instance().icon("merge-layer-below"), 3000, 1)


def _find_root(node: Node) -> Node:
    """Return a root of given node, considering pass-through mode."""
    root = node.parentNode()
    while type(root) is GroupLayer and root.passThroughMode():
        root = root.parentNode()
    return root


def _find_nodes_below(threshold: Node) -> list[Node]:
    """Return flattened list of visible nodes below given threshold."""
    root = _find_root(threshold)

    queue: deque[Node] = deque(root.childNodes())
    output: list[Node] = []

    while queue:
        node = queue.popleft()
        if node == threshold:
            break
        elif not node.visible():
            continue
        elif type(node) is Node:
            output.append(node)
        elif type(node) is GroupLayer:
            queue.extendleft(reversed(node.childNodes()))

    return output


def flatten_inherit_alpha() -> None:
    document = Krita.instance().activeDocument()
    active_node = document.activeNode()

    if type(active_node) is not Node \
            or not active_node.visible() \
            or active_node.locked():
        _display_popup("Current layer cannot be used as projection")
        return

    nodes = _find_nodes_below(active_node)

    Krita.instance().action('deselect').trigger()
    document.waitForDone()
    for node in nodes:
        document.setActiveNode(node)
        Krita.instance().action('selectopaque_add').trigger()

    document.setActiveNode(active_node)
    document.waitForDone()
    Krita.instance().action('invert_selection').trigger()
    document.waitForDone()
    Krita.instance().action('clear').trigger()
    document.waitForDone()
    Krita.instance().action('deselect').trigger()

    active_node.setInheritAlpha(False)

    document.refreshProjection()
    _display_popup("Done!")


# Execute the script only in "Scripter" or "Ten Scripts" plugins
if __name__ in ("__main__", "users_script"):
    flatten_inherit_alpha()
