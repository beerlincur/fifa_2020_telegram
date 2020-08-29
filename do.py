import json
from round_robin_algo import simulate_draw, simulate_game_draw
from add import add_tournament_to_play_json


async def do_generate_tournament_json(tourn_data):
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        try:
            trmnts = data["tournaments"]
            tourn_name = tourn_data.get("tournament")
            
            for t in trmnts:
                if t["name"] == tourn_name:
                    if t["isFormed"] == False:
                        #print(t["name"])
                        teams = t["teams"]
                        amount_of_players = t["amount_of_players"]
                        am_of_games_in_tour = t["amount_of_games"] // t["amount_of_tours"]
                        amount_of_rounds_in_game = t["teams"][0]["amount_of_players"] * t["teams"][0]["amount_of_players"] * 2
                        t["amount_of_rounds"] = t["amount_of_games"] * amount_of_rounds_in_game
                        
                        games = await simulate_draw(teams)
                        
                        through_game_number = 1
                        through_round_number = 1
                        through_tour_number = 1

                        for team1, team2 in games:

                            #competitors = list(zip(team1["players"], team2["players"]))

                            if amount_of_players == 1:
                                competitors = [(team1["players"][0], team2["players"][0], 1, 1)]

                                tais = [
                                    {
                                        "number": 1,
                                        "amount_of_seris": 1,
                                        "seris": [
                                            {
                                                "number": 1,
                                                "1_player": team1["players"][0],
                                                "2_player": team2["players"][0]
                                            }
                                        ]
                                    }
                                ]

                            elif amount_of_players == 2:
                                competitors = []
                                competitors.append((team1["players"][0], team2["players"][0], 1, 1)) # игрок1 игрок2 тайм серия
                                competitors.append((team1["players"][1], team2["players"][1], 1, 2))
                                competitors.append((team1["players"][0], team2["players"][1], 2, 1))
                                competitors.append((team1["players"][1], team2["players"][0], 2, 2))

                                tais = [
                                    {
                                        "number": 1,
                                        "amount_of_seris": 2,
                                        "seris": [
                                            {
                                                "number": 1,
                                                "1_player": team1["players"][0],
                                                "2_player": team2["players"][0]
                                            },

                                            {
                                                "number": 2,
                                                "1_player": team1["players"][1],
                                                "2_player": team2["players"][1]
                                            }
                                        ]
                                    },

                                    {
                                        "number": 2,
                                        "amount_of_seris": 2,
                                        "seris": [
                                            {
                                                "number": 1,
                                                "1_player": team1["players"][0],
                                                "2_player": team2["players"][1]
                                            },

                                            {
                                                "number": 2,
                                                "1_player": team1["players"][1],
                                                "2_player": team2["players"][0]
                                            }
                                        ]
                                    }
                                ]

                            elif amount_of_players == 3:
                                competitors = []
                                competitors.append((team1["players"][0], team2["players"][0], 1, 1))
                                competitors.append((team1["players"][1], team2["players"][1], 1, 2))
                                competitors.append((team1["players"][2], team2["players"][2], 1, 3))
                                competitors.append((team1["players"][0], team2["players"][1], 2, 1))
                                competitors.append((team1["players"][1], team2["players"][2], 2, 2))
                                competitors.append((team1["players"][2], team2["players"][0], 2, 3))
                                competitors.append((team1["players"][0], team2["players"][2], 3, 1))
                                competitors.append((team1["players"][1], team2["players"][0], 3, 2))
                                competitors.append((team1["players"][2], team2["players"][1], 3, 3))

                                
                                
                                tais = [
                                    {
                                        "number": 1,
                                        "amount_of_seris": 3,
                                        "seris": [
                                            {
                                                "number": 1,
                                                "1_player": team1["players"][0],
                                                "2_player": team2["players"][0]
                                            },

                                            {
                                                "number": 2,
                                                "1_player": team1["players"][1],
                                                "2_player": team2["players"][1]
                                            },

                                            {
                                                "number": 3,
                                                "1_player": team1["players"][2],
                                                "2_player": team2["players"][2]
                                            }
                                        ]
                                    },

                                    {
                                        "number": 2,
                                        "amount_of_seris": 3,
                                        "seris": [
                                            {
                                                "number": 1,
                                                "1_player": team1["players"][0],
                                                "2_player": team2["players"][1]
                                            },

                                            {
                                                "number": 2,
                                                "1_player": team1["players"][1],
                                                "2_player": team2["players"][2]
                                            },

                                            {
                                                "number": 3,
                                                "1_player": team1["players"][2],
                                                "2_player": team2["players"][0]
                                            }
                                        ]
                                    },

                                    {
                                        "number": 3,
                                        "amount_of_seris": 3,
                                        "seris": [
                                            {
                                                "number": 1,
                                                "1_player": team1["players"][0],
                                                "2_player": team2["players"][2]
                                            },

                                            {
                                                "number": 2,
                                                "1_player": team1["players"][1],
                                                "2_player": team2["players"][0]
                                            },

                                            {
                                                "number": 3,
                                                "1_player": team1["players"][2],
                                                "2_player": team2["players"][1]
                                            }
                                        ]
                                    }
                                ]

                                    
                            rounds = []
                            local_round_number = 1



                            for p1, p2, taim, seria in competitors:

                                # ser = {
                                #     "number": seria,
                                #     "1_round": None,
                                #     "2_round": None,
                                # }
                                
                                roun = {
                                    "number": local_round_number,
                                    "through_round_number": through_round_number,
                                    "through_game_number": through_game_number,
                                    "through_tour_number": through_tour_number,
                                    "taim": taim,
                                    "seria": seria,
                                    "1_player": p1,
                                    "hitted": None,
                                    "1_score": 0,
                                    "2_player": p2,
                                    "blocked": None,
                                    "2_score": 0,
                                    "goal": None,
                                    "winner": None
                                }
                                rounds.append(roun)
                                t["rounds"].append(roun)
                                local_round_number += 1
                                through_round_number += 1

                                roun = {
                                    "number": local_round_number,
                                    "through_round_number": through_round_number,
                                    "through_game_number": through_game_number,
                                    "through_tour_number": through_tour_number,
                                    "taim": taim,
                                    "seria": seria,
                                    "1_player": p2,
                                    "hitted": None,
                                    "1_score": 0,
                                    "2_player": p1,
                                    "blocked": None,
                                    "2_score": 0,
                                    "goal": None,
                                    "winner": None
                                }
                                rounds.append(roun)
                                t["rounds"].append(roun)
                                local_round_number += 1
                                through_round_number += 1


                            game = {
                                "number": through_game_number,
                                "1_team": team1,
                                "1_score": 0,
                                "2_team": team2,
                                "2_score": 0,
                                "rounds": rounds,
                                "amount_of_taims": amount_of_players,
                                "amount_of_seris": amount_of_players,
                                "taims": tais,
                                "amount_of_rounds": amount_of_rounds_in_game,
                                "winner": None
                            }

                            if t["amount_of_tours"] != 1:
                                if through_game_number % am_of_games_in_tour == 0:
                                    through_tour_number += 1

                            through_game_number += 1
                            
                            

                            rounds = []
                            t["games"].append(game)

                        
                        through_game_number = 1
                        through_tour_number = 1
                        tour_games = []
                        for game in games:
                            
                            tour_games.append(game)

                            if through_game_number % am_of_games_in_tour == 0:
                                tour = {
                                    "through_tour_number": through_tour_number,
                                    "games": tour_games,
                                    "amount_of_games": am_of_games_in_tour
                                }
                                t["tours"].append(tour)
                                tour_games = []
                                through_tour_number += 1
                            through_game_number += 1

                        t["isFormed"] = True

                        file.seek(0)
                        file.write(json.dumps(data, ensure_ascii=False, indent=8))
                        file.truncate()

                        is_added_to_play = await add_tournament_to_play_json(tourn_name)

                        break
                    
                    else:
                        return False



            

            if is_added_to_play:
                return True
            else:
                return False
        except:
            return False


