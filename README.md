# Portfolio

Portfolio pessoal de aplicações de meus conhecimentos na resolução de problemas/curiosidades da vida pessoal.

## [Animes](crunchyroll)
O intuito do projeto é entender mais sobre os animes, quantos temos, quais são suas categorias, distribuição de episódios e afins. Para isso utilizamos o site da Crunchyroll
que possui uma gama vasta de vários animes no qual podemos coletar bastante informação. Após entender essa distribuição, vamos tentar sugerir alguns animes de acordo com os que eu já assisti
levando em consideração alguns pontos (ainda a definir) e, assim, conseguir classificar as sugestões.

Esse projeto é dividido em 4 etapas, nas quais são: coleta dos dados, análise dos dados (python e Power BI) e uma espécie de classificação utilizando ciência dos dados.

### Coleta dos dados
A etapa de coleta de dados foi utilizando Python, especificamente a biblioteca selenium e Beautifulsoup por meio do acesso e requisação dos sites e seus respectivos html.
A partir do html coletei cada tag desejada e, ao fim, exportei os dados para um banco de dados postgre. Ele servirá como base para noissa segunda etapa, a análise dos dados.
