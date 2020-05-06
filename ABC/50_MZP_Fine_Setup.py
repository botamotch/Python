# -*- coding: utf-8 -*-

# Import -----------------------------------------------------------------------

import os
import time

import numpy as np
import toml
from paramiko import SSHClient, AutoAddPolicy

# Config - ---------------------------------------------------------------------

config = toml.load('module.toml')

IP_ADDRESS = config['common']['IP_MOD']
COSA       = config['common']['COSA']

POWER_RANGE = 12.0 #[mW]
POWER_SKIP  =  0.2 #[mW]

SWEEP_CH = [4,5]

# CMD --------------------------------------------------------------------------

BIAS_SET  = 0x20011880
ABC_STATE = 0x2001180C
ERROR_MON = 0x20011A00
MPD_MON   = 0x20011AC4
BIAS_MON  = 0x20011AD0
DIFF_MON  = 0x20011A54

CMD_BIAS_SWEEP = '''
m {0:08X} {1:04X} > /dev/null
sleep 0.5
echo -n `d {2:08X} 2 1`,
echo -n `d {3:08X} 2 1`,
echo -n `d {4:08X} 2 1`,
echo -n `d {5:08X} 2 1`,
echo    `d {6:08X} 2 1` '''
CMD_BIAS_BOL_SET = '''
gpio_dbg w 51 0
gpio_dbg w 52 0
m 20011800 8001

m 2001180C 8012
m 2001180E 8012
m 20011810 8012
m 20011812 8012
m 20011814 8012
m 20011816 8012'''
CMD_BIAS_BOL_GET = '''
d 200151F0 2 1
d 20015214 2 1
d 20015238 2 1
d 2001525C 2 1
d 20015280 2 1
d 200152A4 2 1'''

# Main -------------------------------------------------------------------------

if not os.path.isdir(r'./Log'):
    os.mkdir(r'./Log')

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(IP_ADDRESS, port = '22', username = 'root', password = 'root')

print('')
print('Config =========================================================================')
print(' IP Address     : {}'.format(IP_ADDRESS))
print(' COSA           : {}'.format(COSA))

time.sleep(2.0)
print('')
print('Bias Sweep =====================================================================')

# BIAS_BOL_HEX = ['E4FE', '0DB6', 'F123', '1581', '0000', '0000']
# BIAS_BOL_INT = [(int(x_hex,16) & 0x7FFF) - 0x8000 * (int(x_hex,16) >> 15) for x_hex in BIAS_BOL_HEX]
BIAS_BOL_INT = []

_, stdout, _ = ssh.exec_command(CMD_BIAS_BOL_GET)
for l in stdout:
    x_hex = l.strip()
    BIAS_BOL_INT.append((int(x_hex,16) & 0x7FFF) - 0x8000 * (int(x_hex,16) >> 15))

for i in SWEEP_CH:
    ch = ['XI','XQ','YI','YQ','X','Y'][i]
    print(' {} ch'.format(ch))

    _, stdout, _ = ssh.exec_command(CMD_BIAS_BOL_SET)
    for _ in stdout:
        pass

    CMD = ''
    for p in np.arange(-POWER_RANGE, POWER_RANGE, POWER_SKIP):
        b_int = int(BIAS_BOL_INT[i] + p/2.0*1000) # Power [1/2 uW]

        if i == 4:
            DIFF_MON1 = DIFF_MON + 2*i
            DIFF_MON2 = DIFF_MON + 2*i + 2
        elif i == 5:
            DIFF_MON1 = DIFF_MON + 2*i + 2
            DIFF_MON2 = DIFF_MON + 2*i + 4

        CMD += CMD_BIAS_SWEEP.format(
                BIAS_SET  + 2*i,
                b_int if b_int >= 0 else 0x10000 + b_int,
                ERROR_MON + 2*i,
                DIFF_MON1,
                DIFF_MON2,
                MPD_MON   + 2*i,
                BIAS_MON  + 2*i)

    OUTPUT = []
    _, stdout, _ = ssh.exec_command(CMD)
    for l in stdout:
        OUTPUT.append(l.replace(' ', '').strip('\n'))

    FILENAME = './Log/50_MZP_Fine_Setup_{}.txt'.format(ch)
    print(' Output data : {}'.format(FILENAME))
    with open('{}'.format(FILENAME), 'w') as f:
        f.write('ERROR_MON,DIFF_MON1,DIFF_MON2,MPD_MON,BIAS_MON\n')
        for l in OUTPUT:
            f.write('{}\n'.format(l))

_, stdout, _ = ssh.exec_command(CMD_BIAS_BOL_SET)
for _ in stdout:
    pass

