import json


async def set_now_playing_true(tourn_name):
    with open("to_play.json", "r+", encoding="utf-8") as to_play_file:
        to_play = json.load(to_play_file)
        try:
            trmnts_to_play = to_play["to_play"]

            for t in trmnts_to_play:
                if t["name"] == tourn_name:
                    t["now_playing"] = True
                    to_play_file.seek(0)
                    to_play_file.write(json.dumps(to_play, ensure_ascii=False, indent=8))
                    to_play_file.truncate()
                    return t
            return False
        except:
            return False


async def set_now_playing_false(tourn_name):
    with open("to_play.json", "r+", encoding="utf-8") as to_play_file:
        to_play = json.load(to_play_file)
        try:
            trmnts_to_play = to_play["to_play"]

            for t in trmnts_to_play:
                if t["name"] == tourn_name:
                    t["now_playing"] = False
                    to_play_file.seek(0)
                    to_play_file.write(json.dumps(to_play, ensure_ascii=False, indent=8))
                    to_play_file.truncate()
                    return t
            return False
        except:
            return False


async def set_next_round_to_play(now_playing_info):

    endOfTaim = False
    endOfGame = False
    endOfTour = False
    endOfTournament = False

    with open("to_play.json", "r+", encoding="utf-8") as to_play_file:
        to_play = json.load(to_play_file)
        try:
            trmnts_to_play = to_play["to_play"]

            for t_play in trmnts_to_play:
                if t_play["name"] == now_playing_info["name"]:
                    
                    pr_cur_round_through_num = now_playing_info["current_round"]["through_round_number"]
                    pr_cur_round_num = now_playing_info["current_round"]["number"]
                    pr_cur_game_number = now_playing_info["current_round"]["through_game_number"]
                    pr_cur_tour_number = now_playing_info["current_round"]["through_tour_number"]
                    pr_cur_taim_number = now_playing_info["current_round"]["taim"]
                    pr_cur_seria_number = now_playing_info["current_round"]["seria"]

                    if t_play["current_round"]["goal"]:
                    
                        t_play["current_round"]["1_score"] += 1
                        t_play["current_round"]["1_player"]["score"] += 1
                        t_play["current_round"]["winner"] = t_play["current_round"]["1_player"]
                        
                        i_o_t = 0
                        for team in t_play["teams"]:
                            if team["name"] == t_play["current_round"]["1_player"]["team"]:
                                i_o_p = 0
                                for p in team["players"]:
                                    if p["name"] == t_play["current_round"]["1_player"]["name"]:
                                        t_play["teams"][i_o_t]["players"][i_o_p]["score"] += 1
                                        break
                                    i_o_p += 1
                                break

                            i_o_t += 1

                    else:
                        
                        t_play["current_round"]["winner"] = t_play["current_round"]["2_player"]

                        t_play["current_round"]["2_player"]["saves"] += 1
                        
                        i_o_t = 0
                        for team in t_play["teams"]:
                            if team["name"] == t_play["current_round"]["2_player"]["team"]:
                                i_o_p = 0
                                for p in team["players"]:
                                    if p["name"] == t_play["current_round"]["2_player"]["name"]:
                                        t_play["teams"][i_o_t]["players"][i_o_p]["saves"] += 1
                                        break
                                    i_o_p += 1
                                break

                            i_o_t += 1

                    
                    to_play_file.seek(0)
                    to_play_file.write(json.dumps(to_play, ensure_ascii=False, indent=8))
                    to_play_file.truncate()

                    with open("tournaments.json", "r+", encoding="utf-8") as schedule:
                        data = json.load(schedule)
                        trmnts_schedule = data["tournaments"]
                        for t_sc in trmnts_schedule:
                            if t_sc["name"] == now_playing_info["name"]:

                                t_sc["teams"] = t_play["teams"]

                                schedule.seek(0)
                                schedule.write(json.dumps(data, ensure_ascii=False, indent=8))
                                schedule.truncate()

                                am_of_games_in_tour = t_sc["amount_of_games"] // t_sc["amount_of_tours"]
                                
                                index_of_round = 0
                                for rou_sc in t_sc["rounds"]:

                                    if rou_sc["through_round_number"] == pr_cur_round_through_num:
                                        t_sc["rounds"][index_of_round] = t_play["current_round"]
                                        break

                                    index_of_round += 1

                                index_of_game = 0
                                for game in t_sc["games"]:
                                    if game["number"] == pr_cur_game_number:
                                        
                                        index_of_round = 0
                                        for roun in game["rounds"]:
                                            if roun["number"] == pr_cur_round_num:
                                                game["rounds"][index_of_round] = t_play["current_round"]
                                                break

                                            index_of_round += 1
                                        
                                        if t_play["current_round"]["goal"]:
                                            if game["1_team"]["name"] == t_play["current_round"]["1_player"]["team"]:

                                                game["1_score"] += 1
                                            
                                            else:

                                                game["2_score"] += 1

                                        

                                        if (pr_cur_seria_number == game["amount_of_seris"]) and (pr_cur_round_num % 2 == 0):

                                            endOfTaim = True
                                            taim_result = t_sc["games"][index_of_game]


                                        if pr_cur_round_num == game["amount_of_rounds"]:
                                            
                                            #print(game["1_score"], game["2_score"])

                                            if game["1_score"] > game["2_score"]:
                                                t_sc["games"][index_of_game]["winner"] = game["1_team"]

                                                index_of_team = 0
                                                for team in t_sc["teams"]:
                                                    if team["name"] == game["1_team"]["name"]:
                                                        t_sc["teams"][index_of_team]["score"] += 3
                                                        t_sc["teams"][index_of_team]["goals"] += game["1_score"]
                                                        t_sc["teams"][index_of_team]["misses"] += game["2_score"]
                                                        break
                                                    
                                                    index_of_team += 1

                                                i_o_tt = 0
                                                for team in t_sc["teams"]:
                                                    if team["name"] == game["2_team"]["name"]:
                                                        t_sc["teams"][i_o_tt]["goals"] += game["2_score"]
                                                        t_sc["teams"][i_o_tt]["misses"] += game["1_score"]
                                                        break
                                                    i_o_tt += 1

                                                    

                                                for i in range(index_of_team, 0, -1):
                                                    if t_sc["teams"][i-1]["score"] < t_sc["teams"][i]["score"]:
                                                        t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]

                                                    elif t_sc["teams"][i-1]["score"] == t_sc["teams"][i]["score"]:

                                                        if (t_sc["teams"][i-1]["goals"] - t_sc["teams"][i-1]["misses"]) < (t_sc["teams"][i]["goals"] - t_sc["teams"][i]["misses"]):
                                                            t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]

                                                        elif (t_sc["teams"][i-1]["goals"] - t_sc["teams"][i-1]["misses"]) == (t_sc["teams"][i]["goals"] - t_sc["teams"][i]["misses"]):
                                                            if t_sc["teams"][i-1]["goals"] < t_sc["teams"][i]["goals"]:
                                                                t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]


                                                
                                                endOfGame = True
                                                game_result = t_sc["games"][index_of_game]

                                            elif game["1_score"] < game["2_score"]:
                                                t_sc["games"][index_of_game]["winner"] = game["2_team"]
                                                index_of_team = 0
                                                for team in t_sc["teams"]:
                                                    if team["name"] == game["2_team"]["name"]:
                                                        t_sc["teams"][index_of_team]["score"] += 3
                                                        t_sc["teams"][index_of_team]["goals"] += game["2_score"]
                                                        t_sc["teams"][index_of_team]["misses"] += game["1_score"]
                                                        break
                                                    
                                                    index_of_team += 1
                                                
                                                i_o_tt = 0
                                                for team in t_sc["teams"]:
                                                    if team["name"] == game["1_team"]["name"]:
                                                        t_sc["teams"][i_o_tt]["goals"] += game["1_score"]
                                                        t_sc["teams"][i_o_tt]["misses"] += game["2_score"]
                                                        break
                                                    i_o_tt += 1


                                                    
                                                for i in range(index_of_team, 0, -1):
                                                    if t_sc["teams"][i-1]["score"] < t_sc["teams"][i]["score"]:
                                                        t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]

                                                    elif t_sc["teams"][i-1]["score"] == t_sc["teams"][i]["score"]:

                                                        if (t_sc["teams"][i-1]["goals"] - t_sc["teams"][i-1]["misses"]) < (t_sc["teams"][i]["goals"] - t_sc["teams"][i]["misses"]):
                                                            t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]

                                                        elif (t_sc["teams"][i-1]["goals"] - t_sc["teams"][i-1]["misses"]) == (t_sc["teams"][i]["goals"] - t_sc["teams"][i]["misses"]):
                                                            if t_sc["teams"][i-1]["goals"] < t_sc["teams"][i]["goals"]:
                                                                t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]

                                                endOfGame = True
                                                game_result = t_sc["games"][index_of_game]

                                            elif game["1_score"] == game["2_score"]:
                                                t_sc["games"][index_of_game]["winner"] = [game["1_team"], game["2_team"]]

                                                index_of_team = 0
                                                for team in t_sc["teams"]:
                                                    if team["name"] == game["1_team"]["name"]:
                                                        t_sc["teams"][index_of_team]["score"] += 1
                                                        t_sc["teams"][index_of_team]["goals"] += game["1_score"]
                                                        t_sc["teams"][index_of_team]["misses"] += game["2_score"]

                                                        for i in range(index_of_team, 0, -1):
                                                            if t_sc["teams"][i-1]["score"] < t_sc["teams"][i]["score"]:
                                                                t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]

                                                            elif t_sc["teams"][i-1]["score"] == t_sc["teams"][i]["score"]:

                                                                if (t_sc["teams"][i-1]["goals"] - t_sc["teams"][i-1]["misses"]) < (t_sc["teams"][i]["goals"] - t_sc["teams"][i]["misses"]):
                                                                    t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]

                                                                elif (t_sc["teams"][i-1]["goals"] - t_sc["teams"][i-1]["misses"]) == (t_sc["teams"][i]["goals"] - t_sc["teams"][i]["misses"]):
                                                                    if t_sc["teams"][i-1]["goals"] < t_sc["teams"][i]["goals"]:
                                                                        t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]
                                                        
                                                        break
                                                    index_of_team += 1
                                                
                                                index_of_team = 0
                                                for team in t_sc["teams"]:

                                                    if team["name"] == game["2_team"]["name"]:
                                                        t_sc["teams"][index_of_team]["score"] += 1
                                                        t_sc["teams"][index_of_team]["goals"] += game["2_score"]
                                                        t_sc["teams"][index_of_team]["misses"] += game["1_score"]

                                                        for i in range(index_of_team, 0, -1):
                                                            if t_sc["teams"][i-1]["score"] < t_sc["teams"][i]["score"]:
                                                                t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]

                                                            elif t_sc["teams"][i-1]["score"] == t_sc["teams"][i]["score"]:

                                                                if (t_sc["teams"][i-1]["goals"] - t_sc["teams"][i-1]["misses"]) < (t_sc["teams"][i]["goals"] - t_sc["teams"][i]["misses"]):
                                                                    t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]

                                                                elif (t_sc["teams"][i-1]["goals"] - t_sc["teams"][i-1]["misses"]) == (t_sc["teams"][i]["goals"] - t_sc["teams"][i]["misses"]):
                                                                    if t_sc["teams"][i-1]["goals"] < t_sc["teams"][i]["goals"]:
                                                                        t_sc["teams"][i-1], t_sc["teams"][i] = t_sc["teams"][i], t_sc["teams"][i-1]
                                                        
                                                        break
                                                            
                                                    index_of_team += 1

                                                endOfGame = True
                                                game_result = t_sc["games"][index_of_game]

                                            if game["number"] % am_of_games_in_tour == 0:
                                                semi_results = []
                                                team_place = 1
                                                for team in t_sc["teams"]:
                                                    semi_results.append((team_place, team["name"], team["score"], team["goals"], team["misses"]))
                                                    team_place += 1
                                                
                                                endOfTour = True

                                            
                                            if game["number"] == t_sc["amount_of_games"]:
                                                results = []
                                                team_place = 1
                                                
                                                if t_sc["amount_of_teams"] == 2:
                                                    
                                                    if t_sc["teams"][0]["score"] == t_sc["teams"][1]["score"]:
                                                        t_sc["teams"][0]["winning"] = t_sc["money"]["fond"] * 0.5
                                                        t_sc["teams"][1]["winning"] = t_sc["money"]["fond"] * 0.5
                                                        
                                                    else:
                                                        t_sc["teams"][0]["winning"] = t_sc["money"]["fond"]

                                                    
                                                else:
                                                    i_o_team = 0
                                                    for tea in t_sc["teams"]:
                                                        if i_o_team == 0:
                                                            t_sc["teams"][i_o_team]["winning"] = t_sc["money"]["fond"] * 0.5
                                                        elif i_o_team == 1:
                                                            t_sc["teams"][i_o_team]["winning"] = t_sc["money"]["fond"] * 0.3
                                                        elif i_o_team == 2:
                                                            t_sc["teams"][i_o_team]["winning"] = t_sc["money"]["fond"] * 0.2
                                                        else:
                                                            break

                                                        i_o_team += 1
                                                            
                                                schedule.seek(0)
                                                schedule.write(json.dumps(data, ensure_ascii=False, indent=8))
                                                schedule.truncate()

                                                for team in t_sc["teams"]:
                                                    results.append((team_place, team["name"], team["score"], team["winning"], team["goals"], team["misses"]))
                                                    team_place += 1

                                                endOfTournament = True

                                        break
                                    index_of_game += 1
                                    
                                for rou_sc in t_sc["rounds"]:
                                    if rou_sc["through_round_number"] == pr_cur_round_through_num + 1:
                                        t_play["current_round"] = rou_sc

                                t_play["teams"] = t_sc["teams"]

                                break
                        
                        schedule.seek(0)
                        schedule.write(json.dumps(data, ensure_ascii=False, indent=8))
                        schedule.truncate()

                        
                    break

            to_play_file.seek(0)
            to_play_file.write(json.dumps(to_play, ensure_ascii=False, indent=8))
            to_play_file.truncate()

            
            to_return = [True]
            return_code = [True, False, False, False, False]

            if endOfTaim:
                to_return.append(taim_result)
                return_code[1] = True

            if endOfGame:
                to_return.append(game_result)
                return_code[2] = True

            if endOfTour:
                to_return.append(semi_results)
                return_code[3] = True

            if endOfTournament:
                to_return.append(results)
                return_code[4] = True

            return (return_code, to_return)

        except:
            return False


