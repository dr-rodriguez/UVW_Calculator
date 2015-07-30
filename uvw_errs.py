#!/usr/bin/python

"""
David Rodriguez
June 16, 2015
Translation of my uvw_errs.pro routing from IDL
"""

from math import cos, sin
#from pylab import double
from random import seed, gauss

# ============================================
# Function to calculate UVW given RA, Dec, Distance, RV, and PMs
def uvw(ra,dec,d,pmra,pmde,rv):
	k = 4.74047 #Equivalent of 1 A.U/yr in km/s  
	A00 = 0.0548755604
	A01 = 0.8734370902
	A02 = 0.4838350155
	A10 = 0.4941094279
	A11 = -0.4448296300
	A12 = 0.7469822445
	A20 = -0.8676661490
	A21 = -0.1980763734
	A22 = 0.4559837762

	radcon = 3.1415926/180
	cosd = cos(dec * radcon)
	sind = sin(dec * radcon)
	cosa = cos(ra * radcon)
	sina = sin(ra * radcon)

	vec1 = rv
	plx = 1000./d
	vec2=k*pmra/plx
	vec3=k*pmde/plx

	u = ( A00*cosa*cosd+A01*sina*cosd+A02*sind)*vec1+(-A00*sina +A01*cosa)*vec2+(-A00*cosa*sind-A01*sina*sind+A02*cosd)*vec3
	v = ( A10*cosa*cosd+A11*sina*cosd+A12*sind)*vec1+(-A10*sina+A11*cosa)*vec2+(-A10*cosa*sind-A11*sina*sind+A12*cosd)*vec3
	w = ( A20*cosa*cosd+A21*sina*cosd+A22*sind)*vec1+(-A20*sina+A21*cosa)*vec2+(-A20*cosa*sind-A21*sina*sind+A22*cosd)*vec3
	u = -u

	return u,v,w

# ============================================

if len(sys.argv)<6:
	print """
	requires numbers: ra,dec,pmra,pmde,dist,rv, [pmra_err, pmde_err, rverr, derr]
	"""
	sys.exit()

ra 		= sys.argv[1]
dec 	= sys.argv[2]
pmra0 	= sys.argv[3]
pmdec0 	= sys.argv[4]
dist0 	= sys.argv[5]
rv0 	= sys.argv[6]

if len(sys.argv)>7:
        pmra_err = sys.argv[7]
        pmde_err = sys.argv[8]
else:
        pmra_err = 0.0
        pmde_err = 0.0

if len(sys.argv)>9:
        rverr = sys.argv[9]
else:
        rverr = 0.0

if len(sys.argv)>10:
        derr = sys.argv[10]
else:
        derr = 0.0

# Initialize the arrays
seed() # random seed 
num = 4000
#rv    = []
#dist  = []
#pmra  = []
#pmdec = []
u = []
v = []
w = []

# Compute UVW using the error terms
for i in range(num):
	if rverr>0: rv = gauss(rv0,rverr) else rv = rv0
	if pmra_err>0: pmra = gauss(pmra0,pmra_err) else pmra = pmra0
	if pmde_err>0: pmdec = gauss(pmdec0,pmde_err) else pmdec = pmdec0
	if derr>0: dist = guass(dist0,derr) else dist = dist0

	u0,v0,w0 = uvw(ra,dec,dist,pmra,pmde,rv)
	u.append(u0)
	v.append(v0)
	w.append(w0)

# Compute mean and standard deviation for UVW

