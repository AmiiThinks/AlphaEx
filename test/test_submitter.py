#######################################################################
# Copyright (C) 2019 Yi Wan(wan6@ualberta.ca)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################
from alphaex.submitter import Submitter


def test_submitter():
    clusters = [
        {
            "name": "mp2",
            "capacity": 3,
            "project_root_dir": "/home/yiwan/projects/def-sutton/yiwan/AlphaEx",
            "exp_results_from": [
                "/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/output",
                "/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/error",
            ],
            "exp_results_to": ["test/output", "test/error"],
        },
        {
            "name": "cedar",
            "capacity": 2,
            "project_root_dir": "/home/yiwan/projects/def-sutton/yiwan/AlphaEx",
            "exp_results_from": [
                "/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/output",
                "/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/error",
            ],
            "exp_results_to": ["test/output", "test/error"],
        },
    ]
    num_jobs = 10
    repo_url = "https://github.com/yiwan-rl/AlphaEx.git"
    script_path = "test/submit.sh"
    submitter = Submitter(clusters, num_jobs, script_path, repo_url=repo_url)
    submitter.submit()


if __name__ == "__main__":
    test_submitter()
