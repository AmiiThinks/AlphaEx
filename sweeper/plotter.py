import matplotlib.pyplot as plt
import numpy as np
from sweeper.param_sweeper import ParamSweeper
from sweeper.plot_sweeper import PlotSweeper
from pathlib import Path
import os


class Plotter(object):
	def __init__(self, plot_config_file, PlotConfig, Config):
		self.plot_config_file = plot_config_file
		self.plot_cfg_cls = PlotConfig
		self.sweep_cfg_cls = Config
		self.sweeper = None
		self.plot_sweeper = None
	
	def merge_ids(self):
		"""
		For any parameter, if cfg has a value of that parameter, use the value.
		Otherwise enumerate all values that parameter could take according to exp_cfg file.
		In addition, for each parameter setting, list all run numbers.
		:param cfg: choose parameter settings according to cfg. Parameters in cfg can only take one value.
		:return: a list of parameter settings.
		"""
		
		param_setting_list = []
		plot_cfg_attributes = [a for a in dir(self.plot_sweeper.cfg) if not a.startswith('__')]
		for idx in range(self.sweeper.total_combinations):
			self.sweeper.parse(idx)
			if not hasattr(self.plot_sweeper.cfg, 'num_plot_runs'):
				self.plot_sweeper.cfg.num_plot_runs = 1
			param_setting_list.append(
				{'ids': [idx + run * self.sweeper.total_combinations for run in range(self.plot_sweeper.cfg.num_plot_runs)]})
			for a in plot_cfg_attributes:
				if hasattr(self.sweeper.cfg, a) and getattr(self.sweeper.cfg, a) != getattr(self.plot_sweeper.cfg, a):
					param_setting_list = param_setting_list[:-1]
					break
				param_setting_list[-1][a] = getattr(self.plot_sweeper.cfg, a)
		
		return param_setting_list
	
	def draw_curve(self):
		self.plot_sweeper.cfg.param_setting_list = self.merge_ids()
		
		Path(self.plot_sweeper.cfg.plot_dir).mkdir(parents=True, exist_ok=True)
		means_list = []
		standard_errors_list = []
		label_list = []
		for param_setting in self.plot_sweeper.cfg.param_setting_list:
			label = self.get_label(param_setting)
			label_list.append(label)
			file_names = ['%d.txt' % id for id in param_setting['ids']]
			n_numbers = []
			min_length = None
			for file_name in file_names:
				file_path = os.path.join(os.path.join(self.plot_sweeper.cfg.log_dir, self.plot_sweeper.cfg.sweep_file), file_name)
				numbers = self.get_numbers(file_path)
				if min_length is not None and len(numbers) < min_length:
					min_length = len(numbers)
				n_numbers.append(numbers)
			n_numbers = np.asarray([numbers[:min_length] for numbers in n_numbers])
			means = n_numbers.mean(axis=0)
			standard_errors = n_numbers.std(axis=0) / np.sqrt(n_numbers.shape[0])
			means_list.append(means)
			standard_errors_list.append(standard_errors)
		
		indices = self.get_plot_indices(means_list, standard_errors_list, self.plot_sweeper.cfg.best_k)
		
		for idx in indices:
			label = label_list[idx]
			plt.fill_between(
				np.arange(means_list[idx].shape[0]),
				means_list[idx] - standard_errors_list[idx],
				means_list[idx] + standard_errors_list[idx],
				alpha=0.2
			)
			plt.plot(
				np.arange(means_list[idx].shape[0]), means_list[idx], linewidth=1, label=label
			)
		
	def plot(self):
		self.plot_sweeper = PlotSweeper(self.plot_config_file, self.plot_cfg_cls)
		for plot_num in range(self.plot_sweeper.num_plots):
			for curve_num in range(self.plot_sweeper.num_curves):
				self.plot_sweeper.parse(plot_num, curve_num)
				self.sweeper = ParamSweeper(
					os.path.join(self.plot_sweeper.cfg.cfg_dir, self.plot_sweeper.cfg.sweep_file), self.sweep_cfg_cls
				)
				self.draw_curve()
			plt.legend(loc='lower right')
			plt.xlabel('steps')
			save_dir = os.path.join(self.plot_sweeper.cfg.plot_dir, self.plot_sweeper.cfg.sweep_file)
			if not os.path.exists(save_dir):
				os.makedirs(save_dir)
			plt.savefig(os.path.join(save_dir, str(plot_num) + '.pdf'))
			plt.clf()
			
	def get_numbers(self, file_path):
		raise NotImplementedError
	
	def get_label(self, param_setting):
		raise NotImplementedError
	
	def get_plot_indices(self, means_list, standard_errors_list, k):
		raise NotImplementedError