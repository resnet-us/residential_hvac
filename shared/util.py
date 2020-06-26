def calc_EIR_from_EER(eer, fan_power_rated, fan_flow_per_cap=400.0 / 12000.0):
    return ((1.0 - (fan_power_rated * fan_flow_per_cap) * 3.412) / eer - fan_power_rated * fan_flow_per_cap) * 3.412

def calc_EIR_from_COP(cop, fan_power_rated, fan_flow_per_cap=400.0 / 12000.0):
    return ((1.0/3.412 + fan_power_rated * fan_flow_per_cap) / cop - fan_power_rated * fan_flow_per_cap) * 3.412

def calc_EER_from_EIR(eir, fan_power_rated, fan_flow_per_cap=400.0 / 12000.0):
    return ((1.0 - 3.412 * (fan_power_rated * fan_flow_per_cap)) / (eir / 3.412 + (fan_power_rated * fan_flow_per_cap)))

def calc_biquad(coeff, in_1, in_2):
    return coeff[0] + coeff[1] * in_1 + coeff[2] * in_1 * in_1 + coeff[3] * in_2 + coeff[4] * in_2 * in_2 + coeff[5] * in_1 * in_2

