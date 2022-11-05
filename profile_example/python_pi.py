import random
import numpy as np


def pi_python(num_samps, prn_seed=101):
    """
    Monte Carlo method of calculating pi
  
    num_samps is the number of samples in the unit square
    to probe.
  
    """
    random.seed(prn_seed)
    pi = 0
    n = 0
    for n in range(num_samps):
        x = random.random() 
        y = random.random()
        r = x**2 + y**2
        if r <= 1.0:
            pi += 1
    # The area calculation ... broken up so we see things in the profile
    pi = 4.0 * float(pi)
    pi = pi / float(n)
    return pi

def pi_numpy(num_samps, prn_seed=101):
    """
    Monte Carlo method of calculating pi
  
    num_samps is the number of samples in the unit square
    to probe.
  
    """
    np.random.seed(prn_seed)
    pi = 0
    n = 0
    x = np.random.rand(num_samps)
    y = np.random.rand(num_samps)
    r = x**2 + y**2
    boolarr = r<=1.0
    pi = len(r[boolarr])
    # The area calculation ... broken up so we see things in the profile
    pi = 4.0 * float(pi)
    pi = pi / float(num_samps)
    return pi