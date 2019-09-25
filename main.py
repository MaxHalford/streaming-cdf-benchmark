import argparse
import collections
import random
import statistics
import time

import numpy as np
import tdigest
import tqdm

import histogram
from kll import kll


def format_ns(d):

    units = collections.OrderedDict({'ns': 1})
    units['μs'] = 1000 * units['ns']
    units['ms'] = 1000 * units['μs']
    units['s'] = 1000 * units['ms']
    units['m'] = 60 * units['s']
    units['h'] = 60 * units['m']
    units['d'] = 24 * units['h']

    parts = []

    for unit in reversed(units):
        amount = units[unit]
        quotient, d = divmod(d, amount)
        if quotient > 0:
            quotient = str(quotient).rstrip('0').rstrip('.')
            parts.append(f'{quotient}{unit}')
        elif d == 0:
            break

    return ', '.join(parts)


def boldify(text):
    return f'\033[1m{text}\033[0m'


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='number of random values to generate', type=int, default=100_000)
    parser.add_argument('-m', help='number of quantiles to evaluate on', type=int, default=1_000)
    parser.add_argument('-seed', help='random seed for reproducibility', type=int, default=42)
    parser.parse_args()
    args = parser.parse_args()

    rng = random.Random(args.seed)
    n = args.n
    m = args.m
    X = [None] * n

    random_funcs = {
        'Bimodal gaussian': lambda: rng.gauss(5, 1) if rng.random() < .5 else rng.gauss(10, 2),
        'Exponential': lambda: rng.expovariate(5)
    }

    for func_name, random_func in random_funcs.items():

        methods = {
            'Histogram': histogram.Histogram(max_bins=256),
            'KLL': kll.KLL(k=256, seed=42),
            't-digest': tdigest.TDigest(K=256),
        }
        errors = collections.defaultdict(list)
        update_durations = collections.defaultdict(float)
        query_durations = collections.defaultdict(float)

        print('Updating each method...')
        for i in tqdm.tqdm(range(n)):
            X[i] = random_func()
            for name, method in methods.items():
                tic = time.perf_counter_ns()
                method.update(X[i])
                update_durations[name] += time.perf_counter_ns() - tic

        # Sort all the values in order to get access to the true CDF
        print('Evaluating CDF approximations...')
        X.sort()
        for i in tqdm.tqdm(range(1, len(X), n // m)):
            x = X[i]
            q = i / n

            for name, method in methods.items():
                tic = time.perf_counter_ns()
                e = method.cdf(x)
                query_durations[name] += time.perf_counter_ns() - tic
                errors[name].append(abs(q - e))

        # Make a template to print out the results one method at a time
        headings = [
            'Method',
            'Error (mean)',
            'Error (99th quantile)',
            'Update time (mean)',
            'Query time (mean)',
        ]
        width = max(map(len, headings)) + 2
        row_format = '{:>{width}}' * len(headings)

        # Write down the table headings
        table = boldify(row_format.format(*headings, width=width)) + '\n'

        # Write down the true labels row by row
        table += '\n'.join((
            row_format.format(
                name,
                # Estimation error
                f'{statistics.mean(errors[name]):.8f}',
                f'{np.quantile(errors[name], .99):.8f}',
                # Update duration
                format_ns(update_durations[name] / n),
                # Querying duration
                format_ns(query_durations[name] / n),
                width=width
            )
            for name in methods
        ))

        print()
        print(boldify(func_name))
        print()
        print(table)
        print()
