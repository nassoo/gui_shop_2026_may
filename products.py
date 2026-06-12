import json
import os
import tkinter as tk
from canvas import app
from helpers import clean_screen
from PIL import Image, ImageTk

base_dir = os.path.dirname(__file__)

def update_current_user(username, product_id):
    with open("db/users.txt", "r+") as f:
        users = [json.loads(u.strip()) for u in f]
        for user in users:
            if user["username"] == username:
                user["products"].append(product_id)
                f.seek(0)
                f.truncate()
                f.writelines([json.dumps(u) + "\n" for u in users])
                return

def purchase_product(product_id):
    with open("db/products.txt", "r+") as f:
        products = [json.loads(p.strip()) for p in f]
        for product in products:
            if product["id"] == product_id:
                product["count"] -= 1
                f.seek(0)
                f.truncate()
                f.writelines([json.dumps(p) + "\n" for p in products])
                return

def buy_product(product_id):
    clean_screen()

    with open("db/current_user.txt") as f:
        username = f.read()

    if username:
        update_current_user(username, product_id)
        purchase_product(product_id)

    render_products_screen()

def add_product(name, count, img_path):
    with open("db/products.txt", "a") as f:
        if name == "" or count == "" or img_path == "":
            render_new_product_screen("All fields are required!")
            return
        if not count.isdigit() or int(count) < 0:
            render_new_product_screen("Count must be a non-negative integer!")
            return
        product = {
            "id": len(open("db/products.txt").readlines()) + 1,
            "name": name,
            "count": int(count),
            "img_path": img_path
        }
        f.write(json.dumps(product) + "\n")
    render_products_screen()

def render_new_product_screen(error=None):
    clean_screen()

    tk.Label(app, text="Product name").grid(row=0, column=0)
    name_entry = tk.Entry(app)
    name_entry.grid(row=0, column=1)

    tk.Label(app, text="Product count").grid(row=1, column=0)
    count_entry = tk.Entry(app)
    count_entry.grid(row=1, column=1)

    tk.Label(app, text="Product image path").grid(row=2, column=0)
    img_path_entry = tk.Entry(app)
    img_path_entry.grid(row=2, column=1)

    tk.Button(app,
              text="Add product",
              command=lambda: add_product(name_entry.get(), count_entry.get(), img_path_entry.get())
              ).grid(row=3, column=0, columnspan=2)

    if error:
        tk.Label(app, text=error).grid(row=4, column=0, columnspan=2)

def render_products_screen():
    clean_screen()

    with open("db/current_user.txt") as f:
        username = f.read()
    with open("db/users.txt") as f:
        users = [json.loads(u.strip()) for u in f]
        current_user = next((u for u in users if u["username"] == username), None)
        if current_user:
            tk.Button(app,
                      text="Add product",
                      command=render_new_product_screen).grid(row=0, column=0)

    with open("db/products.txt") as file:
        products = [json.loads(p.strip()) for p in file]
        products = [p for p in products if p["count"] > 0]
        rows_per_product = len(products[0])
        products_per_row = 6
        for i, product in enumerate(products):
            row = i // products_per_row * rows_per_product + 1
            column = i % products_per_row
            tk.Label(app, text=product["name"]).grid(row=row, column=column)

            img = Image.open(os.path.join(base_dir, "db/images", product["img_path"])).resize((100, 100))
            photo_image = ImageTk.PhotoImage(img)
            image_label = tk.Label(image=photo_image)
            image_label.image = photo_image
            image_label.grid(row=row+1, column=column)

            tk.Label(app, text=product["count"]).grid(row=row+2, column=column)
            tk.Button(app,
                      text=f"Buy {product['id']}",
                      command=lambda p=product["id"]: buy_product(p)
                      ).grid(row=row+3, column=column)