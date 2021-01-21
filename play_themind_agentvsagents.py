import gym
import time
from os import system, name 

# Agent players policies
from agents.rulebased.rulebased_agent import rulebased_agent
agent_policies = [rulebased_agent]

# Game parameters
starting_level = 1  # 1-12
players = 2  # 2-4
tries = 1
show_all = True
       
# ---------------------------------------------

# Calculate next agents action
def calculate_actions(env):
    actions = []
    for pid in range(1, env.num_players):        
        if env.players[pid].empty_hand:
            actions.append(env.max_action)
        else:
            actions.append(agent_policies[pid-1](env, pid))
        next_action = min(actions)

    return next_action, actions.index(next_action)+1

# Define our clear function 
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')

# Initialize environment
env = gym.make('gym_themind:themind-v0',
            starting_level=starting_level,
            players=players)

# Error copy environment
err_env = env

# Start playing
while tries > 0:    
    # Generate actions from each a  gent
    next_action, next_action_pid = calculate_actions(env)
    next_action = min(max(next_action, env.min_action), env.max_action)

    # Show environment state
    clear()
    env.render(show_all=show_all)

    # Start listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Human action loop
    user_input = False
    reward = 0
    done = False
    elapsed_time = -1
    start_time = time.time()
    while elapsed_time < next_action:
        elapsed_time = time.time() - start_time

        if user_input:
            listener.stop()
            next_action_pid = 0
            break

    reward, done = env.step(next_action_pid)
    
    # Stop listener if is was not interrupted by the user input
    if not user_input:
        listener.stop()
    
    if reward == -1:
        clear()
        env.render(show_all=show_all)
        print('WRONG card was played')
        time.sleep(1.5)
    
    # Check if game is over
    if done:
        if (env.lives < 1) | (env.level == env.max_level):
            tries -= 1
        else:
            clear()
            env.render(show_all=show_all)
            print('CONGRATULATIONS! next level commencing soon')
            time.sleep(5.0)
        env.reset()
    