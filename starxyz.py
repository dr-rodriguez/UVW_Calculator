#!/usr/bin/python

"""
David Rodriguez
Mar 10, 2013
Read in VOTable and 
"""

from math import cos, sin
from astropy.io.votable import parse
from astropy import coordinates as coord
from astropy import units as u
import sys
from pylab import double

# ==============
# Function to XYZ given RA, Dec, and Distance
def xyz(ra,dec,d):

   c = coord.ICRSCoordinates(ra=ra, dec=dec, unit=(u.degree, u.degree))
   w = c.transform_to(coord.GalacticCoordinates)
   l,b = w.l.radians,w.b.radians

   xgc = d * cos(b) * cos(l)
   ygc = d * cos(b) * sin(l)
   zgc = d * sin(b)
   # See http://www.astro.virginia.edu/class/majewski/astr551/lectures/COORDS/coords.html

   # If positive towards anticenter
   #xgc = -1*xgc

   return xgc,ygc,zgc


if len(sys.argv)==1:
	print """
	starxyz.py runs the XYZ coordinates for a list of stars
	
	Usage: starxyz.py INFILE [OUTFILE RUNTYPE]
	INFILE: Name of VOTable containing RA, Dec, Dist
	OUTFILE: Output text file name (Default: xyz_table.txt)
	"""
	sys.exit()



file = sys.argv[1]

if len(sys.argv)>2:
        outfile = sys.argv[2]
else:
        outfile = 'xyz_table.txt'


votable = parse(file)
t = votable.get_first_table()

"""
ra = t.array['ra']
dec = t.array['dec']
name = t.array['designation']
d = t.array['D_bP']
"""

ra = t.array['RA']
dec = t.array['Dec']
name = t.array['Name']
d = t.array['D']


#d = t.array['Dkin_Oct']
#d = t.array['d10']
#d = t.array['Dist']



#print d

num = len(ra)

# Make some output
f = open(outfile, 'w')
tout = '#Index\tName\tRA\tDec\tD\t'
tout += 'X\tY\tZ\n'
f.write(tout)

# Calculate for all
for i in range(len(ra)):

	print ra[i], dec[i], d[i]
	x,y,z = xyz(double(ra[i]), double(dec[i]), double(d[i]))
	#print x,y,z

	na = name[i]
	na = na.replace(' ','_')

	tout = '%2d\t"%s"\t%3.10f\t%3.10f\t%3.2f\t' % ((i+1), na, ra[i], dec[i], double(d[i]))
	tout += '%3.2f\t%3.2f\t%3.2f\n' % (x,y,z)

	print tout

	f.write(tout)

f.close()

