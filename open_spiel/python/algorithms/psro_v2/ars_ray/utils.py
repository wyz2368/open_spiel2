# Code in this file is copied and adapted from
# https://github.com/openai/evolution-strategies-starter.

import numpy as np

def itergroups(items, group_size):
    assert group_size >= 1
    group = []
    for x in items:
        group.append(x)
        if len(group) == group_size:
            yield tuple(group)
            del group[:]
    if group:
        yield tuple(group)



def batched_weighted_sum(weights, vecs, batch_size):
    total = 0
    num_items_summed = 0
    for batch_weights, batch_vecs in zip(itergroups(weights, batch_size),
                                         itergroups(vecs, batch_size)):
        assert len(batch_weights) == len(batch_vecs) <= batch_size
        total += np.dot(np.asarray(batch_weights, dtype=np.float64),
                        np.asarray(batch_vecs, dtype=np.float64))
        num_items_summed += len(batch_weights)
    return total, num_items_summed

def rewards_combinator(rollout_rewards, pos_reward, neg_reward):
    """
    Re-organize the rewards in multi-agent setting for ARS.
    :param rollout_rewards: see return
    :param pos_reward: a list of reward generated by the positive policy, one per player.
    :param neg_reward: a list of reward generated by the positive policy, one per player.
    :return: a list of lists, one per player. For each player, a list contains the positive
            rewards and negative rewards in a format [[pos rew, neg rew],
                                                      [pos rew, neg rew]]
            , one row per noise.
    """
    for i, pair in enumerate(zip(pos_reward, neg_reward)):
        rollout_rewards[i].append(list(pair))
    return rollout_rewards


def rollout_rewards_combinator(rollout_rewards, new_rewards):
    """
    Combine rewards used in deploy_workers in rl_oracle.py.
    """
    new_rollout_rewards = []
    for i, j in zip(rollout_rewards, new_rewards):
        new_rollout_rewards.append(i + j)
    return new_rollout_rewards


