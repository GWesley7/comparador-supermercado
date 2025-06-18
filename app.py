from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comparar', methods=['POST'])
def comparar():
    produtos_selecionados = request.form.getlist('produtos')
    return f"Produtos selecionados: {', '.join(produtos_selecionados)}"

if __name__ == '__main__':
    app.run(debug=True)
