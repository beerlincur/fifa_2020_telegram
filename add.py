import json


async def add_tournament_to_json(tourn_data):
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        
        try:
            am_of_teams = tourn_data.get("amount_of_teams")
            am_of_players = tourn_data.get("amount_of_players")
            start_time = tourn_data.get("start_time")

            am_of_games = int((am_of_teams * (am_of_teams - 1)) / 2)
            
            if am_of_teams % 2 == 0:
                am_of_tours = am_of_teams - 1
            else:
                am_of_tours = am_of_teams
            
            bank = float(tourn_data.get("bet")) * float(am_of_teams)
            t = {
                "name": tourn_data.get("name"),
                "isFormed": False,
                "typeOfTournament": tourn_data.get("typeOfTournament"),
                "money" : {
                    "bank": bank,
                    "fond": bank * 0.8,
                    "admins_money": bank * 0.2
                },    
                "start_time": start_time,
                "amount_of_teams": am_of_teams,
                "amount_of_players": am_of_players,
                "amount_of_tours": am_of_tours,
                "amount_of_games": am_of_games,
                "amount_of_rounds": 0,
                "teams": [],
                "games": [],
                "tours": [],
                "rounds": []
            }

            data["tournaments"].append(t)

            file.seek(0)
            file.write(json.dumps(data, ensure_ascii=False, indent=8))
            file.truncate()
            
            return True
        except:
            return False


async def add_team_to_tourn_json(team_data):
     with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        try:
            trmnts = data["tournaments"]
            t_name = team_data.get("tournament")
            name = team_data.get("name")

            for t in trmnts:
                if t["name"] == t_name:
                    if len(t["teams"]) < t["amount_of_teams"]:
                        team = {
                            "name": name,
                            "captain_name": None,
                            "captain_id": 0,
                            "winning" : 0,
                            "number": len(t["teams"]) + 1,
                            "amount_of_players": t["amount_of_players"],
                            "players": [],
                            "score": 0,
                            "goals": 0,
                            "misses": 0
                        }

                        t["teams"].append(team)
                        break
                    else:
                        return False

            file.seek(0)
            file.write(json.dumps(data, ensure_ascii=False, indent=8))
            file.truncate()

            return True
        except:
            return False


async def add_player_to_team_json(player_data, isCaptain):
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        try:
            trmnts = data["tournaments"]
            tourn_name = player_data.get("tournament")
            team_name = player_data.get("team")
            if isCaptain:
                player_name = player_data.get("name")
                player_id = player_data.get("idd")

                player = {
                    "name": player_name,
                    "id": int(player_id),
                    "captain_name": player_name,
                    "captain_id": int(player_id),
                    "team": team_name,
                    "hits": {
                        0: 0,
                        1: 0,
                        2: 0
                    },
                    "blocks": {
                        0: 0,
                        1: 0,
                        2: 0
                    },
                    "score": 0,
                    "saves": 0
                }

                for to in trmnts:
                    if to["name"] == tourn_name:
                        for team in to["teams"]:
                            if team["name"] == team_name:
                                if len(team["players"]) < team["amount_of_players"]:
                                    team["captain_name"] = player_name
                                    team["captain_id"] = int(player_id)
                                    team["players"].append(player)
                                    break
                                else:
                                    return False
                        break
            else:
                player_name = player_data.get("name")

                for to in trmnts:
                    if to["name"] == tourn_name:
                        for team in to["teams"]:
                            if team["name"] == team_name:
                                if team["captain_name"] != None:
                                    if len(team["players"]) < team["amount_of_players"]:

                                        player = {
                                            "name": player_name,
                                            "id": None,
                                            "captain_name": team["captain_name"],
                                            "captain_id": team["captain_id"],
                                            "team": team_name,
                                            "hits": {
                                                0: 0,
                                                1: 0,
                                                2: 0
                                            },
                                            "blocks": {
                                                0: 0,
                                                1: 0,
                                                2: 0
                                            },
                                            "score": 0,
                                            "saves": 0
                                        }

                                        team["players"].append(player)
                                        break
                                    else:
                                        return False
                                else:
                                    return False
                        break

            
            file.seek(0)
            file.write(json.dumps(data, ensure_ascii=False, indent=8))
            file.truncate()

            return True

        except:
            return False


async def add_tournament_to_play_json(tourn_name):
    with open("tournaments.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        try:
            trmnts = data["tournaments"]
            
            for t in trmnts:
                if t["name"] == tourn_name:
                    with open("to_play.json", "r+", encoding="utf-8") as to_play_file:
                        to_play = json.load(to_play_file)
                        tp = {
                            "name": t["name"],
                            "now_playing": False,
                            "current_round": t["rounds"][0],
                            "typeOfTournament": t["typeOfTournament"],
                            "money": t["money"],
                            "start_time": t["start_time"],
                            "amount_of_teams": t["amount_of_teams"],
                            "amount_of_players": t["amount_of_players"],
                            "amount_of_tours": t["amount_of_tours"],
                            "amount_of_games": t["amount_of_games"],
                            "amount_of_rounds": t["amount_of_rounds"],
                            "teams": t["teams"]
                        }
                        
                        to_play["to_play"].append(tp)

                        to_play_file.seek(0)
                        to_play_file.write(json.dumps(to_play, ensure_ascii=False, indent=8))
                        to_play_file.truncate()
                    break
            
            return True
            
        except:
            return False