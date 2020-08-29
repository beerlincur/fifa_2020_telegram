import json
from config import SHORT_GOAL_RESULT


async def get_tournaments_string():
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        trmnts = data["tournaments"]
        if len(trmnts) == 0:
            return False

        result = "Турниры:\n"
        i = 1
        for t in trmnts:
            name = t["name"]
            result += f"{i}. {name}\n"
            i += 1
        
        return result


async def get_tournaments_dict():
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        trmnts = data["tournaments"]
        if len(trmnts) == 0:
            return False

        result = {}
        i = 1
        for t in trmnts:
            name = t["name"]
            result[i] = name
            i += 1

        return result


async def get_teams_string(tourn):
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        trmnts = data["tournaments"]
        for t in trmnts:
            if t["name"] == tourn:
                teams = t["teams"]
                if len(teams) == 0:
                    return False

                break
        
        i = 1
        result = ""
        for team in teams:
            name = team["name"]
            result += f"{i}. {name}\n"
            i += 1
        return result


async def get_teams_dict(tourn):
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        trmnts = data["tournaments"]
        for t in trmnts:
            if t["name"] == tourn:
                teams = t["teams"]
                if len(teams) == 0:
                    return False
                    
                break
        
        i = 1
        result = {}
        for team in teams:
            name = team["name"]
            result[i] = name
            i += 1

        return result


async def get_tournament_info(tourn_name):
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        trmnts = data["tournaments"]
        
        for t in trmnts:
            
            if t["name"] == tourn_name:
                t_info = {
                    "name": t["name"],
                    "type": t["typeOfTournament"],
                    "isFormed": t["isFormed"],
                    "money": t["money"],
                    "start_time": t["start_time"],
                    "amount_of_teams": t["amount_of_teams"],
                    "teams": t["teams"],
                    "amount_of_games": t["amount_of_games"],
                    "amount_of_tours": t["amount_of_tours"]
                }
                break
        
        return t_info


async def get_to_play_tournaments_string():
    with open("to_play.json", "r+", encoding="utf-8") as to_play_file:
        to_play = json.load(to_play_file)
        try:
            trmnts_to_play = to_play["to_play"]
            
            if len(trmnts_to_play) == 0:
                return False
            
            result = "⚽️Турниры доступные для игры:\n"
            num_of_to_play = 1
            for tr in trmnts_to_play:
                result = result + f"{num_of_to_play}. " + "🏆" + tr["name"] + "\nТип: " + tr["typeOfTournament"] + \
                    "\nТур: " + str(tr["current_round"]["through_tour_number"]) + \
                    "\nМатч №: " + str(tr["current_round"]["through_game_number"]) + "\n" + \
                    str(tr["current_round"]["1_player"]["team"]).upper() + " - " + str(tr["current_round"]["2_player"]["team"]).upper() + \
                    "\nТайм: " + str(tr["current_round"]["taim"]) + "\nСерия: " + str(tr["current_round"]["seria"]) + "\n" +\
                    str(tr["current_round"]["1_player"]["name"]).upper() + " - " + str(tr["current_round"]["2_player"]["name"]).upper()
                result += "\n\n"
                num_of_to_play += 1
                
            return result
        except:
            return False


async def get_to_play_tournaments_dict():
    with open("to_play.json", "r+", encoding="utf-8") as to_play_file:
        to_play = json.load(to_play_file)
        try:
            trmnts_to_play = to_play["to_play"]
            if len(trmnts_to_play) == 0:
                return False
            
            num_of_to_play = 1
            result = {}
            for tr in trmnts_to_play:
                
                if tr["now_playing"] == True:
                    return False

                name = tr["name"]
                result[num_of_to_play] = name
                num_of_to_play += 1

            return result
        
        except:
            return False


async def get_now_playing_tournament():
    with open("to_play.json", "r+", encoding="utf-8") as to_play_file:
        to_play = json.load(to_play_file)
        try:
            trmnts_to_play = to_play["to_play"]
            
            i_o_t_p = 0
            for t_p in trmnts_to_play:
                if t_p["now_playing"] == True:
                    return to_play["to_play"][i_o_t_p]

                i_o_t_p += 1

        except:
            return -1


