from time import perf_counter


if __name__ == '__main__':
    start_sec = perf_counter()
    cycle_sec = start_sec
    thou = 1000
    mill = 1000000
    bill = 1000000000
    trill = 1000000000000
    size = trill
    gen = (i for i in range(size))
    for i in gen:
        if i % mill == 0:
            print(f"Size:{i:,} _ total sec: {perf_counter() - start_sec} _ cycle sec {perf_counter() - cycle_sec}")
            cycle_sec = perf_counter()