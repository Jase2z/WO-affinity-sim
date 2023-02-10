
from multiprocessing import Pool, Lock
from time import perf_counter

def init_pool_processes(the_lock):
    '''Initialize each process with a global variable lock.
    '''
    global lock
    lock = the_lock
    global start_time 
    start_time = perf_counter()
    global cycle_time
    cycle_time = start_time

def e(i):
    if i % 1000000 == 0:
        lock.acquire()
        print(f'count: {i:,} total time: {perf_counter() - start_time}sec.')
        lock.release()

class MyGen:

    def __init__(self, size:int) -> None:
        self.size = size
        self.gen = self._gen()
    
    def _gen(self):
        for i in range(self.size):
            yield i
        print("generator done")

    def __len__(self) -> int:
        return self.size

    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.gen:
            raise StopIteration
        else:
            return next(self.gen)
        

if __name__ == '__main__':
    thou = 1000
    mill = 1000000
    bill = 1000000000
    tril = 1000000000000
    lock = Lock()
    with Pool(initializer=init_pool_processes, initargs=(lock,)) as pool:
        gen = MyGen(bill)
        list(pool.imap(e, gen, chunksize=1000))
#count: 0 total time: 0.00016289995983242989sec.
#count: 1,000,000 total time: 3.2839888999587856sec.
#count: 2,000,000 total time: 6.865179200016428sec.
#count: 3,000,000 total time: 10.548572500003502sec.