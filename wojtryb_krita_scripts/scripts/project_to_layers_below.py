# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from collections import deque

from krita import Krita, Node, GroupLayer


def _display_popup(message: str):
    view = Krita.instance().activeWindow().activeView()
    view.showFloatingMessage(
        message, Krita.instance().icon("merge-layer-below"), 3000, 1)


def _find_root(active_node: Node) -> Node:
    root = active_node.parentNode()
    while type(root) is GroupLayer and root.passThroughMode():
        root = root.parentNode()
    return root


def _find_nodes(active_node: Node) -> list[Node]:
    root = _find_root(active_node)

    queue: deque[Node] = deque(root.childNodes())
    output: list[Node] = []

    while queue:
        node = queue.popleft()
        if node == active_node:
            break
        elif not node.visible():
            continue
        elif type(node) is Node:
            output.append(node)
        elif type(node) is GroupLayer:
            queue.extendleft(reversed(node.childNodes()))

    return output


def project_to_layers_below() -> None:
    document = Krita.instance().activeDocument()
    active_node = document.activeNode()

    if type(active_node) is not Node \
            or not active_node.visible() \
            or active_node.locked():
        _display_popup("Current layer cannot be used as projection")
        return

    nodes = _find_nodes(active_node)

    to_merge: list[Node] = []

    def duplicate_projection_above(node: Node):
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