async def get_archive_tournaments_string():
    with open("archive.json", "r+", encoding="utf-8") as archive_file:
        archive_data = json.load(archive_file)
        try:

            ar_tourns = archive_data["archive_tournaments"]

            if len(ar_tourns) == 0:
                return False

            n_o_a_t = 1
            result = "Архивные турниры:\n"

            for a_t in ar_tourns:

                result = result + str(n_o_a_t) + ". " + a_t["name"] + "\n"

                n_o_a_t += 1

            return result

        except:
            return False


async def get_archive_tournaments_dict():
    with open("archive.json", "r+", encoding="utf-8") as archive_file:
        archive_data = json.load(archive_file)
        try:

            ar_tourns = archive_data["archive_tournaments"]

            if len(ar_tourns) == 0:
                return False

            n_o_a_t = 1
            result = {}

            for a_t in ar_tourns:

                result[n_o_a_t] = a_t["name"]

                n_o_a_t += 1

            return result

        except:
            return False


async def get_archive_tournament_info_string(tourn_name):
    with open("archive.json", "r+", encoding="utf-8") as archive_file:
        archive_data = json.load(archive_file)
        try:

            ar_tourns = archive_data["archive_tournaments"]

            if len(ar_tourns) == 0:
                return False

            result = "Общая информация:\n"

            for a_t in ar_tourns:
                if a_t["name"] == tourn_name:
                    
                    result = "🏆Турнир: " + a_t["name"] + "\n🎯Тип: " + a_t["typeOfTournament"] +\
                            "\n💰Призовой фонд: " + str(a_t["money"]["fond"]) + "\n⚽️Количество команд: " + str(a_t["amount_of_teams"]) +\
                                "\n⌚️Начало турнира: " + str(a_t["start_time"]) + "\n\n"

                    for team in a_t["teams"]:
                        result = result + "👑№ " + str(team["number"]) + " - " + team["name"] + "\nОчки: " + str(team["score"]) +\
                            "\nЗаб-Проп: " + str(team["goals"]) + "-" + str(team["misses"]) + "\nСостав команды:\n"
                        
                        n_o_p = 1
                        for player in team["players"]:
                            name = player["name"]
                            result += f"{n_o_p}. {name}"
                            if name == player["captain_name"]:
                                result += "(К)"
                            for goal in range(player["score"]):
                                result += "⚽️"
                            result += "\n"
                            n_o_p += 1

                        result += "\n\n"
                
                    result = result + "Количество туров: " + str(a_t["amount_of_tours"]) + "\nКоличество игр: " + str(a_t["amount_of_games"]) + "\n\n"

                    result += "🔥Финальная турнирная таблица:🔥\n"
                    
                    place = 1
                    for team in a_t["teams"]:
                        if place == 1:
                            result += "🥇"
                        elif place == 2:
                            result += "🥈"
                        elif place == 3:
                            result += "🥉"
                        else:
                            result += "🎉"

                        result = result + str(place) + "-е место - " + team["name"] + "\nОчки: " + str(team["score"]) +\
                            "\nЗаб-Проп: " + str(team["goals"]) + "-" + str(team["misses"]) + "\nВыигрыш: " + str(team["winning"]) + "\n\n"
                        place += 1
                    
                    
                    break

            return result

        except:
            return False


async def get_archive_tournament_schedule(tourn_name):
    with open("archive.json", "r+", encoding="utf-8") as archive_file:
        archive_data = json.load(archive_file)
        try:
            ar_tourns = archive_data["archive_tournaments"]
            i_o_t = 0
            result = "🎬Расписание матчей турнира:\n"
            for t_sc in ar_tourns:
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


