import numpy as np
from dedalus.core import coords, distributor, basis, field, operators, arithmetic, problems, solvers
from dedalus.tools.cache import CachedFunction
from dedalus.core.basis import BallBasis, ShellBasis
import dedalus.public as de

Nphi = 32
Ntheta = 16
Nr = 16
k = 0
dealias = 3/2
radius_ball = 1
dtype = np.float64


c = de.SphericalCoordinates('phi', 'theta', 'r')
d = de.Distributor((c,))
b = de.BallBasis(c, (Nphi, Ntheta, Nr), radius=radius_ball, k=k, dealias=(dealias, dealias, dealias), dtype=dtype)
phi, theta, r = b.local_grids(b.domain.dealias)
avg = lambda A: de.Integrate(A, c)/(4*np.pi/3)

f = field.Field(dist=d, bases=(b,), dtype=dtype)
f.set_scales(b.domain.dealias)

f['g'] = 0.5*(1-r**(2))

h = avg(f).evaluate()

hg = 0.5*(radius_ball**3-radius_ball**5*3/5)
print("computed value: {}, expected value: {}".format(h['g'][0][0][0],hg))

f['g'] = 0.5*(1)

h = avg(f).evaluate()

hg = 0.5*(radius_ball**3)

print("computed value: {}, expected value: {}".format(h['g'][0][0][0],hg))
