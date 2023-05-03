import requests
import os
#p2 = Solo
#p10 = Duo
#p9 = Squad

def get_solo_stats(username, platform):
    url = "https://api.fortnitetracker.com/v1/profile/{}/{}".format(platform, username)
    headers = {'TRN-Api-Key' : os.getenv("TRN-Api-Key")}
    r = requests.get(url, headers=headers)

    try:

        #SOLOS
        solo_wins = r.json()['stats']['p2']['top1']['value']
        solo_kills = r.json()['stats']['p2']['kills']['value']
        solo_kd = r.json()['stats']['p2']['kd']['value']
        solo_matches = r.json()['stats']['p2']['matches']['value']

        solo_stats = []
        solo_stats.extend((int(solo_wins), int(solo_kills), float(solo_kd), int(solo_matches)))

        return solo_stats

    except:
        return False

def get_duo_stats(username, platform):
    url = "https://api.fortnitetracker.com/v1/profile/{}/{}".format(platform, username)
    headers = {'TRN-Api-Key' : os.getenv("TRN-Api-Key")}

    r = requests.get(url, headers=headers)

    try:

        #DUOS
        duo_wins = r.json()['stats']['p10']['top1']['value']
        duo_kills = r.json()['stats']['p10']['kills']['value']
        duo_kd = r.json()['stats']['p10']['kd']['value']
        duo_matches = r.json()['stats']['p10']['matches']['value']

        duo_stats = []
        duo_stats.extend((int(duo_wins), int(duo_kills), float(duo_kd), int(duo_matches)))

        return duo_stats

    except:
        return False

def get_squad_stats(username, platform):
    url = "https://api.fortnitetracker.com/v1/profile/{}/{}".format(platform, username)
    headers = {'TRN-Api-Key' : os.getenv("TRN-Api-Key")}

    r = requests.get(url, headers=headers)

    try:

        #SQUADS
        squad_wins = r.json()['stats']['p9']['top1']['value']
        squad_kills = r.json()['stats']['p9']['kills']['value']
        squad_kd = r.json()['stats']['p9']['kd']['value']
        squad_matches = r.json()['stats']['p9']['matches']['value']

        squad_stats = []
        squad_stats.extend((int(squad_wins), int(squad_kills), float(squad_kd), int(squad_matches)))

        return squad_stats

    except:
        return False

def get_lifetime_stats(username, platform):
    url = "https://api.fortnitetracker.com/v1/profile/{}/{}".format(platform, username)
    headers = {'TRN-Api-Key' : os.getenv("TRN-Api-Key")}

    r = requests.get(url, headers=headers)

    try:

        #LIFETIME
        lifetime_list = r.json()['lifeTimeStats']
        for li in lifetime_list:
            if li['key'] == "K/d":
                lifetime_kd = li['value']

        return lifetime_kd

    except:
        return False
