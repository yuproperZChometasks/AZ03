import scrapy
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class DivansvetcsvSpider(scrapy.Spider):
    name = "divansvetcsv2"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/tomsk/category/svet"]

    def __init__(self):
        # Открываем файл для записи в режиме 'write'
        self.csv_file = open('output_scrapy.csv', mode='w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        # Записываем заголовки в CSV файл
        self.csv_writer.writerow(['id', 'price'])

    def start_requests(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        page_number = 1
        
        while True:
            if page_number == 1 :
                url = f"https://www.divan.ru/tomsk/category/svet"    
            else :
                url = f"https://www.divan.ru/tomsk/category/svet/page-{page_number}"
            self.driver.get(url)
            time.sleep(20)  # Ожидание загрузки страницы
            # Получаем HTML-код страницы
            page_source = self.driver.page_source
            
            # Передаем полученный HTML в парсер Scrapy
            yield scrapy.http.HtmlResponse(url=url, body=page_source, encoding='utf-8')

            page_number += 1  # Переход к следующей странице

            # Проверка на наличие данных на странице
            if page_number == 2:
                break  # Если данных нет, выходим из цикла

    def parse(self, response):
      
        self.logger.info("Got successful response from %s", response.url)
        print(response.body)
        svets = response.css('div._Ud0k')
        print(len(svets))
        id = 0
        for svet in svets:
            id += 1
            price = svet.css(' span::text').get()
            self.csv_writer.writerow([id, price])

    def close(self, reason):
        self.driver.quit()  # Закрываем драйвер
        self.csv_file.close()  # Закрываем CSV файл