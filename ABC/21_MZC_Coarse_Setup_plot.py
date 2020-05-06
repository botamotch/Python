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
plt.rcParams['legend.framealpha'] = 0.8

import matplotlib
matplotlib.use('WXAgg')
# matplotlib.use('TkAgg')

# Main -------------------------------------------------------------------------

POWER       = [ [], [], [], [] ]
MPD_LO_out  = [ [], [], [], [] ]
MPD_HI_out  = [ [], [], [], [] ]
MPD_LO_in   = [ [], [], [], [] ]

P_MIN    = [[], [], [], []]
P_MAX    = [[], [], [], []]
BIAS_BOL = [0., 0., 0., 0.]
P_PI     = [0., 0., 0., 0.]

print('Read log file ================================================================')
for i in range(4):
    ch = ['XI', 'XQ', 'YI', 'YQ'][i]
    FILENAME = './Log/20_MZC_Coarse_Setup_{}.txt'.format(ch)
    try:
        f = open(FILENAME, 'r')
    except FileNotFoundError:
        continue
    print(' {}'.format(FILENAME))
    _ = f.readline() # 先頭はヘッダなので無視
    for l in f.readlines():
        ls = l.split(',')
        vdac_p      = 4.5*int(ls[0],16)/0xFFFF
        vdac_n      = 4.5*int(ls[1],16)/0xFFFF
        vadc_p      = 4.5*int(ls[2],16)/0xFFFF
        vadc_n      = 4.5*int(ls[3],16)/0xFFFF

        vadc_lo_out = 2.5*int(ls[4],16)/0xFFFF
        vadc_hi_out = 2.5*int(ls[5],16)/0xFFFF
        vadc_lo_in  = 2.5*int(ls[6],16)/0xFFFF

        power_p = (vdac_p - vadc_p)*vadc_p*1e+2  # [mW]
        power_n = (vdac_n - vadc_n)*vadc_n*1e+2  # [mW]
        POWER[i].append(power_p - power_n)       # [mW]

        MPD_LO_out[i].append((2.4 - vadc_lo_out)/10.7e+3  * 1.0e+6) # [uA]
        MPD_HI_out[i].append((2.4 - vadc_hi_out)/100.0e+3 * 1.0e+6) # [uA]
        MPD_LO_in[i].append( (2.4 - vadc_lo_in)/10.7e+3 * 1.0e+6)    # [uA]
    f.close()

print('')
print('Bias BOL =====================================================================')

for (i, ch) in enumerate(['XI', 'XQ', 'YI', 'YQ']):
    print(' {} ch'.format(ch))
    for (j, _) in enumerate(MPD_LO_out[i][1:-1]):
        tmp_list = MPD_LO_out[i]

        if (tmp_list[j] > tmp_list[j+1]) & (tmp_list[j+1] < tmp_list[j+2]):
            P_MIN[i].append(POWER[i][j])
        if (tmp_list[j] < tmp_list[j+1]) & (tmp_list[j+1] > tmp_list[j+2]):
            P_MAX[i].append(POWER[i][j])

    print('   Null Point [mW] : ', end='')
    for j in P_MIN[i]:
        print('{:7.2f},'.format(j),end='')
    print('')

    print('   On Point   [mW] : ', end='')
    for j in P_MAX[i]:
        print('{:7.2f},'.format(j),end='')
    print('')

    BIAS_BOL[i] = POWER[i][0]
    for j in P_MIN[i]:
        if abs(j) < abs(BIAS_BOL[i]):
            BIAS_BOL[i] = j

    for (j, _) in enumerate(P_MAX[i][:-1]):
        if (P_MAX[i][j] < BIAS_BOL[i]) and (BIAS_BOL[i] < P_MAX[i][j+1]):
            P_PI[i] = (P_MAX[i][j+1] - P_MAX[i][j])/2.0

    print('   Bias BOL   [mW] : {:7.2f}'.format(BIAS_BOL[i]))
    print('   Ppi        [mW] : {:7.2f}'.format(P_PI[i]))

