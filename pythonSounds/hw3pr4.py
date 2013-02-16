#
# hw3pr4.py - extra credit problem "Sounds Good!"
#
# Name:
#
#

import csaudio
from csaudio import *
import math


# a function to make sure everything is working
def test():
    """ a test function that plays swfaith.wav
        You'll need swfailt.wav in this folder.
    """
    play( 'swfaith.wav' )

# hw3pr4.py

import csaudio ; reload(csaudio) ; from csaudio import *
   
# The example changeSpeed function
def changeSpeed(filename, newSR, newFile = "out.wav"):
    """ changeSpeed takes in
          filename, a string indicating the sound you wish to use.
          newSR, an integer representing the new sample rate you want,
                 in units of samples per second.
          newFile, an OPTIONAL string indicating the name to which
                 you wish to save the speed-changed sound.
                 If you don't specify a second input to changeSpeed,
                 the new sound will be saved as "out.wav"

        changeSpeed creates a new file (using the name in newFile)
          that uses the same sound data, but runs it at the
          samplerate of newSR samples per second.
          It plays the new sound and then does not return anything...
    """
    # This next function call returns TWO values:
    #   samples is a LIST of the raw sound data
    #   oldSR is the old sample rate, in samples per second
    #
    # This will be the standard way to get sound data from a file.
    samples, oldSR = read_wav(filename) 

    # This next function call does not return any value, but
    #   it does write the sound data in the list "samples" into
    #   a file whose name is the string in the newFile variable
    #   It uses the new sample rate instead of the old.
    write_wav(samples, newSR, newFile)

    # This next call to play also does not return a value,
    #   but it plays the sound in the file named newFile.
    play(newFile)

    # Now, we return the list of the sound data - it won't always
    #   be needed, we return it just in case it is.
    # actually, let's comment this out for now...
    return samples


# The example flipflop function
def flipflop(filename, newFile = "out.wav"):
    """ flipflop takes in
          filename, a string indicating the sound you wish to use.
          newFile, an OPTIONAL string indicating the name to which
                 you wish to save the flip-flopped sound.
                 If you don't specify a second input to flipflop,
                 the new sound will be saved as "out.wav"

        flipflop creates a new file (using the name in newFile)
          that uses the same sound data, but with the first and second
          halves of the sound interchanged.

        flipflop plays the new sound that it creates (no return value)
    """
    samples, SR = read_wav(filename)

    L = len(samples)
    newsamples = samples[L/2:] + samples[:L/2] # flip flop

    write_wav(newsamples, SR, newFile)

    play(newFile)      # play the new sound for good measure

    #return newsamples  # return the new sound data list - commented for now

def reverse(filename, newFile = "out.wav"):
    samples, SR = read_wav(filename)
    newsamples = [samples[-i] for i in range(len(samples))[1:]] + [samples[0]]
    write_wav(newsamples, SR, newFile)
    play(newFile)

def volume(filename, percent, newFile = "out.wav"):
    samples, SR = read_wav(filename)
    newsamples = [sample * percent for sample in samples]
    write_wav(newsamples, SR, newFile)
    play(newFile)

def oneFreq(freq, newFile = "out.wav"):
    A = 32767.0
    TP = 2*math.pi
    SR = 22050
    samples = [ A*math.cos(freq*x*TP/SR) for x in range(SR) ]
    write_wav(samples, SR, newFile)
    play(newFile)
    return samples
        
    
