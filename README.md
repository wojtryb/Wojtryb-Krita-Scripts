# Wojtryb Krita Scripts **v1.0.1**

[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![wojtryb youtube](https://img.shields.io/badge/YouTube-wojtryb-ee0000.svg?style=flat&logo=youtube)](https://youtube.com/wojtryb)
[![wojtryb portfolio](https://img.shields.io/badge/Art_Portfolio-wojtryb-000000.svg?style=flat&logo=)](https://cara.app/wojtryb)

---

Collection of miscellaneous scripts for painting application [**`Krita`**](https://krita.org/). They can be installed separately or as a single plugin.

The scripts available in this repository:
- [Project to layers below](#project-to-layers-below)
- [Backup layer](#backup-layer)
- [Remove hidden layers](#remove-hidden-layers)
- [Toggle layer collapse](#toggle-layer-collapse)

## Important links
> Download the [**`latest version`**](https://github.com/wojtryb/Wojtryb-Krita-Scripts/archive/refs/heads/main.zip) of the plugin, [**`pick a specific script`**](https://github.com/wojtryb/Wojtryb-Krita-Scripts/tree/main/wojtryb_krita_scripts/scripts) or visit its [**`github page`**](https://github.com/wojtryb/Wojtryb-Krita-Scripts).

## Requirements
- Version of krita on plugin release: **5.2.11**
- Required version of krita: **5.2.0** or later

OS support state:
- [x] Windows
- [x] Linux
- [X] MacOS
- [ ] Android (Does not support python plugins yet)

## Scripts

### Project to layers below

Merges a projection of active layer to each underlying node in group.

![showcase](https://github.com/user-attachments/assets/d765b30f-c840-4e0a-81b2-f7f543b01408)

Usage guide:

- Works only when active layer is a visible, unlocked paint layer.
- Affects visible layers below current one, inside the same group.
- Goes out of the current group, if it is in pass-through mode.
- Recursively goes inside the sub-groups.
- Requires no locked or inherit-alpha layers inside the scope.
- If active layer was not in inherit-alpha mode, remaining content takes place of the original layer.

> Warning: The script modifies content of multiple layers. Undoing it with `ctrl+z` may not be possible, as it creates multiple entries in the undo stack. Ideally, save the document before using this script.

> Note: If `Settings > Configure Krita > General > Window > Show on-canvas popup settings` is turned off, the script will not show its progress.

> Note: Script results in deselecting the current selection.

### Backup layer

Creates a hidden copy of the active layer below it. Makes it easier to create a history of a single layer and compare changes done to it.

It is not possible to affect multiple layers at once by selecting them with `ctrl` or `shift` in the layer stack. It can be achieved only by running the script on the group.

### Remove hidden layers

Removes all hidden layers in the group of active layer. Hidden layers inside the subgroups are also removed. Running the script when active layer is not inside any group, results in removing all hidden layers in the document.

Can be used to remove layer history created with `Backup layer` script.

### Toggle layer collapse

Collapse or expand current layer. If current layer has no children, its parent is toggled instead.

Collapsing a layer activates it. Expanding a layer activates its topmost child.

## How to install or update

Scripts can be installed separately using krita's `Ten Scripts` native plugin, or as a standalone plugin.

### Install a single script

1. Pick and download chosen script from [the repository](https://github.com/wojtryb/Wojtryb-Krita-Scripts/tree/main/wojtryb_krita_scripts/scripts).
   <img alt="Screenshot_20250811_121247-edit" src="https://github.com/user-attachments/assets/41a6ae2f-e9ca-44f3-9ab9-4208f0e9049e" />
2. In krita, go to `Tools > Scripts > Ten Scripts`.
3. Use `...` button to assign the script to a keyboard shortcut. Select a path to *.py file you downloaded.

### Install as a plugin

Installation steps are the same for installing the plugin for the first time and for updating it to the new version:

1. [Download](https://github.com/wojtryb/Wojtryb-Krita-Scripts/archive/refs/heads/main.zip) the plugin.
2. In krita's topbar, open **Tools > Scripts > Import Python Plugin From File** and pick the downloaded .zip file.
3. Restart krita.

Scripts can be accessed from `Tools > Scripts` menu.

You can also set custom shortcuts in **Settings > Configure Krita > Keyboard Shortcuts** under **Scripts >Wojtryb Krita Scripts** section. By intention, there are no default bindings.

> **Warning**
> Some keyboard buttons like **Space, R, Y, V, 1, 2, 3, 4, 5, 6** are reserved for Krita's Canvas Inputs. Assigning those keys to actions (including those from the plugin) may result in conflicts and abnormal behavior different for each OS. Either avoid those keys, or remove their bindings in **Settings > Configure Krita > Canvas Input Settings**.
