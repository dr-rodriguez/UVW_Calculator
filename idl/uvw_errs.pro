; David Rodriguez
; Aug 24, 2010
; Calculate UVWs and output errors too!

pro uvw_errs, ra, dec, pmra0, pmdec0, dist0, rv0, derr=derr, rverr=rverr, pmra_err=pmra_err, pmdec_err=pmdec_err, u0=u0, v0=v0, w0=w0, uerr0=uerr0, verr0=verr0, werr0=werr0

on_error, 2

IF N_PARAMS() LT 6 THEN BEGIN
  print, 'Syntax - UVW_ERRS, RA, DEC, PMRA, PMDEC, DIST, RV, DERR=DERR, RVERR=RVERR, [PMRA_ERR=PMRA_ERR, PMDEC_ERR=PMDEC_ERR]
  RETURN
ENDIF

IF n_elements(pmra_err) EQ 0 AND ~arg_present(pmra_err)   THEN pmra_err  = 0.
IF n_elements(pmdec_err) EQ 0 AND ~arg_present(pmdec_err)   THEN pmdec_err  = 0.
IF n_elements(derr) EQ 0 AND ~arg_present(derr)   THEN derr  = 0 ;0.2*dist0 
IF n_elements(rverr) EQ 0 AND ~arg_present(rverr)   THEN rverr  = 0.

IF pmra_err eq 0. and pmdec_err eq 0. and derr eq 0. and rverr eq 0. THEN BEGIN
  GAL_UVW, u, v, w, RA=ra, DEC=dec, PMRA=pmra0, PMDEC=pmdec0, VRAD=rv0, DISTANCE=dist0
  u = -u  ; Convert U to be towards the galactic center
  print, 'UVW: ', u, v, w
ENDIF

; Initialize the arrays
good = 0
num = 4000
rv    = fltarr(num)
dist  = fltarr(num)
pmra  = fltarr(num)
pmdec = fltarr(num)

IF rverr gt 0. THEN BEGIN
  array = randomn(seed1,num)
  rv = array * rverr + rv0
  good = 1
ENDIF ELSE rv[*] = rv0

IF derr gt 0. THEN BEGIN
  array = randomn(seed1,num)
  dist = array * derr + dist0
  good = 1
ENDIF ELSE dist[*] = dist0

IF pmra_err gt 0. THEN BEGIN
  array = randomn(seed1,num)
  pmra = array * pmra_err + pmra0
  good = 1
ENDIF ELSE pmra[*] = pmra0

IF pmdec_err gt 0. THEN BEGIN
  array = randomn(seed1,num)
  pmdec = array * pmdec_err + pmdec0
  good = 1
ENDIF ELSE pmdec[*] = pmdec0

count = 0
IF good THEN BEGIN
  Uarr = fltarr(num)
  Varr = fltarr(num)
  Warr = fltarr(num)
  FOR i=0, num-1 DO BEGIN
    if dist[i] le 0 THEN continue
    GAL_UVW, u, v, w, RA=ra, DEC=dec, PMRA=pmra[i], PMDEC=pmdec[i], VRAD=rv[i], DISTANCE=dist[i]
    u = -u  ; Convert U to be towards the galactic center
    ;print, 'UVW: ', u, v, w
    Uarr[i] = u
    Varr[i] = v
    Warr[i] = w
    count += 1
  ENDFOR
  
  print, 'Of ',num,' runs, did only ',count
  
  index = where(Uarr ne 0.0)
  Uarr = Uarr[index]
  Varr = Varr[index]
  Warr = Warr[index]
  
  Uavg = mean(Uarr)
  Vavg = mean(Varr)
  Wavg = mean(Warr)
  Uerr = stddev(Uarr)
  Verr = stddev(Varr)
  Werr = stddev(Warr)
  
  print, 'U: ', string(Uavg,format='(F6.2)'), ' +/- ', string(Uerr,format='(F5.2)')
  print, 'V: ', string(Vavg,format='(F6.2)'), ' +/- ', string(Verr,format='(F5.2)')
  print, 'W: ', string(Wavg,format='(F6.2)'), ' +/- ', string(Werr,format='(F5.2)')
  
  u0=Uavg
  v0=Vavg
  w0=Wavg
  uerr0=Uerr
  verr0=Verr
  werr0=Werr
  
  print, Uavg, Uerr, Vavg, Verr, Wavg, Werr
  
  ; XYZ calculation
  GLACTC, ra, dec, 2000, l, b, 1, /degree
  l = l*!PI/180
  b = b*!PI/180
  xgc = dist0 * cos(b) * cos(l)
  ygc = dist0 * cos(b) * sin(l)
  zgc = dist0 * sin(b)
  ;xgc = -1*xgc ;activate this for positive towards *anti*center
  print, 'XYZ: ', xgc, ygc, zgc
  
  print, Uavg, Uerr, Vavg, Verr, Wavg, Werr, xgc, ygc, zgc
  
  
ENDIF

end