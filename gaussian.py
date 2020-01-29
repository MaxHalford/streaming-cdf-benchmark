import math


__all__ = ['Gaussian']


class Gaussian:

    μ = 0
    σ = 0
    n = 0

    def update(self, x):
        self.n += 1
        μ = self.μ
        self.μ += (x - self.μ) / self.n
        self.σ += ((x - μ) * (x - self.μ) - self.σ) / self.n

    def cdf(self, x):
        return .5 * (1 + math.erf((x - self.μ) / (self.σ ** .5 * math.sqrt(2))))

    def __repr__(self):
        return f'𝒩(μ={self.μ:.3f}, σ={self.σ ** .5:.3f})'
