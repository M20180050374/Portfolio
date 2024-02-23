from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, inspect


def iniciar():
    navegador = webdriver.Edge()
    navegador.get("https://www.crunchyroll.com/pt-br/videos/alphabetical")
    navegador.maximize_window()
    sleep(1)
    return navegador


def coleta_links(navegador):
    links_animes = []
    while True:
        sleep(1)
        page = navegador.page_source

        pagina = BeautifulSoup(page, 'html.parser')

        links = pagina.find_all('a', class_='horizontal-card__images-wrapper--ufKkO')
        for anime in links:
            links_animes.append(anime.get_attribute_list(key='href')[0])
        navegador.execute_script("arguments[0].scrollIntoView();", navegador.find_elements(By.CLASS_NAME, 'horizontal-card__images-wrapper--ufKkO')[len(links) - 1])
                                
        if "/pt-br/series/GXYZ123/gxyz123" in links_animes:
            break

    links_animes = set(links_animes)
    navegador.quit()
    return links_animes


def coleta_dados_animes(link):
    navegador = webdriver.Edge()
    navegador.get("https://www.crunchyroll.com" + link)
    espera = WebDriverWait(navegador, 10)
    try:
        ultimo_ep = espera.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'playable-card-hover__link--YVbhn')))[-1]
    except:
        return

    try:
        navegador.execute_script("arguments[0].scrollIntoView();", ultimo_ep)
        espera.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[3]/button'))).click()
    except:
        pass

    navegador.execute_script("arguments[0].scrollIntoView();", ultimo_ep)
    navegador.execute_script("window.scrollBy(0, 200);")
    
    pagina = BeautifulSoup(navegador.page_source, 'html.parser')
    
    foto = pagina.find('img', class_='content-image__image--7tGlg content-image__fade--is-ready--5a8us').attrs['src']
    try:
        titulo = pagina.find('h1', class_='heading--nKNOf heading--is-l--zGnGW heading--is-family-type-one--GqBzU title').text
    except:
        titulo = pagina.find('h1', class_='heading--nKNOf heading--is-l--zGnGW heading--is-family-type-one--GqBzU show-title').text

    nota = pagina.find('span', class_='text--gq6o- text--is-heavy--2YygX text--is-m--pqiL- star-rating-average-data__label--TdvQs').text.split(' ')[0]

    votos = pagina.find('span', class_='text--gq6o- text--is-heavy--2YygX text--is-m--pqiL- star-rating-average-data__label--TdvQs').text.split(' ')[1][1:-1]

    resenhas = pagina.find('a', class_='star-rating__reviews-link--lkG9-').span.text.split(' ')[0]

    try:
        resumo = pagina.find('p', class_='text--gq6o- text--is-l--iccTo expandable-section__text---00oG').text
    except:
        resumo = ""

    classificacao = [categoria.text for categoria in pagina.find_all('div', class_='badge--AHVpY genre-badge')]
    
    num_eps = 0
    while True:
        try:
            ultimo_ep = espera.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'playable-card-hover__link--YVbhn')))[-1]
            navegador.execute_script("arguments[0].scrollIntoView();", ultimo_ep)
            navegador.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[3]/button').click()
        except:
            pass

        pagina = BeautifulSoup(navegador.page_source, 'html.parser')
        num_eps += len(pagina.find_all('a', class_='playable-card-hover__link--YVbhn'))

        try:
            if pagina.find('div', attrs={'class':'cta-wrapper state-disabled', 'data-t':'next-season'}) is not None:
                break

            proxima_temporada = navegador.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[4]/div/div[2]')
            navegador.execute_script("arguments[0].scrollIntoView();", navegador.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[4]'))
            navegador.execute_script("window.scrollBy(0, -200);")
            proxima_temporada.click()
        except:
            break
    navegador.quit()
    return foto, titulo, nota, votos, resenhas, resumo, classificacao, num_eps, link


def verifica_votos(valor):
    if 'k' in valor or 'K' in valor:
        return int(float(valor[:-1]) * 1000)
    else:
        return int(valor)
    

navegador = iniciar()
links_animes = coleta_links(navegador)
resultados = []
#   rodando em paralelismo para aumentar eficiência e coletar os dados em um menor tempo
#   basicamente cada thread roda um navegador e coleta os dados individualmente para cada link
resultados.append(Parallel(n_jobs=8)(delayed(coleta_dados_animes)(link) for link in links_animes))
pd_resultados = pd.DataFrame(resultados[0][1:], columns=['Imagem', 'Titulo', 'Nota', 'Votos', 'Resenhas', 'Resumo', 'Categorias', 'Episodios', 'Link'])
pd_resultados['Data de Atualização'] = datetime.today().date()

animes_com_erro = pd_resultados[pd_resultados['Votos'].isnull()]
animes_corretos = pd_resultados.drop(animes_com_erro.index)

animes_corretos['Nota'] = animes_corretos['Nota'].astype(float)
animes_corretos['Votos'] = animes_corretos['Votos'].apply(verifica_votos)
animes_corretos['Resenhas'] = animes_corretos['Resenhas'].astype(int)
animes_corretos['Categorias'] = animes_corretos['Categorias'].apply(lambda x: ','.join(x))
animes_corretos['Episodios'] = animes_corretos['Episodios'].astype(int)
animes_corretos[animes_corretos['Categorias'] == '']['Categorias'] = 'Sem Classificação'

engine = create_engine('postgresql://postgres:88262283@localhost:5432/portfolio')
sql_database = inspect(engine)
tabela_ja_existente = sql_database.has_table('animes', 'anime')

if tabela_ja_existente:
    animes_sql = pd.read_sql_table('animes', engine, 'anime' )

    animes_retirados = animes_sql[~animes_sql['Titulo'].isin(animes_corretos['Titulo'])]
    animes_to_sql = pd.concat([animes_retirados, animes_corretos])
    animes_to_sql.to_sql('animes', engine, 'anime', if_exists='replace')

else:
    animes_corretos.to_sql('animes', engine, 'anime', if_exists='fail', )
