import numpy as np
from scipy.signal import convolve2d
from bincountnd import bincountnd
from message import message, progress
from collections import deque

class accum:
    '''
    histogram generation from frameseries
    
    '''
    
    @staticmethod
    def accumframes(fs):
        '''
        Accumulate photon through all frames. 
        Wrapper for :func:`photonpacket.frameseries.accumframes`
        
        Parameters
        ----------
        fs : :class:`photonpacket.frameseries`
                Series of photon frames
                
        Returns
        ---------
        accum : :class:`numpy.ndarray`
            photon counts histogram
        
        '''
        return fs.accumframes()

    @staticmethod
    def accumcoinc(fs1, fs2, method='bincount'):
        '''
        Accumulate coincidences
        
        Parameters
        ----------
        fs1 : :class:`photonpacket.frameseries`
                Series of photon frames
                
        fs2 : :class:`photonpacket.frameseries`
                Series of photon frames
                
        signs : tuple of two booleans
                Signs
                
        method : bincount or accum
                Method
                
        Returns
        ----------
        coinchist : :class:`numpy.ndarray`
        
        See Also
        ----------
        
        Notes
        ----------
        
        Examples
        ----------
        '''
        if method == 'bincount':
            i = 0
            cframes = deque([])
            for frame in fs1.frames:
                progress(i)
                frame2 = fs2.frames[i]
                if len(frame2) != 0 and len(frame) != 0:
                    cframe = np.hstack((
                            np.dstack(np.meshgrid(frame[:, 0], frame2[:, 0])).reshape(-1, 2),
                            np.dstack(np.meshgrid(frame[:, 1], frame2[:, 1])).reshape(-1, 2)
                            ))
                    cframes.append(np.array(cframe, dtype=np.uint32))
                i += 1
            accum = bincountnd(np.concatenate(cframes),(fs1.shape[0],fs2.shape[0],fs1.shape[1],fs2.shape[1]))           
            return accum
        
        elif method == 'accum':
            i = 0
            accum=np.zeros(shape=(fs1.shape[0],fs1.shape[0],
                                  fs1.shape[1],fs1.shape[1]))
            for frame in fs1.frames:
                frame2 = fs2.frames[i]
                if len(frame2) != 0 and len(frame) != 0:
                    cframe=np.hstack((
                            np.dstack(np.meshgrid(frame[:,0], frame2[:,0])).reshape(-1, 2),
                            np.dstack(np.meshgrid(frame[:,1], frame2[:,1])).reshape(-1, 2)
                            ))
                    for coinc in cframe:
                        accum[coinc[0],coinc[1],coinc[2],coinc[3]]=accum[coinc[0],
                              coinc[1],coinc[2],coinc[3]]+1
                i += 1
            return accum
        else:
            print 'invalid method'
            
    @staticmethod
    def accumcoincinplace(fs,r1,r2):
        '''
        Accumulate coincidences with simultaneous region selection
        
        Parameters
        ----------
        fs1 : :class:`photonpacket.frameseries`
            
        fs2 : :class:`photonpacket.frameseries`
            
        signs : 
            
        Returns
        ----------
        
        See Also
        ----------
        
        Notes
        ----------
        
        Examples
        ----------
        '''
        i = 0
        cframes = []
        for frame in fs.frames:
            progress(i)
            aux_frame = np.array(frame)
            aux_frame2 = np.array(frame)
            mframe = r1.reshape(np.array(aux_frame[r1.getmask(aux_frame2)]))
            aux_frame = np.array(frame)
            aux_frame2 = np.array(frame)
            mframe2 = r2.reshape(np.array(aux_frame[r2.getmask(aux_frame2)]))
            if len(frame) != 0:
                cframe=np.hstack((
                        np.dstack(np.meshgrid(mframe[:,0], mframe2[:,0])).reshape(-1, 2),
                        np.dstack(np.meshgrid(mframe[:,1], mframe2[:,1])).reshape(-1, 2)
                        ))
                cframes.append(np.array(cframe, dtype=np.uint32))
            i += 1
        accum = bincountnd(np.concatenate(cframes),(r1.shape[0],r2.shape[0],r1.shape[1],r2.shape[1])) 
        return accum
  
    @staticmethod
    def coinchist(fs1,fs2,signs):
        '''
        Obtain coincidence histogram
        
        Parameters
        ----------
        fs1 : :class:`photonpacket.frameseries`
            
        fs2 : :class:`photonpacket.frameseries`
            
        signs : 
            
        Returns
        ----------
        
        See Also
        ----------
        
        Notes
        ----------
        
        Examples
        ----------
        '''
        message('Generating coincidences', 1)
        i = 0
        cframes = []
        for frame in fs1.frames:
            progress(i)
            frame2 = fs2.frames[i]
            if len(frame2) != 0 and len(frame) != 0:
                #cframe = np.hstack((
                #        np.dstack(np.meshgrid(frame[:,0], frame2[:,0])).reshape(-1, 2),
                #        np.dstack(np.meshgrid(frame[:,1], frame2[:,1])).reshape(-1, 2)
                #        ))
                cfx=np.meshgrid(frame[:,0],frame2[:,0])
                cfy=np.meshgrid(frame[:,1],frame2[:,1])
                cframe2 = np.zeros(shape=(len(cfx[0].flatten()),2),dtype=np.uint16)
                if signs[0]:
                    cframe2[:,0] = cfx[0].flatten() + cfx[1].flatten()
                else:
                        cframe2[:,0] = cfx[0].flatten() - cfx[1].flatten() + fs2.shape[0]
                if signs[1]:
                        cframe2[:,1] = cfy[0].flatten() + cfy[1].flatten()
                else:
                        cframe2[:,1] = cfy[0].flatten() - cfy[1].flatten() + fs2.shape[1]
                cframes.append(np.array(cframe2, dtype=np.uint32))
            i += 1
        message("\nCounting coincidences", 1)
        accum = bincountnd(np.concatenate(cframes),(fs1.shape[0]+fs2.shape[0]-1,fs1.shape[1]+fs2.shape[1]-1))
        return accum
    
    @staticmethod
    def acchist(h1,h2,signs,**kwargs):
        '''
        Obtain accidential coincidences histogram
        
        Parameters
        ----------
        h1 : :class:`numpy.ndarray`
            first photon counts histogram
            
        h2 : :class:`numpy.ndarray`
            second photon counts histogram
            
        signs : tuple of booleans
            
        Nframes : int
            number of frames
            
        Returns
        ----------
        
        See Also
        ----------
        
        Notes
        ----------
        
        Examples
        ----------
        '''
        if 'Nframes' in kwargs:
            div = float(kwargs['Nframes'])
        else:
            div = 1.0
        if not signs[0]:
              h2=np.flip(h2,axis=0)
        if not signs[1]:
              h2=np.flip(h2,axis=1)
        return convolve2d(h1,h2)/div
    
