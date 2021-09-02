import numpy as np

import logging
logger = logging.getLogger(__name__)

import dedalus.public as de

L_dealias = N_dealias = dealias = 3/2
Lmax=14
Nmax=15
radius=1
mesh = None

if Lmax % 2 == 1:
    nm = 2*(Lmax+1)
else:
    nm = 2*(Lmax+2)

c = de.SphericalCoordinates('phi', 'theta', 'r')
d = de.Distributor((c,), mesh=mesh, dtype=np.float64)
b = de.BallBasis(c, (nm,Lmax+1,Nmax+1), radius=radius, dealias=(L_dealias,L_dealias,N_dealias))
phi1, theta1, r1 = b.local_grids((1,1,1))
phi, theta, r = b.local_grids((L_dealias,L_dealias,N_dealias))

ez = de.Field(dist=d, bases=(b,), tensorsig=(c,))
ez.set_scales(b.dealias)
logger.info('ping.')
ez['g'][1] = -np.sin(theta)
ez['g'][2] =  np.cos(theta)
logger.info('ping..')
ez_g = de.Grid(ez).evaluate()
logger.info('ping...')
