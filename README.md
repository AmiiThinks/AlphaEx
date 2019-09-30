# AlphaEx
AlphaEx (Alpha Experiment) is a python toolkit that helps you run a large number of experiments easily and efficiently.

With AlphaEx, you can:
1. Run thousands of experiments on multiple computer clusters automatically, so that you can squeeze the most out of your computation resource.
2. Sweep experiment variables in a simple effective way. Just define a json file and do all sweeps with one click.

The above 2 functions are implemented in 2 self-contained python scripts
`submitter.py`, `sweeper.py`.

**Warning**:

Sweeper can be used in any machine with python installed. But submitter is only compatible with **slurm** currently.
Make sure you have access to at least one cluster which has slurm installed. For example, I
have an account on compute canada, so I can use clusters including cedar, mp2, etc.

To test these 2 modules, run
`python test/test_submitter.py`, `python test/test_sweeper.py`
 (submitter needs to be configured first
with you own setting. Please refer to the next section.)

## Dependencies
1. python 3.7
2. numpy
3. json

## Submitter

### What is Submitter
Think about the case when you have 1000 jobs to run and 3 computer clusters to available.
It is not easy to manually assign jobs to clusters in an effective way.
One reason is each computer cluster has different performance.
Some may be faster than other. The other reason is each cluster may have
different restrictions on the number of jos submitted.
Submitter automatically submits all jobs for you in a simple way.
Here is how it works.

1. Synchronize project code from git repo (optional).
<p><img src="./images/submitter_1.png" alt="test" width="300" height="400"></p>

2. Submit jobs to each cluster. The number of jobs in each cluster will be the cluster's capacity.
<p><img src="./images/submitter_2.png" alt="test" width="300" height="300"></p>

3. Monitor clusters to see if there are jobs finished
<p><img src="./images/submitter_3.png" alt="test" width="300" height="300"></p>

4. If there are any, submit same number of new jobs as the finished ones until all jobs are submitted.
<p><img src="./images/submitter_4.png" alt="test" width="300" height="300"></p>

5. When all jobs are finished, copy experiment results from clusters to the server
<p><img src="./images/submitter_5.png" alt="test" width="300" height="230"></p>

### How to Use Submitter
To use submitter, you need to first have automatic ssh access to clusters from the server,
so that whenever you ssh to a cluster, just type in `ssh <cluster name>`
without entering the full url, your username and your password.

#### Ssh Automation

The next 3 steps help you do this. In your server's home directory, execute:

1. `ssh-keygen`
2. `ssh-copy-id <username>@<cluster url>`
3. Add the cluster information in `.ssh/config`

```
Host *
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa

Host <cluster name>
    HostName <cluster url>
    User <username>
```
Next time when you want to add a new cluster, just repeat step 2 and step 3.

#### Example
Now you can use submitter. test/test_submitter.py is a good example to start with.

```
from alphaex.submitter import Submitter


def test_submitter():
    clusters = [
        {
            'name': 'mp2',
            'capacity': 3,
            'project_root_dir': '/home/yiwan/projects/def-sutton/yiwan/AlphaEx',
            'exp_results_from': ['/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/output', '/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/error'],
            'exp_results_to': ['test/output', 'test/error']
        },
        {
            'name': 'cedar',
            'capacity': 2,
            'project_root_dir': '/home/yiwan/projects/def-sutton/yiwan/AlphaEx',
            'exp_results_from': ['/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/output', '/home/yiwan/projects/def-sutton/yiwan/AlphaEx/test/error'],
            'exp_results_to': ['test/output', 'test/error']
        },
    ]
    num_jobs = 10
    repo_url = "https://github.com/yiwan-rl/AlphaEx.git"
    script_path = "test/submit.sh"
    submitter = Submitter(clusters, num_jobs, script_path, repo_url=repo_url)
    submitter.submit()


if __name__ == '__main__':
    test_submitter()
```

`test/submit.sh` is an example of the array job submission script, please refer to the user manual of slurm if you don't understand the following script.

```
#!/bin/bash

#SBATCH --time=02:55:00
#SBATCH --mem-per-cpu=1G
#SBATCH --job-name submit.sh
#SBATCH --output=output/submit_%j.txt
#SBATCH --error=error/submit_%j.txt

export OMP_NUM_THREADS=1
mkdir -p output
mkdir -p error

sleep $((SLURM_ARRAY_TASK_ID / 10))
```

In this simple example, each job is just sleeping for some time. The sleeping time depends on the unique id of each job SLURM_ARRAY_TASK_ID.
This ID will be assigned by submitter automatically.

Now run `python test/test_submitter.py` in the server. Since the total capacity of mp2 and cedar are less than the total number jobs you want to run,
 submitter can not submit all jobs to these two clusters at once.
Instead, it will submit array jobs with array indices 0-2 to cluster mp2, and submit array jobs 3-4 to cluster cedar.
After that, it will periodically check whether there is any submitted job finishes.
And if there is any, the submitter will submit same number of new jobs as the finished ones until all 10 jobs are submitted.

After all jobs are submitted, copy experiment results from a cluster to the server when the cluster finishes all jobs.

### Tips
Since the server needs to  keep running a program to monitor job status and submit new jobs.
It may not be a good idea to use user's own laptop as the server because the laptop might not always have internet connection.
My suggestion is to use one cluster as the server and use program like screen to make
sure the monitor program runs in the background even if the user logout from the server.

## Sweeper
Using sweeper, you can sweep all experiment variables using one click. These
variables can be algorithms, simulators, parameters etc.

To use sweeper, first define a json file which specifies all the combinations of variables that you want to sweep over.
`cfg/variables.json` is an example:

```
{
    "experiments":
    [
        {
            "simulator": ["simulator_1"],
            "algorithm and parameters": [
                {
                    "algorithm": ["algorithm_1"],
                    "param1-2":
                    [
                        {
                            "param1": ["param1_1", "param1_2"],
                            "param2": [0.1, 0.2]
                        },
                        {
                            "param1": ["param1_3", "param1_4"],
                            "param2": [0.3, 0.4]
                        }
                    ],
                    "param3": [1, 2, 3]
                },

                {
                    "algorithm": ["algorithm_2"],
                    "param1":["param1_3", "param1_4"],
                    "param4": [true, false]
                }
            ]
        },
        {
            "simulator": ["simulator_2"],
            "algorithm and parameters": [
                {
                    "algorithm": ["algorithm_2"],
                    "param1":["param1_3", "param1_4"],
                    "param4": [true, false]
                },
                {
                    "algorithm": ["algorithm_3"],
                    "param5":["param5_1"],
                    "param6": [true]
                }
            ]
        }
    ]
}
```

**Three principles of Writing This File are:**
1. The json file should start from dictionary, not list
2. List and dictionary should be nested in alternative way
3. Each combination of variables takes only one element from every list, and takes all elements from every dictionary.


In our example, a legitimate combination of variables is

```
simulator: simulator_2
algorithm: algorithm_3
param1: None
param2: None
param3: None
param4: None
param5: param5_1
param6: True
```

Sweeper can generate all different combinations of variables. test/test_sweeper.py is an example of using it.

## Acknowledgement
This project was inspired by Muhammad Zaheer's sweeper code.

## Citation
Please use the bibtex if you want to cite this repo
```
@misc{alphaex,
  author = {Yi, Wan},
  title = {AlphaEx: A Python Toolkit for Managing Large Number of Experiments},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub Repository},
  howpublished = {\url{https://github.com/umichyiwan/AlphaEx}},
}
```