async def get_archive_tourn_history(tourn_name):
    with open("archive.json", "r+", encoding="utf-8") as archive_file:
        archive_data = json.load(archive_file)
        try:
            ar_tourns = archive_data["archive_tournaments"]
            i_o_t = 0
            result = "🎬История турнира:\n\n1-й тур\n\n"
            
            for a_t in ar_tourns:
                if a_t["name"] == tourn_name:
                    
                    am_of_games_in_tour = a_t["amount_of_games"] // a_t["amount_of_tours"]

                    if a_t["isFormed"] == False:
                        return False
                    
                    tour_num = 2
                    for game in a_t["games"]:

                        result += "\t\t"

                        result = result + "Матч №" + str(game["number"]) + " " + game["1_team"]["name"] + " - " +\
                            game["2_team"]["name"] + " | " + str(game["1_score"]) + " : " + str(game["2_score"]) + "\n\n"

                        first_team_game_score = 0
                        second_team_game_score = 0
                        for roun in game["rounds"]:
                            result += "\t\t\t"

                            if roun["goal"] == True:
                                result += "⚽️"
                                if roun["number"] % 2 != 0:
                                    first_team_game_score += 1
                                else:
                                    second_team_game_score += 1
                            else:
                                result += "🚫"

                            result = result + str(roun["number"]) + "' | " + roun["1_player"]["name"] +\
                                " -> " + roun["2_player"]["name"] + " | " + SHORT_GOAL_RESULT[(roun["hitted"], roun["blocked"])] +\
                                    f" {first_team_game_score}:{second_team_game_score}" + "\n"
                        
                        result += "\n"

                        if (game["number"] % am_of_games_in_tour == 0) and tour_num <= a_t["amount_of_tours"]:
                            result = result + str(tour_num) + "-й тур\n\n"
                            tour_num += 1
                            
                    break

                i_o_t += 1

            return result

        except:
            return False


async def get_players_string(confirm_data):

    tourn_name = confirm_data.get("tournament")
    team_name = confirm_data.get("team")

    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        trmnts = data["tournaments"]
        for t in trmnts:
            if t["name"] == tourn_name:
                teams = t["teams"]
                if len(teams) == 0:
                    return False

                break
        
        for team in teams:
            if team["name"] == team_name:
                players = team["players"]

                if len(players) == 0:
                    return False

                captain_name = team["captain_name"]
                break

        result = f"Команда: {team_name}\nКапитан: {captain_name}\n"
        num = 1
        for player in players:
            player_name = player["name"]
            result += f"{num}. {player_name}\n"
            num += 1

        return result


async def get_players_dict(confirm_data):
    
    tourn_name = confirm_data.get("tournament")
    team_name = confirm_data.get("team")

    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        trmnts = data["tournaments"]
        for t in trmnts:
            if t["name"] == tourn_name:
                teams = t["teams"]
                if len(teams) == 0:
                    return False

                break
        
        for team in teams:
            if team["name"] == team_name:
                players = team["players"]
                if len(players) == 0:
                    return False

                captain_name = team["captain_name"]
                break

        result = {}
        num = 1
        for player in players:
            result[num] = player["name"]
            num += 1

        return result


async def get_seris_to_play(tourn_name, cur_game, cur_taim):
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        trmnts = data["tournaments"]
        for t in trmnts:
            if t["name"] == tourn_name:
                for game in t["games"]:
                    if game["number"] == cur_game:
                        for taim in game["taims"]:
                            if taim["number"] == cur_taim:
                                result = "🎬Серии ударов " + str(taim["number"]) + "-го тайма:\n"
                                for ser in taim["seris"]:
                                    ser_num = ser["number"]
                                    f_player = ser["1_player"]["name"]
                                    s_player = ser["2_player"]["name"]
                                    result += f"{ser_num}. {f_player} - {s_player}\n"
                                
                                return result


async def get_team_score(tourn_name, cur_game, team_number):
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        trmnts = data["tournaments"]
        for t in trmnts:
            if t["name"] == tourn_name:
                for game in t["games"]:
                    if game["number"] == cur_game:
                        if team_number == 1:
                            return game["1_score"]
                        else:
                            return game["2_score"]


async def get_tournament_by_name(tourn_name):
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        trmnts = data["tournaments"]
        for t in trmnts:
            if t["name"] == tourn_name:
                return t
                    

