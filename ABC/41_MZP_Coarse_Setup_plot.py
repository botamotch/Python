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
P_PI      = [ 0., 0. ]
RISE_QUAD = [ [], [] ]
FALL_QUAD = [ [], [] ]
ERROR_AVE = [ [], [] ]

print('Read log file ================================================================')
for (i, ch) in enumerate(['X', 'Y']):

    FILENAME = './Log/40_MZP_Coarse_Setup_{}.txt'.format(ch)
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

    for (j, _) in enumerate(ERROR_AVE[i][:-1]):
        if (ERROR_AVE[i][j] < 0) and (0 < ERROR_AVE[i][j+1]): RISE_QUAD[i].append(j)
        if (ERROR_AVE[i][j] > 0) and (0 > ERROR_AVE[i][j+1]): FALL_QUAD[i].append(j)

    BIAS_BOL[i] = POWER[i][RISE_QUAD[i][0]]
    for j in RISE_QUAD[i]:
        if abs(POWER[i][j]) < abs(BIAS_BOL[i]):
            BIAS_BOL[i] = POWER[i][j]

    print('   Bias BOL        [mW] : {:7.2f}'.format(BIAS_BOL[i]))
    print('   Rise Quad Point [mW] : ', end='')
    for j in RISE_QUAD[i]:
        print('{:7.2f}'.format(POWER[i][j]), end='')

    print('')
    print('   Fall Quad Point [mW] : ', end='')
    for j in FALL_QUAD[i]:
        print('{:7.2f}'.format(POWER[i][j]), end='')
    print('')

print('')
print('Plot figure ==================================================================')
fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(8.0,8.0), sharex='all')

_ = axs[1].set_xlabel( 'Heater Power [mW]' )

for (i, ch) in enumerate(['X', 'Y']):

    line, = axs[i].plot( [], [], '-', label='Error Value {}'.format(ch), color='blue')

    _ = axs[i].set_ylabel( 'Error Value [LSB]' )

    _ = axs[i].set_xlim(-70, 70)
    _ = axs[i].set_ylim(-4000, 4000)
    _ = axs[i].legend(loc=2, borderaxespad=0.5)
    _ = axs[i].grid(True)

    line.set_data(POWER[i], ERROR[i])

    TEXT  =   'Bias BOL        [mW] : {:7.2f}'.format(BIAS_BOL[i])
    TEXT += '\nRise Quad Point [mW] : ' + ''.join(['{:7.2f}'.format(POWER[i][j]) for j in RISE_QUAD[i]])
    TEXT += '\nFall Quad Point [mW] : ' + ''.join(['{:7.2f}'.format(POWER[i][j]) for j in FALL_QUAD[i]])

    axs[i].text(-64, -3500, TEXT, horizontalalignment='left', backgroundcolor='white')

FIGFILE = './Log/41_MZP_Coarse_setup.png'
print(' Save figure : {}'.format(FIGFILE))
fig.savefig(FIGFILE)

print('')
print('RAM/EEPROM command ===========================================================')

LOGFILE = './Log/41_MZP_coarse_setup_write.txt'
print(' write command : {}'.format(LOGFILE))
print('')
f = open(LOGFILE, 'w')

### RAM
for (i,b) in enumerate(BIAS_BOL):
    b_int = int(b * 1000. / 2.)
    f.write('m {0:08X} {1:04X}\n'.format( 0x200151F0 + (i+4)*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

### EEPROM
for (i,b) in enumerate(BIAS_BOL):
    b_int = int(b * 1000. / 2.)
    f.write('eepf_wle {0:06X} {1:04X}\n'.format( 0x0005F0 + (i+4)*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

f.close()

