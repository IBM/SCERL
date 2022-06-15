import copy
from collections.abc import Iterable

from gym.wrappers import TimeLimit
from textworld.core import EnvInfos
from textworld.generator.game import QuestProgression
from textworld.gym.envs import TextworldGymEnv
from textworld.logic import State

from utils.ren_utils import *
from num2words import num2words


class MonitorWrapper():
    def __init__(self, env=None, path=None, max_episode_steps=None, verbose=False, gamefiles=None,
                 additional_infos=None, forbidden_entities=None, observation_mode='pos+constraint', show_edit_score = False):
        if forbidden_entities is None:
            forbidden_entities = [[]]
        if additional_infos is None:
            additional_infos = {}
        req_infos = EnvInfos(game=True, last_action=True, facts=True, **additional_infos)
        if env is not None:
            self.env = env
            if gamefiles is not None:
                self.gamefiles = gamefiles
            self.seed = env.seed
        else:
            self.env = TextworldGymEnv(path, request_infos=req_infos)
        self.time_limit = TimeLimit(self.env, max_episode_steps)
        self.quests = None
        self.qp = None
        self.ren_dict = None
        self.verbose = verbose
        self.forbidden_entities = forbidden_entities
        self.observation_mode = observation_mode
        self.show_edit_score = show_edit_score

    def get_qlabel(self, ind):
        q_label = 'quest_{}'.format(ind)
        return q_label

    def get_ren_dict(self, game_list):
        self.ren_dict = []
        for i in range(len(game_list)):
            self.ren_dict.append(entity_dict(game_list[i]))

    def init_quests(self, game_list):
        self.quests, self.qp = [], []

        for i in range(len(game_list)):
            game_quests = game_list[i].quests
            kb = game_list[i].kb
            self.quests.append(dict())
            self.qp.append(dict())
            for j in range(len(game_quests)):
                quest = game_quests[j]
                q_label = self.get_qlabel(j)
                h_quest = ren_quest(quest, self.ren_dict[i])
                self.qp[i][q_label] = QuestProgression(h_quest, kb)
                self.quests[i][q_label] = {}
                self.quests[i][q_label]['time_step'] = []
                self.quests[i][q_label]['optional'] = quest.optional
                self.quests[i][q_label]['repeatable'] = quest.repeatable
                self.quests[i][q_label]['reward'] = quest.reward

                for k in range(len(h_quest.win_events)):
                    if 'win_{}'.format(k) not in self.quests[i][q_label]:
                        self.quests[i][q_label]['win_{}'.format(k)] = {}
                    self.quests[i][q_label]['win_{}'.format(k)]['desc'] = 'Win Event {} {} '.format(
                        k, q_label) + event2str(
                        h_quest.win_events[k])
                    self.quests[i][q_label]['win_{}'.format(k)]['time_step'] = []
                for k in range(len(h_quest.fail_events)):
                    if 'fail_{}'.format(k) not in self.quests[i]['quest_{}'.format(j)]:
                        self.quests[i][q_label]['fail_{}'.format(k)] = {}
                    self.quests[i][q_label]['fail_{}'.format(k)]['desc'] = 'Fail Event {} {} '.format(
                        k, q_label) + event2str(
                        h_quest.fail_events[k])
                    self.quests[i][q_label]['fail_{}'.format(k)]['time_step'] = []

    def update_epqp(self, infos, nb_steps):
        if not isinstance(infos['game'], Iterable):
            list_games = [infos['game']]
            game_facts = [infos['facts']]
            list_last_action = [infos['last_action']]
        else:
            list_games = infos['game']
            game_facts = infos['facts']
            list_last_action = infos['last_action']
        for i in range(len(self.quests)):
            facts = game_facts[i]
            logic = list_games[i].kb.logic
            last_action = list_last_action[i]
            state = State(logic, facts)
            for quest_id in self.qp[i]:
                # print(quest_id)
                self.qp[i][quest_id].update(action=last_action, state=state)
                if self.verbose and self.qp[i][quest_id].completed and not self.quests[i][quest_id]['time_step']:
                    print("Quest {} completed".format(quest_id))
                if (self.qp[i][quest_id].nb_completions > len(self.quests[i][quest_id]['time_step'])):
                    self.quests[i][quest_id]['time_step'].append(nb_steps)
                for k in range(len(self.qp[i][quest_id].win_events)):
                    # import pdb; pdb.set_trace()
                    # print('quest triggered', self.qp[i][quest_id].win_events[k].triggered)
                    if self.qp[i][quest_id].win_events[k].triggered:
                        # first triggering
                        if not self.quests[i][quest_id]['win_{}'.format(k)]['time_step'] and self.verbose:
                            print(self.quests[i][quest_id]['win_{}'.format(k)][
                                      'desc'] + ' triggered - Step {}'.format(nb_steps))
                        if self.qp[i][quest_id].win_events[k].event.is_triggering(state):
                            self.quests[i][quest_id]['win_{}'.format(k)]['time_step'].append(nb_steps)
                if self.verbose and self.qp[i][quest_id].failed and not self.quests[i][quest_id]['time_step']:
                    print("Quest {} failed".format(quest_id))
                if self.qp[i][quest_id].failed:
                    self.quests[i][quest_id]['time_step'].append(nb_steps)
                for k in range(len(self.qp[i][quest_id].fail_events)):
                    if self.qp[i][quest_id].fail_events[k].triggered:
                        if not self.quests[i][quest_id]['fail_{}'.format(k)]['time_step'] and self.verbose:
                            print(
                                self.quests[i][quest_id]['fail_{}'.format(k)][
                                    'desc'] + ' triggered - Step {}'.format(nb_steps))
                        if self.qp[i][quest_id].fail_events[k].event.is_triggering(state):
                            self.quests[i][quest_id]['fail_{}'.format(k)]['time_step'].append(nb_steps)

    def print_event_status(self, infos):
        if not isinstance(infos['game'], Iterable):
            list_games = [infos['game']]
            game_facts = [infos['facts']]
        else:
            list_games = infos['game']
            game_facts = infos['facts']
        for i in range(len(self.quests)):
            facts = game_facts[i]
            logic = list_games[i].kb.logic
            state = State(logic, facts)
            for quest_id in self.quests[i]:
                print(
                    'Game {}, quest {} quest_completed {} quest_failed {}'.format(
                        i, quest_id, self.qp[i][quest_id].completed, self.qp[i][quest_id].failed))
                # self.quests[i][quest_id][ev]['desc'],
                # self.ep[i][quest_id][ev].triggered, self.ep[i][quest_id][ev].event.is_triggering(state)))
                print("Win Events")
                for ev in self.qp[i][quest_id].win_events:
                    print("{} Triggered {} Triggering {}".format(event2str(ev.event), ev.triggered,
                                                                 ev.event.is_triggering(state)))
                print("Fail Events")
                for ev in self.qp[i][quest_id].fail_events:
                    print("{} Triggered {} Triggering {}".format(event2str(ev.event), ev.triggered,
                                                                 ev.event.is_triggering(state)))

    def get_failed_completed_quests(self, game_ind, nb_step):
        failed, completed = [], []
        for i in range(len(self.qp[game_ind])):
            q_label = self.get_qlabel(game_ind, i)
            if self.qp[game_ind][q_label].failed:
                failed.append(i)
            # check if the quest is completed and if the state still trigerring
            if self.qp[game_ind][q_label].completed and self.quests[game_ind][q_label]['time_step'][-1] == nb_step:
                completed.append(i)
        return failed, completed

    def get_reward_decomposition_game(self, nb_batch):
        pos, neg = 0, 0
        for quest_id in self.quests[nb_batch]:
            # print(quest_id)
            # if quest_id =="quest_3": import pdb; pdb.set_trace()
            if self.quests[nb_batch][quest_id]['repeatable']:
                if self.quests[nb_batch][quest_id]['reward'] > 0:
                    pos += self.quests[nb_batch][quest_id]['reward'] * len(self.quests[nb_batch][quest_id]['time_step'])
                else:
                    neg += self.quests[nb_batch][quest_id]['reward'] * len(self.quests[nb_batch][quest_id]['time_step'])
            else:
                if self.quests[nb_batch][quest_id]['reward'] > 0:
                    pos += self.quests[nb_batch][quest_id]['reward'] * min(1, len(
                        self.quests[nb_batch][quest_id]['time_step']))
                else:
                    neg += self.quests[nb_batch][quest_id]['reward'] * min(1, len(
                        self.quests[nb_batch][quest_id]['time_step']))
        return pos, neg

    def get_reward_decomposition_batch(self):
        pos, neg = [], []
        nb_batch = len(self.quests)
        for i in range(nb_batch):
            b_pos, b_neg = self.get_reward_decomposition_game(i)
            pos.append(b_pos)
            neg.append(b_neg)
        return pos, neg

    def get_instant_reward_decomposition(self, nb_batch, time_step):
        pos, neg = 0, 0
        for quest_id in self.quests[nb_batch]:
            if self.quests[nb_batch][quest_id]['time_step']:
                if self.quests[nb_batch][quest_id]['reward'] > 0:
                    if (len(self.quests[nb_batch][quest_id]['time_step']) == 1 or self.quests[nb_batch][quest_id][
                        'repeatable']) and self.quests[nb_batch][quest_id]['time_step'][-1] == time_step:
                        pos += self.quests[nb_batch][quest_id]['reward']
                else:
                    if (len(self.quests[nb_batch][quest_id]['time_step']) == 1 or self.quests[nb_batch][quest_id][
                        'repeatable']) and self.quests[nb_batch][quest_id]['time_step'][-1] == time_step:
                        neg += self.quests[nb_batch][quest_id]['reward']
        return pos, neg

    def edit_observation(self, obs, time_step):
        nb_batch = len(obs)
        res = []
        for i in range(nb_batch):
            pos, neg = self.get_instant_reward_decomposition(i, time_step)
            n_obs = ''
            for sentence in obs[i].split('.'):
                # not a score update or final score
                if 'score' not in sentence:
                    n_obs += sentence + '.' if sentence and sentence[-1].isalpha() else sentence
                elif 'scored' not in sentence:
                    # score update
                    if pos > 0:
                        n_obs += '\n\n\nYour score has just gone up by ' + num2words(pos) + ' points.'
                    if neg < 0:
                        if self.observation_mode == 'pos+warning' or self.observation_mode == 'pos+constraint':
                            n_obs += '\n\n\nThe environment is in an unsafe state.\n'
                        if self.observation_mode == 'pos+constraint':
                            n_obs += 'You incur a penalty of ' + num2words(neg) + '.'
                else:
                    # final score
                    cum_pos, cum_neg = self.get_reward_decomposition_game(i)
                    if len(sentence) > 0 and 'out' in sentence:
                        p_score = sentence.split(' ')[sentence.split(' ').index('out') - 1]
                        n_obs += sentence.replace(p_score, str(cum_pos)) + '.'
                        if self.observation_mode == 'pos+constraint':
                            n_obs += 'You incur a total penalty of ' + str(cum_neg) + '.'
            res.append(n_obs)
        return res

    def step(self, commands):
        # if isinstance(commands, str):
        #     commands = [commands]
        for i in range(len(commands)):
            for fe in self.forbidden_entities[i]:
                if fe in commands[i]:
                    if self.verbose:
                        print('Blocked command: {}'.format(commands[i]))
                    commands[i] = 'look'
            observation, reward, dones, infos = self.time_limit.step(commands[i])
            # print('original reward {}'.format(reward))
        game = infos['game']
        if not isinstance(game, Iterable):
            game = [game]

        # if 'apply' in commands[i]:
        print('debug')

        if not self.quests:
            self.get_ren_dict(game)
            self.init_quests(game)
        self.update_epqp(infos, self.time_limit._elapsed_steps)
        if not isinstance(dones, Iterable):
            dones = [dones]
        if isinstance(observation, str):
            observation = [observation]
        pos, neg = self.get_reward_decomposition_batch()
        # import pdb; pdb.set_trace()
        # if sum(pos + neg) != reward:
        #     pos = [reward - sum(neg)] #TODO: check this code
        if self.show_edit_score:
            print('before edit')
            print(observation)
        if self.observation_mode != 'textworld':
            observation = self.edit_observation(observation, self.time_limit._elapsed_steps)
        if self.show_edit_score:
            print('after edit')
            print(observation)
            print('*' * 50)
            print('score {} pos {} neg {}'.format(reward, pos, neg))

        return observation, reward, dones, infos, pos, neg

    def reset(self):
        obs, infos = self.env.reset()
        self.time_limit.reset()
        self.ren_dict = None
        self.quests = None
        return obs, infos

    def close(self):
        self.time_limit.close()

    def render(self, mode='human'):
        return self.env.render(mode=mode)

    def get_quests_copy(self):
        return copy.deepcopy(self.quests)
