import numpy as np
cimport numpy as cnp


cdef cnp.ndarray[float, ndim=288] optimised_load_power(cnp.ndarray[object, ndim=1] opt_load_arr):
    cdef int i, j
    cdef cnp.ndarray[float, ndim=288] arr = np.zeros(288)

    for i in range(opt_load_arr.shape[0]):
        for j in range(opt_load_arr[i]._start_time/300, (opt_load_arr[i].start_time+opt_load_arr[i]._cycle_duration)/300):
            arr[j] += opt_load_arr[i]._power_consumption

    return arr


cpdef cost_function():