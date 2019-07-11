from sweeper.sweeper import Sweeper
from sweeper.plotter import Plotter
import os
import logging
from cfg.plot_config import PlotConfig
import numpy as np


def test_sweeper():
	cfg_dir = 'test/cfg'
	log_dir = 'test/log'
	sweep_file_name = 'param.json'
	param_sweeper = Sweeper(os.path.join(cfg_dir, sweep_file_name))
	for sweep_id in range(0, param_sweeper.total_combinations):
		rtn_dict = param_sweeper.parse(sweep_id)
		
		report = 'idx: %d \nenv: %s \noptimizer_name %s\nlearning_rate: %5f' % (
			sweep_id,
			rtn_dict['env'],
			rtn_dict['optimizer_name'],
			rtn_dict['learning_rate'],
		)
		print(report)
		logger = logging.getLogger(str(sweep_id))
		logger.setLevel(logging.INFO)
		if not os.path.exists(os.path.join(log_dir, sweep_file_name)):
			os.makedirs(os.path.join(log_dir, sweep_file_name))
		log_file_path = os.path.join(log_dir, sweep_file_name, str(sweep_id) + '.txt')
		if os.path.exists(log_file_path):
			os.remove(log_file_path)
		fh = logging.FileHandler(log_file_path)
		fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s'))
		fh.setLevel(logging.INFO)
		logger.addHandler(fh)
		for _ in range(100):
			logger.info(report)
		fh.close()


class MyPlotter(Plotter):
	def get_numbers(self, file_path):
		
		file = open(file_path)
		lines = file.readlines()
		numbers = []
		for line in lines:
			if "learning_rate" in line:
				numbers.append(float(line.split(' ')[-1]))
		
		return numbers
	
	def get_print_label(self):
		return ['optimizer_name', 'learning_rate', 'beta1', 'beta2', 'clip_denom', 'alpha1', 'alpha2']
	
	def get_print_title(self):
		return ['env']
	
	def get_plot_indices(self, means_list, standard_errors_list):
		# if plot_cfg.criterion == "mean over all":
		# 	mean_return_per_param_setting = np.array([means.mean() for means in means_list])
		# elif plot_cfg.criterion == 'mean over second half':
		# 	mean_return_per_param_setting = np.array(
		# 		[np.array_split(means, 2)[1].mean() for means in means_list])
		# else:
		# 	raise NotImplementedError
		k = 1
		mean_return_per_param_setting = np.array([means.mean() for means in means_list])
		best_k_param_settings_indices = mean_return_per_param_setting.argsort()[-k:]
		return best_k_param_settings_indices
	
	
def test_plotter():
	
	plot_config_file = 'test/cfg/plot.json'
	my_plotter = MyPlotter(plot_config_file, PlotConfig)
	my_plotter.plot()


if __name__ == '__main__':
	test_sweeper()
	test_plotter()
