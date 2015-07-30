# UVW_Calculator
Javascript, Python, and IDL tools to calculate stellar UVW velocities

## Information
Created July 3, 2015 from a variety of files I have writted in the past.

## Files
* uvwcalculator.html - Direct copy of my Javascript code to calculate UVW given a variety of input parameters
* staruvw.py - Python code to compute UVW for a table following the VOTable format.
* starxyz.py - Python code to compute XYZ for a table following the VOTable format.
* uvw_errs.py - Incomplete file (a translation of the IDL version) to compute errors for the UVW
* dr_uvw.pro - IDL code to compute UVW and select those in the "good UVW box" defined by Zuckerman & Song ARAA 2004, 42, 685
* uvw_errs.pro - IDL code to compute UVW and calculate errors. Also returns XYZ