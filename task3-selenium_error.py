import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt

# Настройка Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Запуск в фоновом режиме (без графического интерфейса)
options.add_argument('--ignore-certificate-errors')  # Игнорировать ошибки сертификата
options.add_argument('--disable-gpu')  # Отключить использование GPU (для headless режима)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)



# Инициализация ChromeDriver
# driver = webdriver.Chrome(ChromeDriverManager().install())

# Теперь вы можете использовать driver для автоматизации вашего браузера
test = driver.get("https://www.example.com")

# Получаем HTML-код страницы
page_source = driver.page_source

# Выводим HTML-код страницы в консоль или работаем с ним
print(page_source)

# Список для хранения цен
prices = []

# Основной URL
base_url = "https://www.divan.ru/tomsk/category/divany-i-kresla"

# Парсинг данных
for page in range(1, 1):  # Страницы от 1 до 48
    #  url = f"{base_url}page-{page}"
    url = base_url
    driver.get(url)
    time.sleep(2)  # Ждем загрузки страницы

    """
    # Получаем HTML-код страницы
    page_source = driver.page_source

    # Выводим HTML-код страницы в консоль или работаем с ним
    print(page_source)
    """    

    # Поиск элементов с ценами
    items = driver.find_elements(By.CSS_SELECTOR, 'span.ui-LD-ZU.KIkOH[data-testid="price"]')
    if not items:
        print(f"Страница {page} пуста, заканчиваем парсинг.")
        break  # Если страница пуста, выходим из цикла

    for item in items:
        price_text = item.text.replace('₽', '').replace(' ', '').strip()
        if price_text.isdigit():
            prices.append(int(price_text))

# Закрываем драйвер
driver.quit()

# Удаляем дубликаты и сохраняем в CSV
prices = list(set(prices))

with open('divan_prices.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Price"])
    for price in prices:
        writer.writerow([price])

# Обработка данных с pandas
df = pd.DataFrame(prices, columns=["Price"])
mean_price = df["Price"].mean()
print(f"Средняя цена на диваны: {mean_price:.2f} ₽")

# Создание гистограммы
plt.figure(figsize=(10, 6))
plt.hist(df["Price"], bins=20, color='blue', alpha=0.7, edgecolor='black')
plt.title('Гистограмма цен на диваны')
plt.xlabel('Цена (₽)')
plt.ylabel('Частота')
plt.grid(axis='y', alpha=0.75)
plt.show()

"""
Обратите внимание на следующие изменения:
- Добавлен параметр `--ignore-certificate-errors` для игнорирования ошибок SSL.
- Проверка на наличие элементов `items` изменена на метод `find_elements`, чтобы возвращать список элементов.


### Описание кода

1. **Импортируем библиотеки.** Мы импортируем необходимые модули, включая `selenium` для парсинга, `pandas` для обработки данных, и `matplotlib` для визуализации.
   
2. **Настраиваем Selenium.** Мы настраиваем драйвер Chrome для работы в фоновом режиме.

3. **Парсинг данных.** Мы проходим по страницам от 1 до 48, извлекаем цены и добавляем их в список. Если страница пуста, цикл прерывается.

4. **Сохранение данных.** Удаляем дубликаты и сохраняем уникальные цены в CSV файл.

5. **Обработка данных.** С помощью `pandas` мы находим среднюю цену и выводим ее на экран.

6. **Создание гистограммы.** Мы строим гистограмму на основе собранных данных."
"""