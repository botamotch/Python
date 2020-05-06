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

ERROR   = [ [], [] ]
DIFF1   = [ [], [] ]
DIFF2   = [ [], [] ]
MPD     = [ [], [] ]
POWER   = [ [], [] ]

BIAS_BOL  = [ 0., 0. ]
SLOPE     = [ 0., 0. ]
FIT       = ['-', '-']
ERROR_AVE = [ [], [] ]

print('Read log file ================================================================')
for (i, ch) in enumerate(['X', 'Y']):

    FILENAME = './Log/50_MZP_Fine_Setup_{}.txt'.format(ch)
    try:
        f = open(FILENAME, 'r')
    except FileNotFoundError:
        continue
    print(' {}'.format(FILENAME))
    _ = f.readline() # 先頭はヘッダなので無視
    for l in f.readlines():
        ls = l.split(',')
        error_int   = (int(ls[0],16) & 0x7FFF) - 0x8000 * (int(ls[0],16) >> 15)
        diff1       = 2.5*int(ls[1],16)/0xFFFF
        diff2       = 2.5*int(ls[2],16)/0xFFFF
        mpd         = 2.5*int(ls[3],16)/0xFFFF
        power_mw    = ((int(ls[4],16) & 0x7FFF) - 0x8000 * (int(ls[4],16) >> 15))/1000.0*2.0

        ERROR[i].append(error_int)  # [DEC]
        DIFF1[i].append(diff1)      # [V]
        DIFF2[i].append(diff2)      # [V]
        MPD[i].append(mpd)          # [V]
        POWER[i].append(power_mw)   # [mW]
    f.close()
    ERROR_AVE[i] = np.convolve(ERROR[i], np.ones(5)/5, mode='same')

print('')
print('Bias BOL =====================================================================')

for (i, ch) in enumerate(['X', 'Y']):
    print(' {} ch'.format(ch))

    for (j, _) in enumerate(ERROR[i][:-1]):
        if (ERROR[i][j] < 0.5*max(ERROR[i])) and (0.5*max(ERROR[i]) < ERROR[i][j+1]):
            MAX_HALF = j
            break

    for (j, _) in enumerate(ERROR[i][:-1]):
        if (ERROR[i][j] < 0.5*min(ERROR[i])) and (0.5*min(ERROR[i]) < ERROR[i][j+1]):
            MIN_HALF = j
            break

    FIT[i]      = np.polyfit(POWER[i][MIN_HALF:MAX_HALF], ERROR_AVE[i][MIN_HALF:MAX_HALF], 1)
    BIAS_BOL[i] = -FIT[i][1]/FIT[i][0]
    SLOPE[i]    = 2.5*FIT[i][0]/0xFFFF*1000

    print('   Bias BOL     [mW] : {:8.2f}'.format(BIAS_BOL[i]))
    print('   Error Slope [V/W] : {:8.3f}'.format(SLOPE[i]))
    print('       100kohm [V/W] : {:8.3f}'.format(SLOPE[i]*100/10.7))

print('')
print('Plot figure ==================================================================')
fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(8.0,8.0))

for (i, ch) in enumerate(['X', 'Y']):

    line,      = axs[i].plot( [], [], '-', label='Error Value {}'.format(ch), color='blue')
    line_null, = axs[i].plot( [], [], '-', label='Fitting {}'.format(ch), color='red')

    _ = axs[i].set_ylabel( 'Error Value [LSB]' )
    _ = axs[i].set_xlabel( 'Heater Power [mW]' )

    _ = axs[i].set_xlim(min(POWER[i])-2, max(POWER[i])+2)
    _ = axs[i].set_ylim(-4000, 4000)
    _ = axs[i].legend(loc=2, borderaxespad=0.5)
    _ = axs[i].grid(True)

    line.set_data(POWER[i], ERROR[i])
    line_null.set_data(POWER[i][MIN_HALF:MAX_HALF],np.polyval(FIT[i], POWER[i][MIN_HALF:MAX_HALF]))

    TEXT  =   'Bias BOL     [mW] : {:8.2f}'.format(BIAS_BOL[i])
    TEXT += '\nError Slope [V/W] : {:8.3f}'.format(SLOPE[i])
    TEXT += '\n  (100kohm) [V/W] : {:8.3f}'.format(SLOPE[i]*100/10.7)

    axs[i].text(max(POWER[i]), -3000, TEXT, horizontalalignment='right', backgroundcolor='white')

FIGFILE = './Log/51_MZP_Fine_setup.png'
print(' Save figure : {}'.format(FIGFILE))
fig.savefig(FIGFILE)

print('')
print('RAM/EEPROM command ===========================================================')

LOGFILE = './Log/51_MZP_Fine_setup_write.txt'
print(' write command : {}'.format(LOGFILE))
print('')
f = open(LOGFILE, 'w')

DFT_TYP = 2502.2242155222 # [V/W]

### RAM
for (i,b) in enumerate(BIAS_BOL):
    b_int = int(b * 1000. / 2.)
    f.write('m {0:08X} {1:04X}\n'.format( 0x200151F0 + (i+4)*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

for (i,b) in enumerate(SLOPE):
    try:
        b_int = int(-0.1*DFT_TYP/(b*100/10.7) * 1000)
    except ZeroDivisionError:
        b_int = 0
    f.write('m {0:08X} {1:04X}\n'.format( 0x2001514A + (i+4)*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

### EEPROM
for (i,b) in enumerate(BIAS_BOL):
    b_int = int(b * 1000. / 2.)
    f.write('eepf_wle {0:06X} {1:04X}\n'.format( 0x0005F0 + (i+4)*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

for (i,b) in enumerate(SLOPE):
    try:
        b_int = int(-0.1*DFT_TYP/(b*100/10.7) * 1000)
    except ZeroDivisionError:
        b_int = 0
    f.write('eepf_wle {0:06X} {1:04X}\n'.format( 0x00054A + (i+4)*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

f.close()

