import sys
import requests
from geocoder import get_coordinates


API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'
def district(address):
    long,lat = get_coordinates(address)
    print( "long,lat", long,lat)

    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": f"{long},{lat}",
        "kind": "district",
        "format": "json"
    }


        # Выполняем запрос.
    response = requests.get(geocoder_request, params=geocoder_params)
    if response:

        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
                {geocoder_request}
                Http статус: {response.status_code} ({response.reason})""")
    #print(json_response)
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]if features else None
a=district(sys.argv[1])
print(a[-2:][0]['name'], a[-2:][1]['name'])

#b=a.split(',')[-2:]
#print(b)



