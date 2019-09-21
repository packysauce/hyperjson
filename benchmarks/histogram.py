## Eat json, create plot
# program takes two positional arguments
# first is the json output of a pytest benchmark run
# second is the output directory (must exist)


import matplotlib.pyplot as plt
import numpy as np
import itertools
from collections import defaultdict
import json
import sys


def nested_dict(): return defaultdict(nested_dict)


BAR_WIDTH = 0.25


def plot(operation, ops, outdir):
    tasks = ops[operation]
    with plt.xkcd():
        fig, axes = plt.subplots(figsize=(10, 20))
        for i, (name, contenders) in enumerate(tasks.items()):
            axes = plt.subplot(len(tasks), 1, i+1)
            axes.set_title("{} {} [operations/second]".format(operation, name))
            N = len(contenders)
            indices = np.arange(N)  # the x locations for the groups
            axes.set_xticks(indices)
            axes.set_xticklabels(contenders.keys())

            for i, (name, ops) in enumerate(contenders.items()):
                color = "#0809fe" if name == "hyperjson" else "#fe4ed8"
                axes.bar(i, ops, BAR_WIDTH, color=color)

        plt.tight_layout()
        plt.savefig("{}/{}.png".format(outdir, operation))


def get_ops(fname):
    data = nested_dict()
    with open(fname) as f:
        raw = json.load(f)
        for benchmark in raw["benchmarks"]:
            name, test = benchmark["param"].split('-', 1)
            ops = benchmark["stats"]["ops"]
            group = benchmark["group"]
            data[group][test][name] = ops
    return data


if __name__ == "__main__":
    ops = get_ops(sys.argv[1])
    plot("serialize", ops, sys.argv[2])
    plot("deserialize", ops, sys.argv[2])
