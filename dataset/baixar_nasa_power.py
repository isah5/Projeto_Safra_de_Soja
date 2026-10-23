"""
Previsão de Produtividade Municipal da Soja no RS
Integrantes:
Orientador:

Síntese do conteúdo deste arquivo: baixa da API pública do NASA POWER (sem
token) o clima diário 2000–2025 das células da grade que cobrem os 497
municípios do RS (chuva, temperatura média/máxima/mínima, ponto de orvalho e
umidade relativa média). A grade do POWER (MERRA-2) tem células de 0,5° de
latitude × 0,625° de longitude, e todos os pontos de uma célula recebem o
mesmo valor; por isso cada município é associado à célula que o contém e
cada célula é baixada uma única vez (87 células). Guarda só os meses de
outubro a maio (janela da safra de soja usada nos notebooks). Gera:
  - dataset/raw/nasa_power_rs_2000_2025.csv (célula × dia)
  - dataset/raw/nasa_power_celulas_municipios_rs.csv (município → célula)

Uso (a partir da raiz do repositório): python dataset/baixar_nasa_power.py

Histórico de alterações:
Data       | Autor           | Descrição
-----------|-----------------|--------------------------------------------
2026-10-23 |                 | Criação do script
"""
import json
import time
import urllib.request

import numpy as np
import pandas as pd

RAW = "dataset/raw"
URL = ("https://power.larc.nasa.gov/api/temporal/daily/point"
       "?parameters=PRECTOTCORR,T2M,T2M_MAX,T2M_MIN,T2MDEW,RH2M&community=AG"
       "&latitude={lat}&longitude={lon}&start=20000101&end=20251231&format=JSON")
COLUNAS = {"PRECTOTCORR": "chuva_mm", "T2M": "t2m_c", "T2M_MAX": "tmax_c",
           "T2M_MIN": "tmin_c", "T2MDEW": "tdew_c", "RH2M": "rh2m_pct"}
MESES_SAFRA = [10, 11, 12, 1, 2, 3, 4, 5]
PASSO_LAT, PASSO_LON = 0.5, 0.625


def baixar(lat, lon, tentativas=3):
    for i in range(tentativas):
        try:
            with urllib.request.urlopen(URL.format(lat=lat, lon=lon), timeout=120) as r:
                dados = json.load(r)
            fill = dados["header"]["fill_value"]
            d = pd.DataFrame(dados["properties"]["parameter"]).rename(columns=COLUNAS)
            return d.replace(fill, np.nan)
        except Exception as erro:
            print(f"  tentativa {i + 1} falhou ({erro}); tentando de novo")
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"não foi possível baixar a célula {lat}, {lon}")


# Município -> célula da grade que o contém (mesmo filtro de UF dos notebooks)
coords = pd.read_csv(f"{RAW}/municipios_brasil_coords.csv")
coords = coords[coords["codigo_uf"] == 43]
mapa = pd.DataFrame({
    "codigo_ibge_municipio": coords["codigo_ibge"],
    "lat_celula": (np.round(coords["latitude"] / PASSO_LAT) * PASSO_LAT).round(3),
    "lon_celula": (np.round(coords["longitude"] / PASSO_LON) * PASSO_LON).round(4),
})
mapa.to_csv(f"{RAW}/nasa_power_celulas_municipios_rs.csv", index=False)
celulas = mapa[["lat_celula", "lon_celula"]].drop_duplicates().to_numpy()
print(f"{len(mapa)} municípios em {len(celulas)} células")

partes = []
for i, (lat, lon) in enumerate(celulas, 1):
    print(f"[{i}/{len(celulas)}] célula {lat}, {lon}")
    d = baixar(lat, lon)
    d.index = pd.to_datetime(d.index, format="%Y%m%d")
    d = d[d.index.month.isin(MESES_SAFRA)]
    partes.append(d.rename_axis("data").reset_index().assign(lat_celula=lat, lon_celula=lon))
    time.sleep(1)  # pausa entre consultas, para não sobrecarregar o servidor

saida = pd.concat(partes, ignore_index=True)
saida = saida[["lat_celula", "lon_celula", "data"] + list(COLUNAS.values())]
saida[list(COLUNAS.values())] = saida[list(COLUNAS.values())].round(2)
saida.to_csv(f"{RAW}/nasa_power_rs_2000_2025.csv", index=False)
print(f"Salvo: {len(saida):,} linhas em {RAW}/nasa_power_rs_2000_2025.csv")
