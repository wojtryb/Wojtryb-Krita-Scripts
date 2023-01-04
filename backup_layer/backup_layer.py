from .api_krita import Krita, Extension
from PyQt5.QtCore import QTimer


class BackupLayer(Extension):
    """
    Krita extension adding `backup layer` action.

    The action leaves a hidden duplicate of current layer.
    Groups are being collapsed, and name is kept without change.
    """

    def backup_layer(self):
        """Create backup of current layer."""
        Krita.trigger_action("duplicatelayer")
        self._document = Krita.get_active_document()
        self._original_layer = self._document.active_node
        QTimer.singleShot(10, self._hide_layer)

    def _hide_layer(self):
        """Hide a stored layer, collapse it and rename new one."""
        self._original_layer.visible = False
        self._original_layer.collapsed = True

        new_layer = self._document.active_node
        new_layer.name = self._original_layer.name

    def setup(self):
        """Obligatory override."""

    def createActions(self, window):
        """Create the action."""
        self._action = Krita.create_action(
            window,
            name="Backup Layer",
            callback=self.backup_layer
        )


Krita.add_extension(BackupLayer)
