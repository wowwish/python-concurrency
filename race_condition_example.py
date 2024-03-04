# Lets replicate the race condition using an example:

# NOTE: In python 3.10, the Global Interpreter Lock (GIL)
# was replaced with a better implementaion to improve
# concurrent execution and reduces the need for explicit
# thread synchronization although it is still recommended
# to keep your threads synchronized to ensure thread safety
# and predictable behaviour.
# Hence this simulation will only work for python < 3.10

import time
from threading import Thread, Lock


class StingySpendy:
    money = 100  # class variable

    def stingy(self):
        # set the range value according to your CPU's capacity
        for i in range(500000000000):
            self.money += 10
        print('Stingy Done')

    def spendy(self):
        # set the range value according to your CPU's capacity
        for i in range(5000000000000):
            self.money -= 10
        print('Spendy Done')


class StingySpendySynchronized:
    money = 100  # class variable
    mutex = Lock()

    def stingy(self):
        # set the range value according to your CPU's capacity
        for i in range(5000000000):
            # This is the way to lock this mutex. This function
            # call inside the Thread will block the Thread until
            # this mutex is acquired if this mutex is locked with
            # some other Thread. The function call will continue
            # execution only after the other Thread releases the
            # mutex which is then acquired by the Thread of this
            # function call.
            self.mutex.acquire()
            self.money += 10
            # Now, after the operation on the shared resource,
            # we release the mutex for other threads to acquire.
            self.mutex.release()
        print('Stingy Done')

    def spendy(self):
        # set the range value according to your CPU's capacity
        for i in range(50000000000):
            self.mutex.acquire()
            self.money -= 10
            self.mutex.release()
        print('Spendy Done')


ss = StingySpendy()
Thread(target=ss.stingy(), args=()).start()
Thread(target=ss.spendy(), args=()).start()
time.sleep(5)
# If we add 10 million times and subtract 10 million times, the result
# should be the original value. But we see a weird result here because
# of race condition.
# To prevent the race condition, we have to lock the access to a particular
# chunk of code so that only one thread can access it at any point of time.
# This is achieved by using a "mutex lock".
# In our example, stingy will ask for mutex locking the access to the
# self.money variable and if it is not already locked, it will be locked
# with the stingy thread. Once stringy is done modifying the variable,
# the mutex lock will be unlocked for the spendy thread to use and vice versa.
# One of the guarantees of mutexes is that if two operations request for
# locking of a resource at the same time, only one of the operations will
# be locked with the resource.

# REMEMBER:
# Optimize the parallel program to lock the resource for minimal amount
# of time and to call the .acquire() and .release() methods of the mutex
# lock minimally
print("Money in the end", ss.money)
