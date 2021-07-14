O código disponível nesse repositório foi produzido e retirado do Google Colaboratory, por esse motivo os arquivos que estão sendo lidos possuem caminho do Google Drive e o código está "fragmentado" em blocos.

# AnimeCom_Clusterization
Processo de limpeza de base de dados e clusterização, a fim de implementar um sistema de indicação de animes com base na descrição fornecida pelo usuário.
Foram utilizados métodos de Natural Language Processing (NLP) e machine learning para a implementação do algoritmo deste repositório.

## Base de dados
A base de dados utilizada foi extraída do MyAnimeList — plataforma online onde você pode catalogar animes ou mangás, obter sugestões,
recomendações, avaliações de animes e mangás e discutir nos fóruns. Se encontra disponível em: https://www.kaggle.com/marlesson/myanimelist-dataset-animes-profiles-reviews.

Inconsistências foram tratadas nas bases de dados, como valores nulos, duplicidades e dados fora do padrão das colunas.

Após o tratamento das inconsistências os reviews fornecidos pelos usuários e disponíveis na base de dados foram empregados nos processos de redução léxica,
lematização e seleção de termos baseado na sua importância nos textos (TF-IDF).

## Clusterização
Posteriormente, aplicamos aos textos "limpos", o algoritmo K-Means, que funciona da seguinte maneira:

Tem como objetivo agrupar os registros da base de dados em k grupos distintos chamados de clusters. Esse agrupamento se baseia na distância entre os dados e os clusters e é
chamado de clustering.
Seu funcionamento consiste inicialmente em gerar de forma aleatória centróides, onde o número de centróides é representado pelo parâmetro k. Esses centróides são pontos de dados
que serão utilizados como pontos centrais dos clusters. Em seguida é calculada a distância entre todos os pontos de dados e cada um dos centróides. Cada registro será atribuído ao
centróides mais próximo formando assim os clusters ( fato importante sobre o algoritmo é que ele tenta fazer os pontos atribuídos aos centróides os mais similares possíveis
enquanto também mantém os centróides os mais diferentes (distantes) possíveis). Assim que forem atribuídas aos centróides mais próximos o passo é recalcular o valor dos centróides,
isto é, o próximo valor do centróide será a média dos valores dos pontos de dados que foram atribuídos à ele. Esse procedimento se repete até que os centróides se tornem estáticos
ou alguma condição de parada tenha sido satisfeita. Os centróides se tornam estáticos quando nenhum dos pontos de dados se alteram com a mudança dos centróides. 

A fim de utilizar o k-means precisamos definir o número de clusters desejados para segregar os dados, para tal empregamos o uso de um procedimento conhecido como Within Clusters
Sum of Squares (WCSS) — método que calcula a quantidade total de clusters através da soma dos quadrados  —,  selecionando o ponto mais estável gerado, conhecido como o cotovelo
do gráfico  — esse método é conhecido como “método do cotovelo”.
Em seguida, aplicamos o k-means e recuperamos os rótulos de cada review juntamente com o uid do anime que esse review está se referindo e exportamos os arquivos .pkl para serem
utilizados no aplicativo Flutter, disponível em: https://github.com/gdias9487/PISI3.

