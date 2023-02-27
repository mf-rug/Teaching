import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

# Define directory
directory = '/Users/max/Downloads/eugokineticsfiles25200umsubstrate/mockdata/'

#import data
df = pd.read_csv(f"{directory}/result.csv")

# define x and y data
reaction_rate = df['s-1']
sub_conc = df['conc']

# make large dummy data for plotting the fitted curve
sub_conc_dense = np.linspace(0, max(sub_conc)*100, 10000)

# define MM formula and extract the data
def michaelis_menten(sub_conc, kcat, Km):
    return (kcat * sub_conc) / (Km + sub_conc)

parameters, _ = curve_fit(michaelis_menten, sub_conc, reaction_rate, bounds =(0, np.inf))
kcat, Km = parameters

# Plot the data points and the fitted curve
plt.plot(sub_conc, reaction_rate, 'ko', label='data')
plt.plot(sub_conc_dense, michaelis_menten(sub_conc_dense, kcat, Km), 'r', label='fit')
plt.xlabel('Substrate concentration')
plt.ylabel('Reaction rate')

# set axis limits slightly beyond the biggest measurement or parameter
plt.xlim(0, 1.1 * max(sub_conc.tolist() + [Km]))
plt.ylim(0, 1.1 *  max(reaction_rate.tolist() + [kcat]))

# Add a dashed vertical line for Km
intersection = np.argwhere(np.diff(np.sign(sub_conc_dense - [Km] *10000))).flatten()
y_of_Km = michaelis_menten(sub_conc_dense[intersection], kcat, Km)
plt.vlines(x=Km, ymin=0, ymax=y_of_Km, linestyle='dashed', label='Km', colors ='grey')

# Annotate Km
plt.text(Km * 1.1, y_of_Km / 2, 'Km = {:.3f}'.format(Km), ha='left', va='bottom')

# Add a dashed horizontal line for kcat
plt.hlines(y=kcat, xmin=0, xmax=max(xvals) * 1.1, linestyle='dashed', label='kcat', colors ='grey')

# Annotate kcat
plt.text(max(sub_conc) /2, kcat, 'kcat = {:.3f}'.format(kcat), ha='center', va='bottom')

plt.show()
