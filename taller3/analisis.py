#! /usr/bin/env python3

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def es_udp_cerrado(port_scans: pd.DataFrame) -> pd.Series:
    """
    `es_udp_cerrado` devuelve un `pd.Series` booleano con True si y solo si el
    puerto se halló cerrado para un scan UDP.
    """
    return port_scans["udp"] == "cerrado"


def es_udp_abierto_o_filtrado(port_scans: pd.DataFrame) -> pd.Series:
    """
    `es_udp_abierto_o_filtrado` devuelve un `pd.Series` booleano con True si y
    solo si el puerto fue clasificado como abierto o filtrado.
    """
    return ~es_udp_cerrado(port_scans)


def es_tcp_abierto(port_scans: pd.DataFrame) -> pd.DataFrame:
    contiene_abierto = lambda s: "abierto" in s
    return port_scans["tcp"].apply(contiene_abierto)


def es_tcp_cerrado(port_scans: pd.DataFrame) -> pd.DataFrame:
    contiene_cerrado = lambda s: "cerrado" in s
    return port_scans["tcp"].apply(contiene_cerrado)


def es_tcp_filtrado(port_scans: pd.DataFrame) -> pd.DataFrame:
    contiene_filtrado = lambda s: "filtrado" in s
    return port_scans["tcp"].apply(contiene_filtrado)


def contar_abiertos_y_cerrados_para_cada_timeout(
    port_scans: pd.DataFrame,
) -> pd.DataFrame:

    """
    Devuelve un dataframe con el total de puetos contados para cada estado
    (_cerrado_ vs _abierto ó filtrado_ en el caso de UDP y _abierto_ vs
    _filtrado_ en el caso de TCP)
    """

    estados = pd.DataFrame.from_dict(
        {
            "timeout": port_scans["timeout"],
            "udp_cerrado": es_udp_cerrado(port_scans),
            "udp_abierto_filtrado": es_udp_abierto_o_filtrado(port_scans),
            "tcp_abierto": es_tcp_abierto(port_scans),
            "tcp_cerrado": es_tcp_cerrado(port_scans),
            "tcp_filtrado": es_tcp_filtrado(port_scans),
        }
    )

    return estados.groupby("timeout").sum()


def plot_puertos_abiertos_segun_timeout(port_scans: pd.DataFrame) -> None:
    cant_puertos_abiertos = contar_abiertos_y_cerrados_para_cada_timeout(port_scans)
    cant_puertos_abiertos["udp_abierto_filtrado"].plot(
        legend="Puertos UDP abiertos|filtrados"
    )
    cant_puertos_abiertos["tcp_abierto"].plot(legend="Puertos TCP abiertos")
    plt.legend()


if __name__ == "__main__":

    sns.set(style="white")

    # Abre el archivo especificado en los args.
    if len(sys.argv) < 2:
        print("usage: poetry run python3 analisis.py <results.csv>")
        sys.exit(1)
    filepath = Path(sys.argv[1])
    port_scans = pd.read_csv(filepath)

    # Imprime conteo de estados de puerto para cada timeout.
    print("Puertos Abiertos/Cerrados segun timeout elegido.")
    print(contar_abiertos_y_cerrados_para_cada_timeout(port_scans))

    # Genera el plot con el experimento de variar timeout.
    print("Mostrando plot con cant. puertos abiertos segun timeout elegido.")
    plot_puertos_abiertos_segun_timeout(port_scans)
    path_to_plot = Path(filepath.name + ".png")
    print(f"Se va a guardar en: {str(path_to_plot)}")
    plt.savefig(path_to_plot)
