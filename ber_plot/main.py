# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# import matplotlib
# matplotlib.use('WXAgg')

DUT = 'BxxX-xx'

pp = PdfPages('output_multiple.pdf')

class BER_Plot:
    def __init__(self):
        self.fig, self.axs = plt.subplots(1, 2,figsize=(12, 7),dpi=100)

        self.axs[0].set_xlim((20, 40))
        self.axs[0].set_xlabel('OSNR [dB]')
        self.axs[0].set_yscale('log')
        self.axs[0].set_ylim((1.0e-4, 1.0e-1))
        self.axs[0].set_ylabel('PreFEC BER')
        self.axs[0].grid(linestyle='--', linewidth=0.5, color='gray')
        self.axs[1].xaxis.set_visible(False)
        self.axs[1].yaxis.set_visible(False)

        self.axs_post = self.axs[0].twinx()
        self.axs_post.set_yscale('log')
        self.axs_post.set_ylim((1.0e-12, 1.0e-1))
        self.axs_post.set_ylabel('PostFEC BER')

fig, axs = plt.subplots(1, 2,figsize=(12, 7),dpi=100)

axs[0].set_xlim((20, 40))
axs[0].set_xlabel('OSNR [dB]')
axs[0].set_yscale('log')
axs[0].set_ylim((1.0e-4, 1.0e-1))
axs[0].set_ylabel('PreFEC BER')
axs[0].grid(linestyle='--', linewidth=0.5, color='gray')
axs[1].xaxis.set_visible(False)
axs[1].yaxis.set_visible(False)

axs_post = axs[0].twinx()
axs_post.set_yscale('log')
axs_post.set_ylim((1.0e-12, 1.0e-1))
axs_post.set_ylabel('PostFEC BER')

with open('log.txt', 'r') as f:
    _ = f.readline()
    DATA = [ l.strip('\n').split(',') for l in f.readlines() ]

OSNR = []
PreFEC_BER  = []
PostFEC_BER = []

for i, l in enumerate(DATA):
    if DATA[i] == ['']:
        DATE      = DATA[i-1][0].strip()
        FREQUENCY = DATA[i-1][1].strip()
        PIN       = DATA[i-1][2].strip()

        _ = axs[0].plot(OSNR, PreFEC_BER, linestyle='-', marker='.',label='PreFEC BER, Pin={}'.format(PIN))
        _ = axs_post.plot(OSNR, PostFEC_BER, linestyle='--', marker='x',label='PostFEC BER, Pin={}'.format(PIN))

        if DATA[i+1] == ['']:
            _ = axs[0].set_title('{0}, {1}[THz] ({2})'.format(DUT, FREQUENCY, DATE))
            handler1, label1 = axs[0].get_legend_handles_labels()
            handler2, label2 = axs_post.get_legend_handles_labels()
            axs[0].legend(handler1 + handler2, label1 + label2, loc='upper right', borderaxespad=0.5)

            pp.savefig(fig)
            # continue
            break
        else:
            OSNR = []
            PreFEC_BER  = []
            PostFEC_BER = []
            continue
    try:
        OSNR.append(float(DATA[i][3]))
    except ValueError:
        continue

    try:
        PreFEC_BER.append(float(DATA[i][4]))
    except ValueError:
        PreFEC_BER.append(1.0)

    try:
        if float(DATA[i][5]) == 0.0:
            PostFEC_BER.append(1.0e-12)
        else:
            PostFEC_BER.append(float(DATA[i][5]))
    except ValueError:
        PostFEC_BER.append(1.0)

pp.close()