async def get_tournament_info_string(tourn_name):
    with open("tournaments.json", "r+", encoding="utf-8") as tourns_file:
        tourns_data = json.load(tourns_file)
        try:
            ar_tourns = tourns_data["tournaments"]

            if len(ar_tourns) == 0:
                return False

            result = "Общая информация:\n"
            #🏆🎯💰⚽️⌚️🎬🎉
            for a_t in ar_tourns:
                if a_t["name"] == tourn_name:
                    
                    result = "🏆Турнир: " + a_t["name"] + "\n🎯Тип: " + a_t["typeOfTournament"] +\
                            "\n💰Призовой фонд: " + str(a_t["money"]["fond"]) + "\n⚽️Количество команд: " + str(a_t["amount_of_teams"]) +\
                                "\n⌚️Начало турнира: " + str(a_t["start_time"]) + "\n\n"

                    for team in a_t["teams"]:
                        result = result + "👑№ " + str(team["number"]) + " - " + team["name"] + "\nОчки: " + str(team["score"]) +\
                            "\nЗаб-Проп: " + str(team["goals"]) + "-" + str(team["misses"]) + "\nСостав команды:\n"
                        
                        n_o_p = 1
                        for player in team["players"]:
                            name = player["name"]
                            result += f"{n_o_p}. {name}"
                            if name == player["captain_name"]:
                                result += "(К)"
                            result += "\n"
                            n_o_p += 1

                        result += "\n\n"
                
                    result = result + "Количество туров: " + str(a_t["amount_of_tours"]) + "\nКоличество игр: " + str(a_t["amount_of_games"]) + "\n\n"

                    result += "🎬Турнирная таблица:\n"
                    
                    place = 1
                    for team in a_t["teams"]:
                        
                        result = result + "🎉" + str(place) + "-е место - " + team["name"] + "\nОчки: " + str(team["score"]) +\
                            "\nЗаб-Проп: " + str(team["goals"]) + "-" + str(team["misses"]) + "\nВыигрыш: " + str(team["winning"]) + "\n\n"
                        place += 1
                    
                    
                    break

            return result

        except:
            return False


async def get_player_stat(tourn, team_name, player_name):
    for team in tourn["teams"]:
        if team["name"] == team_name:
            for player in team["players"]:
                if player["name"] == player_name:
                    h_l = player["hits"]["0"]
                    h_c = player["hits"]["1"]
                    h_r = player["hits"]["2"]

                    b_l = player["blocks"]["0"]
                    b_r = player["blocks"]["1"]
                    b_u = player["blocks"]["2"]

                    return f"Ат: ({h_l}-{h_c}-{h_r}) Защ: ({b_l}-{b_r}-{b_u})"


async def get_best_hitter_blocker(teams):
    try:
        maximum_hit = -1
        maximum_block = -1
        best_hitters = []
        b_h = None
        best_blockers = []
        b_b = None
        for team in teams:
            for player in team["players"]:
                
                if player["score"] > maximum_hit:
                    b_h = player
                    maximum_hit = player["score"]
                    best_hitters.clear()
                    best_hitters.append(b_h)
                
                elif player["score"] == maximum_hit:
                    best_hitters.append(player)
                
                if player["saves"] > maximum_block:
                    b_b = player
                    maximum_block = player["saves"]
                    best_blockers.clear()
                    best_blockers.append(b_b)
                elif player["saves"] == maximum_block:
                    best_blockers.append(player)
        
        result = ""
        #⚽️🥅
        if len(best_hitters) == 1:
            result += "⚽️Лучший бомбардир турнира:⚽️\n"
        else:
            result += "⚽️Лучшие бомбардиры турнира:⚽️\n"

        n_o_h = 1
        for hitter in best_hitters:
            result = result + str(n_o_h) + ". " + hitter["name"].upper() + " (" + hitter["team"] + ") голы: " + str(hitter["score"]) + "\n"  
            n_o_h += 1

        result += "\n"

        if len(best_blockers) == 1:
            result += "🥅Лучший вратарь турнира:🥅\n"
        else:
            result += "🥅Лучшие вратари турнира:🥅\n"

        n_o_b = 1
        for blocker in best_blockers:
            result = result + str(n_o_b) + ". " + blocker["name"].upper() + " (" + blocker["team"] + ") сейвы: " + str(blocker["saves"]) + "\n"
            n_o_b += 1

        return result

    except:
        return False


async def get_archive_tourn_by_name(tourn):
    with open("archive.json", "r+", encoding="utf-8") as archive_file:
        archive_data = json.load(archive_file)
        for ar in archive_data["archive_tournaments"]:
            if ar["name"] == tourn:
                return ar