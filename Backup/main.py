"""
# Documentacao: https://www.crummy.com/software/BeautifulSoup/bs4/doc.ptbr/
"""

# Criar menu para forma de procura: Automoveis, e etc.
# pip freeze > requirements.txt
# \(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})

# Bibliotecas
import re
from threading import Thread
from requests import get
from bs4 import BeautifulSoup

# URLs
DOMINIO = "https://django-anuncios.solyd.com.br"
URL = "https://django-anuncios.solyd.com.br/automoveis/"

LINKS = []
TELEFONES = []

def requisicao(url):

    try:
        resposta = get(url)

        if resposta.status_code == 200:
            resposta_html = resposta.text

            return resposta_html

        else:
            print("Erro ao fazer a requisicao !")

    except Exception as e:
        print(f"Erro desconhecido: {e}")

    return None

def parsing_html(resposta_html):

    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')

        return soup

    except Exception as e:
        print(e)

    return None

def encontrar_links(soup):

    try:
        links = []

        busca_1 = soup.find("div", class_="ui three doubling link cards")
        busca_2 = busca_1.find_all("a")

        for i in busca_2:
            links.append(i["href"])

        return links

    except Exception as e:
        print("Erro ao encontrar links ! ")
        return None

def encontrar_telefones(soup):

    try:
        busca_all = soup.find_all("div", class_="sixteen wide column")
        busca_paragrafo = busca_all[2].p.get_text(strip=True)

        exp_reg= r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})"
        regex = re.findall(exp_reg, busca_paragrafo)

        # for i in regex:
        #     print(f"Celulares: ({i[0]}) {i[1]}-{i[2]}")

        if regex:
            return regex

    except Exception:
        print("Erro ao encontrar telefones !")
        return None

def descobrir_telefones():

    while True:

        try:
            link_anuncio = LINKS.pop(0)

            resposta_anuncio = requisicao(DOMINIO + link_anuncio)

            if resposta_anuncio:
                soup_anuncio = parsing_html(resposta_anuncio)

                if soup_anuncio:
                    telefones = encontrar_telefones(soup_anuncio)

                    if telefones:
                        TELEFONES.append(telefones)
                        salvar_telefones(telefones)

        except Exception:
            return None

def salvar_telefones(tel):

    tel_fmt = f"({tel[0][0]}) {tel[0][1]}-{tel[0][2]}\n"

    try:

        with open("telefones.csv", "a") as file:
            file.write(tel_fmt)

    except Exception as e:
        print(e)

def main():

    global LINKS
    global TELEFONES

    resposta_busca = requisicao(URL)

    if resposta_busca:
        soup_busca = parsing_html(resposta_busca)

        if soup_busca:
            LINKS = encontrar_links(soup_busca)

            print(f"# Buscando telefones ...")

            lista_threads = []
            for i in range(10):
                t = Thread(target=descobrir_telefones)
                lista_threads.append(t)

            for i in lista_threads:
                i.start()

            for i in lista_threads:
                i.join()


if __name__ == '__main__':
    main()