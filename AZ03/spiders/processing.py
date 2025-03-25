import pandas as pd
import matplotlib.pyplot as plt

# Чтение данных из файла
path = "C:\work\ZC_python_and_GPT\Zerocoder_courses\Python_and_GPT\AZ03\AZ03\spiders\output_scrapy.csv"
df = pd.read_csv(path)

# Удаление пробелов и преобразование цен в числовой формат
df['price'] = df['price'].str.replace(' ', '').astype(float)

# Вычисление средней цены
average_price = df['price'].mean()
print(f'Средняя цена: {average_price:.2f}')

# Создание гистограммы
plt.figure(figsize=(10, 6))
plt.hist(df['price'], bins=10, color='blue', edgecolor='black')
plt.title('Гистограмма цен')
plt.xlabel('Цена')
plt.ylabel('Количество товаров')
plt.grid(axis='y')
plt.axvline(average_price, color='red', linestyle='dashed', linewidth=1, label='Средняя цена')
plt.legend()
plt.show()

"""
### Инструкция по запуску скрипта:

1. Сохраните приведенный выше код в файл, например, `price_analysis.py`.
2. Убедитесь, что файл `output_scrapy.scv` находится в той же директории, что и ваш скрипт.
3. Установите необходимые библиотеки, если они еще не установлены, с помощью следующих команд:
   ```bash
   pip install pandas matplotlib
   ```
4. Запустите скрипт:
   ```bash
   python price_analysis.py
   ```
"""