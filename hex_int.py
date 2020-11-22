# -*- Coding: utf-8 -*-

'''
整数と16進数の変換
正：最上位ビットが0
負：最上位ビットが1, 二進数における補数がその数の絶対値を表す
'''

print('')
print('# Int to Hex')

for val in [100,-100]:
    print('  INT : {0:6d} > HEX : {1:04X}'.format(val, val if val > 0 else 0x10000+val))

print('')
print('# Hex to Int')

for val in ['0064','FF9C']:
    print('  HEX : {0} > INT : {1:6d}'.format( val, int(val,16)-0x10000 if int(val,16) >> 15 else int(val,16) ))

# print('')
# print('{0:04X}'.format(0xFF9C + 200))

