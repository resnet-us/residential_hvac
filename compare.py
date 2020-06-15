#%%
import numpy as np
import matplotlib.pyplot as plt

import os

import fsec.hvac
import nrel.air_conditioner
import nrel.heat_pump

import seaborn as sns

sns.set()

#%%
figures_dir = 'figures'
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)
#%%

SEERs = np.arange(8.0, 20.0, 0.01)
HSPFs = np.arange(5.0, 10.0, 0.01)

# %%
def plot_dict(x,y_dict,name):
  fig, ax = plt.subplots()
  for method in y_dict:
    ax.plot(x, y_dict[method],label = method)
  ax.set_xlabel(name)
  ax.set_ylabel('COP')
  ax.legend()
  fig.savefig(os.path.join(figures_dir, name + '.png'), bbox_inches='tight')

#%%
COP_clg = {}
COP_htg = {}

# FSEC regressions
COP_clg['FSEC'] = [fsec.hvac.calc_air_conditioner_COP(seer) for seer in SEERs]
COP_htg['FSEC'] = [fsec.hvac.calc_heat_pump_COP(hspf) for hspf in HSPFs]

# NREL (Cutler) method
# Cooling
COP_clg['NREL_hp'] = [nrel.heat_pump.calc_heat_pump_COPs(seer , 7.7)[0] for seer in SEERs]
COP_clg['NREL_ac'] = [nrel.air_conditioner.calc_air_conditioner_COP(seer) for seer in SEERs]
# Heating
COP_htg['NREL'] = [nrel.heat_pump.calc_heat_pump_COPs(13.0 , hspf)[1] for hspf in HSPFs]

plot_dict(SEERs, COP_clg, 'SEER')

plot_dict(HSPFs, COP_htg, 'HSPF')


# %%


# %%
