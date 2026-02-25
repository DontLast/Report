import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime
import webbrowser


class DNSPriceAggregator:
    def __init__(self, root):
        self.root = root
        self.root.title("DNS Price Aggregator - Благовещенск")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)

        self.setup_styles()

        self.shops = [
            {"name": "DNS - ТРЦ 'Острова'", "address": "ул. 50 лет Октября, 190", "phone": "+7 (4162) 123-456"},
            {"name": "DNS - ТЦ 'Порт Благовещенск'", "address": "ул. Мухина, 118", "phone": "+7 (4162) 234-567"},
            {"name": "DNS - ТЦ 'Флагман'", "address": "ул. Горького, 150", "phone": "+7 (4162) 345-678"},
            {"name": "DNS - ТЦ 'Пионер'", "address": "ул. Ленина, 100", "phone": "+7 (4162) 456-789"}
        ]

        self.products = self.generate_product_data()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        self.bg_color = "#f0f0f0"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.accent_color = "#e74c3c"
        self.success_color = "#27ae60"

        self.root.configure(bg=self.bg_color)

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="white",
                        font=('Arial', 10))

        style.configure("Treeview.Heading",
                        font=('Arial', 11, 'bold'),
                        background=self.primary_color,
                        foreground="white")

        style.map("Treeview.Heading",
                  background=[('active', self.secondary_color)])

        style.configure("Accent.TButton",
                        font=('Arial', 10, 'bold'),
                        background=self.secondary_color,
                        foreground="white")

        style.map("Accent.TButton",
                  background=[('active', self.primary_color)])

    def generate_product_data(self):
        """Генерация расширенного набора товаров (24 шт.)"""
        products = [
            # Ноутбуки
            {"name": "Ноутбук ASUS ROG Strix G15", "category": "Ноутбуки",
             "prices": [random.randint(120000, 135000) for _ in range(4)],
             "in_stock": [True, True, False, True],
             "url": "https://www.dns-shop.ru/product/asus-rog-strix-g15/"},
            {"name": "Ноутбук Acer Aspire 5", "category": "Ноутбуки",
             "prices": [random.randint(50000, 65000) for _ in range(4)],
             "in_stock": [True, False, True, True],
             "url": "https://www.dns-shop.ru/product/acer-aspire-5/"},
            {"name": "Ноутбук Lenovo IdeaPad 3", "category": "Ноутбуки",
             "prices": [random.randint(45000, 55000) for _ in range(4)],
             "in_stock": [True, True, True, False],
             "url": "https://www.dns-shop.ru/product/lenovo-ideapad-3/"},
            {"name": "Ноутбук HP Pavilion 15", "category": "Ноутбуки",
             "prices": [random.randint(60000, 75000) for _ in range(4)],
             "in_stock": [False, True, True, True],
             "url": "https://www.dns-shop.ru/product/hp-pavilion-15/"},

            # Смартфоны
            {"name": "Смартфон Samsung Galaxy S24", "category": "Смартфоны",
             "prices": [random.randint(89990, 95000) for _ in range(4)],
             "in_stock": [True, False, True, True],
             "url": "https://www.dns-shop.ru/product/samsung-galaxy-s24/"},
            {"name": "Смартфон iPhone 15", "category": "Смартфоны",
             "prices": [random.randint(100000, 120000) for _ in range(4)],
             "in_stock": [True, True, True, False],
             "url": "https://www.dns-shop.ru/product/iphone-15/"},
            {"name": "Смартфон Xiaomi Redmi Note 13", "category": "Смартфоны",
             "prices": [random.randint(25000, 35000) for _ in range(4)],
             "in_stock": [True, False, False, True],
             "url": "https://www.dns-shop.ru/product/xiaomi-redmi-note-13/"},
            {"name": "Смартфон Google Pixel 8", "category": "Смартфоны",
             "prices": [random.randint(70000, 85000) for _ in range(4)],
             "in_stock": [False, True, True, False],
             "url": "https://www.dns-shop.ru/product/google-pixel-8/"},

            # Планшеты
            {"name": "Планшет Samsung Tab S9", "category": "Планшеты",
             "prices": [random.randint(70000, 90000) for _ in range(4)],
             "in_stock": [True, True, True, True],
             "url": "https://www.dns-shop.ru/product/samsung-tab-s9/"},
            {"name": "Планшет iPad Pro", "category": "Планшеты",
             "prices": [random.randint(90000, 130000) for _ in range(4)],
             "in_stock": [True, False, True, False],
             "url": "https://www.dns-shop.ru/product/ipad-pro/"},
            {"name": "Планшет Lenovo Tab P12", "category": "Планшеты",
             "prices": [random.randint(40000, 55000) for _ in range(4)],
             "in_stock": [False, True, True, True],
             "url": "https://www.dns-shop.ru/product/lenovo-tab-p12/"},

            # Мониторы
            {"name": "Монитор LG 27UL850", "category": "Мониторы",
             "prices": [random.randint(35000, 45000) for _ in range(4)],
             "in_stock": [True, True, False, True],
             "url": "https://www.dns-shop.ru/product/lg-27ul850/"},
            {"name": "Монитор Samsung Odyssey G5", "category": "Мониторы",
             "prices": [random.randint(30000, 40000) for _ in range(4)],
             "in_stock": [True, False, True, True],
             "url": "https://www.dns-shop.ru/product/samsung-odyssey-g5/"},
            {"name": "Монитор AOC 24G2", "category": "Мониторы",
             "prices": [random.randint(20000, 28000) for _ in range(4)],
             "in_stock": [True, True, True, False],
             "url": "https://www.dns-shop.ru/product/aoc-24g2/"},

            # Наушники
            {"name": "Наушники Sony WH-1000XM5", "category": "Наушники",
             "prices": [random.randint(25000, 32000) for _ in range(4)],
             "in_stock": [True, True, True, True],
             "url": "https://www.dns-shop.ru/product/sony-wh-1000xm5/"},
            {"name": "Наушники JBL Tune 760NC", "category": "Наушники",
             "prices": [random.randint(8000, 12000) for _ in range(4)],
             "in_stock": [True, False, True, False],
             "url": "https://www.dns-shop.ru/product/jbl-tune-760nc/"},
            {"name": "Наушники Apple AirPods Pro", "category": "Наушники",
             "prices": [random.randint(20000, 25000) for _ in range(4)],
             "in_stock": [False, True, True, True],
             "url": "https://www.dns-shop.ru/product/airpods-pro/"},

            # Периферия
            {"name": "Клавиатура Logitech MX Keys", "category": "Периферия",
             "prices": [random.randint(10000, 15000) for _ in range(4)],
             "in_stock": [True, True, False, True],
             "url": "https://www.dns-shop.ru/product/logitech-mx-keys/"},
            {"name": "Мышь Logitech MX Master 3", "category": "Периферия",
             "prices": [random.randint(7000, 10000) for _ in range(4)],
             "in_stock": [True, False, True, True],
             "url": "https://www.dns-shop.ru/product/logitech-mx-master-3/"},

            # Комплектующие
            {"name": "Видеокарта NVIDIA RTX 4070", "category": "Комплектующие",
             "prices": [random.randint(75000, 80000) for _ in range(4)],
             "in_stock": [False, True, True, False],
             "url": "https://www.dns-shop.ru/product/nvidia-rtx-4070/"},
            {"name": "Процессор Intel Core i7-13700K", "category": "Комплектующие",
             "prices": [random.randint(35000, 42000) for _ in range(4)],
             "in_stock": [True, True, True, False],
             "url": "https://www.dns-shop.ru/product/intel-core-i7-13700k/"},
            {"name": "Материнская плата ASUS ROG Strix B760", "category": "Комплектующие",
             "prices": [random.randint(18000, 25000) for _ in range(4)],
             "in_stock": [True, False, True, True],
             "url": "https://www.dns-shop.ru/product/asus-rog-strix-b760/"},
            {"name": "Оперативная память Kingston Fury 32GB", "category": "Комплектующие",
             "prices": [random.randint(9000, 13000) for _ in range(4)],
             "in_stock": [True, True, False, True],
             "url": "https://www.dns-shop.ru/product/kingston-fury-32gb/"},

            # Хранение данных
            {"name": "Внешний SSD Samsung T7 1TB", "category": "Хранение данных",
             "prices": [random.randint(8000, 11000) for _ in range(4)],
             "in_stock": [True, True, True, False],
             "url": "https://www.dns-shop.ru/product/samsung-t7-1tb/"},

            # Принтеры
            {"name": "Принтер HP LaserJet", "category": "Принтеры",
             "prices": [random.randint(15000, 25000) for _ in range(4)],
             "in_stock": [True, False, True, True],
             "url": "https://www.dns-shop.ru/product/hp-laserjet/"},
        ]
        return products

    def create_widgets(self):
        # Верхняя панель
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame,
                               text="🛒 ShopCompase - Благовещенск",
                               font=('Arial', 20, 'bold'),
                               bg=self.primary_color,
                               fg="white")
        title_label.pack(pady=20)

        # Основной контейнер
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Левая панель (фильтры)
        left_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        filter_title = tk.Label(left_panel,
                                text="🔍 Фильтры",
                                font=('Arial', 14, 'bold'),
                                bg="white",
                                fg=self.primary_color)
        filter_title.pack(pady=10, padx=10, anchor=tk.W)

        # Поиск
        search_label = tk.Label(left_panel,
                                text="Поиск товара:",
                                font=('Arial', 10),
                                bg="white")
        search_label.pack(pady=(10, 5), padx=10, anchor=tk.W)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.update_table())
        search_entry = tk.Entry(left_panel,
                                textvariable=self.search_var,
                                font=('Arial', 10),
                                width=25,
                                relief=tk.SOLID,
                                bd=1)
        search_entry.pack(pady=(0, 15), padx=10)

        # Категории (динамически из данных)
        category_label = tk.Label(left_panel,
                                  text="Категория:",
                                  font=('Arial', 10),
                                  bg="white")
        category_label.pack(pady=(10, 5), padx=10, anchor=tk.W)

        self.category_var = tk.StringVar(value="Все")
        # Получаем уникальные категории товаров и добавляем "Все"
        categories = sorted(set(p["category"] for p in self.products))
        categories.insert(0, "Все")

        for cat in categories:
            rb = tk.Radiobutton(left_panel,
                                text=cat,
                                variable=self.category_var,
                                value=cat,
                                font=('Arial', 9),
                                bg="white",
                                command=self.update_table)
            rb.pack(pady=2, padx=20, anchor=tk.W)

        # Кнопка сброса
        reset_btn = ttk.Button(left_panel,
                               text="Сбросить фильтры",
                               style="Accent.TButton",
                               command=self.reset_filters)
        reset_btn.pack(pady=20, padx=10)

        # Информация о магазинах
        shops_label = tk.Label(left_panel,
                               text="🏪 Магазины DNS",
                               font=('Arial', 12, 'bold'),
                               bg="white",
                               fg=self.primary_color)
        shops_label.pack(pady=(20, 10), padx=10, anchor=tk.W)

        for i, shop in enumerate(self.shops):
            shop_frame = tk.Frame(left_panel, bg="white")
            shop_frame.pack(fill=tk.X, pady=5, padx=10)

            color_label = tk.Label(shop_frame,
                                   text="●",
                                   font=('Arial', 12),
                                   bg="white",
                                   fg=self.get_shop_color(i))
            color_label.pack(side=tk.LEFT)

            shop_name = tk.Label(shop_frame,
                                 text=shop["name"],
                                 font=('Arial', 9, 'bold'),
                                 bg="white",
                                 fg=self.primary_color,
                                 wraplength=180,
                                 justify=tk.LEFT)
            shop_name.pack(side=tk.LEFT, padx=(5, 0))

        # Центральная панель (таблица)
        center_panel = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=1)
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Заголовок таблицы
        table_header = tk.Frame(center_panel, bg=self.secondary_color, height=40)
        table_header.pack(fill=tk.X)
        table_header.pack_propagate(False)

        table_title = tk.Label(table_header,
                               text="📊 Сравнение цен",
                               font=('Arial', 14, 'bold'),
                               bg=self.secondary_color,
                               fg="white")
        table_title.pack(side=tk.LEFT, padx=20, pady=8)

        update_time = tk.Label(table_header,
                               text=f"Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                               font=('Arial', 9),
                               bg=self.secondary_color,
                               fg="white")
        update_time.pack(side=tk.RIGHT, padx=20, pady=10)

        # ----- НИЖНЯЯ ПАНЕЛЬ (создаём заранее, чтобы была доступна в update_table) -----
        bottom_frame = tk.Frame(self.root, bg=self.primary_color, height=50)
        bottom_frame.pack_propagate(False)

        self.total_label = tk.Label(bottom_frame,
                                    text="Всего товаров: 3 | Магазинов: 4",
                                    font=('Arial', 10),
                                    bg=self.primary_color,
                                    fg="white")
        self.total_label.pack(side=tk.LEFT, padx=20, pady=15)

        self.best_price_label = tk.Label(bottom_frame,
                                         text="💰 Лучшая цена: найдем для вас!",
                                         font=('Arial', 10, 'bold'),
                                         bg=self.primary_color,
                                         fg=self.success_color)
        self.best_price_label.pack(side=tk.RIGHT, padx=20, pady=15)
        # ------------------------------------------------------------------------------

        # Создание таблицы
        self.create_table(center_panel)

        # Упаковываем нижнюю панель после таблицы, чтобы она оказалась внизу
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

    def get_shop_color(self, index):
        colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12"]
        return colors[index % len(colors)]

    def create_table(self, parent):
        table_frame = tk.Frame(parent, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        vsb = ttk.Scrollbar(table_frame, orient="vertical")
        hsb = ttk.Scrollbar(table_frame, orient="horizontal")

        columns = ("Товар", "Категория", "DNS - Острова", "DNS - Порт", "DNS - Флагман", "DNS - Пионер", "Наличие")
        self.tree = ttk.Treeview(table_frame,
                                 columns=columns,
                                 show="headings",
                                 yscrollcommand=vsb.set,
                                 xscrollcommand=hsb.set,
                                 height=15)

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        column_widths = [250, 120, 100, 100, 100, 100, 100]
        for col, width in zip(columns, column_widths):
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.tree.column(col, width=width, minwidth=80, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<Double-1>", self.on_item_double_click)

        self.update_table()

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_text = self.search_var.get().lower()
        category = self.category_var.get()

        for product in self.products:
            if search_text and search_text not in product["name"].lower():
                continue
            if category != "Все" and product["category"] != category:
                continue

            prices = []
            for i, price in enumerate(product["prices"]):
                if product["in_stock"][i]:
                    prices.append(f"{price:,} ₽".replace(",", " "))
                else:
                    prices.append("Нет в наличии")

            in_stock_any = any(product["in_stock"])
            stock_status = "✅ В наличии" if in_stock_any else "❌ Нет в наличии"

            values = [product["name"], product["category"]] + prices + [stock_status]

            if in_stock_any:
                self.tree.insert("", tk.END, values=values, tags=("in_stock",))
            else:
                self.tree.insert("", tk.END, values=values, tags=("out_of_stock",))

        self.tree.tag_configure("in_stock", background="white")
        self.tree.tag_configure("out_of_stock", background="#ffebee")

        total_items = len(self.tree.get_children())
        self.total_label.config(text=f"Всего товаров: {total_items} | Магазинов: 4")

        self.find_best_price()

    def find_best_price(self):
        best_price = float('inf')
        best_product = None
        best_shop_index = None

        for product in self.products:
            for i, price in enumerate(product["prices"]):
                if product["in_stock"][i] and price < best_price:
                    best_price = price
                    best_product = product["name"]
                    best_shop_index = i

        if best_product and best_shop_index is not None:
            self.best_price_label.config(
                text=f"💰 Лучшая цена: {best_product[:30]}... - {best_price:,} ₽ в {self.shops[best_shop_index]['name'][:20]}..."
            )

    def sort_column(self, col):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort()
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)

    def reset_filters(self):
        self.search_var.set("")
        self.category_var.set("Все")
        self.update_table()

    def on_item_double_click(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        item = selection[0]
        product_name = self.tree.item(item, "values")[0]

        for product in self.products:
            if product["name"] == product_name:
                webbrowser.open(product["url"])
                messagebox.showinfo("Информация",
                                    f"Открыта страница товара:\n{product_name}")
                break


def main():
    root = tk.Tk()
    app = DNSPriceAggregator(root)
    root.mainloop()


if __name__ == "__main__":
    main()