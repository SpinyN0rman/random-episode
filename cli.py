import functions

while True:
    print("What would you like to do?")
    print("1. Search for a show\n2. Get a random episode\n")
    user_action = input("Enter your choice (number): ")

    if user_action == "1":

        search_term = input("Show name: ")
        search_results = functions.tvdb_search(search_term)
        count = 0
        for result in search_results[:5]:
            count = count + 1
            print(f"{count} {result["show_name"]} (id: {result["show_id"]})")
        user_choice = search_results[int(input("\nPick a show (enter number): ")) - 1]
        show, episode = functions.tvdb_episodes(user_choice["show_id"])
        print(
            f"Show: {show["name"]}\nSeason: {episode["seasonNumber"]}\n"
            f"Episode: {episode["number"]}\nEpisode Title: {episode["name"]}\n"
            f"Episode synopsis: {episode["overview"]}\n")

    elif user_action == "2":
        show_id = input("Enter show ID: ")
        show, episode = functions.tvdb_episodes(show_id)
        print(
            f"Show: {show["name"]}\nSeason: {episode["seasonNumber"]}\n"
            f"Episode: {episode["number"]}\nEpisode Title: {episode["name"]}\n"
            f"Episode synopsis: {episode["overview"]}\n")

    elif user_action.startswith('exit'):
        break
    else:
        print('Command not recognised')