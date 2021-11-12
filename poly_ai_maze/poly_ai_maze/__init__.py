from gym.envs.registration import register

register(
    id='simple_maze-v0',
    entry_point='poly_ai_maze.envs:PolyAIMaze',
)