import os
import time
import argparse


class Submitter(object):
	def __init__(self):
		self.starting_job_num = 0
		self.cluster_capacity = 100
		self.total_num_jobs = 960
	
	def submit_jobs(self, job_nums, cluster_name, project_root_dir, script_path):
		bash_script = "ssh %s 'cd %s; sbatch --array=%d-%d %s'" % (
			cluster_name, project_root_dir, self.starting_job_num, self.starting_job_num + job_nums - 1, script_path
		)
		myCmd = os.popen(bash_script).read()
		print(myCmd)
		print('submit jobs from %d to %d' % (self.starting_job_num, self.starting_job_num + job_nums - 1))
		self.starting_job_num += job_nums
		if self.starting_job_num >= self.total_num_jobs:
			return True
		return False
	
	def submit(self, project_root_dir, script_path, user_name, cluster_names):
		duration_between_two_checks = 60
		
		while True:
			for cluster_name in cluster_names:
				bash_script = "ssh %s squeue -u %s -r" % (cluster_name, user_name)
				myCmd = os.popen(bash_script).read()
				# print(myCmd)
				lines = myCmd.split('\n')
				num_current_jobs = 0
				for line in lines:
					if script_path.split('/')[-1] in line:
						num_current_jobs += 1
				print(num_current_jobs)
				
				if num_current_jobs < self.cluster_capacity:
					done = self.submit_jobs(
						self.cluster_capacity - num_current_jobs, cluster_name, project_root_dir, script_path
					)
					if done:
						print("Finish submitting all jobs, yeah!")
						exit(1)
			time.sleep(duration_between_two_checks)


parser = argparse.ArgumentParser(description="run_file")
parser.add_argument('--project-root-dir')
parser.add_argument('--script-path')
parser.add_argument('--user-name')

args = parser.parse_args()
submitter = Submitter()
cluster_names = ['mp2']
submitter.submit(args.project_root_dir, args.script_path, args.user_name, cluster_names)
