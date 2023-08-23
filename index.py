import requests
import random
import time


URL = "https://api.claronetcombo.com.br/produto"
lista_produtos = []

def popular_lista():
    global lista_produtos
    lista_produtos = []
    for item in get_all():
        lista_produtos.append(item["id"])    
    print(lista_produtos)

def get_all():
    r = requests.get(url = URL)     
    return r.json()

def get_by_id(id):
    r = requests.get(url = URL + "/" + str(id))  
    popular_lista()    
    return r.json()

def add_produto(produto):
    r = requests.post(url=URL, json=produto)
    popular_lista()
    print(lista_produtos)

def delete(id):
    r = requests.delete(url = URL + "/?id=" + str(id))  
    popular_lista()        
    return r

popular_lista()

while(True):
    n = random.randint(1,1000)

    if(n % 5 == 0 and len(lista_produtos) > 0):
        delete(random.randint(1,len(lista_produtos)-1))

    if(n % 2 == 0):
        add_produto({"nome": "Produto","preco": 1000,"categoria": "Uma Categoria"})       

    get_all()
    print("Executou")
    print(len(lista_produtos))
    time.sleep(1)    