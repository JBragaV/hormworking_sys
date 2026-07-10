import requests

URL_VIACAO_GARCIA = (
    r"https://sales-api.embarca.ai/api/v1/trips/rio-de-janeiro-novo-rio-rj/sorocaba-sp"
)

params = {
    "departure_at": "2026-07-09",
    "is_round_trip_and_return": "undefined",
    "original_departure_at": "undefined",
    "web_request": "true",
}

headers = {
    "accept": "application/json",
    "accept-language": "pt-BR,pt;q=0.8",
    "origin": "https://passagens.viacaogarcia.com.br",
    "referer": "https://passagens.viacaogarcia.com.br/",
    "user-agent": (
        "Mozilla/5.0 (Linux; Android 15; Pixel 9) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/150.0.0.0 Mobile Safari/537.36"
    ),
    "ngrok-skip-browser-warning": "true",
    "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="150", "Brave";v="150"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1",
    "token_session": "de362c99-4aa0-43de-a33b-1992fea02142",
    "x-api-token": "eyJhbGciOiJIUzI1NiJ9.eyJvcGVyYXRvcl9pZCI6Mn0.WT7RyLm4nKU28suTc9AHqobF_VvlpILJz7B1PYfqUWU",
    "xapikey": "123456789",
}

resp = requests.get(URL_VIACAO_GARCIA, headers=headers, params=params, timeout=30)

print(resp.status_code)

resp.raise_for_status()

viagens_json = resp.json()

viagens = []

for viagem_dict in viagens_json:
    viagens.append(
        {
            "Origem": viagem_dict.get("origin", ""),
            "Destino": viagem_dict.get("destination", ""),
            "partida_em": viagem_dict.get("departure_at", ""),
            "chegada_em": viagem_dict.get("arrival_at", ""),
            "assentos_disponiveis": viagem_dict.get("available_seats", ""),
            "tempo_viagem": f"{viagem_dict.get('hours', '')}:{viagem_dict.get('minutes', '')}",
            "preco_original": viagem_dict.get("original_price", ""),
            "preco": viagem_dict.get("price", ""),
            "tipo_assento": viagem_dict.get("seat_class", "group"),
        }
    )


for viagem in viagens:
    print(viagem)
