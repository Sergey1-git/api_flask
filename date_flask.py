import pandas as pd
import datetime
from datetime import datetime
from datetime import timedelta

try:
    df = pd.read_csv('date.csv',header=0, encoding='utf-8')
    print("Файл успешно прочитан")
except FileNotFoundError:
    print("Ошибка: Файл 'my_date.csv' не найден. Проверьте путь и имя файла.")
except Exception as e:
    print(f"Произошла ошибка при чтении файла: {e}")

df['Datetime'] = pd.to_datetime(df['Datetime'], format='%Y-%m-%d %H:%M')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df=df.sort_values(by='Datetime')
df=df.reset_index(drop=True)

# Функция подготовки  данных для функций time и period.
def data_flask(date1, date2=None):
    # Для функции time.
    if date2 is None:
        value_day_minute = datetime.strptime(date1, "%d.%m.%Y %H:%M")
        value_day_minute_min = datetime.strptime(date1, "%d.%m.%Y %H:%M") - timedelta(minutes=2.1)
        value_day_minute_max = datetime.strptime(date1, "%d.%m.%Y %H:%M") + timedelta(minutes=2.1)
        day_minute_one = df[(df['Datetime'] > value_day_minute_min) & (df['Datetime'] < value_day_minute_max)]

        if (day_minute_one['Datetime'] == value_day_minute).any():
            day_minute_one1 = day_minute_one[(day_minute_one['Datetime'] == value_day_minute)]
            day_minute_one1 = day_minute_one1.to_html()
            return day_minute_one1
        else:
            day_minute_one = day_minute_one.to_html()
            return day_minute_one
    # Для функции period.
    else:
        value_day_minute_min1 = datetime.strptime(date1, "%d.%m.%Y %H:%M")
        value_day_minute_max2 = datetime.strptime(date2, "%d.%m.%Y %H:%M")
        day_minute = df[(df['Datetime'] > value_day_minute_min1) & (df['Datetime'] < value_day_minute_max2)]
        return day_minute