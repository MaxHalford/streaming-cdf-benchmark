import bisect
import collections
import math


__all__ = ['Histogram']


class Bin:
    """A Bin is an element of a Histogram."""

    def __init__(self, left, right=None, count=1):
        self.left = left
        self.right = left if right is None else right
        self.count = count

    def __add__(self, other):
        return Bin(
            left=min(self.left, other.left),
            right=max(self.right, other.right),
            count=self.count + other.count
        )

    def __lt__(self, other):
        return self.right < other.left

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right


class Histogram(collections.UserList):
    """Streaming histogram."""

    def __init__(self, max_bins=256):
        super().__init__()
        self.max_bins = max_bins
        self.n = 0

    def update(self, x):

        self.n += 1
        b = Bin(x)

        # Insert the bin if the histogram is empty
        if not self:
            self.append(b)
            return self

        i = bisect.bisect_left(self, b)
        if i == len(self):
            # x is past the right-most bin
            self.append(b)
        else:
            # Increment the bin counter if x is part of the ith bin
            if x >= self[i].left:
                self[i].count += 1
            # Insert the bin if it is between bin i-1 and bin i
            else:
                self.insert(i, b)

        # Bins have to be merged if there are more than max_bins
        if len(self) > self.max_bins:

            # Find the closest pair of bins
            min_diff = math.inf
            min_idx = None
            for idx, (b1, b2) in enumerate(zip(self.data[:-1], self.data[1:])):
                diff = b2.right - b1.right
                if diff < min_diff:
                    min_diff = diff
                    min_idx = idx

            # Merge the bins
            self[min_idx] += self.pop(min_idx + 1)

        return self

    def cdf(self, x):
        """Cumulative distribution function."""

        # Handle edge cases
        if not self or x < self[0].left:
            return 0.
        elif x >= self[-1].right:
            return 1.

        c = 0

        # Handle the first bin
        b = self[0]
        if x < b.right:
            c += b.count * (x - b.left) / (b.right - b.left)
            return c / self.n
        c += b.count

        # Handle the rest of the bins
        for b1, b2 in zip(self.data[:-1], self.data[1:]):
            if x < b2.right:
                # Interpolate
                c += b2.count * (x - b1.right) / (b2.right - b1.right)
                break
            c += b2.count

        return c / self.n
