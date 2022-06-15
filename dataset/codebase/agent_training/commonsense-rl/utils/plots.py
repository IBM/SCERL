import pickle
import numpy as np
import matplotlib.pyplot as plt
<<<<<<< HEAD

def find_trigger_text(desc):
    text_data = desc.split()
    strt = text_data.index("(trigger")
    end = text_data.index("->")
    trigger_text = " ".join(text_data[strt + 2:end])
    return trigger_text

def get_obj_text(obj):
    obj_text = obj.split(":")[0]
    obj_text = " ".join(obj_text.split())
    return obj_text

def process_cndtn(cndtn_text):
    cndtn = " ".join(cndtn_text.split())
    predicate = cndtn[1 : cndtn.find("(")]
    objects = cndtn[cndtn.find("(") + 1 : cndtn.find(")")].split(",")
    obj_list = []
    for obj in objects:
        obj_list.append(get_obj_text(obj))
    return predicate, obj_list

def process_trigger_text(trigger):
    conditions = trigger.split("&")
    cndtn_text = []
    for cndtn in conditions:
        predicate, obj_list = process_cndtn(cndtn)
        pred_text = " " + predicate + " "
        if len(obj_list) > 1:
            c_text = pred_text.join(obj_list)
        else:
            c_text = predicate + " " + obj_list[0]
        cndtn_text.append(c_text)
    event_text = " & ".join(cndtn_text)
    return event_text


def process_desc(desc):
    trigger_text = find_trigger_text(desc)
    legend_text = process_trigger_text(trigger_text)
    print(legend_text)
    return legend_text
=======
import glob
>>>>>>> 9df449b932310a048c57a2532e629d6b46392412

def return_legend(quest):
    print("quest:", quest)
    res = ''
    # if quest['optional']:
    #     res += 'Optional'
    # if quest['repeatable']:
    #     res += ' Repeatable'
    for k in quest:
        if 'win' in k or 'fail' in k:
            res += process_desc(quest[k]['desc'])
    
    res += ' - Reward = ' + str(quest['reward'])
    return res


def get_quest_reward(quest):
    res = 0
    for k in quest.keys():
        if 'win' in k:
            if quest['repeatable']:
                res += len(quest[k]['time_step']) * quest['reward']
            elif quest[k]['time_step']:
                res += quest['reward']
    return res


def get_bar_data(quests, batch_number, episode_list, quest_filter='repeatable', mode='occurences'):
    bar_data = []
    nb_quests = len(quests[0][batch_number])
    for e in episode_list:
        ep_data = []
        for q in range(nb_quests):
            current_quest = quests[e][batch_number]['quest_' + str(q)]
            if quest_filter == 'repeatable' and current_quest['repeatable']:
                if mode == 'occurences':
                    ep_data.append(len(current_quest['time_step']))
                else:
                    ep_data.append(len(current_quest['time_step']) * current_quest['reward'])
            elif quest_filter == 'non repeatable' and not current_quest['repeatable']:
                if mode == 'occurences':
                    ep_data.append(min(1, len(current_quest['time_step'])))
                else:
                    ep_data.append(min(1, len(current_quest['time_step'])) * current_quest['reward'])

            elif quest_filter == 'both':
                if current_quest['repeatable']:
                    if mode == 'occurences':
                        ep_data.append(len(current_quest['time_step']))
                    else:
                        ep_data.append(len(current_quest['time_step']) * current_quest['reward'])

                else:
                    if mode == 'occurences':
                        ep_data.append(min(1, len(current_quest['time_step'])))
                    else:
                        ep_data.append(min(1, len(current_quest['time_step'])) * current_quest['reward'])
        bar_data.append(ep_data)
    bar_data = np.array(bar_data)
    return bar_data.T


def get_barplot_legend(quests, quest_filter):
    nb_quests = len(quests[0][0])
    legend = []
    for q in range(nb_quests):
        current_quest = quests[0][0]['quest_' + str(q)]
        if quest_filter == 'repeatable' and current_quest['repeatable']:
            legend.append(return_legend(current_quest))
        elif quest_filter == 'non repeatable' and not current_quest['repeatable']:
            legend.append(return_legend(current_quest))
        elif quest_filter == 'both':
            legend.append(return_legend(current_quest))
    return legend


def get_failed_data(quests, batch_number):
    nb_quests = len(quests[0][batch_number])
    episode_list = range(len(quests))
    res = []
    for e in episode_list:
        failed = 0
        q = 0
        while q < nb_quests and failed == 0:
            quest = quests[e][batch_number]['quest_' + str(q)]
            fail_events = [event for event in quest if 'fail' in event]
            for f_event in fail_events:
                if quest[f_event]['time_step']:
                    failed = 1
                    break
            q += 1
        res.append(failed)
    return res


