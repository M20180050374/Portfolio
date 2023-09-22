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

  ```Python
  from bs4 import BeautifulSoup  # biblioteca que ler o html da página e permite coletar as informações
  from selenium import webdriver  # biblioteca que permite carregar o js da página (facilita clicks e preenchimentos)
  from selenium.webdriver.edge.options import Options  # importante para carregar algumas definições do navegador
  import numpy as np
  import pandas as pd
  ```


  ```Python
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

```Python
try:
  data_lancamento.append(pagina_anime.find(name='span', class_='date').getText())
except:
  data_lancamento.append(np.nan)
```
Algumas informações também não serão necessiriamente uma string, e sim um conjunto de string, como por exêmplo os gêneros dos animes, nos quais são bem comum ter um anime com mais de um gênero. Nesse projeto vamos optar por unir as strings em uma lista, como mostrado abaixo:

```Python
generos.append([x.getText() for x in pagina_anime.find(name='div', class_='sgeneros').find_all()])
```
  - [x] Coletar os dados de um anime
  - [ ] Passar por todos os animes de uma página
  - [ ] Passar por todas as páginas do site

_Note que estou salvando as informações dentro de uma lista, pois isso facilitará na organização dos dados para geração do arquivo CSV.
_


Após coletar todas as informações de um único anime, vamos tentar passar por todos os anime de uma página

Você irá nota que em muitos sites a listagem de itens nela é uma lista com mesmo Class e contendo vários elemntos. Tudo que precisamos é identificar qual a Class dessa listagem e acessar o link de cada item da lista.

```Python
animes = pagina_principal.find(name='div', id='archive-content').find_all(name='h3')
```
Esse código gera uma lista com todos os animes da página, contendo o nome do anime e o link para página do anime. Tudo que precisamos fazer é solicitar para Selenium abrir o link do primeiro anime, coletar as informações e depois seguir para o próximo anime da lista. O código fica da seguinte maneira:

```Python
 animes = pagina_principal.find(name='div', id='archive-content').find_all(name='h3')
    for anime in animes:
        navegador.get(anime.find(name='a')['href'])  # acessando o link com as informações do anime em questão
        pagina_anime = BeautifulSoup(navegador.page_source, features='html.parser') #    jogando o html agora com a página do anime
```

Agora não vamos mais coletar as informações do anime de uma página qualquer, mas sim da `pagina_anime` que é o anime atual.

  - [x] Coletar os dados de um anime
  - [x] Passar por todos os animes de uma página
  - [ ] Passar por todas as páginas do site

Nossa última etapa então é passar por todas as páginas do site. Essa etapa pode ser feita de várias manerias a depender do site. Muitos sites trabalham com um elemento que permite ser clicado e levado para próxima página e é o caso que vamos trabalhar nesse projeto. 

Ir para próxima página é só mais um elemento que possui um link, logo só precisamos solicitar ao Selenium que abra esse link e passemos o HTML para o Beautiful Soup continuar o código que já escrevemos. Nesse caso em específico, vamos limitar que o código a parar quando ele tentar entrar em um link que já passou. Isso foi necessário, pois ao chegar na última página, o botão de próxima página se tornava o de página anterior, podendo causar um loop infinito e repetição de coleta dos dados.

Para isso só precisamos armazenar o site atual em uma lista e sempre checar se o próximo site já está contido nessa lista (já definimos lá em cima). O código fica o seguinte:

```Python
while site not in paginas_visitadas: #  garantindo a não repetição do site
  animes = pagina_principal.find(name='div', id='archive-content').find_all(name='h3')
      for anime in animes:
          navegador.get(anime.find(name='a')['href'])  # acessando o link com as informações do anime em questão
          pagina_anime = BeautifulSoup(navegador.page_source, features='html.parser') #    jogando o html agora com a página do anime

#[coleta dos dados da página]

  paginas_visitadas.append(site) #  salvando o site atual na lista de sites visitados
  site = pagina_principal.find(name='span', class_='current').find_next('a')['href'] #    atualiza o site para próxima página para repetir o processo
  navegador.get(site) #  para abrir a próxima página
  pagina_principal = BeautifulSoup(navegador.page_source, 'html.parser') #  jogando o html da nova página
```
