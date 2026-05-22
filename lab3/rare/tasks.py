import itertools


# ─────────────────────────────────────────────
# Задача 1. Слова Васи
# ─────────────────────────────────────────────

def count_vasya_words():
  
    alphabet = ['В', 'И', 'Ш', 'Н', 'Я']
    vowels = {'И', 'Я'}
    count = 0
    for word in itertools.product(alphabet, repeat=6):
        if word[0] == 'Ш':
            continue
        if word[-1] in vowels:
            continue
        if word.count('В') > 1:
            continue
        count += 1
    return count


# ─────────────────────────────────────────────
# Задача 2. Единицы в двоичной записи
# ─────────────────────────────────────────────

def count_ones_in_binary():
  
    value = 4**2014 + 2**2015 - 8
    return bin(value).count('1')


# ─────────────────────────────────────────────
# Задача 3. Числа вида 2^m * 3^n
# ─────────────────────────────────────────────

def find_2m_3n_numbers():
 
    lo, hi = 400_000_000, 600_000_000
    result = []

    m = 0
    while 2**m <= hi:
        if m % 2 == 0:
            base = 2**m
            n = 1
            while True:
                val = base * (3**n)
                if val > hi:
                    break
                if val >= lo and n % 2 == 1:
                    result.append(val)
                n += 1
        m += 1

    return sorted(result)


# ─────────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print('Задача 1. Количество слов Васи:')
    print(count_vasya_words())

    print()
    print('Задача 2. Количество единиц в двоичной записи 4^2014 + 2^2015 - 8:')
    print(count_ones_in_binary())

    print()
    print('Задача 3. Числа N = 2^m * 3^n в [400_000_000; 600_000_000]:')
    for n in find_2m_3n_numbers():
        print(n)
