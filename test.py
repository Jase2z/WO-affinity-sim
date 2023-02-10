import asyncio
from cProfile import run
from itertools import product
from concurrent.futures import ProcessPoolExecutor
import itertools
from multiprocessing import Pool, Queue, current_process, freeze_support, set_start_method, Lock
from time import time, perf_counter
from typing import Generator
from asyncio import wait as asy_wait
from hashlib import sha256
from pipe import select
from math import prod

def unfermented_moonshine() -> tuple:
    toon = [["joe", 87]]
    # [["Ogare", 92]]
    cookers = [["oven", 178], ["rare oven", 179]]
    containers = [["cauldron", 351]]
    water = [["water", 6], ["salt water", 16]]
    sugar = [["sugar", 47]]
    grain = [["wheat", 25], ["barley", 23], ["oat", 25], ["rye", 23]]
    wheat = [["wheat", 25]]
    barley = [["barley", 23]]
    oat = [["oat", 25]]
    rye = [["rye", 23]]
    pea = [["roasted pea", 62], ["fried pea", 59]]
    corn = [["roasted corn", 48], ["fried corn", 45]]
    garlic = [["roasted garlic", 96], ["fried garlic", 93]]
    tomato = [["roasted tomato", 47], ["fried tomato", 44]]
    pea_pods = [["roasted pea pods", 50], ["fried pea pods", 47]]
    carrot = [["roasted carrot", 45], ["fried carrot", 42]]
    cucumber = [["roasted cucumber", 21], ["fried cucumber", 18]]
    onion = [["roasted onion", 95], ["fried onion", 92]]
    potato = [["roasted potato", 51], ["fried potato", 48]]
    lettuce = [["roasted lettuce", 49], ["fried lettuce", 46]]
    pumpkin = [["roasted pumpkin", 49], ["fried pumpkin", 46]]
    cabbage = [["roasted cabbage", 46], ["fried cabbage", 43]]

    weight = [["roasted pumpkin", 49], ["fried pumpkin", 46], ["roasted cabbage", 46], ["fried cabbage", 43]]
    
    ingredients = (toon, cookers, containers, water, sugar, wheat, 
                    barley, oat, rye, pea, corn, garlic, tomato, 
                    pea_pods, carrot, cucumber, onion, potato, lettuce, pumpkin, 
                    cabbage, weight, weight, weight, weight, weight, weight,
                    weight, weight, weight, weight, weight, weight, 
                    weight)
                    #1x2x1x2x1x1
                    #1x1x1x2x2x2x2
                    #2x2x2x2x2x2x2
                    #2x4x4x4x4x4x4
                    #4x4x4x4x4x4x4
                    #1x2x1x2x1x1x1x1x1x2x2x2x2x2x2x2x2x2x2x2x2x4x4x4x4x4x4x4x4x4x4x4x4x4
                    # is about 1.09951E+12 possible combinations. The computer
                    # is not going to do well trying process about 1.1 trillion combinations.
    return ingredients




class AsyncItrProduct:
    """" Convert itertools.product to a async_generator"""
    def __init__(self, product: itertools.product):
        self.aiter = product

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.aiter)
        except StopIteration:
            raise StopAsyncIteration

async def remove_duplicates(x: tuple(list[str, int]), matches:dict):
    _sum = 0
    for ingredient in x:
        _sum = _sum + ingredient[1]
    affinity_num = (_sum % 138) + 1
    _aff = str(affinity_num)
    if str(_aff) not in matches.keys():
        matches[str(_aff)] = x



async def asy_main():
    # asyncio.run(asy_main()) is too slow.
    # Size:27 _ total sec: 585.2600553035736 _ cycle sec 292.39350152015686
    d = {}
    last_len = 0
    start_sec = time()
    cycle_sec = start_sec
    asy_gen = AsyncItrProduct(product(*unfermented_moonshine()))
    async for e in asy_gen:
        await remove_duplicates(e, d)
        if d and len(d) != last_len:
            print(f"Size:{len(d.keys())} _ total sec: {time() - start_sec} _ cycle sec {time() - cycle_sec}")
            cycle_sec = time()
            last_len = len(d)


#########################################
# no concurrency attempts.
# count 2,000,000 __ total 4.476 s' __ 1m cycles time 2.229 s'

def product_wrapper(ingredients:tuple[list]) -> Generator:
    """Wrapper for itertools.product() to check it's size. It's possible
    to have huge outputs, trillions. 
    :param ingredients: All the ingredient pool options to apply product
    combination.
    :type ingredients: tuple(list)
    :returns: a generator for itertools.product(ingredients)
    :rtype: Generator
    """
    size = 1
    for v in ingredients:
        size *= len(v)
    if size > 1000000:
        print(f"Their are {size:,} combinations. This is a lot and you probably don't want more then 1 million.") 
    return (r for r in product(*unfermented_moonshine()))

