# Streaming CDF benchmark

This is a benchmark to compare algorithms that estimate [cumulative density functions](https://www.wikiwand.com/en/Cumulative_distribution_function) (CDF) on streaming data. This is of particular interest to me because being able to estimate CDF functions from a stream is important for online decision trees. Note that [the large body of work devoted to streaming quantiles](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=streaming+quantiles&btnG=) is relevant, as the CDF is simply the inverse of the quantile function. If there are any other methods which you would like me to add to the benchmark, then please send me an email at [maxhalford25@gmail.com](mailto:maxhalford25@gmail.com) or open an issue.

## Methods

- **Histogram**: Custom variant of [*A Streaming Parallel Decision Tree Algorithm*](http://jmlr.org/papers/volume11/ben-haim10a/ben-haim10a.pdf). I implemented this myself.
- **Gaussian**: Uses the CDF of a [Gaussian distribution](https://www.wikiwand.com/en/Normal_distribution) whose parameters `μ` and `σ` are updated online. This only works well in the special case where the data follows a normal distribution. Regardless, this method is still used in practice, for example in the online decision trees from [scikit-multiflow](https://github.com/scikit-multiflow/scikit-multiflow) as of version 0.4.1.
- **KLL**: Implementation of [*Optimal Quantile Approximation in Streams*](https://arxiv.org/abs/1603.05346). I found an implementation [here](https://github.com/edoliberty/streaming-quantiles), to which I added a `cdf(x)` method. Furthermore I made the algorithm deterministic by adding a `seed` parameter.
- **StreamHist**: Implementation of [*A Streaming Parallel Decision Tree Algorithm*](http://jmlr.org/papers/volume11/ben-haim10a/ben-haim10a.pdf). I found an implementation [here](https://github.com/carsonfarmer/streamhist).
- **t-digest**: Implementation of [*Computing Extremely Accurate Quantiles Using t-Digests*](https://arxiv.org/abs/1902.04023). I found an implementation [here](https://github.com/CamDavidsonPilon/tdigest).

Each method has an `update(x)` method as well as a `cdf(x)` method. I evaluated each method by updating it with a stream of `n` values. I stored and then sorted all the streamed values in order to obtain the real CDF function. I then compared took `m` uniformly spaced values and calculated the absolute error between the real CDF values and the output each method's `cdf(x)` function.

## Installation

1. Have Python 3 installed
2. Clone the repository and navigate to it
3. Create a [virtual environment](https://docs.python-guide.org/dev/virtualenvs/) (optional)
4. Run `pip install -r requirements`
5. Run `python main.py -h` to see the possible flags
6. Run `python main.py`

## Results

```
Bimodal gaussian

       Method   Error (mean)   Error (median)   Error (99th quantile)   Update time (mean)   Query time (mean)
    Histogram     0.00009279       0.00006699              0.00039842          11μs, 103ns               362ns
     Gaussian     0.13950737       0.13762724              0.29275235           1μs, 431ns                29ns
          KLL     0.00131907       0.00111000              0.00399090           1μs, 791ns          1μs, 867ns
   StreamHist     0.00010556       0.00006053              0.00085700          75μs, 899ns               286ns
     t-digest     0.00006525       0.00004522              0.00030021          45μs, 488ns          23μs, 23ns

Exponential

       Method   Error (mean)   Error (median)   Error (99th quantile)   Update time (mean)   Query time (mean)
    Histogram     0.00014409       0.00009378              0.00073424          10μs, 832ns               185ns
     Gaussian     0.21126915       0.19606587              0.43767641           1μs, 346ns                26ns
          KLL     0.00135660       0.00117000              0.00435130           1μs, 705ns          1μs, 837ns
   StreamHist     0.02216442       0.00014417              0.99592787          76μs, 667ns               211ns
     t-digest     0.00005562       0.00004158              0.00021403          45μs, 221ns         22μs, 566ns
```

## To do

- [Space-Efficient Online Computation of Quantile Summaries](http://infolab.stanford.edu/~datar/courses/cs361a/papers/quantiles.pdf)
- [Effective Computation of Biased Quantiles over Data Streams](https://www.cs.rutgers.edu/~muthu/bquant.pdf)
- [incubator-datasketches-cpp](https://github.com/apache/incubator-datasketches-cpp/tree/master/python) (not sure about this, didn't take too good a look)
