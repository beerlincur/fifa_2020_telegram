#|------------------------ IMPORTS -------------------|
import os, re, logging, asyncio

from random import randint as ri
from time import gmtime, strftime, sleep
from aiogram.types.message import ContentTypes
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN, BOT_URL, PROXIE_AUTH, PROXIE_URL, ADMINS_IDS, START_PLAYING_KEYBOARD,\
     HIT_KEYBOARD, BLOCK_KEYBOARD, SUPPORT_KEYBOARD, GOAL_RESULT, HIT_RESULT, BLOCK_RESULT, PLAY_ROUND_KEYBOARD, \
         TOURNS_MENU, MAIN_KEYBOARD_2, TEAMS_MENU, PLAYERS_MENU, MAIN_CANCEL

from states import TournamentForm, TeamForm, PlayerForm, GenerateTournamentForm, GetTournamentInfoForm, \
    PlayRound, GetArchiveTournamentForm, ConfirmPartForm

from get import get_tournaments_string, get_tournaments_dict, \
    get_teams_dict, get_teams_string, get_tournament_info, get_to_play_tournaments_string, \
        get_to_play_tournaments_dict, get_now_playing_tournament, \
            get_archive_tournaments_string, get_archive_tournaments_dict, get_archive_tournament_info_string,\
                 get_archive_tournament_schedule, get_archive_tourn_history, get_players_dict, get_players_string,\
                     get_seris_to_play, get_team_score, get_tournament_by_name, get_tournament_info_string,\
                         get_player_stat, get_best_hitter_blocker, get_archive_tourn_by_name

from add import add_tournament_to_json, add_team_to_tourn_json, add_player_to_team_json

from do import do_generate_tournament_json, do_archive_tournament, do_show_tournament_schedule_string, do_confirm_player_part

from set_info import set_now_playing_true, set_now_playing_false, set_next_round_to_play, set_hitted_to_play_json, set_blocked_to_play_json, set_is_goal_to_play_json

#|---------------------- CODE ------------------------|

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()

storage = MemoryStorage()

bot = Bot(token=TOKEN, proxy=PROXIE_URL, proxy_auth=PROXIE_AUTH)

dp = Dispatcher(bot, storage=storage, loop=loop)


