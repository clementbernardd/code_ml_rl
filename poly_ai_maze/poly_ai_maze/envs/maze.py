import gym
from gym import spaces
import numpy as np
# from poly_ai_maze.envs.utils import *
import sys
sys.path.insert(0, 'poly_ai_maze/poly_ai_maze/envs')
from utils import *

WORLD = np.array([[0, 2, 0, 0, 0, 2, 0, 0, 0, 0],
                               [0, 2, 0, 2, 0, 2, 0, 0, 2, 0],
                               [0, 2, 0, 2, 0, 2, 0, 0, 2, 0],
                               [0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
                               [0, 2, 0, 2, 2, 3, 2, 2, 2, 0],
                               [0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 2, 0, 2, 2, 2, 3, 2],
                               [0, 2, 0, 2, 0, 0, 0, 0, 0, 4],
                               [0, 2, 0, 2, 2, 2, 2, 2, 2, 3],
                               [1, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                               ])


class PolyAIMaze(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0,
                                            high=4,
                                            shape=(10, 10),
                                            dtype=np.int16)
        self.reward_range = (-500, 500)
        self.current_episode = 0
        self.success_episode = []
        self.last_action = None

    def _next_observation(self):
        return self.world.copy()

    def check_available_mov(self, new_x, new_y):
        """Check if the new position is available."""
        if new_x < 0 or new_x >= self.world.shape[0] or new_y < 0 or new_y >= self.world.shape[1] :
            return False
        else :
            new_element = self.world[new_x, new_y]
            return new_element != 2

    def _take_action(self, action):
        """
        Action does one of the following thing :
            - 0 : goes down
            - 1 : goes up
            - 2 : goes right
            - 3 : goes left
        """
        self.last_action = action
        (x,y) = np.where(self.world == 1)
        x,y = x[0], y[0]
        if action == 0 :
            # Goes down
            new_x = x+1
            new_y = y
        elif action == 1:
            # Goes up
            new_x = x-1
            new_y = y
        elif action == 2:
            # Goes right
            new_x = x
            new_y = y+1
        elif action == 3:
            # Goes left
            new_x = x
            new_y = y-1
        else :
            print(f'ERROR : ACTION NOT AVAILABLE : {action}')

        if self.check_available_mov(new_x, new_y) :
            self.world[x, y]=0
            if self.world[new_x, new_y] == 4 :
                self.state = 'W'
            elif self.world[new_x, new_y] == 3 :
                self.state = 'L'
            else :
                self.state = 'P'
            self.world[new_x, new_y]=1

    def step(self, action):
        self._take_action(action)
        self.current_step+=1

        if self.state == 'W' and self.current_step < self.max_step:
            show("*" * 25 + " Maze is solved " + "*" * 25)
            reward = 500
            done = True
        elif self.state == 'L' or self.current_step > self.max_step:
            show("*" * 25 + " Game over " + "*" * 25)
            reward = -500
            done = True
        else :
            reward = -1
            done = False

        if self.current_step >= self.max_step:
            done = True

        if done:
            self.render_episode(self.state)
            self.current_episode+=1

        obs = self._next_observation().copy()
        return obs, reward, done, {}

    def render(self, mode='human'):
        """Print the maze and the given action."""
        show_env(self.world, self.last_action)

    def render_episode(self, win_or_lose):
        self.success_episode.append(
            'Success' if win_or_lose == 'W' else 'Failure')

    def reset(self):
        self.state = 'P'
        self.current_step = 0
        self.max_step = 200
        self.world = WORLD.copy()
        return self.world
