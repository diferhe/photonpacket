import numpy as np
cimport numpy as np

cimport cython 

DTYPE = np.uint32
ctypedef np.uint32_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def coinc(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2):
    '''
    Generate coincidences between two frames
    
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*f2l, 4], dtype=DTYPE)
    cdef int i = 0
    cdef int j = 0
    for i in range(f1l):
        for j in range(f2l):
            cframe[i+f1l*j,0] =  frame1[i,0]
            cframe[i+f1l*j,1] =  frame2[j,0]
            cframe[i+f1l*j,2] =  frame1[i,1]
            cframe[i+f1l*j,3] =  frame2[j,1]
    return cframe

@cython.boundscheck(False)
@cython.wraparound(False)  
def bincoinc(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
             np.ndarray[DTYPE_t, ndim=4] hist):
    '''
    Bin coincidences between two frames, adding them to hist
    
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef int i = 0
    cdef int j = 0
    for i in range(f1l):
        for j in range(f2l):
            hist[frame1[i,0], frame2[j,0], frame1[i,1], frame2[j,1]] += 1
  
@cython.boundscheck(False)
@cython.wraparound(False)
def coinc2d(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2, 
            signs, shape):
    '''
    Generete coincidences between two frames in sum/difference variables
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*f2l, 2], dtype=DTYPE)
    cdef int i = 0
    cdef int j = 0
    cdef int shift1 = 0
    cdef int shift2 = 0
    cdef int sign0 = signs[0]
    cdef int sign1 = signs[1]
    if signs[0] == -1:
        shift1 = shape[0]
    if signs[1] == -1:
        shift2 = shape[1]
    for i in range(f1l):
        for j in range(f2l):
            cframe[i+f1l*j,0] =  frame1[i,0] + sign0*frame2[j,0] + shift1
            cframe[i+f1l*j,1] =  frame1[i,1] + sign1*frame2[j,1] + shift2
    return cframe
          
@cython.boundscheck(False)
@cython.wraparound(False)  
def bincoinc2d(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
             np.ndarray[DTYPE_t, ndim=2] hist, signs, shape):
    '''
    Bin coincidences in sum/difference variables, adding them to hist
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef int i = 0
    cdef int j = 0
    cdef int shift1 = 0
    cdef int shift2 = 0
    cdef int sign0 = signs[0]
    cdef int sign1 = signs[1]
    if sign0 == -1:
        shift1 = shape[0]
    if sign1 == -1:
        shift2 = shape[1]
    for i in range(f1l):
        for j in range(f2l):
            hist[frame1[i,0] + sign0*frame2[j,0] + shift1, frame1[i,1] + sign1*frame2[j,1] + shift2] += 1
            
@cython.boundscheck(False)
@cython.wraparound(False)
def autocoinc(np.ndarray[DTYPE_t, ndim=2] frame):
    '''
    Generate autocoincidences inside a single frame
    
    '''
    cdef int f1l = frame.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*(f1l-1), 4], dtype=DTYPE)
    cdef int i = 0
    cdef int j = 0
    cdef int k = 0
    for i in range(f1l):
        for j in range(f1l):
            if i != j:
                cframe[i+f1l*k,0] =  frame1[i,0]
                cframe[i+f1l*k,1] =  frame1[k,0]
                cframe[i+f1l*k,2] =  frame1[i,1]
                cframe[i+f1l*k,3] =  frame1[k,1]
                k += 1
    return cframe