# Using thread joining, we sequentially loop through all the child threads
# of a parent thread and then call the child_thread.join() to
# make the parent thread wait for that child threads completing.
# Even though all the child threads can be commanded to execute
# as soon as they have be created by the parent, by using child_thread.start(),
# The parent thread has to wait till all the child threads complete
# execution, to continue with its remaining job tasks.

# A much more efficient way to make the parent thread wait for the
# completion of all its child threads is through the implementation of
# a "wait group" which simply keeps a condition variable that acts
# as a count of the currently active child threads. when this count reaches
# 0, the parent thread can continue with its other execution tasks.
