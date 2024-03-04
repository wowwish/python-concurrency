# A join is an operation that one thread can call on another thread
# to wait until that thread finishes from its work.
# The simplest example of a thread join is a parent thread that
# creates and starts a new child thread. The child thread
# will go about its task doing what it is asked to do and
# the parent thread would call join on this child thread. This
# blocks the parent thread (thread goes to sleep and becomes
# non-runnable) until the child thread dies off by completing
# its work. Then the parent thread is unblocked (wakes up
# from sleep) and continues its execution.


import time
from threading import Thread, Lock
import os
from os.path import isdir, join


def child():
    print('Child Thread doing work...')
    time.sleep(5)  # sleep for 5 sec
    print('Child Thread Done...')


def parent():
    t = Thread(target=child(), args=([]))
    t.start()
    print('Parent Thread is waiting...')
    # Here, we block the parent thread 't' until the child thread
    # is completed, using join().
    # we can provide a timeout argument to join() that will unblock the
    # parent thread when the timeout is reached irrespective of the status
    # of the child thread.
    t.join()
    print('Parent Thread is unblocked...')


# parent()

# A RECURSIVE FILE SEARCH EXAMPLE USING THREAD JOIN

# Use mutex locking to prevent overwriting of matches by multiple threads
mutex = Lock()
# a list of paths of files
matches = []


def file_search(root, file_name):
    print('Searching in', root)

    child_threads = []

    # loop over subdir in the given root
    for file in os.listdir(root):
        full_path = join(root, file)
        if file_name in file:
            # Wait for matches to be unlocked from other threads
            # and then lock matches with the current thread
            mutex.acquire()
            matches.append(full_path)
            # release matches for other threads to use
            mutex.release()
        if isdir(full_path):
            # Recursive call is done through a child thread
            th = Thread(target=file_search, args=([full_path, file_name]))
            th.start()
            child_threads.append(th)
            # we cannot do th.join() here because we will then be waiting for
            # each child thread to complete before another child thread starts
            # its search. This means that our search will not be parallel.
    for th in child_threads:
        # join every child thread to the parent thread. The parent thread
        # waits on every child thread to give completed signal by sqeuentially
        # communicating with each child thread. But the child threads are all
        # started at the same time and execute concurrently through
        # context-switching
        th.join()


def main():
    t = Thread(target=file_search, args=(["C:/Program Files/", "7z.exe"]))
    t.start()
    # t.join() is used here to make the execution wait until this parent thread
    # has completed its execution and then pick up the results from matches
    t.join()
    for m in matches:
        print('Matched: ', m)


main()
