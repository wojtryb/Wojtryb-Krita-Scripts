# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita, Node, GroupLayer


def _find_root(active_node: Node) -> Node:
    root = active_node.parentNode()
    while isinstance(root, GroupLayer) and root.passThroughMode():
        root = root.parentNode()
    return root


def _find_nodes(active_node: Node, root: Node) -> list[Node]:
    def walk(root: Node) -> tuple[list[Node], bool]:
        output: list[Node] = []
        for node in root.childNodes():
            if node == active_node:
                return output, True
            if type(node) is Node:  # Paint layer, not its subclass
                output.append(node)
            elif isinstance(node, GroupLayer):
                nodes, is_end = walk(node)
                output.extend(nodes)
                if is_end:
                    return output, True
        return output, False

    nodes, _ = walk(root)
    return nodes


def project_to_layers_below() -> None:
    document = Krita.instance().activeDocument()
    active_node = document.activeNode()

    root = _find_root(active_node)
    nodes = _find_nodes(active_node, root)

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

    for node in reversed(nodes):
        duplicate_projection_above(node)

    for node in to_merge:
        node.mergeDown()

    document.refreshProjection()


# Execute the script only in "Scripter" or "Ten Scripts" plugins
if __name__ in ("__main__", "users_script"):
    project_to_layers_below()
