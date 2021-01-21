def rulebased_agent(env, pid):
    # Am I the only one left with cards?
    players = env.players.copy()
    players.pop(pid)
    if all([ply.empty_hand for ply in players]):
        # YES -> play immediately
        action = env.min_action
    else:
        # NO -> use policy
        action = env.players[pid].card2play - env.played_card
        
    return action
