import numpy as np


# makes the assumption that only one game was tried
def create_summary_quest(quests):
    res = dict()
    first_triggering_quest = dict()
    counter = dict()
    first_triggering_event = dict()
    # init
    for quest_id in quests[0][0]:
        res[quest_id] = dict()
        res[quest_id]['first_triggering'] = None
        res[quest_id]['nb_triggerings'] = None
        res[quest_id]['optional'] = quests[0][0][quest_id]['optional']
        res[quest_id]['repeatable'] = quests[0][0][quest_id]['repeatable']
        res[quest_id]['reward'] = quests[0][0][quest_id]['reward']
        counter[quest_id] = dict()
        counter[quest_id]['quest'] = list()
        first_triggering_quest[quest_id] = list()
        first_triggering_event[quest_id] = dict()
        for ev in quests[0][0][quest_id]:
            if 'win' in ev or 'fail' in ev:
                first_triggering_event[quest_id][ev] = list()
                counter[quest_id][ev] = list()
                res[quest_id][ev] = dict()
                res[quest_id][ev]['desc'] = quests[0][0][quest_id][ev]['desc']
                res[quest_id][ev]['first_triggering'] = None
                res[quest_id][ev]['nb_triggerings'] = None

    # collect data
    for ep_id in range(len(quests)):
        for quest_id in quests[ep_id][0]:
            if quests[ep_id][0][quest_id]['time_step']:
                first_triggering_quest[quest_id].append(quests[ep_id][0][quest_id]['time_step'][0])
            counter[quest_id]['quest'].append(len(quests[ep_id][0][quest_id]['time_step']))
            for ev in quests[ep_id][0][quest_id]:
                if 'win' in ev or 'fail' in ev:
                    if quests[ep_id][0][quest_id][ev]['time_step']:
                        first_triggering_event[quest_id][ev].append(quests[ep_id][0][quest_id][ev]['time_step'][0])
                    counter[quest_id][ev].append(len(quests[ep_id][0][quest_id][ev]['time_step']))

    # compute summary stats
    for quest_id in res:
        if first_triggering_quest[quest_id]:
            res[quest_id]['first_triggering'] = np.mean(first_triggering_quest[quest_id])
        else:
            res[quest_id]['first_triggering'] = None
        res[quest_id]['nb_triggerings'] = np.mean(counter[quest_id]['quest'])
        for ev in res[quest_id]:
            if 'win' in ev or 'fail' in ev:
                if first_triggering_event[quest_id][ev]:
                    res[quest_id][ev]['first_triggering'] = np.mean(first_triggering_event[quest_id][ev])
                else:
                    res[quest_id][ev]['first_triggering'] = None
                res[quest_id][ev]['nb_triggerings'] = np.mean(counter[quest_id][ev])
    return res


def print_summary(summary_dict):
    for quest_id in summary_dict:
        print(
            "\nquest {} nb_triggerings {} first_triggering {} - Optional {} - Repeatable {} - Reward {}".format(quest_id, summary_dict[quest_id]['nb_triggerings'],
                                                                    summary_dict[quest_id]['first_triggering'], summary_dict[quest_id]['optional'], summary_dict[quest_id]['repeatable'], summary_dict[quest_id]['reward']))
        for ev in summary_dict[quest_id]:
            if 'win' in ev or 'fail' in ev:
                print("event {} nb_triggerings {} first_triggering {}".format(summary_dict[quest_id][ev]['desc'],
                                                                              summary_dict[quest_id][ev][
                                                                                  'nb_triggerings'],
                                                                              summary_dict[quest_id][ev][
                                                                                  'first_triggering']))

