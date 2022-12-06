from django.shortcuts import render
import requests_cache
import json


def home(request):
    discount_game_list = process_game_information()
    data = {'discount_game_list': discount_game_list}

    return render(request, 'index.html', data)


def process_game_information():
    discount_game_list = []
    json_steamspy = requests_cache.CachedSession('cache_json_steamspy')
    json_steam = requests_cache.CachedSession('cache_json_steam')
    datas_steamspy_raw = json_steamspy.get("https://steamspy.com/api.php?request=top100in2weeks")
    datas_steamspy = json.loads(datas_steamspy_raw.text)

    for i in datas_steamspy:
        if int(datas_steamspy[i]['discount']) != 0:
            datas_steam_raw = json_steam.get("https://store.steampowered.com/api/appdetails?appids=" + i)
            datas_steam = json.loads(datas_steam_raw.text)
            data = datas_steam[i]['data']

            temp = {
                'appid': i,
                'name': data['name'],
                'header_image': data['header_image'],
                'price': data['price_overview']['final_formatted'][2:],
                'initialprice': data['price_overview']['initial_formatted'][2:],
                'discount': data['price_overview']['discount_percent']
            }
            discount_game_list.append(temp)

    return discount_game_list