
# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita, GroupLayer


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


# Execute the script only in "Scripter" or "Ten Scripts" plugins
if __name__ in ("__main__", "users_script"):
    remove_hidden_layers()
