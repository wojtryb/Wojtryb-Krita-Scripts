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


def project_to_layers_below() -> None:
    """
    Merge a projection of active layer to each underlying node in group.

    - Works only when active node is a visible, unlocked paint layer.
    - Affects visible layers below current one, inside the same group.
    - Goes out of the current group, if it is in pass-through mode.
    - Recursively goes inside the sub-groups.
    - Locked layers are not affected, but can cover layers underneath.

    NOTE: script results in deselecting the current selection.
    NOTE: script creates multiple entries in the undo stack.
          Undoing the script outcome can be impossible.
    NOTE: Settings > Configure Krita > General > Window > Show on-canvas
          popup settings must be on for displaying the script progress.
    """
    document = Krita.instance().activeDocument()
    active_node = document.activeNode()

    if type(active_node) is not Node \
            or not active_node.visible() \
            or active_node.locked():
        _display_popup("Current layer cannot be used as projection")
        return

    nodes = _find_nodes_below(active_node)

    to_merge: list[Node] = []

    def duplicate_projection_above(node: Node) -> None:
        if not node.locked():
            copy = active_node.duplicate()
            copy.setInheritAlpha(True)
            to_merge.append(copy)
            node.parentNode().addChildNode(copy, node)

        document.setActiveNode(node)
        Krita.instance().action('selectopaque').trigger()
        document.setActiveNode(active_node)
        document.waitForDone()
        Krita.instance().action('clear').trigger()
        document.waitForDone()
        Krita.instance().action('deselect').trigger()
        document.waitForDone()

    Krita.instance().action('deselect').trigger()

    for i, node in enumerate(reversed(nodes), 1):
        _display_popup(f"Creating layers: {i}/{len(nodes)}")
        duplicate_projection_above(node)

    for i, node in enumerate(to_merge, 1):
        _display_popup(f"Merging layers: {i}/{len(nodes)}")
        node.mergeDown()

    document.refreshProjection()
    _display_popup("Done!")


# Execute the script only in "Scripter" or "Ten Scripts" plugins
if __name__ in ("__main__", "users_script"):
    project_to_layers_below()
