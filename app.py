from flask import Flask, render_template, request
import requests
from typing import Optional

app = Flask(__name__)

PRODUCT_QUERIES = {
    "alcohol-bialcohol": "Alcohol al 70% Bialcohol 1L",
    "arroz-gallo": "Arroz largo fino Gallo 1kg",
    "batatas-mccain": "Papas fritas tradicionales cortadas MCCAIN 700g",
    "chimichurri-alicante": "Condimento para chimichurri Alicante sobre 50g",
    "dulce-leche": "Dulce de leche La Serenísima Colonial",
    "empanadas-jamon-queso": "Empanadas congeladas de jamón y queso",
    "fideos-espaguetis": "Fideos espaguetis MATARAZZO 500g",
    "frambuesas-fra-nui": "Frambuesas Fra-Nui bañadas en chocolate con leche 150g",
    "coca-cola": "Gaseosa Coca-Cola Zero",
    "jabon-dove": "Jabón exfoliante Dove 90g",
    "jabon-palmolive": "Jabón líquido para manos PALMOLIVE Naturals Camelia 500ml",
    "lays": "Papas fritas clásicas Lays 330g",
    "leche-serenisima": "Leche larga vida parcialmente descremada La Serenísima 1% 1L",
    "pan-bimbo": "Pan lacteado blanco rebanado grande Bimbo 610g",
    "papel-elite": "Papel higiénico doble hoja ultra suave ELITE 50m x4 unidades",
    "pimenton-alicante": "Pimentón seleccionado dulce Alicante pote 200g",
    "rollos-felpita": "Rollos de cocina FELPITA 120 paños paquete x3 unidades",
    "toallitas-ayudin": "Toallitas desinfectantes Ayudín aroma fresco 36 unidades",
    "tortillas-rapiditas": "Tortillas Light Rapiditas 10 unidades",
    "yogur-griego": "Yogur griego con frutilla y crema YOGURISIMO 125g",
}

def _fetch_price(base_url: str, query: str) -> Optional[float]:
    """Busca o preço de um produto no site usando a API pública da VTEX."""
    url = f"{base_url}/api/catalog_system/pub/products/search?ft={requests.utils.quote(query)}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        item = data[0]
        return item["items"][0]["sellers"][0]["commertialOffer"]["Price"]
    except Exception:
        return None

def get_carrefour_price(query: str) -> Optional[float]:
    return _fetch_price("https://www.carrefour.com.ar", query)

def get_coto_price(query: str) -> Optional[float]:
    return _fetch_price("https://www.cotodigital3.com.ar", query)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comparar', methods=['POST'])
def comparar():
    produtos_selecionados = request.form.getlist('produtos')
    coca_tamanho = request.form.get('coca-cola-tamano')

    resultados = {}
    for produto in produtos_selecionados:
        nome = produto
        if produto == "coca-cola" and coca_tamanho:
            nome += f" {coca_tamanho}"

        query = PRODUCT_QUERIES.get(produto, produto.replace('-', ' '))
        preco_carrefour = get_carrefour_price(query)
        preco_coto = get_coto_price(query)

        precos = {
            "Carrefour": preco_carrefour,
            "Coto Digital": preco_coto,
        }
        precos_validos = {k: v for k, v in precos.items() if v is not None}
        if not precos_validos:
            continue
        loja_mais_barata = min(precos_validos, key=precos_validos.get)
        resultados[nome] = {
            "loja": loja_mais_barata,
            "preco": precos_validos[loja_mais_barata],
        }

    return render_template('resultado.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
