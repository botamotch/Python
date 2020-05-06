# -*- coding: utf-8 -*-

# Import -----------------------------------------------------------------------
import time

import toml
from paramiko import SSHClient, AutoAddPolicy

# Config - ---------------------------------------------------------------------

config = toml.load('module.toml')

IP_Address = config['common']['IP_MOD']
COSA       = config['common']['COSA']

# VALIABLES --------------------------------------------------------------------

HEATER_POWER_N = []
HEATER_POWER_P = []
HEATER_RESISTANCE_N = []
HEATER_RESISTANCE_P = []

POWER_OFFSET = []

# CMD --------------------------------------------------------------------------
# DACとRAM/EEPROMで並びが違うので注意

# DAC channel
#  40 : Phase XP  /  50 : Phase YP
#  41 : Phase XN  /  51 : Phase YN
#  42 : Bias XIP  /  52 : Bias YIP
#  43 : Bias XIN  /  53 : Bias YIN
#  44 : Bias XQP  /  54 : Bias YQP
#  45 : Bias XQN  /  55 : Bias YQN

# RAM/EEPROM Map
#  2001188C  /  0005F2 : BIAS XI
#  2001188E  /  000616 : BIAS XQ
#  20011890  /  00063A : BIAS YI
#  20011892  /  00065E : BIAS YQ
#  20011894  /  000682 : PHASE X
#  20011896  /  0006A6 : PHASE Y

CMD_DAC_SET = '''
dac_w 40 {0:04X} ;dac_w 41 {1:04X}
dac_w 42 {0:04X} ;dac_w 43 {1:04X}
dac_w 44 {0:04X} ;dac_w 45 {1:04X}

dac_w 50 {0:04X} ;dac_w 51 {1:04X}
dac_w 52 {0:04X} ;dac_w 53 {1:04X}
dac_w 54 {0:04X} ;dac_w 55 {1:04X}
'''

CMD_ADC_GET = '''
adc_r 40 h ;adc_r 41 h
adc_r 42 h ;adc_r 43 h
adc_r 44 h ;adc_r 45 h

adc_r 50 h ;adc_r 51 h
adc_r 52 h ;adc_r 53 h
adc_r 54 h ;adc_r 55 h
'''

# Main -------------------------------------------------------------------------

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
ssh.connect(IP_Address, port = '22', username = 'root', password = 'root')

print('')
print('Config =========================================================================')
print(' IP Address     : {}'.format(IP_Address))
print(' COSA           : {}'.format(COSA))

time.sleep(2.0)
print('')
print('HW Adjust ======================================================================')

print(' ABC Feedback OFF')
_, stdout, _ = ssh.exec_command('m 20011800 8000')
for i in stdout:
    pass

# P側 : 0xFFFF, N側 : 0x0000に設定してP側の電力を取得する
time.sleep(1.0)
print(' Get P side heater power')
_, stdout, _ = ssh.exec_command(CMD_DAC_SET.format(0xFFFF, 0x0000))
for i in stdout:
    pass

time.sleep(1.0)
_, stdout, _ = ssh.exec_command(CMD_ADC_GET)
for i, val in enumerate(stdout):
    if i % 2 == 0: # 奇数個目のADCを読む
        v_adc = 4.5*int(val, 16)/0xffff
        HEATER_POWER_P.append(4.5 * (4.5 - v_adc) / 10.0)
        HEATER_RESISTANCE_P.append(10.0 * 4.5 / (4.5 - v_adc))

# P側 : 0x0000, N側 : 0xFFFFに設定してN側の電力を取得する
time.sleep(1.0)
print(' Get N side heater power')
_, stdout, _ = ssh.exec_command(CMD_DAC_SET.format(0x0000, 0xFFFF))
for i in stdout:
    pass

time.sleep(1.0)
_, stdout, _ = ssh.exec_command(CMD_ADC_GET)
for i, val in enumerate(stdout):
    if i % 2 == 1: # 偶数個目のADCを読む
        v_adc = 4.5*int(val, 16)/0xffff
        HEATER_POWER_N.append(4.5 * (4.5 - v_adc) / 10.0)
        HEATER_RESISTANCE_N.append(10.0 * 4.5 / (4.5 - v_adc))

# 最後に0x0000に戻す
_, stdout, _ = ssh.exec_command(CMD_DAC_SET.format(0x0000, 0x0000))
for i in stdout:
    pass

print('')
print('Power Offset =================================================================')

for i in range(6):
    larger_power = min([HEATER_POWER_P[i], HEATER_POWER_N[i]]) / 2.0 * 1e+6 # [uW]
    POWER_OFFSET.append(int(larger_power))

print('  PHASE X : {0:04X} ({0} uW)'.format(POWER_OFFSET[0]))
print('  BIAS XI : {0:04X} ({0} uW)'.format(POWER_OFFSET[1]))
print('  BIAS XQ : {0:04X} ({0} uW)'.format(POWER_OFFSET[2]))
print('  PHASE Y : {0:04X} ({0} uW)'.format(POWER_OFFSET[3]))
print('  BIAS YI : {0:04X} ({0} uW)'.format(POWER_OFFSET[4]))
print('  BIAS YQ : {0:04X} ({0} uW)'.format(POWER_OFFSET[5]))
print('  VOA X   : ---- ( -  uW)')
print('  VOA Y   : ---- ( -  uW)')
time.sleep(2.0)

print('')
print('RAM/EEPROM command ===========================================================')

LOGFILE = './Log/10_HW_setup_write.txt'
print(' write command : {}'.format(LOGFILE))
print('')
f = open(LOGFILE, 'w')

for (i,b) in enumerate(POWER_OFFSET[1:3] + POWER_OFFSET[4:6] + POWER_OFFSET[0:1] + POWER_OFFSET[3:4]):
    f.write('m {0:08X} {1:04X}\n'.format(0x2001188C + i*0x02, b))

for (i,b) in enumerate(POWER_OFFSET[1:3] + POWER_OFFSET[4:6] + POWER_OFFSET[0:1] + POWER_OFFSET[3:4]):
    f.write('eepf_wle {0:06X} {1:04X}\n'.format(0x0005F2 + i*0x24, b))

f.close()

