# Processes/Threads need to share or communicate with each other in order to
# complete the computational work ahead of them. This manner of
# communication is called as Inter-Process-Communication (IPC) or
# Inter-Thread-Communication in the case of Threads.

# All the different manners of communication between threads and
# processes fall into two categories: 'message passing' and 'shared memory'.
# In 'message passing', one process can send a message to another. In
# 'shared memory', typically a thread writes data to shared memory which can
# be accessed by other threads. This way of IPC is advantageous for
# multiple Threads as threads have shared memory and this reduces
# communication overhead. Which type of IPC you use depends on the
# problem to be solved.


import json
import urllib.request
import time
from threading import Thread, Lock


# Here we implement a letter function to calculate the frequency of
# letters from a given url. This function can be parallelized by utilizing
# the 'shared memory' approach of Threads.

# global variable to keep track of finished calls of count_letters()
finished_count = 0


def count_letters(url, frequency):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    txt = str(response.read())
    for char in txt:
        letter = char.lower()
        if letter in frequency:
            frequency[letter] += 1
    global finished_count
    finished_count += 1


def count_letters_synchronized(url, frequency, mutex):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    txt = str(response.read())
    # It turns out that the code is more performant when the mutex is acquired
    # only once here instead of acquiring the mutex for every letter in the
    # frequency table
    mutex.acquire()
    for char in txt:
        letter = char.lower()
        if letter in frequency:
            mutex.acquire()
            frequency[letter] += 1
            mutex.release()
    global finished_count
    finished_count += 1
    # finished_count is also shared between the threads and hence, we release
    # the lock after it is updated.
    mutex.release()


def main():
    # initialize the frequency dictionary
    frequency = {}
    mutex = Lock()
    for c in 'abcdefghijklmnopqrstuvwxyz':
        frequency[c] = 0

    start = time.time()
    for i in range(1000, 1020):
        rfc_url = f'https://www.rfc-editor.org/rfc/rfc{i}.txt'

        # To perform a synchronized multi-threaded computation of 20 text urls
        Thread(target=count_letters, args=(rfc_url, frequency)).start()
        # To perform a synchronized multi-threaded computation of 20 text urls
        Thread(target=count_letters_synchronized, args=(rfc_url, frequency))\
            .start()
        # NOTE: the threads will be created, but the loop will not wait
        # until all threads finish. So, for our end time measurement,
        # we need to wait until all threads complete using a global
        # count of the finished threads.

        # To Perform a single-threaded computation of 20 text urls
        # count_letters(rfc_url, frequency)

    # wait till all 20 calls to count_letters() completes in the 20 spawned
    # threads. Checks status every 0.5 sec.
    # while finished_count < 20:
    #     time.sleep(0.5)
    # end = time.time()

    # We can use the mutex lock itself to check if all threads have completed
    # computation, instead of using time.sleep() to check every 0.5 sec
    while True:
        mutex.acquire()
        if finished_count == 20:
            break
        mutex.release()
        time.sleep(0.5)
    end = time.time()

    print(json.dumps(frequency, indent=4))
    print('Done, time taken: ', end - start)


main()

# If you examine the results of the threads running in parallel and
# single-thread execution, you will notice that the counts donot match.
# This is because in the parallel execution, the threads step over each
# other due to lack of synchronization.
# When two Threads read and write the same frequency count data from the
# dictionary, there will be instances where one Thread overwrites the value
# of another Thread. The read and write processes donot happen in a
# synchronized manner. This is also called as "race condition" where multiple
# threads or processes access and use the same resources.
