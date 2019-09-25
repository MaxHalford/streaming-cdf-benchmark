# Streaming CDF benchmark

This is a benchmark to compare algorithms that estimate [cumulative density functions](https://www.wikiwand.com/en/Cumulative_distribution_function) (CDF) on streaming data. This is of particular interest to me because being able to estimate CDF functions from a stream is important for online decision trees. Note that [the large body of work devoted to streaming quantiles](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=streaming+quantiles&btnG=) is relevant, as the CDF is simply the inverse of the quantile function. If there are any other methods which you would like me to add to the benchmark, then please send me at email at [maxhalford25@gmail.com](mailto:maxhalford25@gmail.com).

## Methods

- **Histogram**: Custom implementation of [*A Streaming Parallel Decision Tree Algorithm*](http://jmlr.org/papers/volume11/ben-haim10a/ben-haim10a.pdf). I implemented this myself. You can find another implementation written in Golang [here](https://github.com/VividCortex/gohistogram).
- **KLL**: Implementation of [*Optimal Quantile Approximation in Streams*](https://arxiv.org/abs/1603.05346). I found an implementation [here](https://github.com/edoliberty/streaming-quantiles), to which I added a `cdf(x)` method. Furthermore I made the algorithm deterministic by adding a `seed` parameter.
- **t-digest**: Implementation of [*Computing Extremely Accurate Quantiles Using t-Digests*](https://arxiv.org/abs/1902.04023). I found an implementation [here](https://github.com/CamDavidsonPilon/tdigest).

Each method has an `update(x)` method as well as a `cdf(x)` method.

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
  Histogram             0.00009279             0.00039842             6μs, 250ns                  227ns
        KLL             0.00112768             0.00395346             1μs, 469ns             2μs, 826ns
   t-digest             0.00006525             0.00030021            38μs, 740ns            21μs, 288ns

Exponential

     Method           Error (mean)  Error (99th quantile)     Update time (mean)      Query time (mean)
  Histogram             0.00014409             0.00073424             6μs, 119ns                  120ns
        KLL             0.00122809             0.00399595             1μs, 411ns             2μs, 900ns
   t-digest             0.00005562             0.00021403            38μs, 371ns            22μs, 225ns
```
