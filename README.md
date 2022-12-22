# Experiment


## Download
```
git clone https://github.com/almarelo/ColoringGameExperiment
```

## Setup
For development, create a virtual environment as follow:
```
cd ColoringGameExperiment
virtualenv -p python3.10 env # python3.9 also works!
source env/bin/activate
```

Then, install `networkx` and `matplotlib` libraries:
```
pip install networkx matplotlib
```

## Running
By default, experiment prints a brief usage:
```
python experiment.py
usage: experiment.py [-h] -c NUM_COLORS -n NUM_NODES [-p PROBABILITY] [-r REPORT]
experiment.py: error: the following arguments are required: -c/--num-colors, -n/--num-nodes
```

Running an experiment with 2 colors and 24 nodes:
```
python experiment.py -c 2 -n 24
```
