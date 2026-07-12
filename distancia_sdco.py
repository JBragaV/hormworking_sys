"""
Calcula a distância entre um bairro de Sorocaba (informado pelo usuário)
e uma localidade fixa definida diretamente no código.

Requisitos:
    pip install geopy

Uso:
    python distancia_bairro_sorocaba.py
"""

from geopy.geocoders import Nominatim
from geopy.distance import geodesic


# ----------------------------------------------------------------------
# 1) LOCALIDADE DE DESTINO - altere aqui para o local que você quiser.
#    Pode ser um endereço, um ponto turístico, uma cidade etc.
# ----------------------------------------------------------------------
LOCALIDADE_DESTINO = "Avenida Adhemar de Barros, Vila Trujillo, Sorocaba - SP"

# Dica: o Nominatim (OpenStreetMap) é sensível ao nome OFICIAL do logradouro.
# Evite prefixos como "Doutor", "Dr.", "Av." etc se não tiver certeza de que
# é assim que consta no OpenStreetMap. Prefira o nome mais simples possível
# (ex: "Avenida Adhemar de Barros" em vez de "Av. Dr. Adhemar de Barros").
# Se quiser conferir o nome oficial de uma rua, procure por ela no site
# https://www.openstreetmap.org antes de colocar aqui.


def simplificar_titulos(endereco):
    """
    Remove prefixos/títulos que costumam divergir do nome oficial no OSM
    (ex: "Doutor", "Dr.", "Professor", "Prof.", "Engenheiro", "Eng.").
    """
    prefixos = [
        "Doutor ", "Dr. ", "Dr ",
        "Professor ", "Prof. ", "Prof ",
        "Engenheiro ", "Eng. ", "Eng ",
        "Coronel ", "Cel. ", "Cel ",
        "Capitão ", "Cap. ", "Cap ",
        "General ", "Gen. ", "Gen ",
    ]
    resultado = endereco
    for prefixo in prefixos:
        resultado = resultado.replace(prefixo, "")
    return resultado


def obter_coordenadas(geolocator, endereco, tentativas_extras=None, debug=True):
    """
    Busca latitude/longitude de um endereço usando o Nominatim (OpenStreetMap).

    O Nominatim costuma falhar em endereços muito específicos (com número,
    abreviações como "Av.", títulos como "Doutor", etc). Por isso, se a busca
    inicial falhar, tentamos variações mais genéricas do mesmo endereço.
    """
    tentativas_extras = tentativas_extras or []
    tentativas_extras.append(simplificar_titulos(endereco))

    tentativas = [endereco] + tentativas_extras

    for tentativa in tentativas:
        if debug:
            print(f"  tentando: '{tentativa}' ...", end=" ")
        localizacao = geolocator.geocode(
            tentativa, timeout=10, country_codes="br"
        )
        if localizacao is not None:
            if debug:
                print("OK ✔")
            return (localizacao.latitude, localizacao.longitude)
        if debug:
            print("não encontrado ✘")

    raise ValueError(
        f"Não foi possível encontrar o endereço: '{endereco}' "
        f"(nem as variações tentadas: {tentativas_extras})"
    )


def gerar_variacoes_bairro(bairro):
    """Gera variações do endereço do bairro, da mais específica para a mais genérica."""
    return [
        f"{bairro}, Sorocaba, São Paulo, Brasil",
        f"Bairro {bairro}, Sorocaba, SP",
        f"{bairro}, Sorocaba",
    ]


def calcular_distancia(origem, destino):
    """Retorna a distância em km entre duas coordenadas (lat, lon)."""
    return geodesic(origem, destino).km


def main():
    geolocator = Nominatim(user_agent="distancia_sorocaba_app")

    bairro = input("Informe o nome do bairro de Sorocaba: ").strip()
    endereco_bairro = f"{bairro}, Sorocaba, SP, Brasil"
    variacoes_bairro = gerar_variacoes_bairro(bairro)

    # Se a localidade de destino tiver número de rua, geramos uma variação
    # sem o número como plano B (ex: remove ", 295" do endereço).
    destino_sem_numero = LOCALIDADE_DESTINO.split(",")
    destino_sem_numero = (
        f"{destino_sem_numero[0]}, {', '.join(destino_sem_numero[2:])}"
        if len(destino_sem_numero) > 2
        else LOCALIDADE_DESTINO
    )

    print("\nBuscando coordenadas, aguarde...")

    try:
        coord_bairro = obter_coordenadas(
            geolocator, endereco_bairro, tentativas_extras=variacoes_bairro
        )
        coord_destino = obter_coordenadas(
            geolocator,
            LOCALIDADE_DESTINO,
            tentativas_extras=[destino_sem_numero],
        )
    except ValueError as erro:
        print(f"Erro: {erro}")
        print(
            "\nDica: o Nominatim (OpenStreetMap) às vezes não reconhece "
            "endereços com número de rua ou abreviações (Av., R., etc). "
            "Tente informar só o nome do bairro, sem número e sem abreviações."
        )
        return

    distancia_km = calcular_distancia(coord_bairro, coord_destino)

    print(f"\nBairro informado: {bairro}")
    print(f"Coordenadas do bairro: {coord_bairro}")
    print(f"Localidade de destino: {LOCALIDADE_DESTINO}")
    print(f"Coordenadas do destino: {coord_destino}")
    print(f"\nDistância em linha reta: {distancia_km:.2f} km")


if __name__ == "__main__":
    main()
