#######################################################################
# Copyright (C) 2019 Yi Wan(wan6@ualberta.ca)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################


from alphaex.sweeper import Sweeper
import os


def test_sweeper():
	cfg_dir = 'test/cfg'
	sweep_file_name = 'variables.json'
	num_runs = 10
	# test Sweeper.parse
	sweeper = Sweeper(os.path.join(cfg_dir, sweep_file_name))
	for sweep_id in range(0, sweeper.total_combinations * num_runs):
		rtn_dict = sweeper.parse(sweep_id)
		
		report = 'idx: %d \nrun: %d\nsimulator: %s\nalgorithm: %s\nparam1: %s\nparam2: %s \nparam3: %s\nparam4: %s\nparam5: %s\nparam6: %s\n' % (
			sweep_id,
			rtn_dict.get('run', None),
			rtn_dict.get('simulator', None),
			rtn_dict.get('algorithm', None),
			rtn_dict.get('param1', None),
			rtn_dict.get('param2', None),
			rtn_dict.get('param3', None),
			rtn_dict.get('param4', None),
			rtn_dict.get('param5', None),
			rtn_dict.get('param6', None)
		)
		print(report)
	
	# test Sweeper.search
	print(sweeper.search({'param1': 'param1_3', 'param4': True}, num_runs))
	

if __name__ == '__main__':
	test_sweeper()
