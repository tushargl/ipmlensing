import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path

import matplotlib.path as mpath


# STAR_DATAFRAME = pd.read_csv(sys.argv[1], header=None)
# print("/CRUX/LOG> LOADED DATAFRAME SHAPE:",STAR_DATAFRAME.shape)
# # print(STAR_DATAFRAME.loc[[0]])

# STAR_ARR = STAR_DATAFRAME.to_numpy()

# print("/CRUX/LOG> NUMPY ARRAY SHAPE:",STAR_ARR.shape)
# # print(STAR_ARR)


import numpy as np
import  mpl_toolkits.axisartist.angle_helper as angle_helper
import matplotlib.cm as cmap
from matplotlib.projections import PolarAxes
from matplotlib.transforms import Affine2D

from mpl_toolkits.axisartist import SubplotHost

from mpl_toolkits.axisartist import GridHelperCurveLinear


def curvelinear_test2(fig, rect=111):
    """
    polar projection, but in a rectangular box.
    """

    # see demo_curvelinear_grid.py for details
    tr = Affine2D().translate(0,90) + Affine2D().scale(np.pi/180., 1.) + PolarAxes.PolarTransform()

    extreme_finder = angle_helper.ExtremeFinderCycle(10, 60,
                                                     lon_cycle = 360,
                                                     lat_cycle = None,
                                                     lon_minmax = None,
                                                     lat_minmax = (-90, np.inf),
                                                     )

    grid_locator1 = angle_helper.LocatorHMS(12) #changes theta gridline count
    tick_formatter1 = angle_helper.FormatterHMS()

    grid_helper = GridHelperCurveLinear(tr,
                                        extreme_finder=extreme_finder,
                                        grid_locator1=grid_locator1,
                                        tick_formatter1=tick_formatter1
                                        )


    ax1 = SubplotHost(fig, rect, grid_helper=grid_helper)

    # make ticklabels of right and top axis visible.
    ax1.axis["right"].major_ticklabels.set_visible(True)
    ax1.axis["top"].major_ticklabels.set_visible(True)
    ax1.axis["bottom"].major_ticklabels.set_visible(True) #Turn off? 
    # let right and bottom axis show ticklabels for 1st coordinate (angle)
    ax1.axis["right"].get_helper().nth_coord_ticks=0
    ax1.axis["bottom"].get_helper().nth_coord_ticks=0



    fig.add_subplot(ax1)

    grid_helper = ax1.get_grid_helper()

    # You may or may not need these - they set the view window explicitly rather than using the
    # default as determined by matplotlib with extreme finder.
    ax1.set_aspect(1.)
    ax1.set_xlim(-4,25) # moves the origin left-right in ax1
    ax1.set_ylim(-3, 30) # moves the origin up-down

    ax1.set_ylabel('Declination')
    ax1.set_xlabel('Ascension')
    ax1.grid(True)
    #ax1.grid(linestyle='--', which='x') # either keyword applies to both
    #ax1.grid(linestyle=':', which='y')  # sets of gridlines

    return ax1,tr
    
    
def skip_comments(f):
    '''
    Read lines that DO NOT start with a # symbol.
    '''
    for line in f:
        if not line.strip().startswith('#'):
            yield line
            
def get_data_bb():
    '''RA, DEC data file.
    '''

    # Path to data file.
    out_file = 'test.dat'

    # Read data file
    with open(out_file) as f:
        ra, dec = [], []

        for line in skip_comments(f):
            ra.append(float(line.split()[0]))
            dec.append(float(line.split()[1]))

    return ra, dec


import matplotlib.pyplot as plt
fig = plt.figure(1, figsize=(5, 5))
fig.clf()

ax1, tr = curvelinear_test2(fig,121) # tr.transform_point((x, 0)) is always (0,0)
                            # => (theta, r) in but (r, theta) out...             

# Read RA, DEC data from file.
ra, dec = get_data_bb()
xx = zip(ra, dec)
for k in xx:
	print(k)
out_test = list(xx)

# Use this block to generate colored points with a colorbar.
cm = plt.cm.get_cmap('RdYlBu_r')
z = np.random.random((len(ra), 1))  # RGB values

SC = ax1.scatter(out_test[:,0], #ax1 is a global
            out_test[:,1],
            marker = 'o',
            c=z,
            cmap=cm,
            lw = 0.,
            zorder=9) #on top of gridlines
            
# Colorbar
cbar = plt.colorbar(SC, shrink=1., pad=0.1)
cbar.ax.tick_params(labelsize=8)
cbar.set_label('colorbar', fontsize=8)

ax2, tr = curvelinear_test2(fig,122) # tr.transform_point((x, 0)) is always (0,0)
                            # => (theta, r) in but (r, theta) out...             

# Read RA, DEC data from file.
ra, dec = get_data_bb()
out_test = tr.transform(zip(ra, dec))

# Use this block to generate colored points with a colorbar.
cm = plt.cm.get_cmap('RdYlBu_r')
z = np.random.random((len(ra), 1))  # RGB values

SC = ax2.scatter(out_test[:,0], #ax1 is a global
            out_test[:,1],
            marker = 'o',
            c=z,
            cmap=cm,
            lw = 0.,
            zorder=9) #on top of gridlines
            
# Colorbar
cbar = plt.colorbar(SC, shrink=1., pad=0.1)
cbar.ax.tick_params(labelsize=8)
cbar.set_label('colorbar', fontsize=8)

plt.show()