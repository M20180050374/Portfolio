# PROJETO ANIMES

  Esse projeto consiste na busca por dados na internet com uso do Selenium e BS4 do Python, alocar esses dados em um banco de dados qualquer para fazer uma análise descritiva utilizando SQL e Python, após isso é feito um dashboard utilizando Power BI e Python (talvez) e, por fim, é feito um projeto de ciência de dados para catalogação dos animes de acordo os dados obtidos e informados.

## [WEB SCRAPING](https://github.com/M20180050374/Portfolio/blob/main/anime/web%20scrapping.py)

  Web Scraping consiste na coleta de dados de sites para ser armazenado em arquivos ou bancos de dados [(ZHAO, 2017)](https://link.springer.com/referenceworkentry/10.1007/978-3-319-32001-4_483-1)

  Portanto, nossa primeira etapa consiste em coletar os dados da internet. Para isso, podemos previamente definir os dados que vamos buscar e procurar algum site que atenda a demanda, ou verificar nos sites o que mais conter dados e assim optar por ele.
  
  Para esse projeto definimos previamente os dados que vamos buscar e depois procuramos um site que atendesse a tal requisito. O site escolhido foi o [Animes BR](https://animesbr.cc). Os dados a serem consultados foram:
  - Nome do anime
  - Data de lançamento
  - Emissora
  - Avaliação (nota)
  - Quantidade de votos
  - Gênero(s)
  - Resumo
  - Quantidade de episódios
  
  Após isso só precisamos 'passar' por cada anime do site e coletar as informações, jogar essas informações em um pandas e um csv para exportar.

  ### ETAPAS
  Vamos dividir o web scraping em 3 etapas:
  - [ ] Coletar os dados de um anime
  - [ ] Passar por todos os animes de uma página
  - [ ] Passar por todas as páginas do site

  Vale salientar que já vi projetos assim serem executados em ordens distintas, mas eu prefiro executar como está na lista, mesmo que a ordem final do código seja divergente.

  Antes de tudo, vamos definir algumas variáveis padrões, importar nossas bibliotecas e configurar nosso ambiente

  ```python
  from bs4 import BeautifulSoup  # biblioteca que ler o html da página e permite coletar as informações
  from selenium import webdriver  # biblioteca que permite carregar o js da página (facilita clicks e preenchimentos)
  from selenium.webdriver.edge.options import Options  # importante para carregar algumas definições do navegador
  import numpy as np
  import pandas as pd
  ```


  ```python
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
  ```

  #### Coletando dados do anime
  
  Para coletar as informações da página do anime, basta inspecionar o html da página na informação que você deseja coletar e verificar qual melhor maneira de buscar aquele elemento HTML. O Beautiful Soup tem várias opções de busca como por XPATH, ID, Class e várias outras. 
  
  Para esse projeto vamos utilizar a busca por Class, que basicamente é um código que permiti diferenciar de outros tipos iguais (procurem por HTML do professor guanabara).

  Vamos utilizar a função find do Beautiful Soup para procurar o elemento por tipo (div, span, h3) e a Class, logo temos:  `html.find(tipo=tipo, class_=class)`

  Note que precisamos definir previamente uma variável com a página html para que seja possível fazer a busca. Para isso vamos pegar o site de um anime qualquer e abrir com a biblioteca Selenium (webdriver) que definimos anteriormente: `navegador = webdriver.Edge(options=options)` Assim conseguimos abrir o navegador. `navegador.get(site_do_anime)` Aqui mandamos ele abrir o site e aqui salvamos a informação do HTML da página para o Beautiful Soup `pagina_anime = BeautifulSoup(navegador.page_source, features='html.parser')`

  Com o HTML definido, bastante utilizar o find e salvar o elemento desejado: `nome.append(pagina_anime.find(name='span', class_='breadcrumb_last').getText())`.  `get.Text()` permite pegar somente o elemento de texto, que, nesse caso, é o nome do anime.

  Em alguns momentos o que você busca na página não estará disponível, simplesmente por não existir aquela informação. Para tratar isso, utilizei o `try` e o `except` do Python e assim retornando `np.nan` (vazio) no que não fosse encontrado, observe:

```python
try:
  data_lancamento.append(pagina_anime.find(name='span', class_='date').getText())
except:
  data_lancamento.append(np.nan)
```