async def set_hitted_to_play_json(hitted):
    with open("to_play.json", "r+", encoding="utf-8") as to_play_file:
        to_play = json.load(to_play_file)
        try:
            trmnts_to_play = to_play["to_play"]

            i_o_t_p = 0
            for t_p in trmnts_to_play:
                if t_p["now_playing"] == True:
                    to_play["to_play"][i_o_t_p]["current_round"]["hitted"] = hitted
                    in_of_team = 0
                    for team in to_play["to_play"][i_o_t_p]["teams"]:
                        if team["name"] == to_play["to_play"][i_o_t_p]["current_round"]["1_player"]["team"]:
                            in_of_player = 0
                            for player in team["players"]:
                                if player["name"] == to_play["to_play"][i_o_t_p]["current_round"]["1_player"]["name"]:
                                    to_play["to_play"][i_o_t_p]["teams"][in_of_team]["players"][in_of_player]["hits"][str(hitted)] += 1
                                    break
                                in_of_player += 1
                        
                        in_of_team += 1

                    to_play_file.seek(0)
                    to_play_file.write(json.dumps(to_play, ensure_ascii=False, indent=8))
                    to_play_file.truncate()

                    return to_play["to_play"][i_o_t_p]

                i_o_t_p += 1
            
        except:
           return -1


