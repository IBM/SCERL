from textworld import GameMaker
from textworld import g_rng
from textworld.core import EnvInfos
from textworld.generator.game import Quest, Event
from textworld.gym.envs import TextworldGymEnv

path_save = '../twc_games/Easy_SafeExploration.ulx'
req_infos = EnvInfos(game=True, last_action=True, last_command=True, facts=True)
env = TextworldGymEnv(request_infos=req_infos, gamefiles=[path_save])
env.reset()
try:
    done = False
    env.reset()
    i = 0
    while not done:
        if i > 0:
            env.render()
        else:
            obs, reward, done, infos = env.step("look")
            i+=1
            continue
        command = input("> ")
        obs, reward, done, infos = env.step(command)
        print("reward:", reward)
        # print(done)
        # env.render()
        i+=1
    env.render()  # Final message.
except KeyboardInterrupt:
    pass  # Quit the game.