@dp.callback_query_handler(lambda callback_query: True, state="*")
async def start_hit_block_results(callback_query: types.CallbackQuery, state: FSMContext):

    if callback_query.data == "main_cancel":
        
        if state:
            await state.reset_state(with_data=False)

        await callback_query.message.answer("Вы отменили действие.", reply_markup=MAIN_KEYBOARD_2)
    
    elif callback_query.data == "start_round":

        if callback_query.from_user.id in ADMINS_IDS:
            is_set = await get_now_playing_tournament()

            t_t = await get_tournament_by_name(is_set["name"])

            if is_set["current_round"]["through_round_number"] == 1:
                pass # приветственное сообщение в самом начале турнира

            if is_set["current_round"]["number"] == 1:

                torun_hello = "Мы приветствуем вас на матче " + str(is_set["current_round"]["through_tour_number"]) + "-го тура турнира " + is_set["name"] +\
                    "!\n\nВстречаются команды\n" + is_set["current_round"]["1_player"]["team"].upper() + " и " + is_set["current_round"]["2_player"]["team"].upper() +\
                        "\n\nПредставляем составы играющих команд:\n\n" + "Команда " + is_set["current_round"]["1_player"]["team"].upper() + ":\n"

                for team in is_set["teams"]:
                    if team["name"] == is_set["current_round"]["1_player"]["team"]:
                        n_o_p = 1
                        for player in team["players"]:
                            name = player["name"]
                            torun_hello += f"№{n_o_p} {name}"
                            if player["name"] == player["captain_name"]:
                                torun_hello += " (К)"
                            torun_hello += "\n"
                            n_o_p += 1
                        break

                torun_hello = torun_hello + "\nКоманда " + is_set["current_round"]["2_player"]["team"].upper() + ":\n"

                for team in is_set["teams"]:
                    if team["name"] == is_set["current_round"]["2_player"]["team"]:
                        n_o_p = 1
                        for player in team["players"]:
                            name = player["name"]
                            torun_hello += f"№{n_o_p} {name}"
                            if player["name"] == player["captain_name"]:
                                torun_hello += " (К)"
                            torun_hello += "\n"
                            n_o_p += 1
                        break


                torun_hello = torun_hello + "\nПеред этим матчем, команды занимают следующие места:\n\n"

                number = 1
                for team in is_set["teams"]:
                    name = team["name"]
                    score = team["score"]
                    goals = team["goals"]
                    misses = team["misses"]
                    
                    torun_hello += f"🎉{number}-е место {name}\nОчки: {score}\nЗаб-Проп: {goals}-{misses}\n\n"
                    number += 1

                torun_hello += "\n"

                torun_hello += await do_show_tournament_schedule_string(is_set["name"])

                torun_hello += "\n\n"

                torun_hello += await get_seris_to_play(is_set["name"], is_set["current_round"]["through_game_number"], is_set["current_round"]["taim"])

                await callback_query.message.answer(torun_hello)

            f_team_score = await get_team_score(is_set["name"], is_set["current_round"]["through_game_number"], 1)

            s_team_score = await get_team_score(is_set["name"], is_set["current_round"]["through_game_number"], 2)

            

            if is_set["current_round"]["number"] % 2 == 0:
                player_info = is_set["current_round"]["2_player"]["team"].upper() + " - " + is_set["current_round"]["1_player"]["team"].upper() + f" {f_team_score}:{s_team_score}\n" +\
                    str(is_set["current_round"]["taim"]) + "-й тайм\n" + str(is_set["current_round"]["seria"]) + "-Я СЕРИЯ УДАРОВ. "
                player_info += "Ответный удар\n"
            else:
                player_info = is_set["current_round"]["1_player"]["team"].upper() + " - " + is_set["current_round"]["2_player"]["team"].upper() + f" {f_team_score}:{s_team_score}\n" +\
                    str(is_set["current_round"]["taim"]) + "-й тайм\n" + str(is_set["current_round"]["seria"]) + "-Я СЕРИЯ УДАРОВ. "

                player_info += "Первый удар\n"


            player_info = player_info + "Атакует: " + is_set["current_round"]["1_player"]["name"].upper() + "\nЗащищается: " + is_set["current_round"]["2_player"]["name"].upper()

            sleep(1)

            await callback_query.message.answer(player_info)
            

            hit_info = is_set["current_round"]["1_player"]["name"].upper() + " (" + is_set["current_round"]["1_player"]["team"] + ")\n" +\
                await get_player_stat(is_set, is_set["current_round"]["1_player"]["team"], is_set["current_round"]["1_player"]["name"]) + "\n" +\
                "наносит удар по воротам:"

            sleep(2)

            await callback_query.message.answer(hit_info, reply_markup=HIT_KEYBOARD)
        else:
            return

    elif callback_query.data == "cancel_round":

        if callback_query.from_user.id in ADMINS_IDS:
            t = await get_now_playing_tournament()

            is_set = await set_now_playing_false(t["name"])
            await callback_query.message.answer("Вы отменили начало игры.", reply_markup=MAIN_KEYBOARD_2)
        else:
            return
        
    
    elif callback_query.data in ["hit_left", "hit_center", "hit_right"]:

        now_playing = await get_now_playing_tournament()

        if callback_query.from_user.id in [now_playing["current_round"]["1_player"]["id"], now_playing["current_round"]["1_player"]["captain_id"]] or callback_query.from_user.id in ADMINS_IDS:

            hit_result = HIT_RESULT[callback_query.data]
            t = await set_hitted_to_play_json(hit_result)
            if t != -1:
                
                block_info = t["current_round"]["2_player"]["name"].upper() + " (" + t["current_round"]["2_player"]["team"] + ")\n" +\
                    await get_player_stat(t, t["current_round"]["2_player"]["team"], t["current_round"]["2_player"]["name"]) + "\n" +\
                    "защищает ворота:"
                
                sleep(2)
                
                await callback_query.message.answer(block_info, reply_markup=BLOCK_KEYBOARD)

            else:
                await callback_query.message.answer("Ошибка! При записи результата удара произошла ошибка.")
        else:
            return


    elif callback_query.data in ["block_left_center", "block_right_center", "block_left_right"]:

        now_playing = await get_now_playing_tournament()

        if callback_query.from_user.id in [now_playing["current_round"]["2_player"]["id"], now_playing["current_round"]["2_player"]["captain_id"]] or callback_query.from_user.id in ADMINS_IDS:
        
            block_result = BLOCK_RESULT[callback_query.data]

            t = await set_blocked_to_play_json(block_result)

            hit_result = t["current_round"]["hitted"]
            tour = t["current_round"]["through_tour_number"]

            text_result = GOAL_RESULT[(hit_result, block_result)][0]
            l_r_variant = ri(1, 5)
            long_result = GOAL_RESULT[(hit_result, block_result)][l_r_variant]
            is_goal = GOAL_RESULT[(hit_result, block_result)][-1]

            t_after_goal_result = await set_is_goal_to_play_json(is_goal)

            tourn_before_next = await get_tournament_by_name(t_after_goal_result["name"])

            is_set_to_next = await set_next_round_to_play(t_after_goal_result)

            f_team_score = await get_team_score(t["name"], t["current_round"]["through_game_number"], 1)

            s_team_score = await get_team_score(t["name"], t["current_round"]["through_game_number"], 2)

            goal_info = str(t["current_round"]["number"]) + "' " + text_result + f" {f_team_score}:{s_team_score}"

            if is_goal:
                goal_info = goal_info + " ⚽️\n" + t["current_round"]["1_player"]["name"] + " (" + t["current_round"]["1_player"]["team"] + ") " + long_result
            
            else:
                goal_info = goal_info + " 🚫\n" + t["current_round"]["2_player"]["name"] + " (" + t["current_round"]["2_player"]["team"] + ") " + long_result

            await callback_query.message.answer(goal_info)

            tourn_after_next = await get_tournament_by_name(t_after_goal_result["name"])

            if is_set_to_next != False:
                
                return_code, to_return = is_set_to_next
            
            else:

                await callback_query.message.answer("Ошибка!")
                return

            is_set = await set_now_playing_true(t_after_goal_result["name"])

            #⚽️🚫🥅🔥🎬⌚️

            if return_code[1]:

                if not return_code[4]:
                    
                    if not return_code[2]:
                    
                        fut_taim_text = "⌚️Через несколько секунд начнется " + str(is_set["current_round"]["taim"]) + "-й тайм матча команд\n" +\
                            is_set["current_round"]["1_player"]["team"] + " и " + is_set["current_round"]["2_player"]["team"] + ".\n\n"

                        sleep(2)

                        await callback_query.message.answer(fut_taim_text)

                        fut_taim_schedule = await get_seris_to_play(is_set["name"], is_set["current_round"]["through_game_number"], is_set["current_round"]["taim"])

                        sleep(2)

                        await callback_query.message.answer(fut_taim_schedule)

                taim_result = to_return[1]
                prev_tai = t_after_goal_result["current_round"]["taim"]

                prev_taim_text = "🎬После " + str(prev_tai) + "-го тайма, счет " + str(taim_result["1_score"]) + ":" + str(taim_result["2_score"]) + ",\n"

                if taim_result["1_score"] > taim_result["2_score"]:

                    prev_taim_text = prev_taim_text + "впереди команда " + taim_result["1_team"]["name"] + "!\n\n"

                    first_score = 0
                    second_score = 0

                    first_team_name = taim_result["1_team"]["name"]
                    
                    second_team_name = taim_result["2_team"]["name"]

                    for roun in taim_result["rounds"]:
                        if roun["taim"] == prev_tai:
                            if roun["goal"]:
                                if roun["1_player"]["team"] == first_team_name:
                                    first_score += 1
                                else:
                                    second_score += 1

                    first_score = taim_result["1_score"] - first_score
                    second_score = taim_result["2_score"] - second_score

                    for roun in taim_result["rounds"]:
                        if roun["taim"] == prev_tai:
                            if roun["goal"]:
                                if roun["1_player"]["team"] == first_team_name:
                                    first_score += 1
                                else:
                                    second_score += 1

                                prev_taim_text = prev_taim_text + "⚽️" + str(roun["number"]) + "' " + roun["1_player"]["name"] + " (" + roun["1_player"]["team"] +\
                                     f", {first_score}:{second_score})\n"

                elif taim_result["1_score"] < taim_result["2_score"]:

                    prev_taim_text = prev_taim_text + "впереди команда " + taim_result["2_team"]["name"] + "!\n\n"

                    first_score = 0
                    second_score = 0

                    
                    first_team_name = taim_result["1_team"]["name"]
                    
                    second_team_name = taim_result["2_team"]["name"]

                    for roun in taim_result["rounds"]:
                        if roun["taim"] == prev_tai:
                            if roun["goal"]:
                                if roun["1_player"]["team"] == first_team_name:
                                    first_score += 1
                                else:
                                    second_score += 1

                    first_score = taim_result["1_score"] - first_score
                    second_score = taim_result["2_score"] - second_score
                    

                    for roun in taim_result["rounds"]:
                        if roun["taim"] == prev_tai:
                            if roun["goal"]:
                                if roun["1_player"]["team"] == first_team_name:
                                    first_score += 1
                                else:
                                    second_score += 1

                                prev_taim_text = prev_taim_text + "⚽️" + str(roun["number"]) + "' " + roun["1_player"]["name"] + " (" + roun["1_player"]["team"] +\
                                     f", {first_score}:{second_score})\n"

                elif taim_result["1_score"] == taim_result["2_score"]:
                    
                    prev_taim_text = prev_taim_text + "ничья между командами " + taim_result["1_team"]["name"] + " и " + taim_result["2_team"]["name"] + "!\n\n"

                    first_score = 0
                    second_score = 0

                    first_team_name = taim_result["1_team"]["name"]
                    
                    second_team_name = taim_result["2_team"]["name"]



                    for roun in taim_result["rounds"]:
                        if roun["taim"] == prev_tai:
                            if roun["goal"]:
                                if roun["1_player"]["team"] == first_team_name:
                                    first_score += 1
                                else:
                                    second_score += 1

                    first_score = taim_result["1_score"] - first_score
                    second_score = taim_result["2_score"] - second_score

                    for roun in taim_result["rounds"]:
                        if roun["taim"] == prev_tai:
                            if roun["goal"]:
                                if roun["1_player"]["team"] == first_team_name:
                                    first_score += 1
                                else:
                                    second_score += 1

                                prev_taim_text = prev_taim_text + "⚽️" + str(roun["number"]) + "' " + roun["1_player"]["name"] + " (" + roun["1_player"]["team"] +\
                                     f", {first_score}:{second_score})\n"
                
                sleep(2)

                await callback_query.message.answer(prev_taim_text)


            if return_code[2]:
                game_results = to_return[2]
                game_number = game_results["number"]
                f_team_name = game_results["1_team"]["name"].upper()
                f_team_score = game_results["1_score"]
                s_team_name = game_results["2_team"]["name"].upper()
                s_team_score = game_results["2_score"]
                winner = game_results["winner"]
                t_winner = ""
                cur_tour_number = str(is_set["current_round"]["through_tour_number"])
                tourn_name = is_set["name"]

                if len(winner) == 2:
                    f_get = 1
                    s_get = 1
                    result = f"👑Завершился матч {cur_tour_number}-го тура турнира {tourn_name} между командами {f_team_name} и {s_team_name}\nНичья {f_team_score}:{s_team_score}\n\n"

                else:
                    
                    win_get = 3
                    loser_get = 0

                    if winner["name"].upper() == f_team_name:
                        result = f"👑Завершился матч {cur_tour_number}-го тура турнира {tourn_name}. Со счетом {f_team_score}:{s_team_score} команда {f_team_name} одержала победу над командой {s_team_name}\n\n"

            

                    else:
                        result = f"👑Завершился матч {cur_tour_number}-го тура турнира {tourn_name}. Со счетом {s_team_score}:{f_team_score} команда {s_team_name} одержала победу над командой {f_team_name}\n\n"

                result += f"{f_team_name} - {s_team_name} {f_team_score} : {s_team_score}\n"


                first_score = 0
                second_score = 0
                
                for roun in game_results["rounds"]:
                    if roun["goal"]:
                        if roun["1_player"]["team"] == first_team_name:
                            first_score += 1
                        else:
                            second_score += 1

                first_score = f_team_score - first_score
                second_score = s_team_score - second_score

                for roun in game_results["rounds"]:
                    if roun["goal"]:
                        if roun["1_player"]["team"] == first_team_name:
                            first_score += 1
                        else:
                            second_score += 1
                        
                        result = result + "⚽️" + str(roun["number"]) + "' " + roun["1_player"]["name"] + " (" + roun["1_player"]["team"] +\
                                f") {first_score}:{second_score}\n"

                #👑⚽️🎬🎉

                result += "\n🎬Турнирная таблица:\n"
                
                n_o_t = 1
                for team in is_set["teams"]:
                    name = team["name"]
                    score = team["score"]
                    goals = team["goals"]
                    misses = team["misses"]
                    
                    result += f"🎉{n_o_t}-е место {name}\nОчки: {score}\nЗаб-Проп: {goals}-{misses}\n\n"
                    n_o_t += 1

                sleep(2)


                await callback_query.message.answer(result)

            if return_code[3]:

                #🥇🥈🥉

                sleep(1)
                await callback_query.message.answer(f"Тур номер {tour} завершен:\n")
                semi_result = "🎬Турнирная таблица:\n"

                for number, name, score, goals, misses in to_return[3]:
                    
                    semi_result += f"🎉{number}-е место {name}\nОчки: {score}\nЗаб-Проп: {goals}-{misses}\n\n"

                sleep(1)

                await callback_query.message.answer(semi_result)

            if return_code[4]:

                sleep(1)

                await callback_query.message.answer("👑Турнир завершен! Подробную историю турнира Вы можете посмотреть в Архивных турнирах.", reply_markup=MAIN_KEYBOARD_2)
                
                bests = await get_best_hitter_blocker(is_set["teams"])
                
                result = "🔥Финальная турнирная таблица:🔥\n"
                
                for number, name, score, winning, goals, misses in to_return[4]:
                    if number == 1:
                        result += "🥇"
                    elif number == 2:
                        result += "🥈"
                    elif number == 3:
                        result += "🥉"
                    else:
                        result += "🎉"

                    result += f"{number}-е место {name}\nОчки: {score}\nВыигрыш: {winning}\nЗаб-Проп: {goals}-{misses}\n\n"

                sleep(1)

                await callback_query.message.answer(bests)
                
                sleep(1)

                await callback_query.message.answer(result)

                is_set = await set_now_playing_false(t_after_goal_result["name"])

                is_archived = await do_archive_tournament(t_after_goal_result["name"])

                sleep(1)

                his = await get_archive_tourn_history(t_after_goal_result["name"])

                if len(his) > 4096:
                    for x in range(0, len(his), 4096):
                        await callback_query.message.answer(his[x:x+4096])
                else:
                        await callback_query.message.answer(his)

            if return_code[0] and not return_code[4]:
                if to_return[0]:
                    sleep(1)
                    await callback_query.message.answer("Чтобы начать следующий раунд, арбитр матча должен нажать 'Начать'.\nДля отмены нажать 'Отмена'.", reply_markup=PLAY_ROUND_KEYBOARD)

                else:
                    await callback_query.message.answer("Ошибка!")
        else:
            return


