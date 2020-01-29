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
Unimodal gaussian

       Method   Error (mean)   Error (median)   Error (99th quantile)   Update time (mean)   Query time (mean)
    Histogram      0.0000924        0.0000626               0.0004189          16μs, 635ns               436ns
     Gaussian      0.0004454        0.0003688               0.0016372           2μs, 185ns                33ns
          KLL      0.0012744        0.0011500               0.0040004           2μs, 681ns          2μs, 507ns
   StreamHist      0.0001377        0.0000833               0.0008446          119μs, 83ns               337ns
     t-digest      0.0000561        0.0000399               0.0002508           69μs, 64ns         34μs, 270ns

Bimodal gaussian

       Method   Error (mean)   Error (median)   Error (99th quantile)   Update time (mean)   Query time (mean)
    Histogram      0.0000910        0.0000642               0.0004033          16μs, 529ns               403ns
     Gaussian      0.0510183        0.0448778               0.1260782           2μs, 145ns                34ns
          KLL      0.0013514        0.0011500               0.0041501           2μs, 653ns          2μs, 546ns
   StreamHist      0.0001112        0.0000696               0.0005455         121μs, 111ns               331ns
     t-digest      0.0000599        0.0000422               0.0002451            69μs, 5ns         33μs, 276ns

Exponential

       Method   Error (mean)   Error (median)   Error (99th quantile)   Update time (mean)   Query time (mean)
    Histogram      0.0001155        0.0000837               0.0004515          16μs, 813ns               205ns
     Gaussian      0.0769323        0.0827737               0.1511332           2μs, 188ns                30ns
          KLL      0.0012610        0.0010600               0.0040301           2μs, 689ns          2μs, 452ns
   StreamHist      0.0132580        0.0001553               0.9970128         122μs, 528ns               243ns
     t-digest      0.0000575        0.0000419               0.0002502          70μs, 837ns          32μs, 59ns
```

## To do

- [Space-Efficient Online Computation of Quantile Summaries](http://infolab.stanford.edu/~datar/courses/cs361a/papers/quantiles.pdf)
- [Effective Computation of Biased Quantiles over Data Streams](https://www.cs.rutgers.edu/~muthu/bquant.pdf)
- [incubator-datasketches-cpp](https://github.com/apache/incubator-datasketches-cpp/tree/master/python) (not sure about this, didn't take too good a look)
