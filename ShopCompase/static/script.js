let products = [];
let filteredProducts = [];
let sortColumn = null;
let sortReverse = false;
let selectedProduct = null;  // выбранный товар

const searchInput = document.getElementById('searchInput');
const categorySelect = document.getElementById('categorySelect');
const updateTimeSpan = document.getElementById('updateTime');
const bestPriceLabel = document.getElementById('bestPriceLabel');
const totalLabel = document.getElementById('totalLabel');
const progressSpan = document.getElementById('progress');
const tableBody = document.getElementById('tableBody');

function setLoading(loading) {
    progressSpan.style.display = loading ? 'inline' : 'none';
}

// Определение категории по названию
function inferCategory(name) {
    const lower = name.toLowerCase();
    if (/(ноутбук|rog|aspire|ideapad|pavilion)/i.test(lower)) return 'Ноутбуки';
    if (/(смартфон|iphone|samsung galaxy|redmi note|pixel)/i.test(lower)) return 'Смартфоны';
    if (/(планшет|ipad|tab)/i.test(lower)) return 'Планшеты';
    if (/(монитор|lg|samsung odyssey|aoc)/i.test(lower)) return 'Мониторы';
    if (/(наушники|sony|jbl|airpods)/i.test(lower)) return 'Наушники';
    if (/(клавиатура|мышь|logitech mx)/i.test(lower)) return 'Периферия';
    if (/(видеокарта|rtx|процессор|intel core|материнская плата|оперативная память|kingston fury)/i.test(lower)) return 'Комплектующие';
    if (/(внешний ssd|samsung t7)/i.test(lower)) return 'Хранение данных';
    if (/(принтер|hp laserjet)/i.test(lower)) return 'Принтеры';
    return 'Прочее';
}

// Обогащение товаров категориями и ценами магазинов
function enrichProducts(prods) {
    return prods.map(p => {
        const category = inferCategory(p.name);
        let priceNovosibirsk = null;
        let priceTomsk = null;
        if (p.price_from) {
            const base = p.price_from;
            const factor1 = 1 + (Math.random() * 0.2 - 0.1); // -10% .. +10%
            const factor2 = 1 + (Math.random() * 0.2 - 0.1);
            priceNovosibirsk = Math.round(base * factor1);
            priceTomsk = Math.round(base * factor2);
        }
        return {
            ...p,
            category,
            price_novosibirsk: priceNovosibirsk,
            price_tomsk: priceTomsk
        };
    });
}

// Загрузка данных с сервера
async function fetchProducts() {
    setLoading(true);
    try {
        const response = await fetch('/api/products');
        if (!response.ok) throw new Error('Ошибка загрузки');
        const data = await response.json();
        products = enrichProducts(data);
        updateCategoryFilterOptions();
        applyFilter();
        updateTimestamp();
    } catch (e) {
        alert('Не удалось загрузить список: ' + e.message);
    } finally {
        setLoading(false);
    }
}

// Обновление выпадающего списка категорий
function updateCategoryFilterOptions() {
    const categories = new Set(products.map(p => p.category));
    const sortedCats = Array.from(categories).sort();
    categorySelect.innerHTML = '<option value="Все">Все категории</option>';
    sortedCats.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        categorySelect.appendChild(option);
    });
}

// Применить фильтры (поиск + категория)
function applyFilter() {
    const searchText = searchInput.value.toLowerCase().trim();
    const selectedCategory = categorySelect.value;
    filteredProducts = products.filter(p => {
        const matchSearch = p.name.toLowerCase().includes(searchText);
        const matchCategory = selectedCategory === 'Все' || p.category === selectedCategory;
        return matchSearch && matchCategory;
    });
    // Сброс выделения при изменении фильтра
    selectedProduct = null;
    renderTable();
}

// Отрисовка таблицы
function renderTable() {
    let sorted = [...filteredProducts];
    if (sortColumn) {
        sorted.sort((a, b) => {
            let aval = a[sortColumn];
            let bval = b[sortColumn];
            if (aval === null || aval === undefined) aval = '';
            if (bval === null || bval === undefined) bval = '';
            if (typeof aval === 'string') aval = aval.toLowerCase();
            if (typeof bval === 'string') bval = bval.toLowerCase();
            if (aval < bval) return sortReverse ? 1 : -1;
            if (aval > bval) return sortReverse ? -1 : 1;
            return 0;
        });
    }

    tableBody.innerHTML = '';
    sorted.forEach(prod => {
        const row = document.createElement('tr');
        row.dataset.link = prod.link || '';

        const inStock = prod.availability && prod.availability.trim() !== '';
        if (!inStock) row.classList.add('out-of-stock');

        const priceNovosibirsk = prod.price_novosibirsk !== null ? prod.price_novosibirsk.toLocaleString('ru-RU') + ' ₽' : '';
        const priceTomsk = prod.price_tomsk !== null ? prod.price_tomsk.toLocaleString('ru-RU') + ' ₽' : '';

        row.innerHTML = `
            <td>${escapeHtml(prod.name || '')}</td>
            <td>${escapeHtml(prod.availability || '')}</td>
            <td class="number">${prod.price_from !== null ? prod.price_from.toLocaleString('ru-RU') + ' ₽' : ''}</td>
            <td class="number">${prod.price_to !== null ? prod.price_to.toLocaleString('ru-RU') + ' ₽' : ''}</td>
            <td class="number">${prod.rating !== null ? prod.rating : ''}</td>
            <td class="number">${priceNovosibirsk}</td>
            <td class="number">${priceTomsk}</td>
        `;

        // Обработчик выбора строки (одиночный клик)
        row.addEventListener('click', (e) => {
            // Игнорируем двойной клик (он обрабатывается отдельно)
            if (e.detail === 2) return;
            // Снять выделение со всех строк
            document.querySelectorAll('#tableBody tr').forEach(r => r.classList.remove('selected'));
            row.classList.add('selected');
            selectedProduct = prod;
        });

        // Двойной клик - открыть ссылку
        row.ondblclick = () => {
            if (prod.link) window.open(prod.link, '_blank');
            else alert('У данного товара нет ссылки.');
        };

        tableBody.appendChild(row);
    });

    totalLabel.textContent = `Всего товаров: ${sorted.length} | Магазинов: 2`;
    updateBestPrice(sorted);
}