@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    start_text = """
Добро пожаловать в мир кроунбола - нового футбольного симулятора, созданного в период самоизоляции.👽

Кроунбол (Crownball) - это командная игра с простыми правилами.⚽️

Количество игроков в команде - от 1 до 3 (в зависимости от турнира).🏆
Длительность одного матча - от 3 до 15 минут.⌚️
Матчи проводятся в мессенджере Телеграм.📲

Мы проводим как однодневные, так и долгосрочные турниры по кроунболу.📈
А также коммерческие турниры с призовым фондом!💰

Если Вы попали сюда после сообщения капитана команды, 
то подтвердите свое участие, следуя инструкции из сообщения капитана.

Если Вы случайно набрели на этого бота и хотите сыграть, 
то Вам необходимо связаться с одним из администраторов и уточнить расписание планируемых турниров.

Если Вы капитан команды или арбитр матча, 
то Вам следует нажать команду /help и ознакомиться с подробной инструкцией использования этого бота.

Чтобы просмотреть подробную инструкцию и ознакомиться с правилами кроунбола,
нажмите /help.📕

Наш сайт http://wmfl.ru 🌍
Наша группа ВКонтакте - https://vk.com/rfleague 💌

Встретимся на игре!🔥
    """
    await message.answer(start_text, reply_markup=MAIN_KEYBOARD_2)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    help_text = """
📕Инструкция по использованию бота:

1. ИГРОК

Если Вы игрок, которому капитан команды отправил инструкцию, все что Вам нужно сделать - это успешно пройти шаги, указанные в ней, а именно:

а) Нажмите на кнопку 'Игроки' (если у Вас ее нет, нажмите 'Назад на главную')

b) Нажмите на кнопку 'Подтвердить участие'

c) Выберите номер, под которым записан турнир, указанный в Вашей инструкции

d) Выберите номер, под которым записана команда, указанная в Вашей инструкции

e) Выберите номер, под которым написано Ваше имя

f) Сообщите капитану команды об успешном подтверждении участия и следите за событиями в чате игры!

2. КАПИТАН КОМАНДЫ

Если Вы капитан команды и Вам сообщили о создании турнира, то Вам необходимо пройти следующие шаги:

а) Нажмите на кнопку 'Команды'

b) Нажмите на кнопку 'Добавить команду'

с) Из предложенного списка выберите НОМЕР необходимого турнира (в ответ отправьте только цифру-номер турнира)

d) Введите название Вашей команды

После получения ответа об успешном добавлении команды, Вы можете добавить игроков:

а) Нажмите на кнопку 'Игроки' (если у Вас ее нет, нажмите 'Назад на главную')

b) Нажмите на кнопку 'Добавить игрока'

c) Из предложенного списка выберите НОМЕР необходимого турнира

d) Из предложенного списка выберите НОМЕР Вашей команды

e) Для добавления себя, как капитана - перед своим именем введите слово Капитан, например, 'Капитан Кирилл'
Если Вы уже добавили себя и добавляете другого игрока команды, просто введите имя игрока.

f) После ввода имени игрока, Вы получите инструкцию, которую необходимо отправить игроку для того, чтобы он подтверждил свое участие.

g) Для добавления остальных игроков команды, Вам необходимо снова пройти шаги b) - g)

h) После того, как Вы добавили всех игроков и отправили всем инструкцию для подтверждения, уведомите администратора о добавлении игроков,
а также, проконтролируйте, чтобы все игроки подтвердили свое участие.

3. АРБИТР

Если Вы арбитр матча, то для начала игры, нажмите кнопку 'Играть' и затем (когда все будут готовы) нажмите 'Начать',
в течении игры вновь нажимайте 'Начать', если игра продолжается, или 'Отмена', если игра завершается.

4. АДМИНИСТРАТОР

Если Вы администратор, то для создания турнира Вам необходимо пройти следующий шаги:

а) Нажмите кнопку 'Турниры'

b) Нажмите кнопку 'Создать турнир' и следуйте диалогому порядку бота

с) После уведомления, об успешном создании турнира, уведомите всех капитанов команд,
что можно приступать к добавлению команд и игроков (для просмотра прогресса добавления команд, нажмите 'Активные турниры' и выберите нужный турнир)

d) После того, как все капитаны уведомили о добавлении команды и о том, что все игроки подтвердили участие,
нажмите кнопку 'Активные турниры' и выберите нужный турнир для того, чтобы удостовериться в корректности турнира

e) После того, как Вы уверены, что все капитаны добавили команд и игроков, и все игроки подтвердили участие,
нажмите кнопку 'Сформировать турнир' для формирования расписания турнира и открытия доступа для игры в него

f) После успешного формирования турнира, Вы также можете просматривать его в 'Активных турнирах'

g) Для того, чтобы начать турнир, следуйте инструкции для арбитра, описанной выше


4. СЛУЧАЙНЫЙ ИНТЕРНЕТНЫЙ ПРОХОЖИЙ

Если Вы случайный прохожий интернета, то свяжитесь с одним из администраторов в группе ВК, указанной в приветственном сообщении,
и уточните расписание планируемых турниров

Если у Вас есть идеи или предложения по улучшению бота или Вы просто хотите сказать 'Спасибо' разработчику - всегда на связи @zhozh_peppa.
Приятной игры!
    """
    await message.answer(help_text, reply_markup=MAIN_KEYBOARD_2)


