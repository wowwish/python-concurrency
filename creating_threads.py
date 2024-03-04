"""Amdahl's Law - The speedup in execution obtained by increasing the
number of processors running a computational workload is proportional
to the parallelizability of the computational workload. It outlines
the sequential botleneck of multiprocessor systems wherein the speedup
is not infinity even if the number of processors becomes infinity because
a fraction of the workload is can only be processed sequentially.

Gustafson's Law - By increasing the computational workload (number of
workloads being run or expanded workload), we can increase the
utilization of a multiprocessor system even when the workload
is highly sequential and thereby improve the scalability. Put another
way, the law says that the true parallel power of a large multiprocessor
system is achievable only when a large parallel problem is applied.

Sun and Ni's Law - When the local independent memory allocated to
each processor/core is increased when running a memory-intensive
workload in a multiprocessor system, the speedup achieved will
be greater than what is achievable according to Gustafson's law.
This is especially true in the case of workloads which have
parallelizable sub-problems that are memory-intensive and the
multiprocessor system provides the required independent memory
for each of the processor/core to meet the memory requirement
of these sub-problems."""

import time
from threading import Thread


def do_work():
    print("Starting Work")
    time.sleep(1)  # Simulating a calculation or reading from a file
    print("Finished Work")


def do_work2():
    print("Starting Work")
    i = 0
    for _ in range(20000000):
        i += 1
    print("Finished Work")


print("Normal Execution:")
print("=====================================================================")
for _ in range(5):
    do_work()
print("=====================================================================")

print("\n\n")

print("Using Threads:")
print("=====================================================================")
for _ in range(5):
    # Create a new Thread for running the do_work() function
    t = Thread(target=do_work, args=())
    t.start()  # start the thread's execution

"""Context-switching is when a processor/core switches execution from one
Thread/Process to another due to some interruption in the original
Process/Thread. Threads are interrupted by IO operations, downloads
from internet, API calls, waiting for user input etc.


The difference in behaviour observed in Thread based execution is because
of "context-switching" from one thread to another by the CPU processor/core
when the thread is interrupted by time.sleep(). When one thread prints
"Starting Work" and goes to sleep, the next thread from the "ready" queue
is executed by the processor/core. During the interruption due to sleep
the thread is placed at the end of the "ready" queue and the next process
is dequeued and executed. This way, all threads print "Starting Work" and
are cycled back into the queue until the sleep command completes. Then, they
all print "Finished Work". In this case, the whole execution of the five
threads lasted only 1s."""

time.sleep(6)
print("=====================================================================")
for _ in range(5):
    # Create a new Thread for running the do_work2() function
    t = Thread(target=do_work2, args=())
    t.start()  # start the thread's execution

"""In this case, all five threads are started at the same time, but here,
we perform a CPU based calculation, which is non-interrupting, instead
of sleeping. This makes do_work2() a CPU-bound function. Due to
Global-Interpreter Lock (GIL) in python, when one thread/process is
being executed, the other threads/processes will be placed in the
"waiting" queue. When the single processor/core executing
the current thread/process becomes free, all threads/processes
from the "waiting" queue are transferred to the "ready" queue and
the processor/core dequeues and executes the next thread/process
in the "ready" queue. In this case, all Threads start at the same
time, but finish one after another. If you check the CPU utilization
you will find that only one core/processor of the CPU is being
used. This is the Global-Interpreter Lock in python."""
