#######################################################################
# Copyright (C) 2019 Yi Wan(wan6@ualberta.ca)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################
from alphaex.submitter import Submitter


def test_submitter():
    clusters = [
        {
            "name": "cedar",
            "capacity": 3,
            "account": "def-sutton",
            "project_root_dir": "/home/yiwan/projects/def-sutton/yiwan/AlphaEx",
            "exp_results_from": [
                "/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/output",
                "/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/error",
            ],
            "exp_results_to": ["test/output", "test/error"],
        },
        {
            "name": "mp2",
            "capacity": 3,
            "account": "def-sutton",
            "project_root_dir": "/home/yiwan/projects/def-sutton/yiwan/AlphaEx",
            "exp_results_from": [
                "/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/output",
                "/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/error",
            ],
            "exp_results_to": ["test/output", "test/error"],
        },
        
    ]
    job_list = [(1, 4), 6, (102, 105), 100, (8, 12), 107]
    repo_url = "https://github.com/yiwan-rl/AlphaEx.git"
    script_path = "test/submit.sh"
    submitter = Submitter(
        clusters,
        job_list,
        script_path,
        export_params={
            "python_module": "test.my_experiment_entrypoint",
            "config_file": "test/cfg/variables.json",
        },
        sbatch_params={
            "time": "00:10:00",
            "mem-per-cpu": "1G",
            "job-name": script_path.split("/")[1],
        },
        repo_url=repo_url,
        duration_between_two_polls=60,
    )
    submitter.submit()


if __name__ == "__main__":
    test_submitter()
