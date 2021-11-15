import numpy as np
import dedalus.public as d3
import logging
logger = logging.getLogger(__name__)

# Parameters
Lx, Lz = 4, 1
Nz = 32
Nx = 64
dealias = 3/2
dtype = np.float64

# Bases
coords = d3.CartesianCoordinates('x', 'z')
dist = d3.Distributor(coords, dtype=dtype)
xbasis = d3.RealFourier(coords['x'], size=Nx, bounds=(0, Lx), dealias=dealias)
zbasis = d3.ChebyshevT(coords['z'], size=Nz, bounds=(0, Lz), dealias=dealias)
x = xbasis.local_grid(1)
z = zbasis.local_grid(1)

# Fields

#avg = lambda A: d3.Integrate(A, coords)/(Lx*Lz)
avg = lambda A: d3.Integrate(d3.Integrate(A, coords.coords[0]), coords.coords[1])/(Lx*Lz)
#avg = lambda A: d3.Integrate(A, coords['x'])/(Lx*Lz)
one = dist.Field(name='one', bases=(xbasis,zbasis))
one['g'] = 1
print(avg(one).evaluate()['g'])
