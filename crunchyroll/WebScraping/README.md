# WEBSCRAPING

WebScraping consiste, basicamente, na raspagem de dados. Ou seja, vamos tentar visitar páginas na internet e coletar o máximo de informações possível.
Neste caso em específico, vamos coletar dados sobre animes e escolhemos o site da [Crunchyroll](https://www.crunchyroll.com/pt-br/videos/alphabetical) para fazer essa raspagem.

Existem diversas maneiras de se começar um projeto de raspagem de dados, seja definindo os dados que vai raspar e depois procurando uma fonte com os dados ou caminho inverso
definindo a fonte e depois os dados que o site possui e podemos coletar, que foi o caso utilizado nesse projeto.

O processo de raspagem é feito na busca dos dados anexados os HTML, no qual é responsávle pela estrutura de exibição dos sites. Então, se há uma informação exibida no site, essa informação também
está dentro do HTML. O que precisamos fazer é acessar o site, pegar o HTML dele e procurar exatamente onde está a informação desejada. HTML não é uma linguagem de programação, é uma linguagem de marcação 
e segue uma estruturação firme para exposição dos dados, nas chamadas TAGs. Quer entender mais sobre HTML? Assista os vídeos do [Professor Guanabara](https://www.youtube.com/@CursoemVideo)

Entretanto, as empresas buscam aperfeiçoar seus sites utilizando linguagem de programação para tentar dinamizar os sites, fazendo com que o HTML esteja em constante mudança, o que dificulta
nossa raspagem. Por isso a biblioteca selenium é importante nessa raspagem, pois nos permite utilizar o navegador de uma maneira que a linguagem de programação do site seja executada e altere o HTML
e assim teremos tudo o que precisamos.

Isso fica claro no início do projeto no qual foi necessário rolar a página pouco a pouco, pois o HTML da página era atualizado conforme a rolagem, portanto precisamos rolar a página inteira para conseguir
todos os links individuais dos animes.

A primeira etapa de coleta dos links individuais coleta cerca de 1500 links que vamos precisar acessar para coletar as informações de cada anime. Devido a necessidade de esperar carregar a página para
conseguir gerar o HTML e, ainda, necessitar fazer alguns cliques para carregar outras informações, a coleta de um único anime. O tempo médio de coleta de um anime estava em torno de 15 segundos, 
fazer isso individualmente, ou seja, de uma maneira linear, levaria mais de 6 horas. Por isso executamos o código utilizando 8 threads, fazendo com o que a coleta fosse feita em 8 links ao mesmo tempo, 
otimizando bastante o tempo final do código.

Além disso fazemos pequenos tratamentos nos dados para que as análises futuras sejam facilitadas, garantindo os tipos de dados de cada coluna e, ao fim, jogamos a tabela final em um banco de dados postgree
que será nossa fonte de dados da análise.
