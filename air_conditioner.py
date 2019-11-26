import sys
from util import *

def calc_air_conditioner_COP(seer):
    if seer <= 15:
        fan_power_rated = 0.365 # W/cfm
    else:
        fan_power_rated = 0.14 # W/cfm
    
    if seer < 13:
        c_d = 0.20
    else:
        c_d = 0.07

    # Table 8.  AC EIR Coefficients as a Function of Operating Temperatures (deg-F)
    coeff_eir = [-3.302695861, 0.137871531, -0.001056996, -0.012573945, 0.000214638, -0.000145054]
    
    cop_cooling = 1.0 / calc_EIR_cooling_1spd(seer, fan_power_rated, c_d, coeff_eir)
    return cop_cooling

if __name__ == '__main__':
    if len(sys.argv) == 2:
        seer = float(sys.argv[1])
        cop_cooling = calc_air_conditioner_COP(seer)
        print "COP_cooling: %s" % round(cop_cooling, 1)
    else:                  
        sys.exit('Usage: air_conditioner.py SEER')