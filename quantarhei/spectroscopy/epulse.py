"""

Electric field for laser pulse simulation

"""

import numpy
from ..core.dfunction import  DFunction
from .. import REAL


class EField(DFunction):
    """Object representing laser pulse electric field


    Parameters
    ----------

    x: qr.TimeAxis
        Time axis specifying time points on which electric field is defined

    y: numpy.array
        Values of electric field in the given time points

    omega: real
        circular frequency of the electric field

    rwa: real
        rotating wave approximation frequency

    t0: real
        Start of the time axis (phase time of the field)

    polarization: real vector
        Polarization vector of the electric field

    """

    def __init__(self, x, y, omega, rwa=0.0, t0=0.0,
                 polarization=numpy.array([1.0,0.0,0.0],dtype=REAL)):
        super().__init__(x, y)
        if omega < 0.0:
            raise Exception("Frequency must be positive.")
        self.omega = omega
        self.t0 = t0
        self.rwa = rwa
        self._data = numpy.zeros(len(y), dtype=y.dtype)
        self._data[:] = self.data[:]
        self._update_data()


    def set_rwa(self, rwa):
        """Sets rotating wave approximation frequency
        """
        self.rwa = rwa
        self._update_data()


    def _update_data(self):
        """Updates data to reflect the pulse frequency
        """
        self.data = self._data*\
        numpy.exp(-1j*(self.omega-self.rwa)*(self.axis.data - self.t0))


    def reset_to_envelop(self):
        """Resents the data to represent envelop of the pulse
        """
        self.data = self._data


    def get_envelop(self):
        """Returns the pulse envelop
        """
        return self._data
