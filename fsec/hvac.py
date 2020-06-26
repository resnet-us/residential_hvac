import numpy as np

def rated_COP_C(seer):
    return seer / (3.413*0.941)

def rated_COP_H(hspf):
    return hspf / (3.413*0.582)

def Cd_H(hspf):
  return 0.25*1.3

def Cd_C(seer):
  return 0.25

def cap_C_tot(T_odb,T_edb,V=350.0):
  return 1.0 # TODO

def cap_H(T_odb,T_edb,V=350.0):
  qhp = (0.460 + 0.0139*T_odb - 0.00163*T_edb)*(0.7 + 0.32*V/450.0)
  def_tab = [(-20.,0.08),(22.,0.08),(27.,0.12),(37.,0.23),(42.,0.29),(47.,0)]
  qhd = qhp*(1. - np.interp(T_odb,[x[0] for x in def_tab], [y[1] for y in def_tab]))
  return qhd

def COP_C(T_odb,T_edb,V=350.0):
  return 1.0 # TODO

def COP_H(T_odb,T_edb,V=350.0):
  return (0.4138839 + 0.0040874*T_odb +0.0038393*T_edb + 0.0000381*T_odb*T_edb)*(1.16 - 0.165*V/450.0)