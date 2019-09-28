from alphaex.submitter import Submitter


def test_submitter():
	clusters = [
		{
			'name': 'mp2',
			'capacity': 3,
			'project_root_dir': '/home/yiwan/projects/def-sutton/yiwan/AlphaEx',
			'script_path': 'test/submit.sh',
			'exp_results_from': ['/home/yiwan/projects/def-sutton/yiwan/AlphaEx/output', '/home/yiwan/projects/def-sutton/yiwan/AlphaEx/error'],
			'exp_results_to': ['./output', './error']
		},
		{
			'name': 'cedar',
			'capacity': 2,
			'project_root_dir': '/home/yiwan/projects/def-sutton/yiwan/AlphaEx',
			'script_path': 'test/submit.sh',
			'exp_results_from': ['/home/yiwan/projects/def-sutton/yiwan/AlphaEx/output', '/home/yiwan/projects/def-sutton/yiwan/AlphaEx/error'],
			'exp_results_to': ['./output', './error']
		},
	]
	num_jobs = 10
	repo_url = "https://github.com/yiwan-rl/AlphaEx.git"
	submitter = Submitter(clusters, num_jobs, repo_url=repo_url)
	submitter.submit()
	

if __name__ == '__main__':
	test_submitter()