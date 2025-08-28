"""Tkinter based demo POS frontend."""

import tkinter as tk
from tkinter import ttk, messagebox

from ..backend.models import Product, Order


class POSApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("POSPY")
        self.geometry("600x400")
        self.products = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        self.product_list = tk.Listbox(frame)
        self.product_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(side=tk.RIGHT, fill=tk.Y)

        load_btn = ttk.Button(btn_frame, text="Load Products", command=self.load_products)
        load_btn.pack(pady=5)

        order_btn = ttk.Button(btn_frame, text="Create Order", command=self.create_order)
        order_btn.pack(pady=5)

    def load_products(self) -> None:
        self.products = Product.load_products()
        self.product_list.delete(0, tk.END)
        for p in self.products:
            self.product_list.insert(tk.END, f"{p['name']} - {p['list_price']}")

    def create_order(self) -> None:
        selection = self.product_list.curselection()
        if not selection:
            messagebox.showinfo("POSPY", "Select a product first")
            return
        idx = selection[0]
        product = self.products[idx]
        line = (0, 0, {
            'product_id': product['id'],
            'price_unit': product['list_price'],
            'qty': 1,
        })
        order_id = Order.create_order([line], product['list_price'])
        messagebox.showinfo("POSPY", f"Order {order_id} created")


def main() -> None:
    app = POSApp()
    app.mainloop()


if __name__ == "__main__":
    main()
