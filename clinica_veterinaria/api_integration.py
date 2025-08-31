import requests  #importa a biblioteca requests para fazer requisições http (apis)

DOG_API_URL = "https://api.thedogapi.com/v1/breeds"
CAT_API_URL = "https://api.thecatapi.com/v1/breeds"

def buscar_racas_cachorro():
    try:
        resp = requests.get(DOG_API_URL, timeout=5)  #retorna um objeto response com status, dados, cabeçalho, a partir de uma requisição GET
        resp.raise_for_status() #vai lançar uma exceção se o servidor der um código diferente de 200 (ok), como 404
        dados = resp.json() #converte o JSON em dicionário do Python
        racas = [item["name"] for item in dados]  #cria lista com o nome "name" para cada raça de cahorro
        return racas  #retorna a lista de raças
    except Exception as e:
        print("Erro ao buscar raças de cachorro:", e)
        return []

def buscar_racas_gato():
    try:
        resp = requests.get(CAT_API_URL, timeout=5)
        resp.raise_for_status()
        dados = resp.json()
        racas = [item["name"] for item in dados]
        return racas
    except Exception as e:
        print("Erro ao buscar raças de gato:", e)
        return []