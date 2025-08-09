# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita, GroupLayer


def collapse_all_groups() -> None:
    document = Krita.instance().activeDocument()

    # start searching for groups in the top level
    groups: list[GroupLayer] = [document.rootNode()]

    def collapse_in_group(group: GroupLayer) -> None:
        for node in group.childNodes():
            if type(node) is GroupLayer:
                node.setCollapsed(True)
                groups.append(node)

    while groups:
        collapse_in_group(groups.pop())


# Execute the script only in "Scripter" or "Ten Scripts" plugins
if __name__ in ("__main__", "users_script"):
    collapse_all_groups()
