# -*- coding: utf-8 -*-

# Import -----------------------------------------------------------------------
import os
import time

import numpy as np
import toml
from paramiko import SSHClient, AutoAddPolicy
import openpyxl as px

# Config - ---------------------------------------------------------------------

config = toml.load('module.toml')

IP_Address = config['common']['IP_MOD']
COSA       = config['common']['COSA']
COSA_file  = config['common']['COSA_file']

# VALIABLES --------------------------------------------------------------------

DAC_RANGE = 0xFFFF # スキャン範囲[HEX]
DAC_STEP  = 0x0400 # スキャンステップ[HEX]

SWEEP_CH = [0,1,2,3] # スイープするｃｈ（XI,XQ,YI,YQの順に並ぶ）

# COSA Inspection data ---------------------------------------------------------

COSA_data = []

workbook = px.load_workbook(filename=COSA_file, data_only=True)
sheet = workbook["Sheet1"]

for row in sheet:
    if row[4].value == COSA:
        for data in row:
            COSA_data.append(data.value)

# 検査成績書のデータ列
# COSA_INIT = []
# COSA_INIT.append(float(COSA_data[54])) # XPP Quad Point
# COSA_INIT.append(float(COSA_data[55])) # XPN Quad Point
# COSA_INIT.append(float(COSA_data[46])) # XIP Null Point
# COSA_INIT.append(float(COSA_data[47])) # XIN Null Point
# COSA_INIT.append(float(COSA_data[48])) # XQP Null Point
# COSA_INIT.append(float(COSA_data[49])) # XQN Null Point

# COSA_INIT.append(float(COSA_data[56])) # YPP Quad Point
# COSA_INIT.append(float(COSA_data[57])) # YPN Quad Point
# COSA_INIT.append(float(COSA_data[50])) # YIP Null Point
# COSA_INIT.append(float(COSA_data[51])) # YIN Null Point
# COSA_INIT.append(float(COSA_data[52])) # YQP Null Point
# COSA_INIT.append(float(COSA_data[53])) # YQN Null Point

# COSA_INIT_V.append(COSA_data[70]) # TX_X Min attn
# COSA_INIT_V.append(COSA_data[71]) # TX_Y Min attn
# COSA_INIT_V.append(COSA_data[72]) # RX_X Min attn
# COSA_INIT_V.append(COSA_data[73]) # RX_Y Min attn

# CMD --------------------------------------------------------------------------

CMD_DAC_SET = '''
dac_w 40 {00:04X} ;dac_w 41 {01:04X}    #  40 : Phase XP  /  41 : Phase XN
dac_w 42 {02:04X} ;dac_w 43 {03:04X}    #  42 : Bias XIP  /  43 : Bias XIN
dac_w 44 {04:04X} ;dac_w 45 {05:04X}    #  44 : Bias XQP  /  45 : Bias XQN

dac_w 50 {06:04X} ;dac_w 51 {07:04X}    #  50 : Phase YP  /  51 : Phase YN
dac_w 52 {08:04X} ;dac_w 53 {09:04X}    #  52 : Bias YIP  /  53 : Bias YIN
dac_w 54 {10:04X} ;dac_w 55 {11:04X}    #  54 : Bias YQP  /  55 : Bias YQN
'''.format(
        int(float(COSA_data[54])/4.5*0xFFFF), int(float(COSA_data[55])/4.5*0xFFFF),   # XPP/XPN Quad Point
        int(float(COSA_data[46])/4.5*0xFFFF), int(float(COSA_data[47])/4.5*0xFFFF),   # XIP/XIN Null Point
        int(float(COSA_data[48])/4.5*0xFFFF), int(float(COSA_data[49])/4.5*0xFFFF),   # XQP/XQN Null Point
        int(float(COSA_data[56])/4.5*0xFFFF), int(float(COSA_data[57])/4.5*0xFFFF),   # YPP/YPN Quad Point
        int(float(COSA_data[50])/4.5*0xFFFF), int(float(COSA_data[51])/4.5*0xFFFF),   # YIP/YIN Null Point
        int(float(COSA_data[52])/4.5*0xFFFF), int(float(COSA_data[53])/4.5*0xFFFF))   # YQP/YQN Null Point

