"""
# Documentacao: https://www.crummy.com/software/BeautifulSoup/bs4/doc.ptbr/

# Site: https://django-anuncios.solyd.com.br/
# Bibliotecas: pip freeze > requirements.txt
"""

# Bibliotecas
import re                       # Para usar expressões regulares para encontrar os números de telefone
from requests import get        # Para fazer as requisições HTTP
from colorama import Fore       # Para colorir as mensagens no terminal
from threading import Thread    # Para permitir múltiplos threads e rodar o código de forma paralela
from bs4 import BeautifulSoup   # Para fazer o parsing HTML das páginas

# URLs
DOMINIO =   "https://django-anuncios.solyd.com.br"              # Dominio base do site
URL =       "https://django-anuncios.solyd.com.br/automoveis/"  # URL específica para a categoria de automóveis

# Variáveis globais de lista para armazenar links e telefones
LINKS = []
TELEFONES = []


# Função: Fazer uma requisição HTTP
def requisicao(url):

    try:

        # Faz a requisição e checa se a resposta tem status 200 (OK)
        resp_html = get(url)

        if resp_html.status_code == 200:

            # Retorna o HTML da página
            return resp_html.text

    except Exception:
        print(f"{Fore.LIGHTRED_EX}Erro de requisicao !{Fore.RESET}")

    return None


# Função: Fazer o parsing do HTML usando BeautifulSoup
def parsing_soup(resp_html):

    try:
        # Cria um objeto BeautifulSoup para manipular o HTML
        return BeautifulSoup(resp_html, "html.parser")

    except Exception:
        print(f"{Fore.LIGHTRED_EX}Erro no Parsing !{Fore.RESET}")

    return None


# Função: Encontrar todos os links dos anúncios na página principal
def encontrar_links(soup):

    try:
        links = []

        # Busca todos os <a> com a classe "card", que representam os links dos anúncios
        a = soup.find_all(name="a", class_="card")

        # Itera sobre os elementos encontrados
        for i in a:

            # Pega o atributo href (link)
            link = i["href"]

            if link:
                links.append(link)

        return links

    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Erro ao encontrar links !{Fore.RESET}")

    return None


# Função: Encontrar os números de telefone em uma página do anúncio
def encontrar_telefones(soup):

    # Expressão regular para encontrar telefones no formato específico
    telefone_regex = r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})"

    try:
        # Busca os elementos onde os telefones estão
        telefone = soup.find_all("div", class_="sixteen wide column")

        # Itera sobre cada elemento encontrado
        for i in telefone:

            # Pega o texto contido no elemento, sem espaços extras
            texto = i.get_text(strip=True)

            # Aplica a regex para encontrar os números de telefone
            regex = re.findall(telefone_regex, texto)

            if regex:
                return regex

    except Exception:
        print(f"{Fore.LIGHTRED_EX}Erro ao encontrar telefones !{Fore.RESET}")

    return None


# Função: Descobrir telefones
def descobrir_telefone():

    while True:

        try:
            # Pega o próximo link de anúncio da lista de LINKS
            links_anuncio = LINKS.pop(0)

            # Faz a requisição para o link do anúncio
            resp_anuncio = requisicao(DOMINIO + links_anuncio)

            if resp_anuncio:

                # Faz o parsing do HTML do anúncio
                soup_anuncio = parsing_soup(resp_anuncio)

                if soup_anuncio:

                    # Tenta encontrar telefones no anúncio
                    telefones = encontrar_telefones(soup_anuncio)

                    if telefones:

                        # Adiciona os telefones encontrados à lista TELEFONES
                        TELEFONES.append(telefones)

                        # Chama a função para salvar os telefones encontrados
                        salvar_telefones(telefones)

        except Exception:
            return None  # Se ocorrer um erro, encerra a função


# Função: Salvar os telefones em um arquivo
def salvar_telefones(tel):

    # Arquivo onde os telefones serão salvos
    arq = "database.csv"
    tel_fmt = f"({tel[0][0]}) {tel[0][1]}-{tel[0][2]}\n"  # Formata o telefone no formato (XX) 9XXXX-XXXX

    try:
        # Abre o arquivo em modo append para adicionar novos dados
        with open(arq, "a") as file:

            # Escreve o telefone formatado no arquivo
            file.write(tel_fmt)

    except Exception:
        print(f"{Fore.LIGHTRED_EX}Erro ao salvar telefone ! {Fore.RESET}")


# Função: Executa o programa
def main():

    # Torna a variável LINKS global
    global LINKS

    # Lista para armazenar as threads
    lista_threads = []

    # Faz a requisição para a página principal
    resposta = requisicao(URL)

    if resposta:

        # Faz o parsing do HTML da página principal
        soup = parsing_soup(resposta)

        if soup:

            # Encontra todos os links de anúncios
            LINKS = encontrar_links(soup)

            print(f"# Buscando telefones ...")

            # Cria 10 threads para buscar os telefones de forma paralela
            for i in range(10):

                # Cria uma thread para executar a função descobrir_telefone
                t = Thread(target=descobrir_telefone)
                lista_threads.append(t)

            # Inicia todas as threads
            for i in lista_threads:
                i.start()

            # Espera todas as threads terminarem
            for i in lista_threads:
                i.join()


# Verifica se o script é o principal e executa a função main()
if __name__ == '__main__':
    main()
