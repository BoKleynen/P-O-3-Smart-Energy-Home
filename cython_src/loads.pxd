cdef class Load:
    cdef float _power_consumption

cdef class ContinuousLoad(Load):
    pass

cdef class CyclicalLoad(Load):
    cdef int _start_time, _cycle_duration

cdef class TimedLoad(CyclicalLoad):
    pass

cdef class StaggeredLoad(CyclicalLoad):
    cdef int _original_start_time
