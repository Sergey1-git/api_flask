import pandas as pd
from flask import Flask, render_template, url_for,request, flash


app = Flask(__name__)

menu = [{"name": "Главная страница", "url": "/"}]


@app.route("/",methods=['GET'])
def index():

    return render_template('index.html',title="О сайте", menu=menu)




if __name__ == "__main__":
    app.run(debug=True)