async def do_archive_tournament(tourn_name):
    with open("tournaments.json", "r+", encoding="utf-8") as tournaments_file:
        tournaments_data = json.load(tournaments_file)
        try:
            trmnts = tournaments_data["tournaments"]
            index_of_tourn = 0
            for t_sc in trmnts:
                if t_sc["name"] == tourn_name:
                    with open("archive.json", "r+", encoding="utf-8") as archive_file:
                        archive_data = json.load(archive_file)
                        if len(archive_data["archive_tournaments"]) == 20:
                            archive_data["archive_tournaments"].remove(archive_data["archive_tournaments"][0])
                            archive_data["archive_tournaments"].append(trmnts[index_of_tourn])
                        else:
                            archive_data["archive_tournaments"].append(trmnts[index_of_tourn])
                        archive_file.seek(0)
                        archive_file.write(json.dumps(archive_data, ensure_ascii=False, indent=8))
                        archive_file.truncate()
                    
                    tournaments_data["tournaments"].remove(tournaments_data["tournaments"][index_of_tourn])

                    break

                index_of_tourn += 1

            tournaments_file.seek(0)
            tournaments_file.write(json.dumps(tournaments_data, ensure_ascii=False, indent=8))
            tournaments_file.truncate()

        except:
            return False
    
    with open("to_play.json", "r+", encoding="utf-8") as to_play_file:
        to_play_data = json.load(to_play_file)
        try:
            
            to_play_tourns = to_play_data["to_play"]
            index_of_tourn = 0
            for t_p in to_play_tourns:
                if t_p["name"] == tourn_name:
                    
                    to_play_data["to_play"].remove(to_play_data["to_play"][index_of_tourn])

                    to_play_file.seek(0)
                    to_play_file.write(json.dumps(to_play_data, ensure_ascii=False, indent=8))
                    to_play_file.truncate()

                    break

                index_of_tourn += 1
                
        except:
            return False

    return True


