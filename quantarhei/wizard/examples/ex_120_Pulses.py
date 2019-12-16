"""
Usage of finite transform limited pulses


"""
import quantarhei as qr
import matplotlib.pyplot as plt

lab = qr.LabSetup()
freq = qr.FrequencyAxis(-2500, 1000, 5.0)
pulse2 = dict(ptype="Gaussian", FWHM=800.0, amplitude=1.0)
params = (pulse2, pulse2, pulse2)
lab.set_pulse_shapes(freq, params)

freq2 = qr.FrequencyAxis(-1000, 100, 20.0)

dfc1 = lab.get_pulse_spectrum(1, freq.data)
dfc2 = lab.get_pulse_spectrum(1, freq2.data)
pl1 = plt.plot(freq.data, dfc1)
pl2 = plt.plot(freq2.data, dfc2)
plt.show()
