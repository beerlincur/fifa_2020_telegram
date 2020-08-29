import random


async def simulate_draw(teams):
    """Return the list of games."""
    if len(teams) % 2 == 0:
        return await simulate_even_draw(teams)
    else:
        return await simulate_odd_draw(teams)


async def simulate_even_draw(teams):
    """Return the list of games."""
    half_len = int(len(teams)/2)
    arr1 = [i for i in range(half_len)]
    arr2 = [i for i in range(half_len, len(teams))][::-1]
    matches = []
    for i in range(len(teams)-1):
        arr1.insert(1, arr2.pop(0))
        arr2.append(arr1.pop())
        for a, b in zip(arr1, arr2):
            matches.append((teams[a], teams[b]))
    return matches


async def simulate_odd_draw(teams):
    """Return the list of games."""
    half_len = int((len(teams)+1)/2)
    arr1 = [i for i in range(half_len)]
    arr2 = [i for i in range(half_len, len(teams)+1)][::-1]
    matches = []
    for i in range(len(teams)):
        arr1.insert(1, arr2.pop(0))
        arr2.append(arr1.pop())
        for a, b in zip(arr1, arr2):
            if len(teams) not in (a, b):
                matches.append((teams[a], teams[b]))
    return matches


async def simulate_game_draw(team1, team2):
    return zip(team1, team2)


def displays_simulated_draws(teams):
    """Print the list of games."""
    for gm in simulate_draw(teams):
        a, b = random.sample(gm, len(gm))
        print(a + ' plays ' + b)


def test_simulate_draw():
    """Small tests for simulate_draw."""
    # TODO: Use a proper testing framework
    TESTS = [
        ([], []),
        (['A'], []),
        (['A', 'B', 'C', 'D'], [('A', 'C'), ('D', 'B'), ('A', 'B'), ('C', 'D'), ('A', 'D'), ('B', 'C')]),
        (['A', 'B', 'C', 'D', 'E'], [('A', 'E'), ('B', 'C'), ('A', 'D'), ('E', 'C'), ('A', 'C'), ('D', 'B'), ('A', 'B'), ('D', 'E'), ('B', 'E'), ('C', 'D')]),
    ]
    for teams, expected_out in TESTS:
        # print(teams)
        ret = simulate_draw(teams)
        assert ret == expected_out

    #test_simulate_draw()
    #displays_simulated_draws(['1', '2', '3', '4', '5'])