async def do_show_tournament_schedule_string(tourn_name):
    with open("tournaments.json", "r+", encoding="utf-8") as tourn_file:
        tourns_data = json.load(tourn_file)
        try:
            tourns = tourns_data["tournaments"]
            i_o_t = 0
            result = "🎬Расписание матчей турнира:\n\n"
            for t_sc in tourns:
                if t_sc["name"] == tourn_name:
                    
                    if t_sc["isFormed"] == False:
                        return False
                    
                    for tour in t_sc["tours"]:
                        
                        result = result + str(tour["through_tour_number"]) + "-й тур\n"
                        n_o_g = 1
                        for game in tour["games"]:
                            result += "\t\t"
                            result = result + str(n_o_g) + " " + game[0]["name"] + " - " + game[1]["name"] + "\n"
                            n_o_g += 1



                    break
                i_o_t += 1

            return result

        except:
            return False


async def do_confirm_player_part(confirm_data):
    
    tourn_name = confirm_data.get("tournament")
    team_name = confirm_data.get("team")
    player_name = confirm_data.get("name")
    player_id = confirm_data.get("idd")
    
    with open("tournaments.json", "r+", encoding="utf-8") as tourn_file:
        tourns_data = json.load(tourn_file)
        try:
            trmnts = tourns_data["tournaments"]
            for t in trmnts:
                if t["name"] == tourn_name:
                    for team in t["teams"]:
                        if team["name"] == team_name:
                            for player in team["players"]:
                                if player["name"] == player_name:
                                    player["id"] = int(player_id)
                                    tourn_file.seek(0)
                                    tourn_file.write(json.dumps(tourns_data, ensure_ascii=False, indent=8))
                                    tourn_file.truncate()
                                    return True

        except:
            return False