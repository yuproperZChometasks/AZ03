### 2. Код для загрузки всех страниц с помощью Selenium

#код, который сначала загружает все страницы с помощью Selenium, а затем обрабатывает данные с помощью Scrapy:

import scrapy
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class Divansvetcsv1Spider(scrapy.Spider):
    name = "divansvetcsv"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/tomsk/category/svet"]

    def __init__(self):
        # Открываем файл для записи в режиме 'write'
        self.csv_file = open('output_scrapy.csv', mode='w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        # Записываем заголовки в CSV файл
        self.csv_writer.writerow(['id', 'price'])

    def start_requests(self):
        # Инициализация драйвера
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(self.start_urls[0])

        # Прокрутка страницы до конца и загрузка всех данных
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Прокрутка вниз
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Ожидание загрузки новых данных

            # Проверка новой высоты страницы и сравнение с предыдущей
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Получаем HTML-код страницы
        page_source = self.driver.page_source
        self.driver.quit()

        # Передаем полученный HTML в парсер Scrapy
        yield scrapy.http.HtmlResponse(url=self.start_urls[0], body=page_source, encoding='utf-8')

    def parse(self, response):
        # Создаём переменную, в которую будет сохраняться информация
        svets = response.css('div._Ud0k')
        id = 0
        # Настраиваем работу с каждым отдельным светильником в списке
        for svet in svets:
            id += 1
            # Извлекаем данные
            price = svet.css('div.pY3d2 span::text').get()

            # Записываем данные в CSV файл
            self.csv_writer.writerow([id, price])

    def close(self, reason):
        # Закрываем CSV файл после завершения работы парсера
        self.csv_file.close()

"""
### Объяснение кода:
1. **Инициализация Selenium**:
   - Мы используем Selenium для загрузки страницы и прокрутки до конца, чтобы загрузить все данные.
2. **Получение HTML**:
   - После завершения прокрутки мы получаем HTML-код страницы с помощью `self.driver.page_source`.
3. **Передача данных в Scrapy**:
   - Мы создаем объект `HtmlResponse` и передаем в него загруженный HTML-код, чтобы Scrapy мог его обработать.
4. **Парсинг страницы**:
   - В методе `parse` извлекаем данные, как и раньше, и записываем их в CSV файл.

Запуск
```bash
scrapy crawl divansvetcsv
```
"""
