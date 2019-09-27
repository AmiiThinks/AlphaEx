from alphaex.submitter import Submitter


def test_submitter():
	clusters = [
		{
			'name': 'mp2',
			'capacity': 3,
			'project_root_dir': '/home/yiwan/projects/def-sutton/yiwan/AlphaEx',
			'script_path': 'test/submit.sh'
		},
		{
			'name': 'cedar',
			'capacity': 2,
			'project_root_dir': '/home/yiwan/projects/def-sutton/yiwan/AlphaEx',
			'script_path': 'test/submit.sh'
		},
	]
	submitter = Submitter(clusters, 10)
	submitter.submit()
	

if __name__ == '__main__':
	test_submitter()