# -*- coding: utf-8 -*-
from aloe import step
from aloe import world

import numpy

from quantarhei import energy_units
from quantarhei import CorrelationFunction
from quantarhei import Molecule
from quantarhei import Aggregate
from quantarhei.qm import RedfieldRelaxationTensor

@step(r'I calculate Redfield relaxation tensor')
def redfield_tensor(self):
    print("Redfield tensor calculation")

    
    #
    # Correlation function
    #
    params = {"ftype":    world.ctype,
              "reorg":    world.reorg,
              "cortime":  world.ctime,
              "T":        world.temp,
              "matsubara":world.mats}
              
    # FIXME: also time_units, temperature_units
    with energy_units(world.e_units):
        cf = CorrelationFunction(world.ta,params) 

    
    #
    # Homodimer
    #
    with energy_units(world.h_units):
        en = world.senergy
        m1 = Molecule("mol1", [0.0, en])
        m2 = Molecule("mol2", [0.0, en])
        
    m1.set_egcf((0,1), cf)
    m2.set_egcf((0,1), cf)
        
    agg = Aggregate("Homodimer",maxband=1)
    
    agg.add_Molecule(m1)
    agg.add_Molecule(m2)
    
#    with energy_units("1/cm"):
#        Hm = m1.get_Hamiltonian()
#        print(Hm)
#        print(m.convert_energy_2_current_u(Hm._data)) 
        
    with energy_units(world.r_units):
        agg.set_resonance_coupling(0,1,world.r_coupl)
        
    agg.build()
    
    H = agg.get_Hamiltonian()

#    with energy_units("1/cm"):
#        print(H)
#        print(m.convert_energy_2_current_u(H._data))    
    
    sbi = agg.get_SystemBathInteraction()
    
    RRT = RedfieldRelaxationTensor(H, sbi)
    
    world.K12 = numpy.real(RRT.data[1,1,2,2])