def plot_fail(quests, batch_number):
    failed = get_failed_data(quests, batch_number)
    plt.title('Cumulative fail plot')
    plt.xlabel('Episodes')
    plt.ylabel('Fails')
    plt.plot(np.cumsum(failed))
    plt.show()


def line_plot(quests, batch_number):
    fig = plt.figure()
    ax = plt.axes()
    nb_episodes = len(quests)
    x = np.arange(nb_episodes)
    y = []
    legends = []
    nb_quests = len(quests[0][batch_number])
    total_q = [0] * nb_episodes
    for q in range(nb_quests):
        y_quest = []
        legends.append(return_legend(quests[0][batch_number]['quest_' + str(q)]))
        for e in range(nb_episodes):
            current_quest = quests[e][batch_number]['quest_' + str(q)]
            q_comp = get_quest_reward(current_quest)
            y_quest.append(q_comp)
            total_q[e] += q_comp
        ax.plot(x, y_quest, label=legends[q])
        y.append(y_quest)
    ax.plot(x, total_q, label='Total')
    y.append(total_q)
    plt.xlabel("Episodes")
    plt.ylabel("Reward")
    plt.legend(loc='lower center', prop={'size': 6}, bbox_to_anchor=(0.5, -.5))
    plt.tight_layout()
    plt.show()
    return x, y


# Take negative and positive data apart and cumulate
def get_cumulated_array(data, **kwargs):
    cum = data.clip(**kwargs)
    cum = np.cumsum(cum, axis=0)
    d = np.zeros(np.shape(data))
    d[1:] = cum[:-1]
    return d


def stackedbar(bar_data, legend, batch_number, episode_list, quest_filter='repeatable', mode='occurences', agent = 'unknown'
               ):
    x = [str(e) for e in episode_list]
    # bar_data = get_bar_data(quests, batch_number, episode_list, quest_filter, mode)

    width = 5
    fig, ax = plt.subplots()
    cumulated_data = get_cumulated_array(bar_data, min=0)
    cumulated_data_neg = get_cumulated_array(bar_data, max=0)

    row_mask = (bar_data < 0)
    cumulated_data[row_mask] = cumulated_data_neg[row_mask]
    data_stack = cumulated_data

    for i in range(bar_data.shape[0]):
        # starts = bar_cum[i, :] - bar_data[i, :]
        ax.bar(x, bar_data[i, :], width=1, bottom=data_stack[i], label=legend[i])
    ax.set_xlabel("Episodes")
    loc = ax.get_xticks()
    loc = np.array(loc)
    sel_ind = np.linspace(0, len(loc) - 1, 10).astype(int)
    loc, label = tuple(loc[sel_ind]), tuple(np.array(episode_list)[sel_ind])
    plt.xticks(loc, label, rotation='vertical')
    ax.set_ylabel(mode.capitalize())
    title = mode.capitalize() + ' of '
    if quest_filter != 'both':
        title += quest_filter
    title += 'quests - ' + agent
    ax.legend(loc='lower center', prop={'size': 6}, bbox_to_anchor=(0.5, -.5))
    ax.set_title(title)
    plt.tight_layout()
    plt.show()

<<<<<<< HEAD

f = open('test_se_simple_score_mode_textworld_observation_mode_textworld_run2_0.pkl', 'rb')
quests = pickle.load(f)
f.close()
plot_fail(quests, 0)
stackedbar(quests, 0, np.arange(0, 500, 10), quest_filter='both', mode='rewards')
line_plot(quests, 0)
# process_desc()
=======
def return_avg_barplot(file_list, episode_list, quest_filter='both', mode='rewards', agent = 'unknown' ):
    data = None
    for file in file_list:
        with open(file, 'rb') as f:
            quest_f = pickle.load(f)
            if data is None:
                legend = get_barplot_legend(quest_f, quest_filter)
                data = get_bar_data(quest_f, 0, np.arange(0, 500, 10), quest_filter='both', mode='rewards')
            else:
                data = data + get_bar_data(quest_f, 0, np.arange(0, 500, 10), quest_filter='both', mode='rewards')
    data = data/len(file_list)
    print(file_list)
    stackedbar(data, legend, 0, episode_list, quest_filter, mode, agent)



file_list = glob.glob('../res_quests/test_nc/simple_score_mode_pos_only_observation_mode_pos+warning_run*')
return_avg_barplot(file_list, np.arange(0, 500, 10), quest_filter='both', mode='rewards', agent = 'simple - sc pos_only - obs pos+warning (5 runs)')
#
f = open('test_se_knowledgeaware_score_mode_pos_only_observation_mode_pos_only_run1_0.pkl', 'rb')
quests = pickle.load(f)
f.close()
# plot_fail(quests, 0)
# stackedbar(quests, 0, np.arange(0, 500, 10), quest_filter='both', mode='rewards')
# line_plot(quests, 0)
>>>>>>> 9df449b932310a048c57a2532e629d6b46392412
