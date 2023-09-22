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

  #### Coletando dados do anime
  
