# -*- coding: utf-8 -*-
"""
Created on Mon May 25 22:26:12 2021
@author: luiz.vieira
"""
import time, os, csv,json ,sys
from datetime import datetime
from browser import Browser
import requests

#Se anos for vazio, gera a lista para os anos de 1996 até o ano atual.
#Chame o script com um ano como parâmetro. Ex: "python main.py 2016"
anos = [] 

try:
    anos.append(int(sys.argv[1]))
    print(f"Rodando script para o ano {anos[0]}")
except Exception as e:
    print("Nenhum ano especificado, deseja rodar o script para todos os anos?")
    p = input("digite Y para prosseguir.")
    if p.lower() != "y":
        print("Abortado.")
        exit()
        
if len(anos) == 0:
    
    ano_atual = datetime.now().year
    anos = [ano for ano in range(1996,ano_atual)]

navegador = Browser()

def process_file_name(file_name):
    file_name = file_name.lower()
    file_name = file_name.replace(" ","_").replace("-","_").replace("!","").replace("?","")
    file_name = file_name.replace("á","a").replace("à","a").replace("ã","a").replace("â","a")
    file_name = file_name.replace("é","e").replace("ê","e").replace("ẽ","e").replace("è","e")
    file_name = file_name.replace("ú","u").replace("ç","c").replace(":","_").replace("/","")
    file_name = file_name.replace("*","").replace("^","").replace("~","").replace("\\","")
    file_name = file_name.replace(",","").replace(".","").replace("í","i").replace("ó","o")
    file_name = file_name.replace("ô","o").replace("õ","o").replace("'","i").replace("\"","")
    file_name = file_name.replace("\x93","").replace("\x94","").replace("'","i").replace("\"","")
    return file_name

def process_link(url):
    link = url.replace("mostrar.php?url=","")
    return link

#Pega lista
anos_dict = {}
for ano in anos:
    page = navegador.go_to_page(ano)
    if page:
        print(f"Processando dados para o ano: {ano}.")
        rows=navegador.get_rows()
        lista = []
        for row in rows:
            itens = row.find_elements_by_tag_name("td")
            if len(itens) > 0:
                titulo = itens[0].text
                autores = itens[1].text  
                link = row.find_element_by_tag_name("a").get_attribute("href")
                ano = itens[3].text
                sessao = itens[4].text
                lista.append([titulo,autores,link,ano,sessao])
        anos_dict[ano] = lista
    else:
        print(f"Erro ao processar ano: {ano}!! Houve problema com o carregamento da página.")

print("Salvando arquivo bruto")
with open(f'raw-{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as f:
    json.dump(anos_dict, f,indent=4,ensure_ascii=False)

print("Salvando csv com toda a lista de trabalhos")
cabecalho = ['Titulo','autores','link','ano','sessao']

csvpath = f"lista-{datetime.now().strftime('%Y-%m-%d')}.csv"
with open(csvpath, 'w+') as f:
    write = csv.writer(f)
    write.writerow(cabecalho)

for ano in anos:
    with open(csvpath, 'a') as f:
        write = csv.writer(f)
        write.writerows(anos_dict[str(ano)])
        
print(f"Dados salvos em {csvpath}.")
p = input("Digite Y para iniciar o download dos arquivos em PDF ou N para finalizar.")
if p.lower() != "y":
    print("Finalizado.")
    exit()

print("Salvando arquivos PDF")
#Salvando
for ano in anos:
    os.system(f"mkdir -p pdfs/{ano}")    
    artigos = anos_dict[str(ano)]
    for artigo in artigos:
        if not os.path.isfile(f'pdfs/{ano}/{process_file_name(artigo[0])}.pdf'):
            print(f'{artigo[0]} salvo em: pdfs/{ano}/{process_file_name(artigo[0])}.pdf')
            url = process_link(artigo[2])
            r = requests.get(url, stream=True)
            with open(f'pdfs/{ano}/{process_file_name(artigo[0])}.pdf', 'ab') as pdf:
                pdf.write(r.content)
            time.sleep(2)
