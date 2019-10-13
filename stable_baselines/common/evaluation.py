import numpy as np


def evaluate_policy(model, env, n_eval_episodes=10, deterministic=True,
                    render=False, callback=None, min_reward=None):
    """
    Runs policy for n episodes and returns average reward
    :param model: (RL model)
    :param env: (gym.Env)
    :param n_eval_episodes: (int) Number of episode to evalute the agent
    :param deterministic: (bool) Whether to use deterministic or not actions
    :param render: (bool) Whether to render or not the environement
    :param callback: (callable) callback function to do additional checks
    :param min_reward: (float) Minimum expected reward per episode,
        this will raise an error if the performance is not met
    :return: (float, int) Mean reward per episode, total number of steps
    """
    episode_rewards, n_steps = [], 0
    for _ in range(n_eval_episodes):
        obs = env.reset()
        done, state = False, None
        episode_reward = 0.0
        while not done:
            action, state = model.predict(obs, state=state, deterministic=deterministic)
            if callback is not None:
                callback(obs, action, done, episode_reward, model)
            obs, reward, done, _ = env.step(action)
            episode_reward += reward
            n_steps += 1
            if render:
                env.render()
        episode_rewards.append(episode_reward)
    mean_reward = np.mean(episode_rewards)
    if min_reward is not None:
        assert mean_reward > min_reward, '{:.2f} < {:.2f}'.format(mean_reward, min_reward)
    return mean_reward, n_steps
