import json


class PlotSweeper(object):
	"""
	The purpose of this class is to take an index, identify a configuration
	of hyper-parameters and create a Config object
	Important: parameters part of the sweep are provided in a list
	"""
	
	def __init__(self, config_file):
		with open(config_file) as f:
			self.config_dict = json.load(f)
		self.num_plots = 1
		self.set_num_plots()
		self.num_curves = 1
		self.set_num_curves()
	
	def set_num_plots(self):
		if 'on_different_plots' in self.config_dict:
			sweep_params = self.config_dict['on_different_plots']
			# calculating total_combinations
			tc = 1
			for params, values in sweep_params.items():
				tc = tc * len(values)
			self.num_plots = tc

	def set_num_curves(self):
		if 'on_the_same_plot' in self.config_dict:
			sweep_params = self.config_dict['on_the_same_plot']
			# calculating total_combinations
			tc = 1
			for params, values in sweep_params.items():
				tc = tc * len(values)
			self.num_curves = tc

	def parse(self, plot_num, curve_num):
		rtn_dict = dict()
		# Populating parameters on the same plot
		if 'on_the_same_plot' in self.config_dict:
			cumulative = 1
			different_plots_params = self.config_dict['on_the_same_plot']
			for param, values in different_plots_params.items():
				num_values = len(values)
				rtn_dict[param] = values[int(curve_num / cumulative) % num_values]
				cumulative *= num_values

		if 'on_different_plots' in self.config_dict:
			cumulative = 1
			different_plots_params = self.config_dict['on_different_plots']
			for param, values in different_plots_params.items():
				num_values = len(values)
				rtn_dict[param] = values[int(plot_num / cumulative) % num_values]
				cumulative *= num_values
				
		return rtn_dict