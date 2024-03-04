# Conditional Variables can be used to make threads wait for execution
# until a particular condition is met. Whenever a thread is waiting on a
# conditional variable to become true, the mutex lock associated with that
# conditional variable will be released. This is very important because
# otherwise, no other thread will be able to change the conditional variable
# and the condition will never evaluate to true!

# Once the condition evaluates to true due to modification of the condition
# variable by other threads, and the other threads release their mutex lock on
# the conditional variable. Also, whenever the conditional variable is
# modified, a signal/broadcast is sent to be picked up by all waiting threads
# that are waiting for a condition involving the condition variable to become
# true. A signal wakes up only one waiting threads whereas a broadcast will
# wake up all waiting threads.


import time
from threading import Thread, Lock, Condition


# When using this mutex lock based class, you can see that the money variable
# reaches negative numbers which is not ideal. spendy should be able to
# subtract amount only when sufficient balance is present.
class StingySpendy:
    money = 100
    mutex = Lock()

    def stingy(self):
        for i in range(1000000):
            # get the mutex lock to make the class state immutable
            self.mutex.acquire()
            self.money += 10  # modify conditional variable
            # release the mutex lock and make the class mutable again
            self.mutex.release()
            print("Stingy Done")

    def spendy(self):
        for i in range(500000):
            # get the mutex lock to make the class state immutable
            self.mutex.acquire()
            self.money -= 20  # modify conditional variable
            if self.money < 0:
                print("Money in the bank: ", self.money)
            # release the mutex lock and make the class mutable again
            self.mutex.release()
            print("Spendy Done")


# Class that implements a conditional variable instead of a mutex lock
# When using methods of this class, you will notice that the class variable
# 'money' never becomes negative because of its implementation using
# conditional variable
class StingySpendyConditional:
    money = 100
    cv = Condition()

    def stingy(self):
        for i in range(1000000):
            # lock the conditional variable and make it immutable in
            # current thread calling this stingy method
            self.cv.acquire()
            # modify conditional variable release
            # the conditional variable for other methods calls
            # of the same class to be able to access it
            self.money += 10
            # Notify any potential waiting threads that their
            # condition for waiting may not be valid anymore
            self.cv.notify()
            # Release the lock on the conditional variable
            self.cv.release()
            print("Stingy Done")

    def spendy(self):
        for i in range(500000):
            # lock the conditional variable and make it immutable in
            # current thread calling this stingy method
            self.cv.acquire()
            # Make the thread executing spendy wait until sufficient
            # balance is obtained in the common class variable 'money'
            # We can also pass in an argument to the wait() call to make
            # it wait for a specific amount of time before resuming
            # execution instead of keeping it waiting for the condition
            # to become false
            while self.money < 20:
                self.cv.wait()
            self.money -= 20  # modify conditional variable
            if self.money < 0:
                print("Money in the bank: ", self.money)
            # Release the lock on the conditional variable
            self.cv.release()
            print("Spendy Done")


ss = StingySpendy()
ssvc = StingySpendyConditional()
# Thread(target=ss.stingy, args=()).start()
# Thread(target=ss.spendy, args=()).start()
Thread(target=ssvc.stingy, args=()).start()
Thread(target=ssvc.spendy, args=()).start()
time.sleep(5)
print("Money in the end: ", ss.money)
