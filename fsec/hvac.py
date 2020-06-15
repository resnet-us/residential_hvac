def calc_air_conditioner_COP(seer):
    return seer / (3.413*0.941)

def calc_heat_pump_COP(hspf):
    return hspf / (3.413*0.582)
