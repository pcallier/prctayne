#!/usr/bin/env python

import subprocess
from subprocess import PIPE, Popen
import logging
from scipy.io.wavfile import write
from numpy import linspace,sin,pi,int16,concatenate
import numpy as np

def sinosc(freq, dur, amp=1, rate=44100):
    # empty wav
    t = linspace(0,dur,dur*rate)
    # single sine
    data = sin(2*pi*freq*t)*amp
    return data.astype(int16) # (signed) two byte integers

def limiter(sig, limit):
    """ Basic static limiter. Scales sig by ratio
    of max(sig) to limit only if max(sig) > limit
    """
    limit = float(limit)
    sig_dtype = sig.dtype
    sig_max = np.max(sig)
    if sig_max > limit:
        return (sig * (limit / sig_max)).astype(sig_dtype)
    else:
        return sig

def n_random_sines(n, lo, hi, dur=1.0):
    """ Uniformly choose n random freqs from the log space
    between lo and hi and make sounds with them."""

    log_lo = np.log(lo)
    log_hi = np.log(hi)
    log_freqs = np.random.uniform(log_lo, log_hi, n)
    freqs = np.exp(log_freqs)
    level = (2 ** 16) / 2       # max of 2-byte signed int
    level_individual = level / n

    waves = [ sinosc(freq, dur, amp=level_individual) for
            freq in freqs ]
    wave = np.sum(waves, axis=0, dtype=np.int16)
    logger = logging.getLogger(__name__)
    logger.debug('Freqs: {0}; format: {1}'.format(freqs, wave.dtype))
    return wave
        
def play_wav(wav):
    return subprocess.call(['aplay', wav], stdout=PIPE, stderr=PIPE)

if __name__=="__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    np.random.seed()

    tone = sinosc(440,2,amp=10000)
    tone2 = sinosc(660, 2, amp=10000)

    tone_cat = concatenate((tone, tone2), axis=0)
    write('2-tone.wav',44100,tone_cat)

    tone_stack = limiter(tone + tone2, 10000)
    write('stack-tone.wav',44100,tone_stack)
    write('stack-tone-loud.wav',44100,tone+tone2)

    # generate 3 random waves
    three_waves = n_random_sines(3, 220, 660)
    write('3-waves.wav', 44100, three_waves)
    
    # generate random no of waves
    n_waves = n_random_sines(np.random.randint(2,8),150,1000)
    write('n-waves.wav', 44100, n_waves)
    
    play_wav('3-waves.wav')
    play_wav('n-waves.wav')

