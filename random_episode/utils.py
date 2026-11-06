import os, random
import tvdb_v4_official
import requests

tvdb_api = os.getenv("TVDB_API_KEY")
tvdb = tvdb_v4_official.TVDB(tvdb_api)

def tvdb_search(search_term):
    results = tvdb.search(search_term)
    shows = []
    for result in results:
        if result["type"] == "series":
            try:
                show_name = result["translations"]["eng"]
            except KeyError:
                show_name = result["name"]
            try:
                show_synopsis = result["overviews"]["eng"]
            except KeyError:
                try:
                    show_synopsis = result["overview"]
                except KeyError:
                    show_synopsis = "No synopsis"
            show = {
                "show_name": show_name,
                "show_id": result["tvdb_id"],
                "show_synopsis": show_synopsis,
                "show_art": result["image_url"]
            }
            shows.append(show)
    return shows[:10]

def tvdb_episodes(show_id):
    show = tvdb.get_series_extended(show_id)
    season_ids = []
    for season in show["seasons"]:
        if season["type"]["id"] == 1 and season["number"] > 0:
            season_ids.append(season["id"])
    rand_season_id = season_ids[random.randrange(0, len(season_ids))]
    rand_season_info = tvdb.get_season_extended(rand_season_id)
    rand_episode_index = 0
    try:
        rand_episode_index = random.randrange(0, len(rand_season_info["episodes"]))
    except ValueError as e:
        print(f"Encountered an error: {e}")

    return rand_season_id, rand_episode_index

def tvdb_episode_load(show_id, season_id, episode_num):
    show = tvdb.get_series_extended(show_id)
    season_info = tvdb.get_season_extended(season_id)
    episode = season_info["episodes"][int(episode_num)]

    # Find the English alias
    try:
        eng_show = tvdb.get_series_translation(show_id, "eng")
        eng_name = eng_show["name"]
    except KeyError:
        eng_name = "None"

    # Get English episode title and overview
    try:
        eng_episode_deets = tvdb.get_episode_translation(episode["id"], "eng")
    except KeyError:
        eng_episode_deets = "None"

    return show, episode, eng_name, eng_episode_deets


def trending():
    response = requests.get('https://test.northrop.uk/bot/trending_shows.json')
    resp_json = response.json()
    show_ids: list = resp_json.get('trending_series', '')
    shows: list = []

    for show_id in show_ids:
        show_info = tvdb.get_series(show_id)
        show = {
            "show_name": show_info['name'],
            "show_id": show_id,
            "show_art": show_info['image']
        }
        shows.append(show)
    return shows[:8]

def trending_to_string(trending_shows):
    trending_string: str = ''
    for show in trending_shows:
        trending_string += f"{show['show_name']}&&{show['show_id']}&&{show['show_art']}!!"
    trending_string = trending_string.replace(' ', '^^')
    trending_string = trending_string.strip('!!')
    return trending_string

def trending_from_string(trending_cookie):
    if trending_cookie == '':
        return ''
    else:
        trending_cookie = trending_cookie.replace('^^', ' ')
        shows: list = []
        chunks = trending_cookie.split('!!')
        for chunk in chunks:
            bits = chunk.split('&&')
            show = {
                "show_name": bits[0],
                "show_id": bits[1],
                "show_art": bits[2]
            }
            shows.append(show)
        return shows

def recents(ids):
    shows: list = []
    if ids != '':
        for show_id in ids:
            show_info = tvdb.get_series(show_id)
            show = {
                "show_name": show_info['name'],
                "show_id": show_id,
                "show_art": show_info['image']
            }
            shows.append(show)
    return shows[:8]

# if __name__ == "__main__":
#     # print(tvdb.search("The West Wing"))
#     show, episode = tvdb_episodes(259972)
#     print(f"Show: {show["name"]}\nSeason: {episode["seasonNumber"]}\n"
#           f"Episode: {episode["number"]}\nEpisode Title: {episode["name"]}\n"
#           f"Episode synopsis: {episode["overview"]}")
