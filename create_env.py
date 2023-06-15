import os


def make_dirs(env_name: str):
    os.makedirs('gym_{}'.format(env_name))
    os.makedirs('gym_{}/envs'.format(env_name))
    pass


def make_files(env_name: str, stage_names):
    registry_init = 'gym_{}/__init__.py'.format(env_name)
    with open(registry_init, 'w') as f:
        f.write('from gym.envs.registration import register\n\n')
        for name in stage_names:
            register_str = "register(\n    id='{}-v0',\n    entry_point='gym_{}.envs:{}',\n)\n".format(name, env_name,
                                                                                                       ''.join([
                                                                                                                   s.capitalize()
                                                                                                                   for s
                                                                                                                   in
                                                                                                                   name.split(
                                                                                                                       '_')]))
            f.write(register_str)
    envs_init = 'gym_{}/envs/__init__.py'.format(env_name)
    with open(envs_init, 'w') as f:
        for name in stage_names:
            import_str = "from gym_{}.envs.{} import {}\n".format(env_name, name,
                                                                  ''.join([s.capitalize() for s in name.split('_')]))
            f.write(import_str)

    head = """import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

"""

    tail = """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # NEED to specify the action and obs space
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        self.seed()
        pass

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        reward = 0
        done = False
        info = {} # You may need to add some extra information
        '''
        Do some simulation
        '''
        return self.state, reward, done, info

    def reset(self):
        '''
        Reset the env
        '''
        return self.state

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    """
    for name in stage_names:
        env_class = 'class {}(gym.Env):'.format(''.join([s.capitalize() for s in name.split('_')]))
        with open('gym_{}/envs/{}.py'.format(env_name, name), 'w') as f:
            f.write(head + env_class + tail)
    pass


def make_setup(env_name):
    with open('setup.py', 'w') as f:
        tmp = [
            'from setuptools import setup\n\n',
            "setup(name='gym_{}',\n".format(env_name),
            "    version='0.0.1',\n",
            "    install_requires=['gym']  # And any other dependencies foo needs\n",
            ")\n",
        ]
        f.writelines(tmp)


if __name__ == '__main__':
    env_name = input('Please type your env\'s name (string):')
    env_stage_num = int(input('Type the stage number of your Env (int):'))
    print(
        'Please type yout stage names\n(start with alphabet, lowercase and number, split by underscore(_), e.g. my_env_v1)')
    env_stage_names = []
    for i in range(env_stage_num):
        env_stage_names.append(input("Stage {}s name:".format(i)))
    make_dirs(env_name)
    make_files(env_name, env_stage_names)
    generate_setup = input('Generate `setup.py`?[y/n]')
    if generate_setup.lower() == 'y':
        make_setup(env_name)