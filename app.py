from flask import Flask, render_template, request
from scrapers import fetch_total_coto, fetch_total_carrefour

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comparar', methods=['POST'])
def comparar():
    produtos_selecionados = request.form.getlist('produtos')

    total_coto = fetch_total_coto(produtos_selecionados)
    total_carrefour = fetch_total_carrefour(produtos_selecionados)

    return render_template(
        'resultado.html',
        produtos=produtos_selecionados,
        total_coto=total_coto,
        total_carrefour=total_carrefour,
    )

if __name__ == '__main__':
    app.run(debug=True)
