import gym
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import fire


class EvalRL(object):
    """Class that evaluates the RL convergence algorithms"""
    def __init__(self, env, solution, n_episodes=1000, MAX_REWARD=350, N=10):
        """
        params :
            - env : the environment to use
            - solution : the solution of the candidat
            - n_episodes : the number of episodes to run the algorithm
            - MAX_REWARD : the maximum rewards to make it acceptable
            - N : the number of times we run the experience
        """
        self.env = env
        self.solution = solution
        self.n_episodes = n_episodes
        self.MAX_REWARD = MAX_REWARD
        self.N = N

    def eval(self, verbose=False):
        """Solve the given environment."""
        scores = []
        for i in range(self.N):
            np.random.seed(i)
            self.solution.reset()
            score = self.solve(self.env, self.solution, n_episodes=self.n_episodes,
                               MAX_REWARD=self.MAX_REWARD, verbose=verbose)
            scores.append(score)
        return np.mean(scores)

    def solve(self, env, solution, n_episodes, MAX_REWARD, verbose=False):
        """Eval the solution : whenever the solution gets 50 times the good rewards."""
        all_rewards = deque(maxlen=50)
        all_r = []
        for e in range(n_episodes):
            state = env.reset()
            rewards = 0
            done = False
            while not done:
                action = solution.action(state)
                new_state, reward, done, info = env.step(action)
                solution.update(state, action, new_state, reward, done, info, e)
                state = new_state
                rewards += reward
            all_r.append(rewards)
            all_rewards.append(rewards)
            if np.mean(list(all_rewards)) >= MAX_REWARD and len(list(all_rewards)) == 50:
                return e+1
        if verbose:
            plt.plot(list(all_r))
            plt.show()
        return e


if __name__ == '__main__' :
    fire.Fire(EvalRL)