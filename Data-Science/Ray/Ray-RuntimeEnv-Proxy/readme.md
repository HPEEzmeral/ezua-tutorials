## Simple instructions to run experiments.

## EXAMPLE-1
With environmental variables such as (runtime_env, num_cpus, proxy, etc.)
To complete the tutorial follow simple steps below:
1. Login to you EzAF cluster.
2. Create a new notebook server using the `jupyter-data-science` image.
3. Clone the repository locally.
4. Launch the `ray-cpu-experiment.ipynb` notebook file.

## EXAMPLE-2 
With out pre-installing the packages on top of ray head-node, worker node docker images, However, if the client/user wants to create a more robust environment and minimize the potential issues. The bellow example demostrates how can a user compile ray experiments at scale, with out relaying on top of environmental variable such as (runtime_env).

# VITAL NOTE:
1. Please remember that these suggestions are meant to provide a workaround if the user/client continuesly facing or encounter issues with the runtime environment setup.
2. It's important to use the official runtime_env feature provided by Ray whenever possible, as it offers a more standardized and reliable approach to managing dependencies in remote tasks.
3. I have updated the proxy information because the experiment tested on top LR1 network, if you wish to compline other non-restricted network systems proxy considers (optional).

To complete the tutorial follow simple steps below:
1. Login to you EzAF cluster.
2. Create a new notebook server using the `jupyter-data-science` image.
3. Clone the repository locally.
4. Launch the `ray-runtimeenv-workaround.ipynb` notebook file.