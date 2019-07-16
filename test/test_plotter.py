from experimenter.plotter import Plotter
from test.cfg.plot_config import PlotConfig
import numpy as np


class MyPlotter(Plotter):
	def get_numbers(self, file_path):
		
		file = open(file_path)
		lines = file.readlines()
		numbers = []
		for line in lines:
			if "param3" in line:
				numbers.append(float(line.split(' ')[-1]))
		
		return numbers
	
	def get_print_label(self):
		return ['param1', 'param2', 'param3', 'param4', 'param5', 'param6', 'param7', 'param8']
	
	def get_plot_indices(self, means_list, standard_errors_list):
		k = 1
		mean_return_per_param_setting = np.array([means.mean() for means in means_list])
		best_k_param_settings_indices = mean_return_per_param_setting.argsort()[-k:]
		return best_k_param_settings_indices


def test_plotter():
	plot_config_file = 'test/cfg/plot.json'
	my_plotter = MyPlotter(plot_config_file, PlotConfig)
	my_plotter.plot()


if __name__ == '__main__':
	test_plotter()