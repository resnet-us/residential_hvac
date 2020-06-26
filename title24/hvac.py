import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], 'shared'))

from util import *

def rated_EER(seer):
  if seer < 13.0:
    return 10.0  + 0.84 * (seer - 11.5)
  elif seer < 16.0:
    return 11.3 + 0.57 * (seer - 13.0)
  else:
    return 13.0

def rated_COP_C(seer,fan_power_rated=0.365, fan_flow_per_cap=350.0):
  eer95 = rated_EER(seer)
  return 1.0/calc_EIR_from_EER(eer95, fan_power_rated=fan_power_rated, fan_flow_per_cap=fan_flow_per_cap / 12000.0)

def rated_COP_H(hspf, fan_power_rated=0.365, fan_flow_per_cap=350.0):
  cop_net = 0.3225 * hspf + 0.9099
  return 1.0/calc_EIR_from_COP(cop_net, fan_power_rated=fan_power_rated, fan_flow_per_cap=fan_flow_per_cap / 12000.0)


def Cd_H(hspf):
  return max(min(.25 - 0.2*(hspf-6.8)/(10.0-6.8),0.25),0.05)

def Cd_C(seer):
  return 0

def CA_regression(coeffs,T_ewb,T_odb,T_edb,V):
  return coeffs[0]*T_edb + \
    coeffs[1]*T_ewb + \
    coeffs[2]*T_odb + \
    coeffs[3]*V + \
    coeffs[4]*T_edb*T_odb + \
    coeffs[5]*T_edb*V + \
    coeffs[6]*T_ewb*T_odb + \
    coeffs[7]*T_ewb*V + \
    coeffs[8]*T_odb*V + \
    coeffs[9]*T_ewb*T_ewb + \
    coeffs[10]/V + \
    coeffs[11]

def SHR(T_ewb,T_odb,T_edb,V):
  coeffs = [0.0242020,-0.0592153,0.0012651,0.0016375,0,0,0,-0.0000165,0,0.0002021,0,1.5085285]
  SHR = CA_regression(coeffs,T_ewb,T_odb,T_edb,V)
  return min(1.0, SHR)

def cap_C_tot(T_ewb,T_odb,T_edb,V):
  shr = SHR(T_ewb,T_odb,T_edb,V)
  if shr < 1:
    coeffs = [0,0.009645900,0.002536900,0.000171500,0,0,-0.000095900,0.000008180,-0.000007550,0.000105700,-53.542300000,0.381567150]
  else: # shr == 1
    coeffs = [0.009483100,0,-0.000600600,-0.000148900,-0.000032600,0.000011900,0,0,-0.000005050,0,-52.561740000,0.430751600]
  return CA_regression(coeffs,T_ewb,T_odb,T_edb,V)

def rated_cap_17(hspf):
  if hspf < 7.5:
    return 0.1113 * hspf - 0.22269
  elif hspf < 9.5567:
    return 0.017 * hspf + 0.4804
  elif hspf < 10.408:
    return 0.0982 * hspf - 0.2956
  else:
    return 0.0232 * hspf + 0.485

def cap_H(T_odb,hspf=8.0,V=350.0,P_fan=0.365):
  q_fan = P_fan*3.412*V/12000.0 # (W/cfm * Btu/h/W * cfm/ton * ton/Btu/h) Btu fan heat per Btu capacity
  cap_47 = 1.0 + q_fan
  cap_17 = rated_cap_17(hspf)
  cap_35 = 0.9*(cap_17 + 0.6*(cap_47 - cap_17))

  if (T_odb > 17.0 and T_odb < 45.0):
    slope = (cap_35 - cap_17)/(35.0 - 17.0)
  else:
    slope = (cap_47 - cap_17)/(47.0 - 17.0)
  return cap_17 + slope*(T_odb - 17.0) - q_fan

def COP_C(T_ewb,T_odb,T_edb,V,P_fan,seer):
  shr = SHR(T_ewb,T_odb,T_edb,V)
  cap_C = cap_C_tot(T_ewb,T_odb,T_edb,V)
  eer = rated_EER(seer)
  COP_rated = rated_COP_C(seer,P_fan,V)
  q_fan = P_fan*3.412*V/12000.0 # (W/cfm * Btu/h/W * cfm/ton * ton/Btu/h) Btu fan heat per Btu capacity
  if T_odb < 95.0:
    if shr < 1:
      seer_coeffs = [0,-0.0202256,0.0236703,-0.0006638,0,0,-0.0001841,0.0000214,-0.00000812,0.0002971,-27.95672,0.209951063]
    else: # shr == 1
      seer_coeffs = [0.0046103,0,0.0125598,-0.000512,-0.0000357,0.0000105,0,0,0,0,0,-0.316172311]
    seer_nf = (cap_C / CA_regression(seer_coeffs,T_ewb,T_odb,T_edb,V))*(1.09+q_fan)/(1.09/seer-q_fan/3.413)
  else:
    seer_nf = 0.0
  if T_odb > 82.0:
    if shr < 1:
      eer_coeffs = [0,-0.020225600,0.023670300,-0.000663800,0,0,-0.000184100,0.000021400,-0.000008120,0.000297100,-27.956720000,0.015003100]
    else: # shr == 1
      eer_coeffs = [0.004610300,0,0.012559800,-0.000512000,-0.000035700,0.000010500,0,0,0,0,0,-0.475306500]
    eer_nf = (cap_C *(1.0+q_fan))/ (CA_regression(eer_coeffs,T_ewb,T_odb,T_edb,V)*(1.0/eer - q_fan/3.413))
  else:
    eer_nf = 0.0
  if T_odb <= 82.0:
    eer_t = seer_nf
  elif T_odb < 95.0:
    eer_t = seer_nf + (T_odb - 82.0)*(eer_nf - seer_nf)/13.0
  else:
    eer_t = eer_nf
  return eer_t / COP_rated / 3.413


