class PlotConfig:
	def __init__(self, plot_dict=None):
		self.log_dir = "test/log"
		self.plot_dir = "test/plot"
		self.cfg_dir = "test/cfg"
		self.criterion = "mean over all"
		self.x_label = 'steps'
		self.y_label = 'return'
		self.distance_between_two_points = 1000
		if plot_dict is not None:
			for key, value in plot_dict.items():
				setattr(self, key, value)