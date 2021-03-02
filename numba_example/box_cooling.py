#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anaytical model for a conductively cooling cuboid with constant Ts.

Created on Mon Feb 22 18:23:25 2021
Modified by Andrew, March 2nd.

@author: maeve
"""

import numpy as np

def theta(iteration, x, X, t, diffusivity):
    """Analytical solution returns dimensionless theta."""
    f = 0
    for n in range(0, iteration):

        f += ((((-1)**n)/((2*n) + 1)) *
              np.cos((((2*n) + 1)*np.pi*x)/(2*X)) *
              np.exp(-1*diffusivity*t*(((2*n) + 1)**2)/(4*(X**2))))

    f = f*(4/np.pi)

    return f


def box_temperature(t, x, y, z, alpha, X, Y, Z, Tinit, Text, iterations=1000):
    """Return the box temperature"""
    theta_x = theta(iterations, x, X, t, alpha)
    theta_y = theta(iterations, y, Y, t, alpha)
    theta_z = theta(iterations, z, Z, t, alpha)
    theta_xyz = theta_x * theta_y * theta_z
    temperature = Text + ((Tinit - Text) * theta_xyz)
    return temperature