def check_HSPF(cap_47,inp_47,cap_35,inp_35,cap_17,inp_17,C_D):
  # Calculate region 4 HSPF
  out_tot = 0
  inp_tot = 0

  T_bins = [62.0, 57.0, 52.0, 47.0, 42.0, 37.0, 32.0, 27.0, 22.0, 17.0, 12.0, 7.0, 2.0, -3.0, -8.0]
  frac_hours = [0.132, 0.111, 0.103, 0.093, 0.100, 0.109, 0.126, 0.087, 0.055, 0.036, 0.026, 0.013, 0.006, 0.002, 0.001]

  T_design = 5.0
  T_edb = 65.0
  C = 0.77  # AHRI "correction factor"
  T_off = 0.0  # low temp cut-out "off" temp (F)
  T_on = 5.0  # low temp cut-out "on" temp (F)
  dHRmin = cap_47

  for i, T_odb in enumerate(T_bins):
    bL = ((T_edb - T_odb) / (T_edb - T_design)) * C * dHRmin

    if (T_odb > 17.0 and T_odb < 45.0):
      cap_slope = (cap_35 - cap_17)/(35.0 - 17.0)
      inp_slope = (inp_35 - inp_17)/(35.0 - 17.0)
    else:
      cap_slope = (cap_47 - cap_17)/(47.0 - 17.0)
      inp_slope = (inp_47 - inp_17)/(47.0 - 17.0)
    cap = cap_17 + cap_slope*(T_odb - 17.0)
    inp = inp_17 + inp_slope*(T_odb - 17.0)

    x_t = min(bL / cap, 1.0)
    PLF = 1.0 - (C_D * (1.0 - x_t))
    if T_odb <= T_off or cap/(inp*3.412) >= 1.0:
      sigma_t = 0.0
    elif T_off < T_odb and T_odb <= T_on and cap/(inp*3.412) >= 1.0:
      sigma_t = 0.5
    else:
      sigma_t = 1.0

    inp_tot += x_t*inp*sigma_t / PLF * frac_hours[i] + (bL - (x_t*cap*sigma_t))/3.412*frac_hours[i]
    out_tot += bL*frac_hours[i]

  return out_tot / inp_tot * 3.412

def COP_H(T_odb,hspf=8.0,V=350.0,P_fan=0.365):
  q_fan = P_fan*3.412*V/12000.0 # (W/cfm * Btu/h/W * cfm/ton * ton/Btu/h) Btu fan heat per Btu capacity
  cap_47 = 1.0 + q_fan
  cap_17 = rated_cap_17(hspf)
  cap_35 = 0.9*(cap_17 + 0.6*(cap_47 - cap_17))

  cop_47 = rated_COP_H(hspf,P_fan,V)
  inp_47 = cap_47 / cop_47

  cop_17 = 0.2186 * hspf + 0.6734  # Initial guess

  inp_17 = cap_17 / cop_17

  inp_35 = 0.985*(inp_17 + 0.6*(inp_47 - inp_17))
  C_D = Cd_H(hspf)

  # Iterate
  tol = 0.001
  max_it = 100
  it = 0
  while True:
    hspf_check = check_HSPF(cap_47,inp_47,cap_35,inp_35,cap_17,inp_17,C_D)
    error = abs(hspf - hspf_check)
    cop_17 *= hspf/hspf_check
    inp_17 = cap_17 / cop_17
    if it > max_it:
      break
    if error <= tol:
      break
    it +=1

  if (T_odb > 17.0 and T_odb < 45.0):
    cap_slope = (cap_35 - cap_17)/(35.0 - 17.0)
    inp_slope = (inp_35 - inp_17)/(35.0 - 17.0)
  else:
    cap_slope = (cap_47 - cap_17)/(47.0 - 17.0)
    inp_slope = (inp_47 - inp_17)/(47.0 - 17.0)
  cap = cap_17 + cap_slope*(T_odb - 17.0) - q_fan
  inp = inp_17 + inp_slope*(T_odb - 17.0) - q_fan

  COP_rated = rated_COP_H(hspf,P_fan,V)

  return cap/inp / COP_rated