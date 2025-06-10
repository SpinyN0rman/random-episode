import os, random
import tvdb_v4_official

tvdb_api = os.getenv("TVDB_API_KEY")
tvdb = tvdb_v4_official.TVDB(tvdb_api)

def tvdb_search(search_term):
    results = tvdb.search(search_term)
    shows = []
    for result in results:
        if result["type"] == "series":
            try:
                show_synopsis = result["overview"]
            except KeyError:
                show_synopsis = "No synopsis"
            show = {
                "show_name": result["name"],
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
    rand_episode = rand_season_info["episodes"][rand_episode_index]

    return show, rand_episode

# if __name__ == "__main__":
#     # print(tvdb.search("The West Wing"))
#     show, episode = tvdb_episodes(259972)
#     print(f"Show: {show["name"]}\nSeason: {episode["seasonNumber"]}\n"
#           f"Episode: {episode["number"]}\nEpisode Title: {episode["name"]}\n"
#           f"Episode synopsis: {episode["overview"]}")
