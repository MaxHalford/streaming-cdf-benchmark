# Streaming CDF benchmark

This is a benchmark to compare algorithms that estimate [cumulative density functions](https://www.wikiwand.com/en/Cumulative_distribution_function) (CDF) on streaming data. This is of particular interest to me because being able to estimate CDF functions from a stream is important for online decision trees. Note that [the large body of work devoted to streaming quantiles](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=streaming+quantiles&btnG=) is relevant, as the CDF is simply the inverse of the quantile function. If there are any other methods which you would like me to add to the benchmark, then please send me at email at [maxhalford25@gmail.com](mailto:maxhalford25@gmail.com).

## Methods

- **Histogram**: Custom variant of [*A Streaming Parallel Decision Tree Algorithm*](http://jmlr.org/papers/volume11/ben-haim10a/ben-haim10a.pdf). I implemented this myself. You can find another implementation written in Golang [here](https://github.com/VividCortex/gohistogram).
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

     Method           Error (mean)  Error (99th quantile)     Update time (mean)      Query time (mean)
  Histogram             0.00009279             0.00039842             6μs, 679ns                  234ns
        KLL             0.00114572             0.00397040             1μs, 622ns             2μs, 858ns
 StreamHist             0.00010556             0.00085700            67μs, 382ns                  183ns
   t-digest             0.00006525             0.00030021            42μs, 895ns            21μs, 328ns

Exponential

     Method           Error (mean)  Error (99th quantile)     Update time (mean)      Query time (mean)
  Histogram             0.00014409             0.00073424             7μs, 205ns                  129ns
        KLL             0.00123010             0.00400120             1μs, 744ns             2μs, 918ns
 StreamHist             0.02216442             0.99592787            74μs, 307ns                  151ns
   t-digest             0.00005562             0.00021403            45μs, 699ns            22μs, 452ns
```
