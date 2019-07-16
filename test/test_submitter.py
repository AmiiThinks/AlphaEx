from experimenter.submitter import Submitter


def test_submitter():
	clusters = [
		{
			'name': 'mp2',
			'capacity': 200,
			'user_name': 'yiwan',
			'project_root_dir': '/home/yiwan/projects/def-sutton/yiwan/experimenter',
			'script_path': 'test/submit.sh'
		},
		{
			'name': 'cedar',
			'capacity': 100,
			'user_name': 'yiwan',
			'project_root_dir': '/home/yiwan/projects/def-sutton/yiwan/experimenter',
			'script_path': 'test/submit.sh'
		},
	]
	submitter = Submitter(clusters, 1000)
	submitter.submit()
	

if __name__ == '__main__':
	test_submitter()