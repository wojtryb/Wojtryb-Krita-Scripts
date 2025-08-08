# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita
from .wojtryb_krita_scripts import WojtrybKritaScripts

Krita.instance().addExtension(WojtrybKritaScripts(Krita.instance()))