print('')
print('Plot figure ==================================================================')
fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(14.0,8.0), sharex='all', sharey='all')

for (i, ch) in enumerate(['XI', 'XQ', 'YI', 'YQ']):

    axs_in = axs[i//2][i%2].twinx()
    _ = axs_in.set_ylim(  0, 120)

    if i in [0,2]: _ = axs[i//2][i%2].set_ylabel( 'Monitor PD out [uA]' )
    if i in [2,3]: _ = axs[i//2][i%2].set_xlabel( 'Heater Power [mW]' )
    if i in [1,3]: _ = axs_in.set_ylabel( 'Monitor PD in [uA]' )

    _ = axs[i//2][i%2].set_xlim(-80, 80)
    _ = axs[i//2][i%2].set_ylim(  0, 45)

    line_LO_out, = axs[i//2][i%2].plot( [], [], '-', label='MPD Lo out {}'.format(ch), color='blue')
    line_HI_out, = axs[i//2][i%2].plot( [], [], '-', label='MPD Hi out {}'.format(ch), color='green')
    line_LO,     = axs_in.plot( [], [], '-', label='MPD Lo in {}'.format(ch), color='purple')

    handler1, label1 = axs[i//2][i%2].get_legend_handles_labels()
    handler2, label2 = axs_in.get_legend_handles_labels()
    axs[i//2][i%2].legend(handler1 + handler2, label1 + label2, loc='lower right', borderaxespad=0.5)
    axs[i//2][i%2].grid(True)

    line_LO_out.set_data(POWER[i], MPD_LO_out[i])
    line_HI_out.set_data(POWER[i], MPD_HI_out[i])
    line_LO.set_data(POWER[i], MPD_LO_in[i])

FIGFILE = './Log/21_MZC_Coarse_setup.png'
print(' Save figure : {}'.format(FIGFILE))
fig.savefig(FIGFILE)

print('')
print('RAM/EEPROM command ===========================================================')

LOGFILE = './Log/21_MZC_Coarse_setup_write.txt'
print(' write command : {}'.format(LOGFILE))
print('')
f = open(LOGFILE, 'w')

### RAM
for (i,b) in enumerate(BIAS_BOL):
    b_int = int(b * 1000. / 2.)
    f.write('m {0:08X} {1:04X}\n'.format( 0x200151F0 + i*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

for (i,b) in enumerate(P_PI):
    f.write('m {0:08X} {1:04X}\n'.format( 0x200118B0 + i*0x24, int(b / 180 * 0.8 * 1000) ))
    f.write('m {0:08X} {1:04X}\n'.format( 0x200118B2 + i*0x24, int(b / 180 * 0.8 * 1000) ))

for (i,b) in enumerate(P_PI):
    f.write('m {0:08X} {1:04X}\n'.format( 0x200118C0 + i*0x24, int(b / 180 * 0.4 * 1000) ))
    f.write('m {0:08X} {1:04X}\n'.format( 0x200118C2 + i*0x24, int(b / 180 * 0.4 * 1000) ))

### EEPROM
for (i,b) in enumerate(BIAS_BOL):
    b_int = int(b * 1000. / 2.)
    f.write('eepf_wle {0:06X} {1:04X}\n'.format( 0x0005F0 + i*0x24, b_int if b_int >= 0 else 0x10000 + b_int))

for (i,b) in enumerate(P_PI):
    f.write('eepf_wle {0:06X} {1:04X}\n'.format( 0x0005F8 + i*0x24, int(b / 180 * 0.8 * 1000) ))
    f.write('eepf_wle {0:06X} {1:04X}\n'.format( 0x0005FA + i*0x24, int(b / 180 * 0.8 * 1000) ))

for (i,b) in enumerate(P_PI):
    f.write('eepf_wle {0:06X} {1:04X}\n'.format( 0x000688 + i*0x24, int(b / 180 * 0.4 * 1000) ))
    f.write('eepf_wle {0:06X} {1:04X}\n'.format( 0x00068A + i*0x24, int(b / 180 * 0.4 * 1000) ))

f.close()

