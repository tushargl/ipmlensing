import sys
import os

from astropy.table import Table, unique
import pyvo as vo
from astroquery.gaia import Gaia

import astropy.units as u
from astropy.coordinates import SkyCoord


def download_GAIA():
	coord = SkyCoord(ra=280, dec=-60, unit=(u.degree, u.degree), frame='icrs')
	width = u.Quantity(0.1, u.deg)
	height = u.Quantity(0.1, u.deg)
	r = Gaia.query_object_async(coordinate=coord, width=width, height=height)
	r.pprint()

# download_rawcands('.','test.fit')

download_GAIA()
