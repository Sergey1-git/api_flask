import pandas as pd
from flask import Flask, render_template, url_for, request, flash, session
from date_flask import data_flask
from datetime import datetime
from flask_paginate import Pagination, get_page_args
import  os
from dotenv import load_dotenv


app = Flask(__name__)

dict_result_period={}
dict_visits_session={}


# Ссылки на страницы.
menu = [{"name": "Главная страница", "url": "/"},
        {"name": f"Получение данных на указанное время", "url": "time"},
        {"name": f"Получение данных за указанный период", "url": "period"}]


# Функция выполняе проверку корректности  заполнения полей ввода даты и времени.
def correct_input(string):
    date_format = "%d.%m.%Y %H:%M"
    try:
        datetime.strptime(string, date_format)
        return True
    except ValueError:
        return False

# Функция выполняе проверку, что дата и время начала периода больше даты и времени конца периода.
def correct_interval(date1, date2):
    date1 = datetime.strptime(date1, "%d.%m.%Y %H:%M")
    date2 = datetime.strptime(date2, "%d.%m.%Y %H:%M")
    return date1 < date2



@app.route("/",methods=['GET'])
def index():
    return render_template('index.html',title="О сайте", menu=menu)


@app.route("/time" , methods=['GET','POST'])
def time():
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
    if request.method=='POST':
        date1 = request.form['date1']
        date2 = request.form['date2']
        if date1 !='' and date2 !='':
            if correct_input(date1) is True :
                if correct_input(date2) is True:
                    if correct_interval(date1, date2) is True:
                        result_period = data_flask(date1, date2)
                        dict_result_period[session['visits']] = result_period
                    else:
                        flash(f'Значение  {date1} в поле "Начало периода" больше значения {date2} в поле "Конец периода"'
                              f', повторите ввод.')
                else:
                    flash(f'Данные {date2} в поле "Начало периода" не соответствуют требуемому формату, повторите ввод.')
            else:
                flash(f'Данные {date1} в поле "Конец периода" не соответствуют требуемому формату, повторите ввод.')
        else:
            flash('Одно или оба поля ввода данных не заполнены.')

    if 'referer' in request.headers:
        if '/period' not in request.headers['referer']:
            if 'visits' not in session:
                session['visits'] = next(generator_session)
                dict_visits_session[session['visits']] = 0
            return render_template('period.html', title="Запрос данных по периоду.", menu=menu,
                                   items=None)
        else:
            n = 1
            page, per_page, offset = get_page_args(page=1, per_page_count=10,  # Количество элементов на странице
                                               path=url_for('period'))  # Путь для ссылок пагинации
            items_on_page = dict_result_period[session['visits']][offset:offset + per_page]
            pagination = Pagination(page=page, per_page=per_page, total=len(dict_result_period[session['visits']]),
                                css_framework='Bootstrap5')  # Или другой фреймворк CSS
            return render_template('period.html', title="Запрос данных по периоду.", menu=menu,
                               items=items_on_page, pagination=pagination, n=n)
    else:
        return render_template('period.html', title="Запрос данных по периоду.", menu=menu, items=None)

def session_generator():
    n = 122
    while True:
        yield n
        n += 1
generator_session = session_generator()

if __name__ == "__main__":
    load_dotenv()
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.run(debug=True)
