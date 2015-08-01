# UVW_Calculator
Javascript, Python, and IDL tools to calculate stellar UVW velocities

## Information
Created July 3, 2015 from a variety of files I have writted in the past.

## Files

HTML
* uvwcalculator.html - Direct copy of my Javascript code to calculate UVW given a variety of input parameters

Python
* druvw.py - contains the functions uvw and xyz that are called in subsequent Python programs
* staruvw.py - computes UVW for a table following the VOTable format
* starxyz.py - computes XYZ for a table following the VOTable format
* uvw_errs.py - computes UVW and errors for a single object

IDL
* dr_uvw.pro - computes UVW and select those in the "good UVW box" defined by Zuckerman & Song ARAA 2004, 42, 685
* uvw_errs.pro - computes UVW and calculate errors. Also returns XYZ