def _terms_AA(kk, mw, mh, c, s):
    # returns (coefficients of the finite loop functions {name: coeff}, rational rest, UV-pole coefficient); units alpha/(4 pi)
    co = {}
    co['A0f_W'] = 4
    co['B0f_WW'] = -3*kk - 4*mw**2
    rest = -4*mw**2
    pole = -3*kk
    return co, rest, pole

def _terms_AZ(kk, mw, mh, c, s):
    # returns (coefficients of the finite loop functions {name: coeff}, rational rest, UV-pole coefficient); units alpha/(4 pi)
    co = {}
    co['A0f_W'] = 2*(6*c**2 - 1)/(3*c*s)
    co['B0f_WW'] = -(18*c**2*kk + 24*c**2*mw**2 + kk + 8*mw**2)/(6*c*s)
    rest = -(36*c**2*mw**2 + kk - 6*mw**2)/(9*c*s)
    pole = -(18*c**2*kk + kk + 12*mw**2)/(6*c*s)
    return co, rest, pole

def _terms_ZZ(kk, mw, mh, c, s):
    # returns (coefficients of the finite loop functions {name: coeff}, rational rest, UV-pole coefficient); units alpha/(4 pi)
    co = {}
    co['A0f_H'] = -(2*c**2*kk - c**2*mh**2 + mw**2)/(12*c**4*kk*(c - 1)*(c + 1))
    co['A0f_W'] = -(12*c**4 - 4*c**2 + 1)/(3*c**2*(c - 1)*(c + 1))
    co['A0f_Z'] = -(2*c**2*kk + c**2*mh**2 - mw**2)/(12*c**4*kk*(c - 1)*(c + 1))
    co['B0f_HZ'] = -(c**4*kk**2 - 2*c**4*kk*mh**2 + c**4*mh**4 + 10*c**2*kk*mw**2 - 2*c**2*mh**2*mw**2 + mw**4)/(12*c**6*kk*(c - 1)*(c + 1))
    co['B0f_WW'] = (36*c**4*kk + 48*c**4*mw**2 + 4*c**2*kk + 32*c**2*mw**2 - kk - 20*mw**2)/(12*c**2*(c - 1)*(c + 1))
    rest = (72*c**6*mw**2 + 4*c**4*kk - 24*c**4*mw**2 - 2*c**2*kk + 3*c**2*mh**2 + 6*c**2*mw**2 + 3*mw**2)/(18*c**4*(c - 1)*(c + 1))
    pole = (18*c**6*kk + 2*c**4*kk + 24*c**4*mw**2 - c**2*kk - 12*c**2*mw**2 - 6*mw**2)/(6*c**4*(c - 1)*(c + 1))
    return co, rest, pole

def _terms_W(kk, mw, mh, c, s):
    # returns (coefficients of the finite loop functions {name: coeff}, rational rest, UV-pole coefficient); units alpha/(4 pi)
    co = {}
    co['A0f_H'] = -(2*kk - mh**2 + mw**2)/(12*kk*(c - 1)*(c + 1))
    co['A0f_W'] = -(20*c**2*kk + c**2*mh**2 - 2*c**2*mw**2 + mw**2)/(12*c**2*kk*(c - 1)*(c + 1))
    co['A0f_Z'] = -(8*c**2 + 1)*(2*c**2*kk + c**2*mw**2 - mw**2)/(12*c**2*kk*(c - 1)*(c + 1))
    co['B0f_0W'] = -2*(5*kk**2 + 2*kk*mw**2 - mw**4)/(3*kk)
    co['B0f_HW'] = -(kk**2 - 2*kk*mh**2 + 10*kk*mw**2 + mh**4 - 2*mh**2*mw**2 + mw**4)/(12*kk*(c - 1)*(c + 1))
    co['B0f_WZ'] = (40*c**6*kk**2 + 16*c**6*kk*mw**2 - 8*c**6*mw**4 - c**4*kk**2 + 54*c**4*kk*mw**2 + 15*c**4*mw**4 - 10*c**2*kk*mw**2 - 6*c**2*mw**4 - mw**4)/(12*c**4*kk*(c - 1)*(c + 1))
    rest = (2*c**2*kk + 3*c**2*mh**2 + 54*c**2*mw**2 + 3*mw**2)/(18*c**2*(c - 1)*(c + 1))
    pole = (19*c**2*kk + 12*c**2*mw**2 - 6*mw**2)/(6*c**2*(c - 1)*(c + 1))
    return co, rest, pole
