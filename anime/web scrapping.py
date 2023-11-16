from bs4 import BeautifulSoup  # biblioteca que ler o html da página e permite coletar as informações
from selenium import webdriver  # biblioteca que permite carregar o js da página (facilita clicks e preenchimentos)
from selenium.webdriver.edge.options import Options  # importante para carregar algumas definições do navegador
import numpy as np

options = Options()
options.add_argument("--start-minimized")  # para ir testando, não gosto de abrir o navegador sempre

''' com site definido, vamos abrir ele e entender o seu html, os navegadores permite que você verifique o html de 
    qualquer site e entender como a disposição das informações podem ser encontradas como uma espécie de vetor,
    logo o seu objetivo é encontrar uma maneira de iterar nas informações que você deseja.'''

#   lista de informações que conseguimos retirar do site
nome = []
data_lancamento = []
emissora = []
nota = []
votos = []
generos = []
resumo = []
qtd_eps = []

paginas_visitadas = [] #    uma lista com os links da páginas que visitamos para garantir não visitar a mesma página

site = 'https://animesbr.cc/anime/' #    definição do site

navegador = webdriver.Edge(options=options) #    inicia o navegador com as opções deifinidas
navegador.get(site) #     Abre a página que informamos

pagina_principal = BeautifulSoup(navegador.page_source, 'html.parser') #    pega o html da página e joga para o BS4 trabalhar
while site not in paginas_visitadas:

    ''' A página inicial é um vetor com o nome do anime e o link de acesso a ele,
        vamos iterar nessa lista e acessar cada anime'''
    animes = pagina_principal.find(name='div', id='archive-content').find_all(name='h3')
    for anime in animes:
        navegador.get(anime.find(name='a')['href'])  # acessando o link com as informações do anime em questão
        pagina_anime = BeautifulSoup(navegador.page_source, features='html.parser') #    jogando o html agora com a página do anime

        ''' É nessa página que contém as informações que desejamos obter, portanto vamos inspecionar cada elemento
            e entender como acessar essa informações pelo html. Note que coloquei vários try para evitar erros de algum anime não possuir as informações que desejamos
            Se aplicarmos uma função o código não ficaria melhor?'''
        nome.append(pagina_anime.find(name='span', class_='breadcrumb_last').getText())
        try:
            data_lancamento.append(pagina_anime.find(name='span', class_='date').getText())
        except:
            data_lancamento.append(np.nan)

        ''' É importante entender o tipo de informação que estamos raspando, ao vasculhar alguns animes pude identificar
            que alguns animes foram exibidos em mais de uma emissora, logo não poderia armazenar como uma string.
            Então procure observar e tentar abranger o máximo de variáveis possíveis'''
        try:
            emissoras = pagina_anime.find(name='div', class_='extra')  # gera duas span
            emissora.append(", ".join([x.getText() for x in emissoras.select('div.extra span:nth-child(2)')[0].find_all()])) #    um vetor com todas as emissoras
        except:
            emissora.append(np.nan)

        try:
            nota.append(pagina_anime.find(name='span', class_='dt_rating_vgs').getText())
        except:
            nota.append(np.nan)

        try:
            votos.append(pagina_anime.find(name='span', class_='rating-count').getText())
        except:
            votos.append(np.nan)

        ''' Mesma situação das emissoras, um anime pode ter vários gêneros associados e class "sgeneros" possue todos eles
            por isso crio um vetor com todos os resultados desse trecho do html'''
        generos.append(", ".join([x.getText() for x in pagina_anime.find(name='div', class_='sgeneros').find_all()]))

        try:
            resumo.append(pagina_anime.find(name='div', class_='single_tabs').find(name='p').getText())
        except:
            resumo.append(np.nan)

        try:
            qtd_eps.append(len(pagina_anime.find(name='ul', class_='episodios')))
        except:
            qtd_eps.append(np.nan)

    paginas_visitadas.append(site) # adiciona o site na lista de sites visitados
    site = pagina_principal.find(name='span', class_='current').find_next('a')['href'] #    atualiza o site para próxima página para repetir o processo
    navegador.get(site) #    abrir a próxima página
    pagina_principal = BeautifulSoup(navegador.page_source, 'html.parser') #    jogando html do novo site


''' Após raspar todos os dados, jogamos em um pandas e depois exportamos em um csv
    Vamos fazer algumas operações para que fique de acordo com o banco de dados criado.
    Precisamos garantir os tipos dos dados, retirar os dados que estão em listas e separa-los por ",". '''
import pandas as pd

dados = {"nome": nome,
         "qtd_eps": qtd_eps,
         "emissao_date": data_lancamento,
         "emissoras": emissora,
         "nota": nota,
         "votos": votos,
         "generos": generos,
         "resumo": resumo}


dados_df = pd.DataFrame(dados)

dados_df.info

dados_df['qtd_eps'] = dados_df['qtd_eps'].astype(int, errors='ignore')
dados_df['emissao_date'] = pd.to_datetime(dados_df['emissao_date'], errors='ignore')
dados_df['nota'] = dados_df['nota'].astype(float, errors='ignore')
dados_df['votos'] = dados_df['votos'].str.replace(',','').astype(int, errors='ignore')

dados_df.to_excel('C:\\Projetos\\projetos_portfolio\\Portfolio.xlsx', index=False)
dados_df.to_csv('C:\\Projetos\\projetos_portfolio\\Portfolio.csv', sep="|", index=False)
