# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita, Node


def project_to_layers_below() -> None:
    document = Krita.instance().activeDocument()
    root = document.activeNode().parentNode()
    nodes = root.childNodes()
    current_node = nodes[-1]

    to_merge: list[Node] = []

    def duplicate_projection_above(node: Node):
        copy = current_node.duplicate()
        to_merge.append(copy)
        root.addChildNode(copy, node)

        document.setActiveNode(node)
        Krita.instance().action('selectopaque_add').trigger()
        document.setActiveNode(current_node)
        Krita.instance().action('clear').trigger()
        Krita.instance().action('deselect').trigger()

    Krita.instance().action('deselect').trigger()
    for i in range(2):
        duplicate_projection_above(nodes[-2-i])

    for node in to_merge:
        node.mergeDown()

    document.refreshProjection()


# Execute the script only in "Scripter" or "Ten Scripts" plugins
if __name__ in ("__main__", "users_script"):
    project_to_layers_below()
