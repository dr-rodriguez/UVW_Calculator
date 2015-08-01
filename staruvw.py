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
from druvw import uvw, xyz

# ===============================================

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

