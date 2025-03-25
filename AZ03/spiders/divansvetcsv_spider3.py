import scrapy
import csv
import time

class DivansvetcsvSpider(scrapy.Spider):
    name = "divansvetcsv3"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/tomsk/category/svet"]

    def __init__(self):
        # Открываем файл для записи в режиме 'write'
        self.csv_file = open('output_scrapy.csv', mode='w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        # Записываем заголовки в CSV файл
        self.csv_writer.writerow(['name', 'price', 'url'])


    def parse(self, response):
   # Создаём переменную, в которую будет сохраняться информация
   # Пишем ту же команду, которую писали в терминале
        svets = response.css('div._Ud0k')
        print (len(svets))
        # Настраиваем работу с каждым отдельным диваном в списке
        for svet in svets:
            # Извлекаем данные
            name = svet.css('div.lsooF span::text').get()
            price = svet.css('div.pY3d2 span::text').get()
            url = svet.css('a').attrib['href']
            
            # Записываем данные в CSV файл
            self.csv_writer.writerow([name, price, url])
    def close(self, reason):
        # Закрываем CSV файл после завершения работы парсера
        self.csv_file.close()