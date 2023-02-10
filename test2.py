from itertools import product
from time import perf_counter
from asyncio import run as asyrun
from typing import Generator

class AsyncItrProduct:
    """" Convert itertools.product to a async_generator"""  
    def __init__(self, gen:Generator, size:int) -> None:
        self.gen = gen
        self.size = size

    def __len__(self) -> int:
        return self.size

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.gen)
        except StopIteration:
            raise StopAsyncIteration

def my_gen(stop:int)->int:
    index = 0
    while index < stop:
        yield index
        index += 1

async def asy_main():
    start_sec = perf_counter()
    cycle_sec = start_sec
    thou = 1000
    mill = 1000000
    bill = 1000000000
    trill = 1000000000000

    size = trill
    gen = my_gen(size)
    gen = (i for i in range(size))
    asy_gen = AsyncItrProduct(gen=gen, size=size)
    async for e in asy_gen:
        if e % (mill) == 0:
            print(f"Size:{e:,} _ total sec: {perf_counter() - start_sec} _ cycle sec {perf_counter() - cycle_sec}")
            cycle_sec = perf_counter()

if __name__ == '__main__':
    asyrun(asy_main())
#Size:0 _ total sec: 0.00018450000789016485 _ cycle sec 0.00018909998470917344
#Size:1,000,000 _ total sec: 4.666366300021764 _ cycle sec 4.6659165999735706
#Size:2,000,000 _ total sec: 9.315977499994915 _ cycle sec 4.649298900039867
#Size:3,000,000 _ total sec: 13.945185000018682 _ cycle sec 4.6289321999647655
#Size:4,000,000 _ total sec: 18.61181650002254 _ cycle sec 4.666366699966602