import numpy as np

import logging
logger = logging.getLogger(__name__)

import dedalus.public as de

L_dealias = N_dealias = dealias =  3/2
Nθ=4
Nφ=2*Nθ
Nr=4
radius=1
mesh = None

for dtype in [np.float64, np.complex128]:
    c = de.SphericalCoordinates('phi', 'theta', 'r')
    d = de.Distributor((c,), mesh=mesh, dtype=dtype)

    b_ball = de.BallBasis(c, shape=(Nφ,Nθ,Nr), radius=radius, dealias=(L_dealias,L_dealias,N_dealias), dtype=dtype)
    b_shell = de.ShellBasis(c, shape=(Nφ,Nθ,Nr), radii=(0.5,radius), dealias=(L_dealias,L_dealias,N_dealias), dtype=dtype)

    for b in [b_ball, b_shell]:
        phi, theta, r = b.local_grids((L_dealias,L_dealias,N_dealias))

        azavg = lambda A: de.Average(A, c.coords[0])

        f_m0 = de.Field(dist=d, bases=(b,), name='f_m0')
        f_m0.require_scales(dealias)
        f_m0['g'] = r*np.sin(theta)*(1-r*np.sin(theta))
        f_m01 = de.Field(dist=d, bases=(b,), name='f_m01')
        f_m01.require_scales(dealias)
        f_m01['g'] = f_m0['g']*(1+np.cos(phi))
        for f in [f_m0, f_m01]:
            avg_test = azavg(f).evaluate()
            logger.info("azavg({})=\n{}".format(f, avg_test['g']))
            logger.info("|{}-azavg({})|_max={}".format(f,f,np.max(np.abs(f['g']-avg_test['g']))))
            logger.info("{}.shape {}, azavg({}).shape {}".format(f, f['g'].shape, f, avg_test['g'].shape))
            logger.info(b)
