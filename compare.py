#%%
import numpy as np
import matplotlib.pyplot as plt

import os

import fsec.hvac
import title24.hvac
import nrel.air_conditioner
import nrel.heat_pump

import seaborn as sns

sns.set()

#%%
figures_dir = 'figures'
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)

# %%
def plot_dict(d):
  fig, ax = plt.subplots()
  for method in d['y-values']:
    ax.plot(d['x-values'], d['y-values'][method],label = method)
  ax.set_xlabel(d['x-label'])
  ax.set_ylabel(d['y-label'])
  ax.legend()
  fig.savefig(os.path.join(figures_dir, d['x-label'] + '.png'), bbox_inches='tight')

#%%
COP_clg = {}
COP_clg['x-label'] = 'SEER'
COP_clg['x-values'] = np.arange(8.0, 20.0, 0.01)
COP_clg['y-label'] = 'COP_95'
COP_clg['y-values'] = {}

COP_htg = {}
COP_htg['x-label'] = 'HSPF'
COP_htg['x-values'] = np.arange(5.0, 10.0, 0.01)
COP_htg['y-label'] = 'COP_47'
COP_htg['y-values'] = {}

#%%

# FSEC regressions
COP_clg['y-values']['FSEC'] = [fsec.hvac.calc_air_conditioner_COP(seer) for seer in COP_clg['x-values']]
COP_htg['y-values']['FSEC'] = [fsec.hvac.calc_heat_pump_COP(hspf) for hspf in COP_htg['x-values']]

# CA Title 24 regressions
COP_clg['y-values']['CA'] = [title24.hvac.calc_air_conditioner_COP(seer) for seer in COP_clg['x-values']]
COP_htg['y-values']['CA'] = [title24.hvac.calc_heat_pump_COP(hspf) for hspf in COP_htg['x-values']]

# NREL (Cutler) method
# Cooling
COP_clg['y-values']['NREL_hp'] = [nrel.heat_pump.calc_heat_pump_COPs(seer , 7.7)[0] for seer in COP_clg['x-values']]
COP_clg['y-values']['NREL_ac'] = [nrel.air_conditioner.calc_air_conditioner_COP(seer) for seer in COP_clg['x-values']]
# Heating
COP_htg['y-values']['NREL'] = [nrel.heat_pump.calc_heat_pump_COPs(13.0 , hspf)[1] for hspf in COP_htg['x-values']]

plot_dict(COP_clg)

plot_dict(COP_htg)


# %%
