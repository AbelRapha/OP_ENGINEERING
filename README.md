## 🗺️ OR Engineering

OR Engineering é uma aplicação interativa desenvolvida com Streamlit que permite mapear e calcular distâncias entre múltiplos pontos de origem e destino utilizando dados da API do OpenStreetMap (OSM). O projeto é ideal para análises logísticas, planejamento de rotas, Pesquisa Operacional e qualquer cenário que envolva geolocalização.

🚀 Funcionalidades

📍 Entrada de múltiplos endereços de origem e destino

🌐 Geocodificação automática via API Nominatim (OpenStreetMap)

🧭 Cálculo de matriz de distância ou tempo via OSRM (Open Source Routing Machine)

📊 Exportação dos resultados em formato Excel ou CSV



## 🧠 Como funciona

Entrada de dados: O usuário insere listas de endereços de origem e destino.

Geocodificação: Cada endereço é convertido em coordenadas geográficas (latitude e longitude) usando a API Nominatim.

Cálculo de matriz: As coordenadas são enviadas para a API OSRM, que retorna uma matriz de distâncias ou tempos entre todos os pontos.

Download: O usuário pode baixar os resultados em Excel ou CSV para análise posterior.

## 🛠️ Tecnologias utilizadas

Streamlit – Interface interativa

OpenStreetMap – Base de dados geográficos

Nominatim – Geocodificação de endereços

OSRM – Cálculo de rotas e matrizes

Python (requests, pandas, StringIO)

## 📦 Instalação

```
git clone https://github.com/seu-usuario/op-engineering.git
cd map-engineering
pip install -r requirements.txt
streamlit run app.py
```

## ✍️ Exemplo de uso

Insira os endereços de origem e destino no campo apropriado.

Clique em "Calcular Matriz".

Aguarde a geocodificação e o cálculo da matriz.

Baixe o resultado no formato desejado.

## ⚠️ Observações

A API Nominatim possui limites de uso.

Endereços mal formatados ou não mapeados no OSM podem gerar erros de geocodificação.

Para maior precisão, inclua cidade, estado e país nos endereços.

```
Ex. Avenida Paulista, São Paulo, São Paulo, Brasil
```