# LoL Analytics

Um sistema de análise de dados de partidas de League of Legends que coleta informações da API oficial da Riot Games, processa esses dados e gera visualizações informativas sobre o desempenho dos campeões por classes e lanes.

## Estrutura do Projeto

O projeto está organizado nos seguintes arquivos:

- **analytics.py**: Contém funções para comunicação com a API da Riot Games
- **main.py**: Ponto de entrada principal do programa, com menu interativo
- **visualizacao.py**: Módulo para geração de visualizações gráficas e análises estatísticas

## Requisitos

Para executar este projeto, você precisará de:

1. Python 3.6 ou superior
2. As seguintes bibliotecas Python:
   - requests
   - pandas
   - matplotlib
   - seaborn
   - numpy

Você pode instalar as dependências usando o seguinte comando:

```bash
pip install requests pandas matplotlib seaborn numpy
```

3. Uma chave de API da Riot Games, que pode ser obtida em: https://developer.riotgames.com/

## Como Usar

1. Clone este repositório ou baixe os arquivos
2. Instale as dependências necessárias
3. Execute o programa usando:

```bash
python main.py
```

4. No menu principal, você terá as seguintes opções:
   - **Coletar dados de partidas**: Coleta dados da API da Riot e salva em um arquivo CSV
   - **Atualizar chave de API**: Atualiza sua chave de API da Riot
   - **Visualização de dados**: Abre o menu de visualizações para analisar os dados coletados
   - **Sair**: Encerra o programa

## Funcionalidades

### Coleta de Dados
- Coleta dados de jogadores de diferentes ligas (Challenger, Grandmaster, Master)
- Extrai informações das partidas recentes desses jogadores
- Salva os dados em formato CSV para análise posterior

### Visualizações
- **Distribuição de classes de campeões**: Mostra a quantidade de campeões por classe
- **Desempenho por classe**: Compara métricas como kills, deaths, assistências entre diferentes classes
- **Matriz de correlação**: Exibe correlações entre diferentes métricas de desempenho
- **Desempenho por lane**: Compara métricas de desempenho entre diferentes lanes
- **Campeões populares**: Mostra os campeões mais jogados no conjunto de dados
- **Resumo estatístico**: Fornece estatísticas descritivas sobre as métricas coletadas

## Sobre a API da Riot

Este projeto utiliza a API oficial da Riot Games para League of Legends. Alguns pontos importantes:

- A API possui limites de requisições (rate limits)
- Sua chave de API expira a cada 24 horas
- Certifique-se de respeitar os Termos de Serviço da Riot Games

## Observações

- O projeto inclui um dicionário de mapeamento entre campeões e suas classes
- As requisições à API contêm pausas para respeitar os limites de taxa da Riot
- Os dados são filtrados para incluir apenas partidas com informações completas

## Contribuições

Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request. 