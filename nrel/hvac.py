from .heat_pump import *
from .util import *
import psychrolib as psy
psy.SetUnitSystem(psy.IP)

def rated_COP_C(seer):
    return calc_heat_pump_COPs(seer , 7.7)[0]

def rated_COP_H(hspf):
    return calc_heat_pump_COPs(13.0 , hspf)[1]

def Cd_H(hspf):
  if hspf < 7:
   return 0.20
  else:
    return 0.11

def Cd_C(seer):
  if seer < 13:
    return 0.20
  else:
    return 0.07

def cap_C_tot(T_ewb,T_odb):
  return calc_biquad([3.68637657,-0.098352478,0.000956357,0.005838141,-0.0000127,-0.000131702],T_ewb,T_odb)

def calc_dw_coil_o(T_odb,T_owb, P=14.7):
    T_coil_o = 0.82*(T_odb - 9.7)
    dw_coil_o = psy.GetHumRatioFromTWetBulb(T_odb,T_owb,P) - psy.GetHumRatioFromTWetBulb(T_coil_o,T_coil_o,P)
    return max(1.0e-6,dw_coil_o)

def cap_H(T_edb,T_odb,T_owb,t_defrost=0.058333):
  if T_odb < 40.0:
    dw_coil_o = calc_dw_coil_o(T_odb,T_owb)
    fCapH_defrost = 0.909 - 107.33*dw_coil_o
    q_defrost = 0.01*t_defrost*(45.0-T_odb)/1.01667
  else:
    fCapH_defrost = 1.0
    q_defrost = 0.0
  q_nom = calc_biquad([ 0.566333415, -0.000744164, -0.0000103,   0.009414634,  0.0000506,  -0.00000675],T_edb,T_odb)
  return q_nom*fCapH_defrost - q_defrost

def COP_C(T_ewb,T_odb):
  return 1.0 /calc_biquad([-3.437356399, 0.136656369, -0.001049231, -0.0079378, 0.000185435, -0.0001441],T_ewb,T_odb)

def COP_H(T_edb,T_odb,T_owb,t_defrost=0.058333):
  if T_odb < 40.0:
    dw_coil_o = calc_dw_coil_o(T_odb,T_owb)
    fInpH_defrost = 0.9 - 36.45*dw_coil_o
    p_defrost = 0.1528*t_defrost/1.01667
  else:
    fInpH_defrost = 1.0
    p_defrost = 0.0
  eir = calc_biquad([0.718398423, 0.003498178, 0.000142202, -0.005724331, 0.00014085, -0.000215321],T_edb,T_odb)
  return 1.0/(eir*fInpH_defrost + p_defrost)