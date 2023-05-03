import requests
#p2 = Solo
#p10 = Duo
#p9 = Squad

#curr_

def get_8_solo_stats(username, platform):
    url = "https://api.fortnitetracker.com/v1/profile/{}/{}".format(platform, username)
    headers = {'TRN-Api-Key' : '8257ed18-77dd-4918-9816-fa41c6312ad3'}

    r = requests.get(url, headers=headers)

    try:

        #SOLOS
        solo_wins = r.json()['stats']['curr_p2']['top1']['value']
        solo_kills = r.json()['stats']['curr_p2']['kills']['value']
        solo_kd = r.json()['stats']['curr_p2']['kd']['value']
        solo_matches = r.json()['stats']['curr_p2']['matches']['value']

        solo_stats = []
        solo_stats.extend((int(solo_wins), int(solo_kills), float(solo_kd), int(solo_matches)))

        return solo_stats

    except:
        return False

def get_8_duo_stats(username, platform):
    url = "https://api.fortnitetracker.com/v1/profile/{}/{}".format(platform, username)
    headers = {'TRN-Api-Key' : '8257ed18-77dd-4918-9816-fa41c6312ad3'}

    r = requests.get(url, headers=headers)

    try:

        #DUOS
        duo_wins = r.json()['stats']['curr_p10']['top1']['value']
        duo_kills = r.json()['stats']['curr_p10']['kills']['value']
        duo_kd = r.json()['stats']['curr_p10']['kd']['value']
        duo_matches = r.json()['stats']['curr_p10']['matches']['value']

        duo_stats = []
        duo_stats.extend((int(duo_wins), int(duo_kills), float(duo_kd), int(duo_matches)))

        return duo_stats

    except:
        return False

def get_8_squad_stats(username, platform):
    url = "https://api.fortnitetracker.com/v1/profile/{}/{}".format(platform, username)
    headers = {'TRN-Api-Key' : '8257ed18-77dd-4918-9816-fa41c6312ad3'}

    r = requests.get(url, headers=headers)

    try:

        #SQUADS
        squad_wins = r.json()['stats']['curr_p9']['top1']['value']
        squad_kills = r.json()['stats']['curr_p9']['kills']['value']
        squad_kd = r.json()['stats']['curr_p9']['kd']['value']
        squad_matches = r.json()['stats']['curr_p9']['matches']['value']

        squad_stats = []
        squad_stats.extend((int(squad_wins), int(squad_kills), float(squad_kd), int(squad_matches)))

        return squad_stats

    except:
        return False
