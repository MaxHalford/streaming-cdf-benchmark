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
    Histogram      0.0000928        0.0000670               0.0003984           9μs, 894ns               263ns
     Gaussian      0.1395074        0.1376272               0.2927523           1μs, 274ns                19ns
          KLL      0.0013191        0.0011100               0.0039909           1μs, 592ns          1μs, 597ns
   StreamHist      0.0001056        0.0000605               0.0008570          71μs, 800ns               218ns
     t-digest      0.0000653        0.0000452               0.0003002          42μs, 900ns         20μs, 794ns

Exponential

       Method   Error (mean)   Error (median)   Error (99th quantile)   Update time (mean)   Query time (mean)
    Histogram      0.0001441        0.0000938               0.0007342          10μs, 184ns               166ns
     Gaussian      0.2112691        0.1960659               0.4376764           1μs, 271ns                23ns
          KLL      0.0013566        0.0011700               0.0043513           1μs, 654ns          1μs, 748ns
   StreamHist      0.0221644        0.0001442               0.9959279          75μs, 621ns               190ns
     t-digest      0.0000556        0.0000416               0.0002140          44μs, 473ns         22μs, 517ns
```

## To do

- [Space-Efficient Online Computation of Quantile Summaries](http://infolab.stanford.edu/~datar/courses/cs361a/papers/quantiles.pdf)
- [Effective Computation of Biased Quantiles over Data Streams](https://www.cs.rutgers.edu/~muthu/bquant.pdf)
- [incubator-datasketches-cpp](https://github.com/apache/incubator-datasketches-cpp/tree/master/python) (not sure about this, didn't take too good a look)
