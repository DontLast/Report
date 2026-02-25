# parser.py
import csv
import re
import requests
from bs4 import BeautifulSoup

DEFAULT_URL = "https://www.nix.ru/price/price_list.html?section=notebooks_all"

def parse_price(price_text):
    """Преобразует строку с ценой в целое число."""
    if not price_text:
        return None
    cleaned = re.sub(r'[^\d\s]', '', price_text)
    cleaned = re.sub(r'\s+', '', cleaned)
    return int(cleaned) if cleaned else None

def extract_rating(rating_cell):
    """Считает количество полных звёзд."""
    if not rating_cell:
        return 0
    stars = rating_cell.find_all('i', class_='nix-icon-star-full')
    return len(stars)

def fetch_html_from_url(url):
    """Загружает HTML по URL и возвращает байты."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ошибка загрузки страницы: {e}")

def parse_html(html_content):
    """
    Парсит HTML и возвращает список товаров.
    html_content может быть строкой (unicode) или байтами.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', id='search_results')
    if not table:
        raise ValueError("Таблица с id='search_results' не найдена")

    products = []
    rows = table.find_all('tr', class_='search-result-row')
    for row in rows:
        name_span = row.find('span', class_='search-result-name')
        if not name_span:
            continue
        link_tag = name_span.find('a', class_='t')
        if not link_tag:
            continue
        name = link_tag.get_text(strip=True)
        link = link_tag.get('href', '')
        if link and not link.startswith('http'):
            link = 'https://www.nix.ru' + link

        availability_td = row.find('td', class_='region_order_button_mini')
        availability = ''
        if availability_td:
            span = availability_td.find('span', class_='btn-toolbar-buy')
            if span:
                availability = span.get_text(strip=True)

        price_cells = row.find_all('td', class_='cell-half-price')
        price_from = None
        price_to = None
        if len(price_cells) >= 2:
            span_from = price_cells[0].find('span')
            if span_from:
                price_from = parse_price(span_from.get_text())
            span_to = price_cells[1].find('span')
            if span_to:
                price_to = parse_price(span_to.get_text())

        rating_td = row.find('td', class_='cell-best-choise')
        rating = extract_rating(rating_td)

        products.append({
            'name': name,
            'link': link,
            'availability': availability,
            'price_from': price_from,
            'price_to': price_to,
            'rating': rating,
        })
    return products

def save_to_csv(products, output_file):
    """Сохраняет список товаров в CSV (UTF-8 with BOM)."""
    fieldnames = ['name', 'link', 'availability', 'price_from', 'price_to', 'rating']
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for prod in products:
            prod_copy = prod.copy()
            prod_copy['price_from'] = prod['price_from'] if prod['price_from'] is not None else ''
            prod_copy['price_to'] = prod['price_to'] if prod['price_to'] is not None else ''
            writer.writerow(prod_copy)

def read_csv(csv_file, encoding='utf-8-sig'):
    """Читает CSV в указанной кодировке и возвращает список товаров."""
    products = []
    with open(csv_file, 'r', encoding=encoding) as f:
        reader = csv.DictReader(f)
        for row in reader:
            price_from = row['price_from'].strip()
            price_from = int(price_from) if price_from else None
            price_to = row['price_to'].strip()
            price_to = int(price_to) if price_to else None
            rating = int(row['rating']) if row['rating'].isdigit() else 0
            products.append({
                'name': row['name'],
                'link': row['link'],
                'availability': row['availability'],
                'price_from': price_from,
                'price_to': price_to,
                'rating': rating,
            })
    return products