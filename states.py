from aiogram.dispatcher.filters.state import StatesGroup, State


class TournamentForm(StatesGroup):
    name = State()
    typeOfTournament = State()
    bet = State()
    amount_of_teams = State()
    amount_of_players = State()
    start_time = State()


class TeamForm(StatesGroup):
    tournament = State()
    name = State()


class PlayerForm(StatesGroup):
    tournament = State()
    team = State()
    name = State()
    idd = State()


class ConfirmPartForm(StatesGroup):
    tournament = State()
    team = State()
    name = State()
    idd = State()


class GenerateTournamentForm(StatesGroup):
    tournament = State()


class GetTournamentInfoForm(StatesGroup):
    name = State()


class GetArchiveTournamentForm(StatesGroup):
    name = State()


class PlayRound(StatesGroup):
    tournament = State()
    current_tournament = State()
    start = State()
    hit = State()
    block = State()
    is_goal = State()


