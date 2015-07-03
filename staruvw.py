#!/usr/bin/python

"""
David Rodriguez
Apr 28, 2013
Read in VOTable and compute UVW
"""

from math import cos, sin
from astropy.io.votable import parse
from astropy import coordinates as coord
from astropy import units as u
import sys
from pylab import double

# ==============
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
	sind = sin(dec * radcon )
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


# Function to XYZ given RA, Dec, and Distance
def xyz(ra,dec,d):

   c = coord.ICRSCoordinates(ra=ra, dec=dec, unit=(u.degree, u.degree))
   w = c.transform_to(coord.GalacticCoordinates)
   l,b = w.l.radians,w.b.radians

   xgc = d * cos(b) * cos(l)
   ygc = d * cos(b) * sin(l)
   zgc = d * sin(b)
   # See http://www.astro.virginia.edu/class/majewski/astr551/lectures/COORDS/coords.html

   # left-handed? (wrong?)
   #xgc = -1*xgc

   return xgc,ygc,zgc


if len(sys.argv)==1:
	print """
	staruvw.py runs the UVW coordinates for a list of stars
	
	Usage: staruvw.py INFILE [OUTFILE RUNTYPE]
	INFILE: Name of VOTable containing RA, Dec, Dist, PM, RV
	OUTFILE: Output text file name (Default: uvw_table.txt)
	"""
	sys.exit()



file = sys.argv[1]

if len(sys.argv)>2:
        outfile = sys.argv[2]
else:
        outfile = 'uvw_table.txt'


votable = parse(file)
t = votable.get_first_table()

ra = t.array['ra']
dec = t.array['dec']
name = t.array['designation']
#name = t.array['Name']

#d = t.array['Dist']
#pmra = t.array['pmra']
#pmde = t.array['pmde']
#rv = t.array['RV']

d = t.array['D_bP']
pmra = t.array['pmra']
pmde = t.array['pmde']
rv = t.array['RV']

num = len(ra)

# Make some output
f = open(outfile, 'w')
tout = '#Index\tName\tRA\tDec\tD\t'
tout += 'U\tV\tW\n'
f.write(tout)

# Calculate for all
for i in range(len(ra)):

	print ra[i], dec[i], d[i]
	#x,y,z = xyz(double(ra[i]), double(dec[i]), double(d[i]))
	#print x,y,z
	u,v,w = uvw(double(ra[i]), double(dec[i]), double(d[i]),pmra[i],pmde[i],rv[i])

	na = name[i]
	na = na.replace(' ','_')

	tout = '%2d\t"%s"\t%3.10f\t%3.10f\t%3.2f\t' % ((i+1), na, ra[i], dec[i], double(d[i]))
	tout += '%3.2f\t%3.2f\t%3.2f\n' % (u,v,w)
	#tout += '%3.2f\t%3.2f\t%3.2f\n' % (x,y,z)

	print tout

	f.write(tout)

f.close()

