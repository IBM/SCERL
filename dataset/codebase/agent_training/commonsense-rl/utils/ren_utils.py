from textworld.generator.game import Event, Quest
from textworld.logic import Action, Proposition, Variable


def revert_dict(game):
    dict_entity = game.infos
    e2n = {}
    for k in dict_entity.keys():
        name = dict_entity[k].name
        if name is not None:
            e2n[name] = k
        else:
            e2n[k] = k
    return e2n


def entity_dict(game):
    dict_entity = game.infos
    n2e = {}
    for k in dict_entity.keys():
        name = dict_entity[k].name
        if name is not None:
            n2e[k] = name
        else:
            n2e[k] = k
    return n2e


def ren_prop(prop, ren_dict):
    n_names = [ren_dict[n] for n in prop.names]
    n_arguments = [Variable(n_names[i], prop.arguments[i].type) for i in range(len(n_names))]
    n_prop = Proposition(name=prop.name, arguments=n_arguments)
    return n_prop


def ren_action(action, ren_dict):
    precond, postcond = [ren_prop(p, ren_dict) for p in action.preconditions], [ren_prop(p, ren_dict) for p in
                                                                                action.postconditions]
    return Action(action.name, precond, postcond)


def ren_facts(facts, ren_dict):
    n_facts = [ren_prop(p, ren_dict) for p in facts]
    return n_facts


def ren_commands(commands, ren_dict):
    res = []
    for command in commands:
        for k in ren_dict:
            command = command.replace(k, ren_dict[k])
        res.append(command.replace(k, ren_dict[k]))
    return res


def ren_event(event, ren_dict):
    n_actions = []
    for act in event.actions:
        n_actions.append(ren_action(act, ren_dict))
    n_cond = [ren_prop(p, ren_dict) for p in event.condition.preconditions]
    return Event(actions=n_actions, conditions=n_cond, commands=ren_commands(event.commands, ren_dict))


def ren_quest(quest, ren_dict):
    ren_win = [ren_event(e, ren_dict) for e in quest.win_events]
    ren_fail = [ren_event(e, ren_dict) for e in quest.fail_events]
    return Quest(ren_win, ren_fail, quest.reward, quest.desc, quest.commands, quest.optional, quest.repeatable)


def event2str(event):
    res = 'Event: '
    res += 'Action (' + ' '.join([str(act) for act in event.actions]) + ')'
    res += ' Condition (' + str(event.condition) + ')'
    res += ' Commands (' + ';'.join(event.commands) + ')'
    return res
