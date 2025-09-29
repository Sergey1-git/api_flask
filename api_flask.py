import pandas as pd
from flask import Flask, render_template, url_for,request, flash
from date_flask import data_flask
import re
from datetime import datetime
from flask_paginate import Pagination, get_page_args


app = Flask(__name__)

app.config['SECRET_KEY'] = 'gdgas43gdfgfgs46hfg6hf7gh9f'

# Ссылки на страницы.
menu = [{"name": "Главная страница", "url": "/"},
        {"name": f"Получение данных на указанное время", "url": "time"},
        {"name": f"Получение данных за указанный период", "url": "period"}]


# Функция выполняе проверку корректности  заполнения полей ввода даты и времени.
def correct_input(string):
    if 15<=len(string)<=16:
        is_valid = re.search (r"[0-2]{1}\d{1}\.[0-1]{1}\d{1}\.2025\s[0-2]?[0-9]{1}:[0-5]{1}[0-9]{1,1}$", string)
        if is_valid:
            return True
        else:
            return False
    else:
        return False

# Функция выполняе проверку, что дата и время начала периода больше даты и времени конца периода.
def correct_interval(date1, date2):
    date1 = datetime.strptime(date1, "%d.%m.%Y %H:%M")
    date2 = datetime.strptime(date2, "%d.%m.%Y %H:%M")
    if date1 < date2:
        return True
    else:
        return False


global result_period
result_period = pd.DataFrame()


@app.route("/",methods=['GET'])
def index():
    global result_period
    result_period = pd.DataFrame()
    return render_template('index.html',title="О сайте", menu=menu)


@app.route("/time" , methods=['GET','POST'])
def time():
    global result_period
    result_period = pd.DataFrame()
    result_time = ''
    if request.method == 'POST':
        date1 = request.form['date1']
        if date1 !='' :
            if correct_input(date1) is True:
                result_time = data_flask(date1)
            else:
                flash(f'Данные {date1} не соответствуют требуемому формату, повторите ввод.')
        else:
            flash('Поле ввода данных не заполнено.')
    return render_template('time.html', title="Запрос данных по времени.", menu=menu,
                           result=result_time)


@app.route("/period" , methods=['GET','POST'])
def period():
    n = 0
    if request.method=='POST':
        date1 = request.form['date1']
        date2 = request.form['date2']
        if date1 !='' and date2 !='':
            if correct_input(date1) is True :
                if correct_input(date2) is True:
                    if correct_interval(date1, date2) is True:
                        global result_period
                        print('V',len(result_period))
                        result_period = data_flask(date1, date2)
                        print('V', len(result_period))
                    else:
                        flash(f'Значение  {date1} в поле "Начало периода" больше значения {date2} в поле "Конец периода"'
                              f', повторите ввод.')
                else:
                    flash(f'Данные {date2} в поле "Начало периода" не соответствуют требуемому формату, повторите ввод.')
            else:
                flash(f'Данные {date1} в поле "Конец периода" не соответствуют требуемому формату, повторите ввод.')
        else:
            flash('Одно или оба поля ввода данных не заполнены.')

    if result_period.empty:
        return render_template('period.html', title="Запрос данных по периоду.", menu=menu, items=None)
    else:
        n = 1
        page, per_page, offset = get_page_args(page=1, per_page_count=10,  # Количество элементов на странице
                                           path=url_for('period'))  # Путь для ссылок пагинации
        items_on_page = result_period[offset:offset + per_page]
        pagination = Pagination(page=page, per_page=per_page, total=len(result_period),
                                css_framework='Bootstrap5')  # Или другой фреймворк CSS
        return render_template('period.html', title="Запрос данных по периоду.", menu=menu,
                               items=items_on_page, pagination=pagination, n=n)

if __name__ == "__main__":
    app.run(debug=True)