def rec_sync_test():
    """Test method to see how long it takes to simply iter through a 
    generator. example for 1 million entries:
    count 2,000,000 __ total 4.476 s' __ 1m cycles time 2.229 s'"""
    _gen = product_wrapper(unfermented_moonshine())
    start_time = perf_counter()
    cycle_time = start_time
    for k,e in enumerate(_gen):
        if k % 1000000 == 0:
            print(f'count {k:,} __ total {perf_counter() - start_time:,.3f} s\' __ 1m cycles time {perf_counter() - cycle_time:,.3f} s\'')
            cycle_time = perf_counter()

#todo make a generation Queue from this simulated_recipes = list(it.product(*ingredients))


#########################################
# Using multiprocess.Pool and Pool.imap()
#index: 0   time: 0.646s
#combo sha256: ee5025579e448fcb73b0c99b71720225fc39194a17cc2ed9ed0155a1682e6799
#index: 1,000,000   time: 4.681s
#combo sha256: 3842e4f674b9c1a9446b45cb3651e1d1033da92e768edf2bcc31e30e30f6372c
#index: 2,000,000   time: 8.705s
#combo sha256: f11786232fbad1342366092b95c4e33095c34cf4b4a53e9b0f11dab5b9d879da

def init_pool_processes(the_lock):
    '''Initialize each process with a global variable lock.
    '''
    global lock
    lock = the_lock

class MyGenT2:

    def __init__(self, ingredient_pools:tuple[list]) -> None:
        self.ingredient_pools = ingredient_pools
        self.iterable_length = prod(ingredient_pools | select(lambda x: len(x)))
        if self.iterable_length > 1000000:
            print(f"***\nTheir are {self.iterable_length:,} combinations."\
                "This is a lot and you probably don't want more then 1 million."\
                "\n***") 
            # It's possible to have huge number of combinations, trillions. 
        self.rec_gen = ((k,v) for k,v in enumerate(product(*self.ingredient_pools)))

    def __len__(self) -> int:
        return self.iterable_length

    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.rec_gen:
            raise StopIteration
        else:
            return next(self.rec_gen)

class Test2:
    #index: 2,000,000   time: 8.757s
    #combo sha256: f11786232fbad1342366092b95c4e33095c34cf4b4a53e9b0f11dab5b9d879da
    def __init__(self) -> None:
        self.cnt = 0
    
    def function(self, t):
        if t[0] % 1000000 == 0:
            lock.acquire()
            hash = sha256()
            st = ''.join(map(str, t[1])).encode("utf-8")
            hash.update(st)
            print(f'index: {t[0]:,}   time: {perf_counter() - self.start_time:,.3f}s\ncombo sha256: {hash.hexdigest()}')
            lock.release()
    
    def function2(self, t):
        if self.cnt % 1000000 == 0:
            lock.acquire()
            hash = sha256()
            st = ''.join(map(str, t)).encode("utf-8")
            hash.update(st)
            print(f'index: {self.cnt:,}   time: {perf_counter() - self.start_time:,.3f}s\ncombo sha256: {hash.hexdigest()}')
            lock.release()
        self.cnt = self.cnt + 1
    
    def fun_run(self):
        lock = Lock()
        gen = MyGenT2(unfermented_moonshine())
        p = Pool(initializer=init_pool_processes, initargs=(lock,))
        self.start_time = perf_counter()
        r = p.imap(self.function, gen, chunksize=10000)
        p.close()
        p.join()
    
    def fun_run2(self):
        lock = Lock()
        #gen = ((k,v) for k,v in enumerate(product(*unfermented_moonshine())))
        gen = (r for r in product(*unfermented_moonshine()))
        self.start_time = perf_counter()
        with Pool(initializer=init_pool_processes, initargs=(lock,)) as pool:
            it = pool.imap(self.function2, gen, chunksize=1000)
            for r in it:
                pass

        



if __name__ == '__main__':
    freeze_support()
    #set_start_method('spawn', True)

    #t_gen = MyGenT2(unfermented_moonshine())
    #for k, v in t_gen:
    #    a = 1

    a = Test2()
    a.fun_run2()
    







#todo make a consumer to take from the generator Queue.

#todo tweek generator and consumer count to get a somewhat balance processing.
#   Things like Queue max size can be used to prevent generator from geting too far 
#   ahead of consumer.
