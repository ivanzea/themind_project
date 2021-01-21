from gym.envs.registration import register

register(
    id='themind-v0',
    entry_point='gym_themind.envs:TheMind'
    )
