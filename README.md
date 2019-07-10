# Sweeper
This toolkit makes it possible to run thousands of experiments on
multiple remote clusters automatically.

The workflow is as following:

1. You generate a json file, which contains all different parameter settings and give that json file
 to sweeper.
2. You give sweeper a list of remote clusters to run your experiments.
2. Sweeper parses that json file and generate many bash
 files. Each of these bash files sweeps part of all settings. For
 example, `cluster1.sh` will sweep parameter settings with index from 1 to
 10000, `cluster2.sh` will sweep 10001 to 20000, etc.
3. These bash files will be sent to remote clusters
 \[cluster1, cluster2, ...\] and each cluster runs its corresponding
 bash file.
4. All results will be sent to a user-defined cluster.
5. Given your json file, plotter will generate figures for you.