#CMD_DAC_SET = '''
#dac_w 40 {00:04X} ;dac_w 41 {01:04X}    #  40 : Phase XP  /  41 : Phase XN
#dac_w 42 {02:04X} ;dac_w 43 {03:04X}    #  42 : Bias XIP  /  43 : Bias XIN
#dac_w 44 {04:04X} ;dac_w 45 {05:04X}    #  44 : Bias XQP  /  45 : Bias XQN
#
#dac_w 50 {06:04X} ;dac_w 51 {07:04X}    #  50 : Phase YP  /  51 : Phase YN
#dac_w 52 {08:04X} ;dac_w 53 {09:04X}    #  52 : Bias YIP  /  53 : Bias YIN
#dac_w 54 {10:04X} ;dac_w 55 {11:04X}    #  54 : Bias YQP  /  55 : Bias YQN
#'''.format(
#        int(COSA_INIT[0] /4.5*0xFFFF), int(COSA_INIT[1] /4.5*0xFFFF),   # XPP/XPN Quad Point
#        int(COSA_INIT[2] /4.5*0xFFFF), int(COSA_INIT[3] /4.5*0xFFFF),   # XIP/XIN Null Point
#        int(COSA_INIT[4] /4.5*0xFFFF), int(COSA_INIT[5] /4.5*0xFFFF),   # XQP/XQN Null Point
#        int(COSA_INIT[6] /4.5*0xFFFF), int(COSA_INIT[7] /4.5*0xFFFF),   # YPP/YPN Quad Point
#        int(COSA_INIT[8] /4.5*0xFFFF), int(COSA_INIT[9] /4.5*0xFFFF),   # YIP/YIN Null Point
#        int(COSA_INIT[10]/4.5*0xFFFF), int(COSA_INIT[11]/4.5*0xFFFF))   # YQP/YQN Null Point

# 1.BIAS DAC P
# 2.BIAS DAC N
# 3.BIAS ADC P
# 4.BIAS ADC N
# 5.PD MONITOR (after VOA Low Imp.)
# 6.PD MONITOR (after VOA High Imp.)
# 7.PD MONITOR (before VOA Low Imp.)
CMD_MPD_SWEEP = '''
gpio_dbg w 51 0 > /dev/null
gpio_dbg w 52 1 > /dev/null
dac_w {0:02X} {2:04X} > /dev/null
dac_w {1:02X} {3:04X} > /dev/null
echo -n `dac_r {0:02X} h`,
echo -n `dac_r {1:02X} h`,
echo -n `adc_r {0:02X} h`,
echo -n `adc_r {1:02X} h`,
echo -n `adc_r 03 h`,
gpio_dbg w 52 0 > /dev/null
echo -n `adc_r 03 h`,
gpio_dbg w 51 1 > /dev/null
gpio_dbg w 52 1 > /dev/null
echo    `adc_r 03 h`'''

# Main -------------------------------------------------------------------------

if not os.path.isdir(r'./Log'):
    os.mkdir(r'./Log')

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(IP_Address, port = '22', username = 'root', password = 'root')

print('')
print('Config =========================================================================')
print(' IP Address     : {}'.format(IP_Address))
print(' COSA           : {}'.format(COSA))

time.sleep(2.0)
print('')
print('Bias Sweep =====================================================================')

_, stdout, _ = ssh.exec_command('m 20011800 8000')
for i in stdout:
    pass
time.sleep(2.0)

for i in SWEEP_CH:
    ch = [0x42, 0x44, 0x52, 0x54][i]
    print(' ch : {0} ({1:02X}, {2:02X})'.format(['XI', 'XQ', 'YI', 'YQ'][i], ch, ch+1))

    if i // 2 == 0:
        _, stdout, _ = ssh.exec_command('gpio_dbg w 53 1 > /dev/null') # Pol X
    elif i // 2 == 1:
        _, stdout, _ = ssh.exec_command('gpio_dbg w 53 0 > /dev/null') # Pol Y
    for _ in stdout:
        pass

    _, stdout, _ = ssh.exec_command(CMD_DAC_SET)
    for l in stdout:
        pass
    time.sleep(1.0)

    CMD = ''
    for DAC_P in np.arange(0, DAC_RANGE, DAC_STEP):
        DAC_N = 0xFFFF - DAC_P
        CMD += CMD_MPD_SWEEP.format(ch, ch+1, DAC_P, DAC_N)

    OUTPUT = []
    _, stdout, _ = ssh.exec_command(CMD)
    for l in stdout:
        OUTPUT.append(l.strip('\n'))

    FILENAME = './Log/20_MZC_Coarse_Setup_{}.txt'.format(['XI', 'XQ', 'YI', 'YQ'][i])
    print(' Output data : {}'.format(FILENAME))
    with open('{}'.format(FILENAME), 'w') as f:
        f.write('DAC_P,DAC_N,ADC_P,ADC_N,MPD_LO_out,MPD_HI_out,MPD_LO\n')
        for l in OUTPUT:
            f.write('{}\n'.format(l))

_, stdout, _ = ssh.exec_command(CMD_DAC_SET)
for _ in stdout:
    pass

