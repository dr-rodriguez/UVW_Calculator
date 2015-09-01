#!/usr/bin/python

"""
David Rodriguez
June 16, 2015
Translation of my uvw_errs.pro routing from IDL
"""

import sys
from pylab import mean, std #double
from random import seed, gauss
from druvw import uvw # import my UVW package

# ============================================

if len(sys.argv)<6:
	print """
	requires numbers: ra,dec,pmra,pmde,dist,rv, [pmra_err, pmde_err, rverr, derr]
	"""
	sys.exit()

ra 		= float(sys.argv[1])
dec 	= float(sys.argv[2])
pmra0 	= float(sys.argv[3])
pmdec0 	= float(sys.argv[4])
dist0 	= float(sys.argv[5])
rv0 	= float(sys.argv[6])

if len(sys.argv)>7:
    pmra_err = float(sys.argv[7])
    pmde_err = float(sys.argv[8])
else:
    pmra_err = 0.0
    pmde_err = 0.0

if len(sys.argv)>9:
    rverr = float(sys.argv[9])
else:
    rverr = 0.0

if len(sys.argv)>10:
    derr = float(sys.argv[10])
else:
    derr = 0.0

# Initialize the arrays
seed() # random seed 
num = 4000
u = []
v = []
w = []

# Compute UVW using the error terms
for i in range(num):
	if rverr>0: 
		rv = gauss(rv0,rverr) 
	else: 
		rv = rv0

	if pmra_err>0: 
		pmra = gauss(pmra0,pmra_err) 
	else: 
		pmra = pmra0

	if pmde_err>0: 
		pmdec = gauss(pmdec0,pmde_err) 
	else: 
		pmdec = pmdec0

	if derr>0: 
		dist = gauss(dist0,derr) 
	else: 
		dist = dist0

	u0,v0,w0 = uvw(ra,dec,dist,pmra,pmdec,rv)
	u.append(u0)
	v.append(v0)
	w.append(w0)


# Compute mean and standard deviation for UVW
u_val = mean(u)
v_val = mean(v)
w_val = mean(w)
u_err = std(u)
v_err = std(v)
w_err = std(w)

print
print 'U: %3.2f +/- %1.2f' % (u_val, u_err)
print 'V: %3.2f +/- %1.2f' % (v_val, v_err)
print 'W: %3.2f +/- %1.2f' % (w_val, w_err)

