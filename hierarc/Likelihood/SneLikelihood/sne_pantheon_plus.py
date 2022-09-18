import os
import pandas as pd
import numpy as np
import hierarc

_PATH_2_DATA = os.path.join(os.path.dirname(hierarc.__file__), 'Data', 'SNe')


class PantheonPlusData(object):

    def __init__(self):
        self._data_file = os.path.join(_PATH_2_DATA, 'Pantheon+SH0ES', 'Pantheon+SH0ES.dat')
        self._cov_file = os.path.join(_PATH_2_DATA, 'Pantheon+SH0ES', 'Pantheon+SH0ES_STAT+SYS.cov')

        data = pd.read_csv(self._data_file, delim_whitespace=True)
        self.origlen = len(data)

        self.ww = (data['zHD'] > 0.01)

        self.zCMB = data['zHD'][self.ww].to_numpy()  # use the vpec corrected redshift for zCMB
        self.zHEL = data['zHEL'][self.ww].to_numpy()
        self.m_obs = data['m_b_corr'][self.ww].to_numpy()

        self.cov_mag_b = self.build_covariance()

    def build_covariance(self):
        """Run once at the start to build the covariance matrix for the data"""
        filename = self._cov_file

        # The file format for the covariance has the first line as an integer
        # indicating the number of covariance elements, and the the subsequent
        # lines being the elements.
        # This function reads in the file and the nasty for loops trim down the covariance
        # to match the only rows of data that are used for cosmology

        f = open(filename)
        line = f.readline()
        n = int(len(self.zCMB))
        C = np.zeros((n,n))
        ii = -1
        jj = -1
        mine = 999
        maxe = -999
        for i in range(self.origlen):
            jj = -1
            if self.ww[i]:
                ii += 1
            for j in range(self.origlen):
                if self.ww[j]:
                    jj += 1
                val = float(f.readline())
                if self.ww[i]:
                    if self.ww[j]:
                        C[ii,jj] = val
        f.close()
        return C
