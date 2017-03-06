# -*- coding: utf-8 -*-
import numpy as np

def bincountnd(array, shape):
    '''
    Multidimensional version of numpy function bincount
    works only for uint16
    '''
    if len(shape)==2:
        return bincount2d(array,shape)
    aux_shape = np.sort(shape)[::-1]
    sel = np.argsort(shape)[::-1]
    flat_array = np.zeros(shape=array.shape[0],dtype=np.uint16)
    exp = 1
    array = array[:,sel]
    for dim, size in enumerate(aux_shape):
        flat_array = flat_array + array[:,dim] * exp
        exp = exp * size
    accum = np.bincount(flat_array, minlength = np.prod(aux_shape))
    return np.reshape(accum,shape)
    
def bincount2d(array, shape):
    xe = np.arange(0,shape[0]+1)
    ye = np.arange(0,shape[1]+1)
    H,X,Y=np.histogram2d(array[:,0],array[:,1],bins=[xe,ye])
    return H