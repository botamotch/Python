# -*- coding: utf-8 -*-

# Import -----------------------------------------------------------------------
import os
import sys
import time
import wx

import numpy as np

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = [ 'Yu Gothic' , 'Noto Sans CJK JP']
plt.rcParams['font.size'] = 10
plt.rcParams['legend.framealpha'] = 1.0

import matplotlib
matplotlib.use('WXAgg')
# matplotlib.use('TkAgg')

# Main -------------------------------------------------------------------------

ERROR   = [ [], [], [], [] ]
DIFF    = [ [], [], [], [] ]
I_PD    = [ [], [], [], [] ]
POWER   = [ [], [], [], [] ]

BIAS_BOL = [0.0, 0.0, 0.0, 0.0]
SLOPE    = [0.0, 0.0, 0.0, 0.0]
FIT      = ['-', '-', '-', '-']

print('Read log file ================================================================')
for (i, ch) in enumerate(['XI', 'XQ', 'YI', 'YQ']):

    FILENAME = './Log/30_MZC_Fine_Setup_{}.txt'.format(ch)
    try:
        f = open(FILENAME, 'r')
    except FileNotFoundError:
        continue
    print(' {}'.format(FILENAME))
    _ = f.readline() # 先頭はヘッダなので無視
    for l in f.readlines():
        ls = l.split(',')
        error_int   = (int(ls[0],16) & 0x7FFF) - 0x8000 * (int(ls[0],16) >> 15)
        diff        = 2.5*int(ls[1],16)/0xFFFF
        mpd         = 2.5*int(ls[2],16)/0xFFFF
        power_mw    = ((int(ls[3],16) & 0x7FFF) - 0x8000 * (int(ls[3],16) >> 15))/1000.0*2.0

        ERROR[i].append(error_int)  # [DEC]
        DIFF[i].append(diff)        # [V]
        I_PD[i].append(mpd)         # [V]
        POWER[i].append(power_mw)   # [mW]
    f.close()

print('')
print('Bias BOL =====================================================================')

for (i, ch) in enumerate(['XI', 'XQ', 'YI', 'YQ']):
    if len(ERROR[i]) == 0:
        continue
    print(' {} ch'.format(ch))
    for (j, _) in enumerate(ERROR[i][:-1]):
        if (ERROR[i][j] < 0.5*max(ERROR[i])) and (0.5*max(ERROR[i]) < ERROR[i][j+1]):
            MAX_HALF = j
            break

    for (j, _) in enumerate(ERROR[i][:-1]):
        if (ERROR[i][j] < 0.5*min(ERROR[i])) and (0.5*min(ERROR[i]) < ERROR[i][j+1]):
            MIN_HALF = j
            break

    FIT[i]      = np.polyfit(POWER[i][MIN_HALF:MAX_HALF], ERROR[i][MIN_HALF:MAX_HALF], 1)
    BIAS_BOL[i] = -FIT[i][1]/FIT[i][0]
    SLOPE[i]    = 2.5*FIT[i][0]/0xFFFF*1000

    print('   Bias BOL     [mW] : {:8.2f}'.format(BIAS_BOL[i]))
    print('   Error Slope [V/W] : {:8.3f}'.format(SLOPE[i]))
    print('       100kohm [V/W] : {:8.3f}'.format(SLOPE[i]*100/10.7))

print('')
print('Plot figure ==================================================================')
fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(14.0,8.0), sharey='all')

for (i, ch) in enumerate(['XI', 'XQ', 'YI', 'YQ']):

    if len(ERROR[i]) == 0:
        continue
    line_error, = axs[i//2][i%2].plot( [], [], '-', label='Error Value {}'.format(ch), color='blue')
    line_null,  = axs[i//2][i%2].plot( [], [], '-', label='Fitting {}'.format(ch), color='red')

    if i in [0,2]: _ = axs[i//2][i%2].set_ylabel( 'Error Value [LSB]' )
    if i in [2,3]: _ = axs[i//2][i%2].set_xlabel( 'Heater Power [mW]' )

    _ = axs[i//2][i%2].set_xlim(min(POWER[i])-2, max(POWER[i])+2)
    _ = axs[i//2][i%2].set_ylim(-40000, 40000)
    _ = axs[i//2][i%2].legend(loc=2, borderaxespad=0.5)
    _ = axs[i//2][i%2].grid(True)

    line_error.set_data(POWER[i], ERROR[i])
    line_null.set_data(POWER[i][MIN_HALF:MAX_HALF],np.polyval(FIT[i], POWER[i][MIN_HALF:MAX_HALF]))

    TEXT  =   'Bias BOL     [mW] : {:8.2f}'.format(BIAS_BOL[i])
    TEXT += '\nError Slope [V/W] : {:8.3f}'.format(SLOPE[i])
    TEXT += '\n  (100kohm) [V/W] : {:8.3f}'.format(SLOPE[i]*100/10.7)

    axs[i//2][i%2].text(max(POWER[i]), -30000, TEXT, horizontalalignment='right', backgroundcolor='white')

FIGFILE = './Log/31_MZC_Fine_setup.png'
print(' Save figure : {}'.format(FIGFILE))
fig.savefig(FIGFILE)

print('')
print('RAM/EEPROM command ===========================================================')

LOGFILE = './Log/31_MZC_Fine_setup_write.txt'
print(' write command : {}'.format(LOGFILE))
print('')
f = open(LOGFILE, 'w')

DFT_TYP = 2502.2242155222 # [V/W]

### RAM
for (i,b) in enumerate(BIAS_BOL):
    b_int = int(b * 1000. / 2.)
    f.write('m {0:08X} {1:04X}\n'.format( 0x200151F0 + i*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

for (i,b) in enumerate(SLOPE):
    try:
        b_int = int(-0.1*DFT_TYP/(b*100/10.7) * 1000)
    except ZeroDivisionError:
        b_int = 0
    f.write('m {0:08X} {1:04X}\n'.format( 0x2001514A + i*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

### EEPROM
for (i,b) in enumerate(BIAS_BOL):
    b_int = int(b * 1000. / 2.)
    f.write('eepf_wle {0:06X} {1:04X}\n'.format( 0x0005F0 + i*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

for (i,b) in enumerate(SLOPE):
    try:
        b_int = int(-0.1*DFT_TYP/(b*100/10.7) * 1000)
    except ZeroDivisionError:
        b_int = 0
    f.write('eepf_wle {0:06X} {1:04X}\n'.format( 0x00054A + i*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

f.close()

