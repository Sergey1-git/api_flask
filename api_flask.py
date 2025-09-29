import pandas as pd
from flask import Flask, render_template, url_for,request, flash
from date_flask import data_flask
import re


app = Flask(__name__)

app.config['SECRET_KEY'] = 'gdgas43gdfgfgs46hfg6hf7gh9f'

menu = [{"name": "Главная страница", "url": "/"},
        {"name": f"Получение данных на указанное время", "url": "time"}]



def correct_input(string):
    if 15<=len(string)<=16:
        is_valid = re.search (r"[0-2]{1}\d{1}\.[0-1]{1}\d{1}\.2025\s[0-2]?[0-9]{1}:[0-5]{1}[0-9]{1,1}$", string)
        if is_valid:
            return True
        else:
            return False
    else:
        return False

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
    return render_template('time.html', title="Запрос данных по времени.", menu=menu, result=result_time)




if __name__ == "__main__":
    app.run(debug=True)
