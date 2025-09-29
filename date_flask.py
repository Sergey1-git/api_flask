import pandas as pd

try:
    # Попробуйте прочитать CSV-файл
    df = pd.read_csv('date.csv',header=0, encoding='utf-8')
    print("Файл успешно прочитан")
except FileNotFoundError:
    print("Ошибка: Файл 'my_data.csv' не найден. Проверьте путь и имя файла.")
except Exception as e:
    print(f"Произошла ошибка при чтении файла: {e}")

df = pd.read_csv('date.csv',header=0)
df['Datetime'] = pd.to_datetime(df['Datetime'], format='%Y-%m-%d %H:%M')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df=df.sort_values(by='Datetime')
df=df.reset_index(drop=True)