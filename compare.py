#%%
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import os

import fsec.hvac
import title24.hvac
import nrel.hvac

figures_dir = 'figures'
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)

def plot_dict(d):
  sns.set(rc={'figure.figsize': (10.0,7.0)})
  sns.set_context("poster")
  fig, ax = plt.subplots()
  for method in d['y-values']:
    ax.plot(d['x-values'], d['y-values'][method],label = method)
  ax.set_xlabel(d['x-label'])
  ax.set_ylabel(d['y-label'])
  ax.legend()
  fig.savefig(os.path.join(figures_dir, f"{d['y-label']}-vs-{d['x-label']}.png"), bbox_inches='tight')

#%%

plot_data = {}

# Cooling

## Gross Cooling COP at rated conditions from SEER

plot_data['x-label'] = 'SEER'
plot_data['x-values'] = np.linspace(8.0, 20.0, 100)
plot_data['y-label'] = 'COP_95'
plot_data['y-values'] = {}

plot_data['y-values']['FSEC'] = [fsec.hvac.rated_COP_C(seer) for seer in plot_data['x-values']]
plot_data['y-values']['CA'] = [title24.hvac.rated_COP_C(seer) for seer in plot_data['x-values']]
plot_data['y-values']['NREL'] = [nrel.hvac.rated_COP_C(seer) for seer in plot_data['x-values']]

plot_dict(plot_data)

## Cooling C_D
plot_data['y-label'] = 'C_D Cooling'
plot_data['y-values'] = {}

plot_data['y-values']['FSEC'] = [fsec.hvac.Cd_C(seer) for seer in plot_data['x-values']]
plot_data['y-values']['CA'] = [title24.hvac.Cd_C(seer) for seer in plot_data['x-values']]
plot_data['y-values']['NREL'] = [nrel.hvac.Cd_C(seer) for seer in plot_data['x-values']]

plot_dict(plot_data)

## Gross Cooling capacity

plot_data['y-label'] = 'Normalized Cooling Capacity'
plot_data['y-values'] = {}
plot_data['x-label'] = 'T_odb [F]'
plot_data['x-values'] = np.linspace(55.0, 120.0, 100)


T_ewb = 67.0 # F
T_edb = 80.0 # F
V = 350 # CFM/ton
P_fan = 0.365 #W/cfm

plot_data['y-values']['FSEC'] = [fsec.hvac.cap_C_tot(T_ewb,T_odb) for T_odb in plot_data['x-values']]
plot_data['y-values']['CA'] = [title24.hvac.cap_C_tot(T_ewb,T_odb,T_edb,V) for T_odb in plot_data['x-values']]
plot_data['y-values']['NREL'] = [nrel.hvac.cap_C_tot(T_ewb,T_odb) for T_odb in plot_data['x-values']]

plot_dict(plot_data)

## Gross cooling COP
plot_data['y-label'] = 'Normalized Cooling COP'
plot_data['y-values'] = {}

plot_data['y-values']['FSEC'] = [fsec.hvac.COP_C(T_ewb,T_odb) for T_odb in plot_data['x-values']]
plot_data['y-values']['CA'] = [title24.hvac.COP_C(T_ewb,T_odb,T_edb,V,P_fan,13.0) for T_odb in plot_data['x-values']]
plot_data['y-values']['NREL'] = [nrel.hvac.COP_C(T_ewb,T_odb) for T_odb in plot_data['x-values']]

plot_dict(plot_data)

# Heating

plot_data['x-label'] = 'HSPF'
plot_data['x-values'] = np.linspace(5.0, 13.0, 100)
plot_data['y-label'] = 'COP_47'
plot_data['y-values'] = {}

plot_data['y-values']['FSEC'] = [fsec.hvac.rated_COP_H(hspf) for hspf in plot_data['x-values']]
plot_data['y-values']['CA'] = [title24.hvac.rated_COP_H(hspf) for hspf in plot_data['x-values']]
plot_data['y-values']['NREL'] = [nrel.hvac.rated_COP_H(hspf) for hspf in plot_data['x-values']]

plot_dict(plot_data)

## Heating C_D

plot_data['y-label'] = 'C_D Heeting'
plot_data['y-values'] = {}

plot_data['y-values']['FSEC'] = [fsec.hvac.Cd_H(hspf) for hspf in plot_data['x-values']]
plot_data['y-values']['CA'] = [title24.hvac.Cd_H(hspf) for hspf in plot_data['x-values']]
plot_data['y-values']['NREL'] = [nrel.hvac.Cd_H(hspf) for hspf in plot_data['x-values']]

plot_dict(plot_data)

## Integrated heating capacity (includes defrost)

plot_data['y-label'] = 'Normalized Heating Capacity'
plot_data['y-values'] = {}
plot_data['x-label'] = 'T_odb [F]'
plot_data['x-values'] = np.linspace(-10, 55, 100)

T_edb = 65.0 # F
T_owb = -10 # F
V = 350 # CFM/ton
P_fan = 0.365 #W/cfm

plot_data['y-values']['FSEC'] = [fsec.hvac.cap_H(T_odb,T_edb,V) for T_odb in plot_data['x-values']]
plot_data['y-values']['CA'] = [title24.hvac.cap_H(T_odb) for T_odb in plot_data['x-values']]
plot_data['y-values']['NREL'] = [nrel.hvac.cap_H(T_edb,T_odb,T_owb) for T_odb in plot_data['x-values']]

plot_dict(plot_data)

## Integrated heating COP (includes defrost)
plot_data['y-label'] = 'Normalized Heating COP'
plot_data['y-values'] = {}

plot_data['y-values']['FSEC'] = [fsec.hvac.COP_H(T_odb,T_edb,V) for T_odb in plot_data['x-values']]
plot_data['y-values']['CA'] = [title24.hvac.COP_H(T_odb,8.0,V,P_fan) for T_odb in plot_data['x-values']]
plot_data['y-values']['NREL'] = [nrel.hvac.COP_H(T_edb,T_odb,T_owb) for T_odb in plot_data['x-values']]

plot_dict(plot_data)


# %%
