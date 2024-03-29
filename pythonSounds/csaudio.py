# csaudio.py

# import csaudio ; reload(csaudio) ; from csaudio import *

import wave

def get_data(filename):
    """ the file needs to be in .wav format
        there are lots of conversion programs online, however,
        to create .wav from .mp3 and other formats
    """
    # this will complain if the file isn't there!
    fin = wave.open(filename, 'rb')
    params = fin.getparams()
    #printParams(params)
    rawFrames = fin.readframes(params[3])
    # need to extract just one channel of sound data at the right width...
    fin.close()
    return params, rawFrames
    
    
def printParams(params):
    print 'Parameters:'
    print '  nchannels:', params[0]
    print '  sampwidth:', params[1]
    print '  framerate:', params[2]
    print '  nframes  :', params[3]
    print '  comptype :', params[4]
    print '  compname :', params[5]
    
    
def tr(params,rf):
    """ tr transforms raw frames to floating-point samples """
    
    samps = [ord(x) for x in rf]    # convert to numeric bytes
    
    # give parameters nicer names
    nchannels = params[0]
    sampwidth = params[1]
    nsamples  = params[3]
    
    if sampwidth == 1:

        for i in range(nsamples):
            if samps[i] < 128:
                samps[i] *= 256.0       # Convert to 16-bit range, floating
            else:
                samps[i] = (samps[i] - 256) * 256.0

    elif sampwidth == 2:

        newsamps = nsamples * nchannels * [0]

        for i in range(nsamples * nchannels):
            # The wav package gives us the data in native
            # "endian-ness".  The clever indexing with wave.big_endian
            # makes sure we unpack in the proper byte order.
            sampval = samps[2*i + 1 - wave.big_endian] * 256 \
              + samps[2*i + wave.big_endian]
            if sampval >= 32768:
                sampval -= 65536
            newsamps[i] = float(sampval)

        samps = newsamps

    else:
        print 'A sample width of', params[1], 'is not supported.'
        print 'Returning silence.'
        samps = nsamples * [0.0]
        
    if nchannels == 2:
        # Mix to mono
        newsamps = nsamples * [0]
        for i in range(nsamples):
            newsamps[i] = (samps[2 * i] + samps[2 * i + 1]) / 2.0
        samps = newsamps

    return samps
    
    
    
def tri(params,samps):
    """ tri is tr inverse, i.e. from samples to rawframes """
    
    if params[1] == 1:                 # one byte per sample
        samps = [int(x+127.5) for x in samps]
        #print 'max, min are', max(samps), min(samps)
        rf = [chr(x) for x in samps]
        
    elif params[1] == 2:               # two bytes per sample
        bytesamps = (2*params[3])*[0]  # start at all zeros
        for i in range(params[3]):
            # maybe another rounding strategy in the future?
            intval = int(samps[i])
            if intval >  32767: intval = 32767
            if intval < -32767: intval = -32767  # maybe could be -32768
            
            if intval < 0: intval += 65536 # Handle negative values

            # The wav package wants its data in native "endian-ness".
            # The clever indexing with wave.big_endian makes sure we
            # pack in the proper byte order.
            bytesamps[2*i + 1 - wave.big_endian] = intval / 256
            bytesamps[2*i + wave.big_endian] = intval % 256
                
        samps = bytesamps
        #print 'max, min are', max(samps), min(samps)
        rf = [chr(x) for x in samps]
        
    return ''.join(rf)
    

    
def read_wav(filename):
    """ get_wav returns the audio data in the format
    
            [ [d0, d1, d2, ...], samplingrate ]
            
        where each d0, d1, d2, ... is a floating-point value
        and sampling rate is an integer, representing the
        frequency with which audio samples were taken
    """
    params, rf = get_data(filename)
    samps = tr(params,rf)
    
    numchannels = params[0]
    datawidth = params[1]
    framerate = params[2]
    numsamples = params[3]
    
    print
    print 'You opened', filename, 'which has'
    print '   ', numsamples, 'audio samples, taken at'
    print '   ', framerate, 'hertz (samples per second).'
    print
    
    return [samps, framerate]


def write_data(params=None, rawFrames=None, filename="out.wav"):
    """ back out to .wav format """

    fout = wave.open(filename,'wb')
    if params:
        fout.setparams(params)
        if rawFrames:
            fout.writeframes(rawFrames)
        else:
            print 'no frames'
    else:
        print 'no params'
    
    fout.close()
    
    
    
def write_wav(data, samplingrate, filename="out.wav"):
    """ write_wav outputs a .wav file whose
            first parameter is the audio data as a list
            
            second parameter is the integer sampling rate
                the minimum allowed value is 1 hertz (1 sample per second),
                which is well under human hearing range
                
            third parameter is the output file name
                if no name is specified, this parameter defaults to 'out.wav'
    """
    framerate = int(samplingrate)
    if framerate < 0:
        framerate = -framerate
    if framerate < 1:
        framerate = 1
        
    # always 1 channel and 2 output bytes per sample
    params = [1, 2, framerate, len(data), "NONE", "No compression"]
    
    # convert to raw frames
    rawframesstring = tri(params,data)
    write_data(params, rawframesstring, filename)
    
    print
    print 'You have written the file', filename, 'which has'
    print '   ', len(data), 'audio samples, taken at'
    print '   ', samplingrate, 'hertz.'
    print
    
    
# a useful thing to have... can be done all in sw under windows...
import os

if os.name == 'nt':
    import winsound
elif os.uname()[0] == 'Linux':
    import ossaudiodev

def play(filename):
    """ play a .wav file for Windows, Linux, or Mac 
        for Mac, you need to have the "play"
        application in the current folder (.)
    """
    if type(filename) != type(''):
        raise TypeError, 'filename must be a string'
    if os.name == 'nt':
        winsound.PlaySound(filename, winsound.SND_FILENAME)
    elif os.uname()[0] == 'Linux':
        (params, frames) = get_data(filename)
    	oss = ossaudiodev.open('w')
        if wave.big_endian:
            if params[1] == 1:
                oss.setfmt(ossaudiodev.AFMT_S8_BE)
            else:
                oss.setfmt(ossaudiodev.AFMT_S16_BE)
        else:
            if params[1] == 1:
                oss.setfmt(ossaudiodev.AFMT_S8_LE)
            else:
                oss.setfmt(ossaudiodev.AFMT_S16_LE)
        oss.channels(params[0])
        oss.speed(params[2])
        oss.writeall(frames)
        oss.close()
    # assume MAC, if not a Windows or Linux machine
    # if you're using another OS, you'll need to adjust this...
    else:
        os.system( ('./play ' + filename) )  
        

        
        
   
# The example changeSpeed function
def changeSpeed(filename):
    """prompts the user to change the audio file's speed"""
    [samps, fr] = read_wav(filename) # get data
    newfr = input('What new frequency? ') #prompt
    write_wav( samps, newfr ) # write data to out.wav
    play( 'out.wav' )   # play the new file...
    
    

# The example reverse function
import time
def reverse(filename):
    """ plays and reverse-plays a file """
    play(filename)
    [samps, fr] = read_wav(filename)
    time.sleep(1)
    newsamps = samps[::-1]
    newfr = fr
    write_wav( newsamps, newfr ) # out.wav
    play( 'out.wav' )
