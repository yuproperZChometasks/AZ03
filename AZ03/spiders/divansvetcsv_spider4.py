"""
Мы будем использовать модуль `os` для определения полного пути к файлу `output_scrapy.csv` 
и добавим отладочные сообщения для вывода информации о пути создания файла.
"""
import scrapy
import os

class DivansvetcsvSpider(scrapy.Spider):
    name = "divansvetcsv4"
    allowed_domains = ["divan.ru"]
    start_urls = [
        "https://www.divan.ru/tomsk/category/svet",
        "https://www.divan.ru/tomsk/category/svet/page-2",
        "https://www.divan.ru/tomsk/category/svet/page-3",
        "https://www.divan.ru/tomsk/category/svet/page-4",
        "https://www.divan.ru/tomsk/category/svet/page-5"
    ]
    
    # Определите путь к выходному файлу
    output_dir1 = os.path.dirname(os.path.abspath(__file__))  # Директория текущего файла
    output_file1 = 'output_scrapy.csv'
    output_path1 = os.path.join(output_dir1, output_file1)
    # print (output_dir1, output_file1, output_path1)

    output_path = 'C:\\work\\ZC_python_and_GPT\\Zerocoder_courses\\Python_and_GPT\\AZ03\\AZ03\\spiders\\output_scrapy.csv'
    
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': output_path,  # Используем полный путь к файлу
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        svets = response.css('div._Ud0k')
        self.logger.info(f'Найдено {len(svets)} светильников на странице {response.url}')
        
        # Вывод отладочной информации о пути к файлу
        self.logger.debug(f'Путь к выходному файлу: {self.output_path}')  # выводим путь к файлу

        for svet in svets:
            name = svet.css('div.lsooF span::text').get()
            price = svet.css('div.pY3d2 span::text').get()
            url = svet.css('a').attrib.get('href')

            if name and price and url:
                yield {
                    'name': name.strip(),
                    'price': price.strip(),
                    'url': response.urljoin(url)  # Полный URL
                }

"""
### Изменения и улучшения:
1. **Определение пути к выходному файлу**: Мы используем `os.path.abspath(__file__)`, чтобы получить полный путь к текущему файлу скрипта, и затем создаём путь к `output_scrapy.csv`.
2. **Использование полного пути в `FEED_URI`**: Мы заменили `'output_scrapy.csv'` на полный путь `output_path`, чтобы Scrapy знал, куда сохранять файл.
3. **Отладочные сообщения**: Добавлено сообщение для вывода полного пути к выходному файлу с помощью `self.logger.debug()`. Это поможет вам увидеть, куда именно пытается сохранить файл.
Мы должны увидеть отладочные сообщения в консоли, которые помогут нам проверить, правильно ли определяется путь к выходному файлу."
"""