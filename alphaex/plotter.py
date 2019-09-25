import matplotlib.pyplot as plt
import numpy as np
from alphaex.sweeper import Sweeper
from pathlib import Path
import os


class Plotter(object):
	def __init__(self, plot_config_file, PlotConfig):
		self.plot_config_file = plot_config_file
		self.plot_cfg_cls = PlotConfig
		self.plot_cfg = None
	
	def merge_ids(self):
		"""
		For any parameter, if cfg has a value of that parameter, use the value.
		Otherwise enumerate all values that parameter could take according to exp_cfg file.
		In addition, for each parameter setting, list all run numbers.
		:param cfg: choose parameter settings according to cfg. Parameters in cfg can only take one value.
		:return: a list of parameter settings.
		"""
		param_sweeper = Sweeper(
			os.path.join(self.plot_cfg.cfg_dir, self.plot_cfg.sweep_file)
		)
		param_setting_list = []
		
		for idx in range(param_sweeper.total_combinations):
			if not hasattr(self.plot_cfg, 'num_plot_runs'):
				self.plot_cfg.num_plot_runs = 1
			
			param_setting_list.append(
				{'ids': [idx + run * param_sweeper.total_combinations for run in range(self.plot_cfg.num_plot_runs)]}
			)
			
			param_sweeper_dict = param_sweeper.parse(idx)
			for key, value in param_sweeper_dict.items():
				if hasattr(self.plot_cfg, key) and getattr(self.plot_cfg, key) != value:
					param_setting_list = param_setting_list[:-1]
					break
				param_setting_list[-1][key] = value
		
		return param_setting_list
	
	def get_label(self, param_setting, print_labels):
		print_str = ''
		for label in print_labels:
			if label in param_setting:
				print_str += label + ': '
				print_str += str(param_setting[label]) + '  '
		return print_str
		
	def draw_curve(self):
		param_setting_list = self.merge_ids()

		Path(self.plot_cfg.plot_dir).mkdir(parents=True, exist_ok=True)
		means_list = []
		standard_errors_list = []
		label_list = []
		
		print_labels = self.get_print_label()
		
		for param_setting in param_setting_list:
			label = self.get_label(param_setting, print_labels)
			label_list.append(label)
			file_names = ['%d.txt' % id for id in param_setting['ids']]
			n_numbers = []
			min_length = None
			for file_name in file_names:
				file_path = os.path.join(os.path.join(self.plot_cfg.log_dir, self.plot_cfg.sweep_file), file_name)
				numbers = self.get_numbers(file_path)
				if min_length is not None and len(numbers) < min_length:
					min_length = len(numbers)
				n_numbers.append(numbers)
			n_numbers = np.asarray([numbers[:min_length] for numbers in n_numbers])
			means = n_numbers.mean(axis=0)
			standard_errors = n_numbers.std(axis=0) / np.sqrt(n_numbers.shape[0])
			means_list.append(means)
			standard_errors_list.append(standard_errors)
		
		indices = self.get_plot_indices(means_list, standard_errors_list)
		
		for idx in indices:
			label = label_list[idx]
			plt.fill_between(
				np.arange(means_list[idx].shape[0]) * self.plot_cfg.distance_between_two_points,
				means_list[idx] - standard_errors_list[idx],
				means_list[idx] + standard_errors_list[idx],
				alpha=0.2
			)
			plt.plot(
				np.arange(means_list[idx].shape[0]) * self.plot_cfg.distance_between_two_points,
				means_list[idx], linewidth=1, label=label
			)
		
	def plot(self):
		plot_sweeper = Sweeper(self.plot_config_file)
		for plot_num in range(plot_sweeper.config_dict['on_different_plots'][0]['num_combinations']):
			plot_dict = dict()
			if 'on_different_plots' in plot_sweeper.config_dict:
				plot_sweeper.parse_helper(plot_num, plot_sweeper.config_dict['on_different_plots'][0], plot_dict)
			plot_label = str(plot_dict)
			for curve_num in range(plot_sweeper.config_dict['on_the_same_plot'][0]['num_combinations']):
				if 'on_the_same_plot' in plot_sweeper.config_dict:
					plot_sweeper.parse_helper(curve_num, plot_sweeper.config_dict['on_the_same_plot'][0], plot_dict)
				self.plot_cfg = self.plot_cfg_cls(plot_dict)
				self.draw_curve()
			plt.legend(loc='lower right')
			plt.title(plot_label)
			plt.xlabel(self.plot_cfg.x_label)
			plt.ylabel(self.plot_cfg.y_label)
			save_dir = os.path.join(self.plot_cfg.plot_dir, self.plot_cfg.sweep_file)
			if not os.path.exists(save_dir):
				os.makedirs(save_dir)
			plt.savefig(os.path.join(save_dir, str(plot_num) + '.pdf'))
			plt.clf()
			
	def get_numbers(self, file_path):
		raise NotImplementedError
	
	def get_print_label(self):
		raise NotImplementedError
	
	def get_plot_indices(self, means_list, standard_errors_list):
		raise NotImplementedError