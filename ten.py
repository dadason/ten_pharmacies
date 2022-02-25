
import os
import sys

from business import find_businesses
from distance import lonlat_distance
from geocoder import get_coordinates, get_ll_span
from mapapi_PG import show_map
import requests
import pygame
import json
map_param = []

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def main():
    name=[]
    address=[]
    time=[]
    distance=[]
    pt = []
    toponym_to_find = input('Что будем искать?\n')

    # Формируем параметры запроса по основнуму адресу
    ll, spn = get_ll_span(toponym_to_find)
    lon,lat = map(float, ll.split(","))
    #print('long lat',lon, lat,)

    # Получаем координаты 10 ближайших аптек.


    organizations= find_businesses(ll, spn, "аптека")
    #print(find_businesses(ll, spn, "аптека"))
    i = 0
    for organization in organizations:

        #print(organization["properties"]["name"])
        point = organization["geometry"]["coordinates"]
        org_lat = float(point[1])
        org_lon = float(point[0])
        max_len = 20

      #Сниппет
     # Название организации.
        #print(i)
        name.append(organization["properties"]["CompanyMetaData"]["name"])
#     # Адрес организации.
        address.append(organization["properties"]["CompanyMetaData"]["address"])
#     # Время работы
        if organization.get("properties",{}).get("CompanyMetaData", {}).get("Hours",{}).get("text", 0):
            time.append(organization["properties"]["CompanyMetaData"]["Hours"]["text"])
        else: time.append(0)
#     # Расстояние
        distance.append(round(lonlat_distance((lon, lat), (org_lon, org_lat))))
        #print(name,'\n',distance,'\n', time,'\n', address)
        point = organization["geometry"]["coordinates"]
        org_lat = float(point[0])
        org_lon = float(point[1])
        if time[i] == "ежедневно, круглосуточно":
            #print('yes!!')
            pt.append(f"{org_lat},{org_lon},pm2gnl24")
        elif time[i]=="0":
            pt.append(f"{org_lat},{org_lon},pmgrs")
        else:
            pt.append(f"{org_lat},{org_lon},pmbls")


        i+=1
        if i == max_len:
            break
    most_distant_farmacy_index= distance.index(max(distance))
    #print('most_distant_farmacy_index=', most_distant_farmacy_index)
    most_distant_farmacy_name= name[int(most_distant_farmacy_index)]
    most_distant_farmacy_address = address[int(most_distant_farmacy_index)]
    org_long,org_lat = get_coordinates(most_distant_farmacy_address)
    #print("farthestfarm",org_long,org_lat )

    map_param = {
            "ll": ll,

            "l": "map",
            "pt": "~".join(pt)
        }

#     # print(map_param)

    show_map(params=map_param,text=None)


if __name__ == "__main__":
    main()