@dp.message_handler(lambda message: message.text.lower() == "назад на главную")
async def main_menu(message: types.Message):
    await message.answer("Выберите пункт главного меню и нажмите на кнопку:", reply_markup=MAIN_KEYBOARD_2)


@dp.message_handler(lambda message: message.text.lower() == "турниры")
async def tournaments_menu(message: types.Message):
    await message.answer("Выберите действие и нажмите кнопку:", reply_markup=TOURNS_MENU)


@dp.message_handler(lambda message: message.text.lower() == "команды")
async def teams_menu(message: types.Message):
    await message.answer("Выберите действие и нажмите кнопку:", reply_markup=TEAMS_MENU)


@dp.message_handler(lambda message: message.text.lower() == "игроки")
async def players_menu(message: types.Message):
    await message.answer("Выберите действие и нажмите кнопку:", reply_markup=PLAYERS_MENU)


@dp.message_handler(lambda message: message.text.lower() == "добавить турнир")
async def add_tournament(message: types.Message):
    if message.chat.id in ADMINS_IDS:
        await message.answer("Введите название турнира:", reply_markup=MAIN_CANCEL)
        await TournamentForm.name.set()
    else:
        return


@dp.message_handler(state=TournamentForm.name)
async def get_tournament_name(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS_IDS:
        await state.update_data(name=message.text)
        await message.answer("Выберите тип турнира из списка ниже: (введите только цифру - номер типа турнира из списка)", reply_markup=MAIN_CANCEL)
        await message.answer("1. В 1 круг")

        await TournamentForm.typeOfTournament.set()
    else:
        return


@dp.message_handler(state=TournamentForm.typeOfTournament)
async def get_tournament_type(message: types.Message, state: FSMContext):

    if message.chat.id in ADMINS_IDS:
        tot = message.text

        types_of_tournaments = {
            1: "В 1 круг"
        }

        if tot.isdigit():
            if int(tot) in range(1, 2):
                await state.update_data(typeOfTournament=types_of_tournaments[int(tot)])
                await message.answer("Теперь введите турнирный взнос: ", reply_markup=MAIN_CANCEL)
                await TournamentForm.bet.set()
            else:
                await message.answer("Ошибка! Пожалуйста, введите только цифру - номер типа турнира из списка", reply_markup=MAIN_CANCEL)
                await TournamentForm.typeOfTournament.set()
        else:
            await message.answer("Ошибка! Пожалуйста, введите только цифру - номер типа турнира из списка", reply_markup=MAIN_CANCEL)
            await TournamentForm.typeOfTournament.set()
    else:
        return


@dp.message_handler(state=TournamentForm.bet)
async def get_tournament_bet(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS_IDS:
        tourn_bet = message.text

        if tourn_bet.isdigit():
            await state.update_data(bet=tourn_bet)
            await TournamentForm.amount_of_teams.set()
            await message.answer("Теперь введите количество команд:", reply_markup=MAIN_CANCEL)
        else:
            await message.answer("Ошибка! Введите число!", reply_markup=MAIN_CANCEL)
            await TournamentForm.bet.set()
    else:
        return


@dp.message_handler(state=TournamentForm.amount_of_teams)
async def get_tournament_amount_of_teams(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS_IDS:
        num_of_teams = message.text
        if num_of_teams.isdigit():
            if int(num_of_teams) in range(2, 17):
                await state.update_data(amount_of_teams=int(num_of_teams))
                await message.answer("Теперь введите количество игроков в командах: ", reply_markup=MAIN_CANCEL)
                await TournamentForm.amount_of_players.set()
            else:
                await message.answer("Ошибка! Введите число от 2 до 16.", reply_markup=MAIN_CANCEL)
                await TournamentForm.amount_of_teams.set()
        else:
            await message.answer("Ошибка! Введите число.", reply_markup=MAIN_CANCEL)
            await TournamentForm.amount_of_teams.set()
    else:
        return


@dp.message_handler(state=TournamentForm.amount_of_players)
async def get_tournament_amount_of_players(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS_IDS:
        num_of_players = message.text
        if num_of_players.isdigit():
            if int(num_of_players) in range(1, 4):
                await state.update_data(amount_of_players=int(num_of_players))
                await message.answer("Теперь введите время начала турнира в формате: год-месяц-день-время, например, 2020-04-24 12:00", reply_markup=MAIN_CANCEL)
                await TournamentForm.start_time.set()
            else:
                await message.answer("Ошибка! Введите число от 1 до 3.", reply_markup=MAIN_CANCEL)
                await TournamentForm.amount_of_players.set()
        else:
            await message.answer("Ошибка! Введите число.", reply_markup=MAIN_CANCEL)
            await TournamentForm.amount_of_players.set()
    else:
        return


@dp.message_handler(state=TournamentForm.start_time)
async def get_tournament_start_time(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS_IDS:
        st_time = message.text
        await state.update_data(start_time=st_time)
        isAdded = await add_tournament_to_json(await state.get_data())
        tourn_data = await state.get_data()
        if isAdded:
            await message.answer(await get_tournament_info_string(tourn_data.get("name")))
            await message.answer("Турнир был успешно добавлен! Теперь Вы можете добавить к нему команды.", reply_markup=MAIN_KEYBOARD_2)
            await state.reset_state(with_data=False)
        else:
            await message.answer("Ошибка! При добавлении турнира произошла ошибка.", reply_markup=MAIN_KEYBOARD_2)
            await state.reset_state(with_data=False)
    else:
        return


@dp.message_handler(lambda message: message.text.lower() == "добавить команду")
async def add_team_to_tournament(message: types.Message):
    if message.chat.id in ADMINS_IDS:
        t_string = await get_tournaments_string()
        if t_string:
            await message.answer("Выберите в какой турнир добавить эту команду: (введите только цифру - номер турнира из списка)", reply_markup=MAIN_CANCEL)
            await message.answer(t_string)
            await TeamForm.tournament.set()
        else:
            await message.answer("Ошибка! Сначала добавьте хотя бы один турнир!", reply_markup=MAIN_KEYBOARD_2)
    else:
        return


@dp.message_handler(state=TeamForm.tournament)
async def get_teams_tournament(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS_IDS:
        num_of_t = message.text
        
        if num_of_t.isdigit():
            t_dict = await get_tournaments_dict()
            try:
                tourn = t_dict[int(num_of_t)]
                await state.update_data(tournament=tourn)
                await message.answer("Теперь введите название команды:", reply_markup=MAIN_CANCEL)
                await TeamForm.name.set()
            except:
                await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
                await TeamForm.tournament.set()

        else:
            await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
            await TeamForm.tournament.set()
    else:
        return


@dp.message_handler(state=TeamForm.name)
async def get_teams_name(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS_IDS:
        await state.update_data(name=message.text)
        isAdded = await add_team_to_tourn_json(await state.get_data())

        if isAdded:
            await message.answer("Команда была успешно добавлена.", reply_markup=MAIN_KEYBOARD_2)
            await state.reset_state(with_data=False)
        else:
            await message.answer("Ошибка! При добавлении команды произошла ошибка. Возможно, турнир переполнен.", reply_markup=MAIN_KEYBOARD_2)
            await state.reset_state(with_data=False)
    else:
        return


@dp.message_handler(lambda message: message.text.lower() == "добавить игрока")
async def add_player_to_team(message: types.Message):
    t_string = await get_tournaments_string()
    if t_string:
        await message.answer("Выберите в какой турнир добавить этого игрока: (введите только цифру - номер турнира из списка)", reply_markup=MAIN_CANCEL)
        await message.answer(t_string)
        await PlayerForm.tournament.set()
    else:
        await message.answer("Ошибка! Добавьте хотя бы один турнир!", reply_markup=MAIN_KEYBOARD_2)


@dp.message_handler(state=PlayerForm.tournament)
async def get_player_tournament(message: types.Message, state: FSMContext):
    num_of_t = message.text
    
    if num_of_t.isdigit():
        t_dict = await get_tournaments_dict()
        try:
            tourn = t_dict[int(num_of_t)]
            await state.update_data(tournament=tourn)
            
            team_string = await get_teams_string(tourn)
            if team_string:
                await message.answer("Теперь выберите номер команды для добавления игрока:", reply_markup=MAIN_CANCEL)
                await message.answer(team_string)
                await PlayerForm.team.set()
            else:
                await message.answer("Ошибка! Добавьте хотя бы одну команду!", reply_markup=MAIN_KEYBOARD_2)
                await state.reset_state(with_data=False)
        except:
            await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
            await PlayerForm.tournament.set()

    else:
        await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
        await PlayerForm.tournament.set()


@dp.message_handler(state=PlayerForm.team)
async def get_player_team(message: types.Message, state: FSMContext):
    num_of_team = message.text
    
    if num_of_team.isdigit():
        data = await state.get_data()
        tourn = data.get("tournament")
        team_dict = await get_teams_dict(tourn)
        try:
            team = team_dict[int(num_of_team)]
            await state.update_data(team=team)
            await message.answer("Теперь введите имя игрока:", reply_markup=MAIN_CANCEL)
            await PlayerForm.name.set()
        except:
            await message.answer("Ошибка! Введите только цифру - номер команды из списка.", reply_markup=MAIN_CANCEL)
            await PlayerForm.team.set()
    else:
        await message.answer("Ошибка! Введите только цифру - номер команды из списка.", reply_markup=MAIN_CANCEL)
        await PlayerForm.team.set()


@dp.message_handler(state=PlayerForm.name)
async def get_player_team(message: types.Message, state: FSMContext):
    text = message.text
    isCaptain = False

    if text.lower().startswith("капитан"):
        isCaptain = True
        name = " ".join(text.split()[1:])
        await state.update_data(name=name, idd=message.chat.id)
    else:
        name = text
        await state.update_data(name=name)
    
    data = await state.get_data()

    team_name = data.get("team")

    tourn_name = data.get("tournament")

    isAdded = await add_player_to_team_json(data, isCaptain)

    if isAdded:
        if isCaptain:
            await message.answer(f"{name}, Вы были успешно добавлены как капитан команды {team_name}.")
            await state.reset_state(with_data=False)
        else:
            await message.answer(f"Игрок {name} был успешно добавлен в команду {team_name}.")
            inst = f"""
Отправьте эту инструкцию игроку {name}, 
он должен подтвердить свое участие в турнире, пройдя следующие шаги:

1. Зайти в личный чат с ботом, @Mister_F_bot

2. Перейти во вкладку Игроки с помощью клавиатуры

3. Нажать на кнопку Подтвердить участие

4. Выбрать номер, под которым записан турнир {tourn_name}

5. Выбрать номер, под которым записана команда {team_name}

ВНИМАНИЕ! После выполнения шага №6 игрок подтверждает свое участие! Будьте внимательны при выборе номера!

6. Ввести номер, под которым написано его имя {name}.

7. Сообщить капитану команды об успешном подтверждении участия.
            """
            await message.answer(inst)
            await state.reset_state(with_data=False)
    else:
        await message.answer("Ошибка! При добавлении игрока произошла ошибка. Либо команда переполнена, либо Вы не добавили капитана.", reply_markup=MAIN_KEYBOARD_2)
        await state.reset_state(with_data=False)


@dp.message_handler(lambda message: message.text.lower() == "подтвердить участие")
async def confirm_participation(message: types.Message):
    t_string = await get_tournaments_string()
    if t_string:
        await message.answer("Выберите номер турнира для подтверждения участия: (введите только цифру - номер турнира из списка)", reply_markup=MAIN_CANCEL)
        await message.answer(t_string)
        await ConfirmPartForm.tournament.set()
    else:
        await message.answer("Ошибка! Добавьте хотя бы один турнир!", reply_markup=MAIN_KEYBOARD_2)


@dp.message_handler(state=ConfirmPartForm.tournament)
async def get_tourn_to_confirn_part(message: types.Message, state: FSMContext):
    num_of_t = message.text
    
    if num_of_t.isdigit():
        t_dict = await get_tournaments_dict()
        try:
            tourn = t_dict[int(num_of_t)]
            await state.update_data(tournament=tourn)
            
            team_string = await get_teams_string(tourn)
            if team_string:
                await message.answer("Теперь выберите номер команды для подтверждения участия:", reply_markup=MAIN_CANCEL)
                await message.answer(team_string)
                await ConfirmPartForm.team.set()
            else:
                await message.answer("Ошибка! Добавьте хотя бы одну команду!", reply_markup=MAIN_KEYBOARD_2)
                await state.reset_state(with_data=False)
        except:
            await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
            await ConfirmPartForm.tournament.set()

    else:
        await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
        await ConfirmPartForm.tournament.set()


@dp.message_handler(state=ConfirmPartForm.team)
async def get_team_to_confirm_part(message: types.Message, state: FSMContext):
    num_of_team = message.text
    
    if num_of_team.isdigit():
        data = await state.get_data()
        tourn = data.get("tournament")
        team_dict = await get_teams_dict(tourn)
        try:
            team = team_dict[int(num_of_team)]
            await state.update_data(team=team)
            
            p_string = await get_players_string(await state.get_data())
            if p_string:

                await message.answer("Теперь введите номер, под которым написано Ваше имя:\nБУДЬТЕ ВНИМАТЕЛЬНЫ! ОТПРАВЛЯЯ НОМЕР, ВЫ ПОДТВЕРЖДАЕТЕ УЧАСТИЕ В ТУРНИРЕ!", reply_markup=MAIN_CANCEL)
                await message.answer(p_string)
                await ConfirmPartForm.name.set()
            else:
                await message.answer("Ошибка! Дождитесь пока капитан команды внесет игроков в список.", reply_markup=MAIN_KEYBOARD_2)

        except:
            await message.answer("Ошибка! Введите только цифру - номер команды из списка.", reply_markup=MAIN_CANCEL)
            await ConfirmPartForm.team.set()
    else:
        await message.answer("Ошибка! Введите только цифру - номер команды из списка.", reply_markup=MAIN_CANCEL)
        await ConfirmPartForm.team.set()


@dp.message_handler(state=ConfirmPartForm.name)
async def get_player_name_to_confirm(message: types.Message, state: FSMContext):
    num_of_player = message.text
    
    if num_of_player.isdigit():

        if int(num_of_player) != 1:

            data = await state.get_data()
            player_dict = await get_players_dict(data)
            try:
                player = player_dict[int(num_of_player)]
                await state.update_data(name=player, idd=message.chat.id)

                isConfirmed = await do_confirm_player_part(await state.get_data())
                
                if isConfirmed:
                    await message.answer("Вы успешно подтвердили участие! Следите за сообщениями от капитана, чтобы не пропустить свой ход.", reply_markup=MAIN_KEYBOARD_2)
                    await state.reset_state(with_data=False)
                    
                else:
                    await message.answer("Ошибка! При подтверждении Вашего участия произошла ошибка.", reply_markup=MAIN_KEYBOARD_2)
                    await state.reset_state(with_data=False)

            except:
                await message.answer("Ошибка! Введите только цифру - Ваш номер из списка игроков.", reply_markup=MAIN_CANCEL)
                await ConfirmPartForm.name.set()

        else:
            await message.answer("Ошибка! Капитан уже подтвердил свое участие, выберите СВОЙ номер. (Если в списке только капитан, отмените подтверждение и дождитесь пока капитан добавит Вас в список)", reply_markup=MAIN_CANCEL)
            await ConfirmPartForm.name.set()
    else:
        await message.answer("Ошибка! Введите только цифру - Ваш номер из списка игроков.", reply_markup=MAIN_CANCEL)
        await ConfirmPartForm.name.set()


@dp.message_handler(lambda message: message.text.lower() == "сформировать турнир")
async def generate_tournament(message: types.Message):
    if message.chat.id in ADMINS_IDS:
        t_string = await get_tournaments_string()
        if t_string:
            await message.answer("Выберите какой турнир сформировать: (введите только цифру - номер турнира из списка)", reply_markup=MAIN_CANCEL)
            await message.answer(t_string)
            await GenerateTournamentForm.tournament.set()
        else:
            await message.answer("Ошибка! Добавьте хотя бы один турнир!", reply_markup=MAIN_KEYBOARD_2)
    else:
        return


@dp.message_handler(state=GenerateTournamentForm.tournament)
async def get_tournament_to_generate(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS_IDS:
        num_of_t = message.text
        
        if num_of_t.isdigit():
            t_dict = await get_tournaments_dict()
            try:
                tourn = t_dict[int(num_of_t)]
                await state.update_data(tournament=tourn)
                isGenerated = await do_generate_tournament_json(await state.get_data())
                if isGenerated:
                    
                    await message.answer(await get_tournament_info_string(tourn))
                    
                    await message.answer(await do_show_tournament_schedule_string(tourn))

                    await message.answer("Турнир был успешно сформирован!", reply_markup=MAIN_KEYBOARD_2)

                    await state.reset_state(with_data=False)
                else:
                    await message.answer("Ошибка! При формировании турнира произошла ошибка.", reply_markup=MAIN_KEYBOARD_2)
                    await state.reset_state(with_data=False)
                
            except:
                await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
                await GenerateTournamentForm.tournament.set()

        else:
            await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
            await GenerateTournamentForm.tournament.set()
    else:
        return


@dp.message_handler(lambda message: message.text.lower() == "активные турниры")
async def get_tournament_info_by_name(message: types.Message):
    t_string = await get_tournaments_string()
    if t_string:
        await message.answer("Выберите турнир для просмотра: (введите только цифру - номер турнира из списка)", reply_markup=MAIN_CANCEL)
        await message.answer(t_string)
        await GetTournamentInfoForm.name.set()
    else:
        await message.answer("Ошибка! Добавьте хотя бы один турнир!", reply_markup=MAIN_KEYBOARD_2)


@dp.message_handler(state=GetTournamentInfoForm.name)
async def get_tournament_name_to_get_info(message: types.Message, state: FSMContext):
    num_of_t = message.text
    
    if num_of_t.isdigit():
        t_dict = await get_tournaments_dict()
        try:
            tourn = t_dict[int(num_of_t)]
            await state.update_data(name=tourn)
            t = await state.get_data()
            isGot = await get_tournament_info(t.get("name"))
            
            if isGot:
                
                result = await get_tournament_info_string(tourn)

                await message.answer(result)
                
                
                if isGot["isFormed"] == True:
                    await message.answer(await do_show_tournament_schedule_string(tourn))

                await state.reset_state(with_data=False)


            else:
                await message.answer("Ошибка! При просмотре турнира произошла ошибка.", reply_markup=MAIN_KEYBOARD_2)
                await state.reset_state(with_data=False)
            
        except:
            await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
            await state.reset_state(with_data=False)

    else:
        await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
        await GetTournamentInfoForm.name.set()


@dp.message_handler(lambda message: message.text.lower() == "архив турниров")
async def archive_tournaments(message: types.Message):
    
    t_string = await get_archive_tournaments_string()
    if t_string:
        await message.answer("Выберите архивный турнир для просмотра: (введите только цифру - номер турнира из списка)", reply_markup=MAIN_CANCEL)
        await message.answer(t_string)
        await GetArchiveTournamentForm.name.set()
    else:
        await message.answer("Ошибка! Завершите хотя бы один турнир!", reply_markup=MAIN_KEYBOARD_2)


@dp.message_handler(state=GetArchiveTournamentForm.name)
async def get_archive_tourn_name(message: types.Message, state: FSMContext):
    num_of_t = message.text
    
    if num_of_t.isdigit():
        t_dict = await get_archive_tournaments_dict()
        try:
            tourn = t_dict[int(num_of_t)]
            await state.update_data(name=tourn)
            t = await state.get_data()
            isGot = await get_archive_tournament_info_string(tourn)
            
            if isGot:

                sleep(1)
                
                await bot.send_message(message.chat.id, isGot)

                sleep(1)
                
                await bot.send_message(message.chat.id, await get_archive_tournament_schedule(tourn))

                his = await get_archive_tourn_history(tourn)

                sleep(1)

                if len(his) > 4096:
                    for x in range(0, len(his), 4096):
                        await message.answer(his[x:x+4096])
                else:
                        await message.answer(his)

                ar_tourn = await get_archive_tourn_by_name(tourn)
                
                sleep(1)

                await bot.send_message(message.chat.id, await get_best_hitter_blocker(ar_tourn["teams"]))

                await state.reset_state(with_data=False)

            else:
                await message.answer("Ошибка! При просмотре турнира произошла ошибка.", reply_markup=MAIN_KEYBOARD_2)
                await state.reset_state(with_data=False)
            
        except:
            await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
            await state.reset_state(with_data=False)

    else:
        await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
        await GetArchiveTournamentForm.name.set()


@dp.message_handler(lambda message: message.text.lower() == "играть")
async def play_button(message: types.Message):
    if message.from_user.id in ADMINS_IDS:
        t_string = await get_to_play_tournaments_string()
        if t_string:
            await message.answer("Выберите турнир для игры: (введите только цифру - номер турнира из списка)", reply_markup=MAIN_CANCEL)
            await message.answer(t_string)
            await PlayRound.tournament.set()
        else:
            await message.answer("Ошибка! Либо один из турниров сейчас в игре, либо у вас не сформирован ни один турнир.", reply_markup=MAIN_KEYBOARD_2)
    else:
        await message.answer("Только арбитр матча или администратор может начать игру.")


@dp.message_handler(state=PlayRound.tournament)
async def get_tourn_to_play(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS_IDS:
        num_of_t = message.text
        if message.from_user.id in ADMINS_IDS:
        
            if num_of_t.isdigit():
                t_dict = await get_to_play_tournaments_dict()
                try:
                    tourn = t_dict[int(num_of_t)]
                    await state.update_data(tournament=tourn)
                    is_set = await set_now_playing_true(tourn)
                    
                    if is_set:

                        torun_hello = "Мы приветствуем вас на турнире " + is_set["name"].upper() + "!\n"
                            
                        main_info = await get_tournament_info_string(is_set["name"])
                        
                        torun_hello += main_info

                        sleep(1)

                        await message.answer(torun_hello)

                        sleep(2)

                        await message.answer(await do_show_tournament_schedule_string(is_set["name"]))

                        sleep(2)

                        await message.answer("Для начала раунда арбитр матча должен нажать 'Начать'.\nДля отмены нажать 'Отмена'.", reply_markup=PLAY_ROUND_KEYBOARD)
                        await state.reset_state(with_data=False)

                    else:
                        await message.answer("Ошибка! При выборе турнира для игры произошла ошибка.", reply_markup=MAIN_KEYBOARD_2)
                        await state.reset_state(with_data=False)
                    
                except:
                    await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
                    await PlayRound.tournament.set()

            else:
                await message.answer("Ошибка! Введите только цифру - номер турнира из списка.", reply_markup=MAIN_CANCEL)
                await PlayRound.tournament.set()
        else:
            return
    else:
        return


@dp.message_handler()
async def all_mes(message: types.Message):

    if message.text.lower().startswith("поддержать"):
        return
        
    await message.answer("Пожалуйста, введите корректный ответ.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

