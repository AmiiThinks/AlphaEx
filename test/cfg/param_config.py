#######################################################################
# Copyright (C) 2017 Shangtong Zhang(zhangshangtong.cpp@gmail.com)    #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import argparse


class ParamConfig:

    def __init__(self, param_dict=None):
        self.parser = argparse.ArgumentParser()
        
        # the following things must be defined in config file
        self.exp_name = None
        self.task_name = None
        self.agent_name = None
        self.network_name = None

        # problem definition
        self.discount = 0.99
        self.state_normalizer_name = 'DummyNormalizer'
        self.reward_normalizer_name = 'DummyNormalizer'
        self.history_length = None
        
        # experimental parameters
        self.log_level = 0
        self.log_interval = 1000
        self.if_save_network = False
        self.save_interval = 0
        self.if_eval = False
        self.eval_interval = 5000
        self.eval_episodes = 10
        self.max_steps = 1000000
        self.num_workers = 1
        self.timeout = None
        self.bootstrap_from_timeout = False

        # optimizer
        self.optimizer_name = 'RMSprop'
        self.learning_rate = 0.001
        self.optimizer_alpha = 0.99
        self.optimizer_eps = 0.00000001
        self.optimizer_centered = False
        self.sgd_update_frequency = 1
        self.gradient_clip = None
        self.clip_denom = None
        self.amsgrad = False
        self.beta1 = 0
        self.beta2 = 0
        self.beta3 = 0
        self.bbb = 0
        self.ttt = 0
        self.aaa = 0
        
        """
        The following are algorithm/trick specific parameters
        """
        
        # n-step method
        self.rollout_length = None
        
        # experience replay or planning
        self.memory_size = 50000
        self.batch_size = 32
        
        # target network
        self.use_target_network = False
        self.target_network_update_freq = None
        self.target_network_mix = 0.001
        
        # initial exploration
        self.initial_exploration = False
        self.exploration_steps = 0
        
        # double q
        self.double_q = False
        
        # gae
        self.use_gae = False
        self.gae_tau = 1.0
        
        # asynchronous replay or actor
        self.async_actor = False
        self.async_replay = False

        # scheduler for epsilon-greedy
        self.linear_schedule_start = 0.1
        self.linear_schedule_end = 0.1
        self.linear_schedule_steps = 1000
        
        # balancing multiple objectives
        self.actor_weight = 1.
        self.entropy_weight = 0.
        self.value_loss_weight = 1.0
        
        # categorical prediction
        self.categorical_v_min = None
        self.categorical_v_max = None
        self.categorical_n_atoms = 51
        
        # quantile
        self.num_quantiles = None
        
        # ppo
        self.optimization_epochs = 4
        
        # option-critic
        self.termination_regularizer = 0
        
        # self.__eval_env = None
        self.tasks = False

        if param_dict is not None:
            for key, value in param_dict.items():
                setattr(self, key, value)