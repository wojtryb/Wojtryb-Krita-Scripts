# SPDX-FileCopyrightText: © 2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita
from .backup_layer import BackupLayer

Krita.instance().addExtension(BackupLayer(Krita.instance()))