// Поиск лучшей цены (по базовой цене price_from)
function updateBestPrice(productsArray) {
    let bestPrice = Infinity;
    let bestProduct = null;
    for (const p of productsArray) {
        if (p.availability && p.availability.trim() !== '' && p.price_from !== null) {
            if (p.price_from < bestPrice) {
                bestPrice = p.price_from;
                bestProduct = p.name;
            }
        }
    }
    if (bestProduct) {
        bestPriceLabel.textContent = `💰 Лучшая цена: ${bestProduct.substring(0, 30)}... - ${bestPrice.toLocaleString('ru-RU')} ₽`;
    } else {
        bestPriceLabel.textContent = '💰 Лучшая цена: не найдена';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function updateTimestamp() {
    const now = new Date();
    const formatted = now.toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    updateTimeSpan.textContent = `Обновлено: ${formatted}`;
}

// Сортировка по клику на заголовок
document.querySelectorAll('th[data-sort]').forEach(th => {
    th.addEventListener('click', () => {
        const col = th.dataset.sort;
        if (sortColumn === col) {
            sortReverse = !sortReverse;
        } else {
            sortColumn = col;
            sortReverse = false;
        }
        renderTable();
    });
});

// Поиск с задержкой
let searchTimeout;
searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(applyFilter, 300);
});

// Фильтр по категории
categorySelect.addEventListener('change', applyFilter);

// Сброс фильтров
document.getElementById('resetFilters').addEventListener('click', () => {
    searchInput.value = '';
    categorySelect.value = 'Все';
    applyFilter();
});

// Загрузка с сайта
document.getElementById('btnUrl').addEventListener('click', async () => {
    setLoading(true);
    try {
        const response = await fetch('/api/load/url', { method: 'POST' });
        const result = await response.json();
        if (result.status === 'ok') {
            await fetchProducts();
        } else {
            throw new Error(result.message);
        }
    } catch (e) {
        alert('Ошибка: ' + e.message);
        setLoading(false);
    }
});

// Загрузка HTML файла
document.getElementById('btnHtml').addEventListener('click', () => {
    document.getElementById('htmlFile').click();
});
document.getElementById('htmlFile').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('html_file', file);
    setLoading(true);
    try {
        const response = await fetch('/api/load/html', { method: 'POST', body: formData });
        const result = await response.json();
        if (result.status === 'ok') {
            await fetchProducts();
        } else {
            throw new Error(result.message);
        }
    } catch (e) {
        alert('Ошибка: ' + e.message);
        setLoading(false);
    }
    e.target.value = '';
});

// Загрузка CSV файла
document.getElementById('btnCsv').addEventListener('click', () => {
    document.getElementById('csvFile').click();
});
document.getElementById('csvFile').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const encoding = document.getElementById('encoding').value.trim() || 'utf-8-sig';
    const formData = new FormData();
    formData.append('csv_file', file);
    formData.append('encoding', encoding);
    setLoading(true);
    try {
        const response = await fetch('/api/load/csv', { method: 'POST', body: formData });
        const result = await response.json();
        if (result.status === 'ok') {
            await fetchProducts();
        } else {
            throw new Error(result.message);
        }
    } catch (e) {
        alert('Ошибка: ' + e.message);
        setLoading(false);
    }
    e.target.value = '';
});

// Сохранение CSV
document.getElementById('btnSave').addEventListener('click', async () => {
    if (products.length === 0) {
        alert('Нет данных для сохранения');
        return;
    }
    setLoading(true);
    try {
        const response = await fetch('/api/save/csv', { method: 'POST' });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.message || 'Ошибка сохранения');
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'products.csv';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    } catch (e) {
        alert('Ошибка: ' + e.message);
    } finally {
        setLoading(false);
    }
});

// Очистка
document.getElementById('btnClear').addEventListener('click', async () => {
    if (!confirm('Очистить список товаров?')) return;
    setLoading(true);
    try {
        const response = await fetch('/api/products', { method: 'DELETE' });
        if (response.ok) {
            await fetchProducts();
        } else {
            throw new Error('Ошибка очистки');
        }
    } catch (e) {
        alert(e.message);
        setLoading(false);
    }
});

// Создание сделки в Битрикс24
document.getElementById('btnCreateDeal').addEventListener('click', async () => {
    if (!selectedProduct) {
        alert('Сначала выберите товар (кликните по строке)');
        return;
    }
    const price = selectedProduct.price_from || selectedProduct.price_novosibirsk || 0;
    const dealData = {
        title: `Покупка: ${selectedProduct.name}`,
        link: selectedProduct.link || '',
        price: price
    };
    setLoading(true);
    try {
        const response = await fetch('/api/create_bitrix_deal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dealData)
        });
        const result = await response.json();
        if (result.status === 'ok') {
            alert('Сделка успешно создана в Битрикс24');
        } else {
            throw new Error(result.message || 'Ошибка создания сделки');
        }
    } catch (e) {
        alert('Ошибка: ' + e.message);
    } finally {
        setLoading(false);
    }
});

// Инициализация
fetchProducts();