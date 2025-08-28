"""Simplified bus communication using Odoo's bus through XML-RPC."""

from xmlrpc import client
from typing import Any, Dict

from .. import config


def get_rpc_object(endpoint: str) -> client.ServerProxy:
    return client.ServerProxy(f"{config.ODOO_URL}/xmlrpc/{endpoint}")


class POSBus:
    def __init__(self):
        self.common = get_rpc_object("2/common")
        self.models = get_rpc_object("2/object")
        self.uid = self.common.authenticate(config.ODOO_DB, config.ODOO_USER, config.ODOO_PASSWORD, {})

    def notify(self, channel: str, message: Dict[str, Any]) -> None:
        """Send a simplified notification to Odoo's bus."""
        self.models.execute_kw(
            config.ODOO_DB,
            self.uid,
            config.ODOO_PASSWORD,
            "bus.bus",
            "sendone",
            [channel, message],
        )

    def poll(self, channels: list[str], last: int = 0) -> Any:
        """Poll the bus for notifications."""
        return self.models.execute_kw(
            config.ODOO_DB,
            self.uid,
            config.ODOO_PASSWORD,
            "bus.bus",
            "poll",
            [channels, last],
        )
