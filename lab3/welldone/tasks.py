import itertools


class VasyaWords:
    """
    >>> w = VasyaWords()
    >>> w.count()
    4352
    """

    def __init__(self, alphabet=None, length=6, forbidden_start=None, forbidden_end=None, limited=None):
        self.alphabet = alphabet or ['В', 'И', 'Ш', 'Н', 'Я']
        self.length = length
        self.forbidden_start = set(forbidden_start or ['Ш'])
        self.forbidden_end = set(forbidden_end or ['И', 'Я'])
        self.limited = limited or {'В': 1}

    def _is_valid(self, word):
        if word[0] in self.forbidden_start:
            return False
        if word[-1] in self.forbidden_end:
            return False
        for letter, max_count in self.limited.items():
            if word.count(letter) > max_count:
                return False
        return True

    def count(self):
        """
        >>> VasyaWords().count()
        4352
        """
        return sum(
            1 for word in itertools.product(self.alphabet, repeat=self.length)
            if self._is_valid(word)
        )

    def generate(self):
        """
        >>> words = VasyaWords().generate()
        >>> len(words)
        4352
        >>> all(w[0] != 'Ш' for w in words)
        True
        >>> all(w[-1] not in ('И', 'Я') for w in words)
        True
        """
        return [
            ''.join(word)
            for word in itertools.product(self.alphabet, repeat=self.length)
            if self._is_valid(word)
        ]


class BinaryOnesCounter:
    """
    >>> c = BinaryOnesCounter(a=4, p=2014, b=2, q=2015, c=8)
    >>> c.count_ones()
    2013
    """

    def __init__(self, a, p, b, q, c):
        self.a = a
        self.p = p
        self.b = b
        self.q = q
        self.c = c

    def value(self):
        """
        >>> BinaryOnesCounter(4, 2014, 2, 2015, 8).value() > 0
        True
        """
        return self.a**self.p + self.b**self.q - self.c

    def count_ones(self):
        """
        >>> BinaryOnesCounter(4, 2014, 2, 2015, 8).count_ones()
        2013
        >>> BinaryOnesCounter(2, 3, 2, 2, 0).count_ones()
        2
        """
        return bin(self.value()).count('1')

    def binary_length(self):
        """
        >>> BinaryOnesCounter(2, 3, 2, 2, 0).binary_length()
        4
        """
        return self.value().bit_length()


class PowerProductFinder:
    """
    >>> f = PowerProductFinder(2, 3, 400_000_000, 600_000_000, m_even=True, n_even=False)
    >>> f.find()
    [408146688, 452984832, 516560652, 573308928]
    """

    def __init__(self, base_a, base_b, lo, hi, m_even=True, n_even=False):
        self.base_a = base_a
        self.base_b = base_b
        self.lo = lo
        self.hi = hi
        self.m_even = m_even
        self.n_even = n_even

    def _parity_ok(self, value, want_even):
        return (value % 2 == 0) if want_even else (value % 2 == 1)

    def find(self):
        """
        >>> PowerProductFinder(2, 3, 400_000_000, 600_000_000).find()
        [408146688, 452984832, 516560652, 573308928]
        >>> PowerProductFinder(2, 3, 1, 100).find()
        [3, 12, 27, 48]
        """
        result = []
        m = 0
        while self.base_a**m <= self.hi:
            if self._parity_ok(m, self.m_even):
                factor_a = self.base_a**m
                n = 1
                while True:
                    val = factor_a * self.base_b**n
                    if val > self.hi:
                        break
                    if val >= self.lo and self._parity_ok(n, self.n_even):
                        result.append(val)
                    n += 1
            m += 1
        return sorted(result)


if __name__ == '__main__':
    print('Задача 1. Количество слов Васи:')
    print(VasyaWords().count())

    print()
    print('Задача 2. Количество единиц в двоичной записи 4^2014 + 2^2015 - 8:')
    print(BinaryOnesCounter(a=4, p=2014, b=2, q=2015, c=8).count_ones())

    print()
    print('Задача 3. Числа N = 2^m * 3^n в [400_000_000; 600_000_000]:')
    for n in PowerProductFinder(2, 3, 400_000_000, 600_000_000, m_even=True, n_even=False).find():
        print(n)
