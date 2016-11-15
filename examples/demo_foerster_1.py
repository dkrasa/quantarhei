# -*- coding: utf-8 -*-
"""

    Propagation with Foerster theory using Aggregate object




"""


import numpy

from quantarhei import *
import quantarhei as qm

import matplotlib.pyplot as plt

print("""
*******************************************************************************
*                                                                             *
*                         Foerster Theory Demo                                *
*                                                                             *                  
*******************************************************************************
""")

time = TimeAxis(0.0, 5000, 1.0)
with energy_units("1/cm"):

    m1 = Molecule("Mol 1", [0.0, 10100.0])
    m2 = Molecule("Mol 2", [0.0, 10050.0])
    m3 = Molecule("Mol 3", [0.0, 10000.0])
    
    
    m1.position = [0.0, 0.0, 0.0]
    m2.position = [15.0, 0.0, 0.0]
    m3.position = [10.0, 10.0, 0.0]
    m1.set_dipole(0,1,[5.8, 0.0, 0.0])
    m2.set_dipole(0,1,[5.8, 0.0, 0.0])
    m3.set_dipole(0,1,[numpy.sqrt(12.0), 0.0, 0.0])
    agg = Aggregate("Trimer")
    agg.add_Molecule(m1)
    agg.add_Molecule(m2)
    agg.add_Molecule(m3)
    
#    m4 = Molecule("Mol 4", [0.0, 11000.0])
#    m5 = Molecule("Mol 5", [0.0, 11000.0])   
#    m4.position = [15.0, 15.0, 0.0]
#    m5.position = [15.0, 10.0, 0.0]
#    m4.set_dipole(0,1,[5.8, 0.0, 0.0])
#    m5.set_dipole(0,1,[5.8, 0.0, 0.0])
#    agg.add_Molecule(m4)
#    agg.add_Molecule(m5)
    
    agg.set_coupling_by_dipole_dipole()

    params = dict(ftype="OverdampedBrownian", reorg=20, cortime=100, T=300)
    cf = CorrelationFunction(time, params)

m1.set_transition_environment((0,1), cf)
m2.set_transition_environment((0,1), cf)
m3.set_transition_environment((0,1), cf)

#m4.set_transition_environment((0,1), cf)
#m5.set_transition_environment((0,1), cf)

agg.build()

H = agg.get_Hamiltonian()
with energy_units("1/cm"):
    print(H)

#
# Aggregate object can return a propagator
#
prop_Foerster = agg.get_ReducedDensityMatrixPropagator(time,
                           relaxation_theory="standard_Foerster")   

#
# Initial density matrix
#
shp = 4
rho_i1 = ReducedDensityMatrix(dim=shp, name="Initial DM")
rho_i1.data[shp-2,shp-2] = 1.0   
   
#
# Propagation of the density matrix
#   
rho_t1 = prop_Foerster.propagate(rho_i1,
                                 name="Foerster evolution from aggregate")
rho_t1.plot(coherences=False, axis=[0,4000.0,0,1.0])

#
# Thermal excited state to compare with
#
rho0 = agg.get_DensityMatrix(condition_type="thermal_excited_state",
                             relaxation_theory_limit="strong_coupling",
                             temperature=300)
 
#with eigenbasis_of(H):
if True:       
    pop = numpy.zeros((time.length,shp),dtype=numpy.float64)
    for i in range(1, H.dim):
        pop[:,i] = numpy.real(rho0.data[i,i]) 

    # plot the termal distrubution
    plt.plot(time.data,pop[:,1],'--r')
    plt.plot(time.data,pop[:,2],'--b')
    plt.plot(time.data,pop[:,3],'--g')  
