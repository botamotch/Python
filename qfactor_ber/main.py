from math import erfc, sqrt, log10
import matplotlib.pyplot as plt

FILENAME = 'output.pdf'
X_MAX, X_MIN = 18, 2
Y_MAX, Y_MIN = 1, 15

fig = plt.figure(figsize=(6, 7), dpi=100)
axs = fig.add_subplot(1, 1, 1)
line, = axs.plot([], [], linestyle='--', marker='o')
axs.grid(linestyle='--', linewidth=0.5, color='gray')

qfactor = [i*2 for i in range (1, 11)]
ber = [0.5*erfc(10**(q/20.0)/sqrt(2.0)) for q in qfactor]

line.set_data(qfactor, [abs(log10(b)) for b in ber])

axs.set_yscale('log')
axs.set_xlim((X_MIN, X_MAX))
axs.set_ylim((abs(log10(0.1**Y_MIN)), abs(log10(0.1**Y_MAX))))
axs.set_xlabel('Q-factor [dB]')
axs.set_ylabel('BER')
axs.set_yticks([abs(log10(0.1**i)) for i in range(Y_MAX, Y_MIN)])
axs.set_yticklabels([r'$10^{' + r'{0:d}'.format(i) + r'}$' for i in range(Y_MAX, Y_MIN)])

# fig.savefig(FILENAME)
# print('> save to {0}'.format(FILENAME))
plt.show()

