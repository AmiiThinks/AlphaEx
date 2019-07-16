from experimenter.sweeper import Sweeper
import logging
import os


def test_sweeper():
	cfg_dir = 'test/cfg'
	log_dir = 'test/log'
	sweep_file_name = 'param.json'
	param_sweeper = Sweeper(os.path.join(cfg_dir, sweep_file_name))
	for sweep_id in range(0, param_sweeper.total_combinations):
		rtn_dict = param_sweeper.parse(sweep_id)
		
		report = 'idx: %d \nparam1: %s \nparam2 %s\nparam3: %s\nparam4: %s \nparam5 %s\nparam6: %s\nparam7: %s \nparam8 %s\n' % (
			sweep_id,
			rtn_dict.get('param1', None),
			rtn_dict.get('param2', None),
			rtn_dict.get('param3', None),
			rtn_dict.get('param4', None),
			rtn_dict.get('param5', None),
			rtn_dict.get('param6', None),
			rtn_dict.get('param7', None),
			rtn_dict.get('param8', None),
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
		

if __name__ == '__main__':
	test_sweeper()
