import collections
import random
import statistics
import time

import tdigest

import histogram


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
            parts.append(f'{quotient}{unit}')
        elif d == 0:
            break

    return ', '.join(parts)


if __name__ == '__main__':

    rng = random.Random(42)
    n = 100_000
    m = 100
    X = [None] * n

    methods = {
        'Histogram': histogram.Histogram(max_bins=256),
        'TDigest': tdigest.TDigest()
    }
    errors = collections.defaultdict(list)
    update_durations = collections.defaultdict(float)
    query_durations = collections.defaultdict(float)

    for i in range(n):
        X[i] = rng.gauss(5, 1) if rng.random() < .5 else rng.gauss(10, 2)
        for name, method in methods.items():
            tic = time.perf_counter_ns()
            method.update(X[i])
            update_durations[name] += time.perf_counter_ns() - tic

    X.sort()

    for i in range(1, len(X), n // m):
        x = X[i]
        q = i / n

        for name, method in methods.items():
            tic = time.perf_counter_ns()
            e = method.cdf(x)
            query_durations[name] += time.perf_counter_ns() - tic
            errors[name].append(abs(q - e))

    # Make a template to print out the results one method at a time
    headings = ['Method', 'Mean absolute error', 'Median absolute error', 'Mean update time', 'Mean query time']
    width = max(map(len, headings)) + 2
    row_format = '{:>{width}}' * len(headings)

    # Write down the table headings
    table = row_format.format(*headings, width=width) + '\n'

    # Write down the true labels row by row
    table += '\n'.join((
        row_format.format(
            name,
            f'{statistics.mean(errors[name]):.8f}',
            f'{statistics.median(errors[name]):.8f}',
            format_ns(update_durations[name] / n),
            format_ns(query_durations[name] / n),
            width=width
        )
        for name in methods
    ))

    print(table)
