import sys
from .util import *

def calc_heat_pump_COPs(seer, hspf):
    if seer <= 15:
        fan_power_rated = 0.365 # W/cfm
    else:
        fan_power_rated = 0.14 # W/cfm

    if seer < 13:
        c_d_cooling = 0.20
    else:
        c_d_cooling = 0.07

    if hspf < 7:
        c_d_heating = 0.20
    else:
        c_d_heating = 0.11

    # Table 13. HP EIR Coefficients as a Function of Operating Temperatures (deg-F)
    coeff_eir_cooling = [-3.437356399, 0.136656369, -0.001049231, -0.0079378, 0.000185435, -0.0001441]
    coeff_eir_heating = [0.718398423, 0.003498178, 0.000142202, -0.005724331, 0.00014085, -0.000215321]

    # Table 12. HP Total Capacity Coefficients as a Function of Operating Temperatures (deg-F)
    coeff_q_heating = [0.566333415, -0.000744164, -0.0000103, 0.009414634, 0.0000506, -0.00000675]

    cop_cooling = 1.0 / calc_EIR_cooling_1spd(seer, fan_power_rated, c_d_cooling, coeff_eir_cooling)
    cop_heating = 1.0 / calc_EIR_heating_1spd(hspf, fan_power_rated, c_d_heating, coeff_eir_heating, coeff_q_heating)

    return cop_cooling, cop_heating

if __name__ == '__main__':
    if len(sys.argv) == 3:
        seer = float(sys.argv[1])
        hspf = float(sys.argv[2])

        cop_cooling, cop_heating = calc_heat_pump_COPs(seer, hspf)

        print("COP_cooling: %s" % round(cop_cooling, 2))
        print("COP_heating: %s" % round(cop_heating, 2))
    else:
        sys.exit('Usage: heat_pump.py SEER HSPF')