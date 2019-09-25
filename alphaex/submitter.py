import os
import time


class Submitter(object):
	def __init__(self, clusters, total_num_jobs, duration_between_two_checks=60):
		self.clusters = clusters
		self.starting_job_num = 0
		self.total_num_jobs = total_num_jobs
		self.duration_between_two_checks = duration_between_two_checks
	
	def submit_jobs(self, num_jobs, cluster_name, project_root_dir, script_path):
		bash_script = "ssh %s 'cd %s; sbatch --array=%d-%d %s'" % (
			cluster_name, project_root_dir, self.starting_job_num, self.starting_job_num + num_jobs - 1, script_path
		)
		myCmd = os.popen(bash_script).read()
		print(myCmd)
		print('submit jobs from %d to %d to %s' % (
			self.starting_job_num, self.starting_job_num + num_jobs - 1, cluster_name
		))
		self.starting_job_num += num_jobs
		if self.starting_job_num >= self.total_num_jobs:
			return True
		return False
	
	def submit(self):
		for cluster in self.clusters:
			bash_script = "ssh %s whoami" % cluster.name
			myCmd = os.popen(bash_script).read()
			cluster.username = myCmd.split('\n')
			
		while True:
			for cluster in self.clusters:
				bash_script = "ssh %s squeue -u %s -r" % (cluster.name, cluster.user_name)
				myCmd = os.popen(bash_script).read()
				lines = myCmd.split('\n')
				num_current_jobs = 0
				for line in lines:
					if cluster['script_path'].split('/')[-1] in line:
						num_current_jobs += 1
				print("cluster %s has %d jobs" % (cluster.name, num_current_jobs))
				
				if num_current_jobs < cluster.capacity:
					done = self.submit_jobs(
						min(cluster.capacity - num_current_jobs, self.total_num_jobs - self.starting_job_num),
						cluster['name'], cluster['project_root_dir'], cluster['script_path']
					)
					if done:
						print("Finish submitting all jobs, yeah!")
						exit(1)
			time.sleep(self.duration_between_two_checks)
