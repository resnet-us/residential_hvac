def calc_air_conditioner_COP(seer):
  if seer < 13.0:
    eer95 = 10.0  + 0.84 * (seer - 11.5)
  elif seer < 16.0:
    eer95 = 11.3 + 0.57 * (seer - 13.0)
  else:
    eer95 = 13.0
  return eer95 / 3.413

def calc_heat_pump_COP(hspf):
  return 0.3225 * hspf + 0.9099
