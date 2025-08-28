"""Lightweight models accessing Odoo backend via XML-RPC."""

from xmlrpc import client
from typing import Any, Dict, List

from .. import config
from .database import Database
from .bus import get_rpc_object


def get_model_proxy() -> client.ServerProxy:
    return get_rpc_object("2/object")


def authenticate() -> int:
    common = get_rpc_object("2/common")
    return common.authenticate(config.ODOO_DB, config.ODOO_USER, config.ODOO_PASSWORD, {})


class Product:
    @staticmethod
    def load_products() -> List[Dict[str, Any]]:
        models = get_model_proxy()
        uid = authenticate()
        fields = ["name", "list_price", "image_128"]
        ids = models.execute_kw(
            config.ODOO_DB,
            uid,
            config.ODOO_PASSWORD,
            "product.product",
            "search",
            [[]],
        )
        data = models.execute_kw(
            config.ODOO_DB,
            uid,
            config.ODOO_PASSWORD,
            "product.product",
            "read",
            [ids, fields],
        )
        db = Database()
        for d in data:
            db.insert_product(d["name"], d["list_price"], None)
        db.close()
        return data


class Order:
    @staticmethod
    def create_order(lines: List[Dict[str, Any]], amount_total: float) -> int:
        models = get_model_proxy()
        uid = authenticate()
        order_vals = {
            "lines": lines,
            "amount_total": amount_total,
        }
        order_id = models.execute_kw(
            config.ODOO_DB,
            uid,
            config.ODOO_PASSWORD,
            "pos.order",
            "create",
            [order_vals],
        )
        db = Database()
        db.insert_order(str(order_id), amount_total)
        db.close()
        return order_id

