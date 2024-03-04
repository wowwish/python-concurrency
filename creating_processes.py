# REMEMBER:

# Threads run in the same memory space. Two or more threads running
# at the same time will share the same memory space. However, each Process
# will have its own independent memory space.

# As a result of the independent memory space for each Process, multiple
# Processes are more resource heavy than multiple Threads. Processes also
# take a longer time to be created than Threads.

# Threads have no isolation whereas Processes provide isolation. When
# using a Thread. If something crashes one Thread, all the associated
# Threads sharing the same memory space under a Process can also crash.
# This problem does not happen with Processes. If one Process crashes,
# the other ones are not affected.

# Processes are not affected by the Global Interpreter Lock (GIL) in python.
# You can have several Processes running simultaneously in a truly parallel
# fashion, unlike the case of Threads which are affected by the GIL and rely
# on "context-switching".

# When you create a new instance of a Process, it creates a copy of the
# parent Process's memory space. Processes can be started in python
# using the 'spawn', 'fork' and 'forkserver' methods. 'spawn' works both
# on windows (where is the default way to start a Process) and linux
# whereas 'fork' (the default method to start Process in linux) and
# 'forkserver' work only on linux.

# 'fork' creates a instnace of the Process object with a copy of the entire
# parent memory space. 'spawn' leaves out some file descriptors and other
# unneccessary things to save up on memory space. It is slightly better
# optimized that 'fork', but it takes longer time to start the Process.
# 'forkserver' is a hybrid that tries to save memory while also being fast
# by creating a forkserver Process out of the parent Process, that is used
# for instaniating new Processes. The first Process created by this method
# is a relatively slower because the forkserver Process has to be created,
# but subsequent Processes are created fast.

import multiprocessing
from multiprocessing import Process


def do_work():
    print('Starting Work')
    i = 0
    for _ in range(20000000):
        i += 1
    print('Finished Work')


if __name__ == '__main__':
    # Set 'spawn' as the Process starting method
    multiprocessing.set_start_method('spawn')
    # Initiate and start a number of processes according to
    # your CPU's capacity. you will see a peak in the cpu utilization
    # graph when this script is run.
    for _ in range(12):
        # Create the Process instance
        p = Process(target=do_work, args=())
        # Start the Process
        p.start()