async def set_blocked_to_play_json(blocked):
    with open("to_play.json", "r+", encoding="utf-8") as to_play_file:
        to_play = json.load(to_play_file)
        try:
            trmnts_to_play = to_play["to_play"]

            i_o_t_p = 0
            for t_p in trmnts_to_play:
                if t_p["now_playing"] == True:
                    to_play["to_play"][i_o_t_p]["current_round"]["blocked"] = blocked
                    in_of_team = 0
                    for team in to_play["to_play"][i_o_t_p]["teams"]:
                        if team["name"] == to_play["to_play"][i_o_t_p]["current_round"]["2_player"]["team"]:
                            in_of_player = 0
                            for player in team["players"]:
                                if player["name"] == to_play["to_play"][i_o_t_p]["current_round"]["2_player"]["name"]:
                                    to_play["to_play"][i_o_t_p]["teams"][in_of_team]["players"][in_of_player]["blocks"][str(blocked)] += 1
                                    break
                                in_of_player += 1
                        
                        in_of_team += 1

                    to_play_file.seek(0)
                    to_play_file.write(json.dumps(to_play, ensure_ascii=False, indent=8))
                    to_play_file.truncate()

                    return to_play["to_play"][i_o_t_p]

                i_o_t_p += 1
            
        except:
            return -1


async def set_is_goal_to_play_json(is_goal):
    with open("to_play.json", "r+", encoding="utf-8") as to_play_file:
        to_play = json.load(to_play_file)
        try:
            trmnts_to_play = to_play["to_play"]

            i_o_t_p = 0
            for t_p in trmnts_to_play:
                if t_p["now_playing"] == True:
                    to_play["to_play"][i_o_t_p]["current_round"]["goal"] = is_goal

                    to_play_file.seek(0)
                    to_play_file.write(json.dumps(to_play, ensure_ascii=False, indent=8))
                    to_play_file.truncate()

                    return to_play["to_play"][i_o_t_p]

                i_o_t_p += 1
            
        except:
            return -1