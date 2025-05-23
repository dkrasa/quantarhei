# -*- coding: utf-8 -*-
import numpy


from ..qm.hilbertspace.hamiltonian import Hamiltonian
from ..qm.liouvillespace.heom import KTHierarchy
from ..qm.liouvillespace.heom import KTHierarchyPropagator
from ..core.managers import eigenbasis_of
from ..core.managers import energy_units
from ..qm import SelfAdjointOperator
from ..qm import ReducedDensityMatrix
from ..core.dfunction import DFunction
from ..core.units import kB_intK
from .. import REAL
from .. import COMPLEX

class OpenSystem:
    """The class representing a general open quantum system
    
    It provides routines to store and extract the most interesting
    characteristics of an open qwuantum system, such as the Hamiltonian,
    SystemBathInteraction object, relaxation tensor and the reduced density
    matrix evolution.
    
    
    """
    
    def __init__(self):
        
        self._built = False
        
        self.RelaxationTensor = None
        self.RelaxationHamiltonian = None
        self._has_relaxation_tensor = False
        self._relaxation_theory = "standard_Redfield"
        self.has_Iterm = False
        
        self.Nel = 0
        self.Ntot = 0
        
        self.which_band = None

        self.mult = 0
        
        self.WPM = None # weighted participation matrix (for spectroscopy)
        self._has_wpm = False
        

    def diagonalize(self):
        """Diagonalizes the Hamltonian of the system 
        
        
        The routine calculates eigenenergies, transformation matrix and
        other properties of the system to be used in other calculations.
        
        """
        raise Exception("diagonalize() is not implemented.")


    def get_Hamiltonian(self):
        """Returns the system Hamiltonian 
        
        
        This is a method to be implemented by the particular system
        
        """
        raise Exception("get_Hamiltonian() is not implemented.")


    def get_band(self, band=1):
        """Returns indices of all states in a given band
        
        """
        raise Exception("get_band() is not implemented.")
    

    def get_RWA_suggestion(self):
        """Returns average transition energy

        Average transition energy of the monomer as a suggestion for
        RWA frequency

        """
        raise Exception("get_RWA_suggestion() is not implemented.")


    def get_lineshape_functions(self):
        """Returns lineshape functions defined for this system
        
        """
        sbi = self.get_SystemBathInteraction()
        return sbi.get_goft_storage()


    def map_lineshape_to_states(self, mpx):
        """Maps the participation matrix on g(t) functions storage
        
        This should work for a simple mapping matrix and first excited band.
        Specialized mapping such as those for 2 exciton states is implemented
        in classes that inherite from here.
        
        """

        ss = self.SS
        Ng = self.Nb[0]
        Ne1 = self.Nb[1] + Ng
        
        if self.mult > 1:
            raise Exception("Participation matrix not implemented for"+
                            "multiplicity higher than mult=1.")

        WPM = numpy.einsum("na,nb,ni->abi",ss[Ng:Ne1,Ng:Ne1]**2,
                                           ss[Ng:Ne1,Ng:Ne1]**2,mpx) 
            
        return WPM
    

    def get_weighted_participation(self):
        """Returns a participation matrix weighted by the mapping onto g(t) storage
        
        
        """
        self.diagonalize()
        
        if self._has_wpm:
            return self.WPM
        
        # mapping of the function storage
        gg = self.get_lineshape_functions()
        mpx = gg.get_mapping_matrix()

        # here we get the mapping of energy gap correlation functions to states
        self.WPM = self.map_egcf_to_states(mpx)
        self._has_wpm = True               
        
        return self.WPM


    def get_eigenstate_energies(self):
        """Returns the energies of the system's eigenstates
        
        """
        self.diagonalize()
        
        return self.HD


    def get_F4d(self, which="bbaa"):
        """Get vector of transition dipole moments for 4 wave-mixing 
        
        F4 is one of the vectors/matrices needed for orientational average
        of the third order non-linear signal.
        
        Parameters
        ----------
        
        which : string
            A string characterizing the type of dipole moment product
            
        """
        
        def DD(aa,bb):
            return numpy.dot(self.DD[aa[1],aa[0]],self.DD[bb[1],bb[0]])
        
        def _setF4(F4, x1, x2, x3, x4):
            F4[0] = DD(x4,x3)*DD(x2,x1)
            F4[1] = DD(x4,x2)*DD(x3,x1)
            F4[2] = DD(x4,x1)*DD(x3,x2) 
        
        gg = 0
        Ng = self.Nb[0]
        band1 = self.get_band(1)
        N1b = self.Nb[1] 
        if self.mult > 1:
            band2 = self.get_band(2)
            N2b = self.Nb[2]
            
        if which == "abba":
            F4 = numpy.zeros((N1b,N1b,3), dtype=REAL)
            for aa in band1:
                a = aa - Ng
                for bb in band1:
                    b = bb - Ng
                    _setF4(F4[a,b,:],(aa,gg),(bb,gg),(bb,gg),(aa,gg))
                    
            
        elif which == "baba":
            F4 = numpy.zeros((N1b,N1b,3), dtype=REAL)
            for aa in band1:
                a = aa - Ng
                for bb in band1:
                    b = bb - Ng
                    _setF4(F4[a,b],(aa,gg),(bb,gg),(aa,gg),(bb,gg))
                    
        elif which == "bbaa":
            F4 = numpy.zeros((N1b,N1b,3), dtype=REAL)
            for aa in band1:
                a = aa - Ng
                for bb in band1:
                    b = bb - Ng
                    _setF4(F4[a,b,:],(aa,gg),(aa,gg),(bb,gg),(bb,gg))
                    
        elif which == "fbfaba":
            F4 = numpy.zeros((N2b,N1b,N1b,3), dtype=REAL)
            for aa in band1:
                a = aa - Ng
                for bb in band1:
                    b = bb - 1
                    for ff in band2:
                        f = ff - Ng - N1b
                        _setF4(F4[f,a,b,:],(aa,gg),(bb,gg),(ff,aa),(ff,bb))
                    
        elif which == "fafbba":
            F4 = numpy.zeros((N2b,N1b,N1b,3), dtype=REAL)    
            for aa in band1:
                a = aa - Ng
                for bb in band1:
                    b = bb - Ng
                    for ff in band2:
                        f = ff - Ng - N1b
                        _setF4(F4[f,a,b,:], (aa,gg), (bb,gg), (ff,bb), (ff,aa)) 
                        
        elif which == "fbfbaa":
            F4 = numpy.zeros((N2b,N1b,N1b,3), dtype=REAL)    
            for aa in band1:
                a = aa - Ng
                for bb in band1:
                    b = bb - Ng
                    for ff in band2:
                        f = ff - Ng - N1b
                        _setF4(F4[f,a,b,:], (aa,gg), (aa,gg), (ff,bb), (ff,bb)) 
                    
        return F4
        

    def get_SystemBathInteraction(self):
        """Returns the aggregate SystemBathInteraction object

        """
        if self._built:
            return self.sbi
        else:
            raise Exception("The object not built.")       
    
    

    def get_RelaxationTensor(self, timeaxis,
                       relaxation_theory=None,
                       as_convolution_kernel=False,
                       time_dependent=False,
                       secular_relaxation=False,
                       relaxation_cutoff_time=None,
                       coupling_cutoff=None,
                       recalculate=True,
                       as_operators=False):
        """Returns a relaxation tensor corresponding to the system


        Parameters
        ----------

        timeaxis : TimeAxis
            Time axis of the relaxation tensor calculation. It has to be
            compatible with the time axis of the correlation functions

        relaxation_theory: str
            One of the available relaxation theories

        time_dependent : boolean
            Should the relaxation tensor time dependent?

        secular_relaxation :
            Should the tensor be secular?


        Returns
        -------

        RR : RelaxationTensor
            Relaxation tensor of the aggregate

        ham : Hamiltonian
            Hamiltonian corresponding to the aggregate, renormalized by
            the system-bath interaction


        """

        from ..qm import RedfieldRelaxationTensor
        from ..qm import TDRedfieldRelaxationTensor
        from ..qm import ModRedfieldRelaxationTensor
        from ..qm import TDModRedfieldRelaxationTensor
        from ..qm import FoersterRelaxationTensor
        from ..qm import TDFoersterRelaxationTensor
        from ..qm import NEFoersterRelaxationTensor
        from ..qm import RedfieldFoersterRelaxationTensor
        from ..qm import TDRedfieldFoersterRelaxationTensor
        from ..qm import LindbladForm

        from ..core.managers import eigenbasis_of

        if self._built:
            ham = self.get_Hamiltonian()
            sbi = self.get_SystemBathInteraction()
        else:
            raise Exception()

        #
        # Dictionary of available theories
        #
        theories = dict()
        theories[""] = [""]
        theories["standard_Redfield"] = ["standard_Redfield","stR","Redfield",
                                         "CLME2","QME"]
        theories["standard_Foerster"] = ["standard_Foerster","stF","Foerster"]
        theories["combined_RedfieldFoerster"] = ["combined_RedfieldFoerster",
                                                 "cRF","Redfield-Foerster"]
        theories["noneq_Foerster"] = ["noneq_Foerster", "neF"]
        
        #
        # Future
        #
        theories["modified_Redfield"] = ["modifield_Redfield", "mR"]
        theories["noneq_modified_Redfield"] = ["noneq_modified_Redfield",
                                               "nemR"]
        theories["generalized_Foerster"] = ["generalized_Foerster", "gF",
                                            "multichromophoric_Foerster"]
        theories["combined_WeakStrong"] = ["combined_WeakStrong", "cWS"]
        theories["Lindblad_form"] = ["Lindblad_form", "Lf"]
        theories["electronic_Lindblad"] = ["electronic_Lindblad", "eLf"]

        #if ((not recalculate) and
        #    (relaxation_theory in theories[self._relaxation_theory])):
        #    return self.RelaxationTensor, self.RelaxationHamiltonian


        if relaxation_theory in theories["standard_Redfield"]:

            if time_dependent:

                # Time dependent standard Refield

                ham.protect_basis()
                with eigenbasis_of(ham):
                    relaxT = TDRedfieldRelaxationTensor(ham, sbi,
                                        cutoff_time=relaxation_cutoff_time,
                                        as_operators=as_operators)
                    if secular_relaxation:
                        relaxT.secularize()
                ham.unprotect_basis()

            else:

                # Time independent standard Refield


                ham.protect_basis()

                with eigenbasis_of(ham):
                    relaxT = RedfieldRelaxationTensor(ham, sbi,
                                                    as_operators=as_operators)

                    if secular_relaxation:
                        relaxT.secularize()

                ham.unprotect_basis()


            self.RelaxationTensor = relaxT
            self.RelaxationHamiltonian = ham
            self._has_relaxation_tensor = True
            self._relaxation_theory = "standard_Redfield"

            return relaxT, ham

        elif relaxation_theory in theories["modified_Redfield"]:

            if time_dependent:

                # Time dependent standard Refield

                ham.protect_basis()
                with eigenbasis_of(ham):
                    relaxT = TDModRedfieldRelaxationTensor(ham, sbi,
                                        cutoff_time=relaxation_cutoff_time,
                                        as_operators=as_operators)
                    if secular_relaxation:
                        relaxT.secularize()
                ham.unprotect_basis()

            else:

                # Time independent standard Refield


                ham.protect_basis()

                with eigenbasis_of(ham):
                    relaxT = ModRedfieldRelaxationTensor(ham, sbi,
                                                    as_operators=as_operators)

                    if secular_relaxation:
                        relaxT.secularize()

                ham.unprotect_basis()


            self.RelaxationTensor = relaxT
            self.RelaxationHamiltonian = ham
            self._has_relaxation_tensor = True
            self._relaxation_theory = "modified_Redfield"

            return relaxT, ham


        elif relaxation_theory in theories["standard_Foerster"]:

            if time_dependent:

                # Time dependent standard Foerster
                relaxT = TDFoersterRelaxationTensor(ham, sbi)
                dat = numpy.zeros((ham.dim,ham.dim),dtype=REAL)
                for i in range(ham.dim):
                    dat[i,i] = ham._data[i,i]
                ham_0 = Hamiltonian(data=dat)
                ham_0.set_rwa(ham.rwa_indices)

            else:

                # Time independent standard Foerster

                #
                # This is done strictly in site basis
                #

                relaxT = FoersterRelaxationTensor(ham, sbi, 
                                                  pure_dephasing=True)
                dat = numpy.zeros((ham.dim,ham.dim),dtype=REAL)
                for i in range(ham.dim):
                    dat[i,i] = ham._data[i,i]
                ham_0 = Hamiltonian(data=dat)
                ham_0.set_rwa(ham.rwa_indices)

            # The Hamiltonian for propagation is the one without
            # resonance coupling
            self.RelaxationTensor = relaxT
            self.RelaxationHamiltonian = ham_0
            self._has_relaxation_tensor = True
            self._relaxation_theory = "standard_Foerster"

            return relaxT, ham_0

        elif relaxation_theory in theories["noneq_Foerster"]:

            if time_dependent:


                # Time dependent standard Foerster
                relaxT = NEFoersterRelaxationTensor(ham, sbi, 
                                            as_kernel=as_convolution_kernel)
                
                
                dat = numpy.zeros((ham.dim,ham.dim),dtype=REAL)
                
                #for i in range(ham.dim):
                #    dat[i,i] = ham._data[i,i]
                
                ham_0 = Hamiltonian(data=dat)
                
                # this type of theory has an inhomogeneous term
                self.has_Iterm = True

            else:

                # Fixme Check that it makes sense to have here
                # the time-independent theory !!!
                # Time independent standard Foerster

                #
                # This is done strictly in site basis
                #

                relaxT = FoersterRelaxationTensor(ham, sbi)
                dat = numpy.zeros((ham.dim,ham.dim),dtype=REAL)
                for i in range(ham.dim):
                    dat[i,i] = ham._data[i,i]
                ham_0 = Hamiltonian(data=dat)

            # The Hamiltonian for propagation is the one without
            # resonance coupling
            self.RelaxationTensor = relaxT
            self.RelaxationHamiltonian = ham_0
            self._has_relaxation_tensor = True
            self._relaxation_theory = "noneq_Foerster"

            return relaxT, ham_0

        elif relaxation_theory in theories["combined_RedfieldFoerster"]:

            if time_dependent:

                # Time dependent combined tensor
                ham.subtract_cutoff_coupling(coupling_cutoff)
                ham.protect_basis()
                with eigenbasis_of(ham):
                    relaxT = \
                             TDRedfieldFoersterRelaxationTensor(ham, sbi,
                                            coupling_cutoff=coupling_cutoff,
                                            cutoff_time=relaxation_cutoff_time)
                    if secular_relaxation:
                        relaxT.secularize()
                ham.unprotect_basis()
                ham.recover_cutoff_coupling()

            else:

                # Time independent combined tensor
                ham.subtract_cutoff_coupling(coupling_cutoff)
                ham.protect_basis()
                with eigenbasis_of(ham):
                    relaxT = \
                             RedfieldFoersterRelaxationTensor(ham, sbi,
                                            coupling_cutoff=coupling_cutoff,
                                            cutoff_time=relaxation_cutoff_time)
                    if secular_relaxation:
                        relaxT.secularize()

                    #print("Last line of the context", 
                    #      Manager().get_current_basis())
                #print("Left context", Manager().get_current_basis())
                ham.unprotect_basis()
                ham.recover_cutoff_coupling()

            #
            # create a corresponding propagator
            #
            ham1 = Hamiltonian(data=ham.data.copy())
            #ham1.subtract_cutoff_coupling(coupling_cutoff)
            ham1.remove_cutoff_coupling(coupling_cutoff)

            self.RelaxationTensor = relaxT
            self.RelaxationHamiltonian = ham1
            self._has_relaxation_tensor = True
            self._relaxation_theory = "combined_RedfieldFoerster"

            return relaxT, ham1

        elif relaxation_theory in theories["combined_WeakStrong"]:

            pass

        elif relaxation_theory in theories["Lindblad_form"]:

            if time_dependent:

                # Time dependent standard Refield
                raise Exception("Time dependent Lindblad not implemented yet")

            else:

                # Linblad form

                #ham.protect_basis()
                #with eigenbasis_of(ham):
                relaxT = LindbladForm(ham, sbi)
                if secular_relaxation:
                    relaxT.convert_2_tensor()
                    relaxT.secularize()
                #ham.unprotect_basis()

            self.RelaxationTensor = relaxT
            self.RelaxationHamiltonian = ham
            self._has_relaxation_tensor = True
            self._relaxation_theory = "Lindblad_form"

            return relaxT, ham

        elif relaxation_theory in theories["electronic_Lindblad"]:

            if time_dependent:

                # Time dependent standard Refield
                raise Exception("Time dependent Lindblad not implemented yet")

            else:

                # For purely electronic system, calculate normal Lindblad form
                if self.Ntot == self.Nel:
                    relaxT, ham = self.get_RelaxationTensor(timeaxis,
                                relaxation_theory="Lindblad_form",
                                time_dependent=time_dependent,
                                secular_relaxation=secular_relaxation,
                                relaxation_cutoff_time=relaxation_cutoff_time,
                                coupling_cutoff=coupling_cutoff,
                                recalculate=recalculate)
                # if vibrational states are present, we create a new SBI
                else:
                    # we assume that we have only electronic sbi
                    # FIXME: make sure that Molecule also has Nel
                    if sbi.system.Nel == sbi.KK.shape[1]:
                        # upgrade sbi to vibrational levels

                        eKK = sbi.KK
                        vKK = numpy.zeros((eKK.shape[0], ham.dim, ham.dim),
                                          dtype=REAL)

                        # use eKK to calculate vKK

                        sbi.KK = vKK
                    else:
                        raise Exception("SystemBathInteraction object has to"+
                                        " purely electronic")

                    relaxT = LindbladForm(ham, sbi)

                if secular_relaxation:
                    relaxT.convert_2_tensor()
                    relaxT.secularize()

            self.RelaxationTensor = relaxT
            self.RelaxationHamiltonian = ham
            self._has_relaxation_tensor = True
            self._relaxation_theory = "Lindblad_form"

            return relaxT, ham


        else:

            raise Exception("Theory not implemented")


    def get_ReducedDensityMatrixPropagator(self, timeaxis,
                       relaxation_theory=None,
                       time_nonlocal=False,
                       time_dependent=False,
                       secular_relaxation=False,
                       relaxation_cutoff_time=None,
                       coupling_cutoff=None,
                       as_operators=False,
                       recalculate=True):
        """Returns propagator of the density matrix



        """


        from ..qm import ReducedDensityMatrixPropagator
        from ..core.managers import eigenbasis_of


        relaxT, ham = self.get_RelaxationTensor(timeaxis,
                       relaxation_theory=relaxation_theory,
                       as_convolution_kernel=time_nonlocal,
                       time_dependent=time_dependent,
                       secular_relaxation=secular_relaxation,
                       relaxation_cutoff_time=relaxation_cutoff_time,
                       coupling_cutoff=coupling_cutoff,
                       recalculate=recalculate,
                       as_operators=as_operators)
        

        if time_nonlocal:
            # here we create time non-local propagator
            prop = None
            raise Exception()
        else:
            # FIXME: is the eigenbases needed???
            #with eigenbasis_of(ham):
            prop = ReducedDensityMatrixPropagator(timeaxis, ham, relaxT)

        return prop


    #FIXME: There must be a general theory here
    def get_RedfieldRateMatrix(self):
        """Returns Redfield rate matrix
        
        """

        from ..qm import RedfieldRateMatrix
        from ..core.managers import eigenbasis_of

        if self._built:
            ham = self.get_Hamiltonian()
            sbi = self.get_SystemBathInteraction()
        else:
            raise Exception()

        ham.protect_basis()
        with eigenbasis_of(ham):
            RR = RedfieldRateMatrix(ham, sbi)
        ham.unprotect_basis()

        return RR
    
    
    def get_FoersterRateMatrix(self):
        """Returns Förster rate matrix for the open system
        
        
        """

        from ..qm import FoersterRateMatrix
        
        if self._built:        
            ham = self.get_Hamiltonian()
            sbi = self.get_SystemBathInteraction()
        else:
            raise Exception()

        return FoersterRateMatrix(ham, sbi)

    

    def get_KTHierarchy(self, depth=2):
        """Returns the Kubo-Tanimura hierarchy of an open system
        
        """
        
        HH = self.get_Hamiltonian()
        HH.set_rwa([0,1])
        sbi = self.get_SystemBathInteraction()
        return KTHierarchy(HH, sbi, depth=depth)
    
    
    def get_KTHierarchyPropagator(self, depth=2):
        """Returns a propagator based on the Kubo-Tanimura hierarchy
        
        """
        
        kth = self.get_KTHierarchy(depth)
        ta = kth.sbi.TimeAxis
        
        return KTHierarchyPropagator(ta, kth)
    
    
    def get_excited_density_matrix(self, condition="delta", polarization=None):
        """Returns the density matrix corresponding to excitation condition
        
        
        """
        
        dip = self.get_TransitionDipoleMoment()
        if polarization is None:
            dip = dip.get_dipole_length_operator()
        else:
            # FIXME: This method is not implemented yet
            dip = dip.get_dipole_projection(polarization)
            
        with energy_units("int"):
            rho0 = self.get_thermal_ReducedDensityMatrix()
        
        
        if isinstance(condition, str):
            cond = condition
            
        else:
            cond = condition[0]

        
        if cond == "delta":
            
            rdi = numpy.dot(dip.data,numpy.dot(rho0.data,dip.data))
            rhoi = ReducedDensityMatrix(data=rdi)
            
            return rhoi

        elif cond == "pulse_spectrum":
            
            spectrum = condition[1]
            
            HH = self.get_Hamiltonian()
            
            if isinstance(spectrum, DFunction):
                
                dat = numpy.zeros((HH.dim,HH.dim), dtype=REAL)
                with eigenbasis_of(HH):
                    
                    for ii in range(HH.dim):
                        for jj in range(ii):
                            # frequency will always be >= 0.0
                            freque = HH.data[ii,ii] - HH.data[jj,jj]
                            if ((spectrum.axis.max > freque) 
                                and (spectrum.axis.min < freque)):
                                weight = numpy.sqrt(spectrum.at(freque))
                            else:
                                weight = 0.0
                            
                            dat[ii,jj] = weight*dip.data[ii,jj]
                            dat[jj,ii] = dat[ii,jj]
                            
                    dip = SelfAdjointOperator(data=dat)        
                    rdi = numpy.dot(dip.data,numpy.dot(rho0.data,dip.data))
                    rhoi = ReducedDensityMatrix(data=rdi)
                            
                return rhoi
            
            else:
                
                raise Exception("Spectrum must be specified through"+
                                " a DFunction object")

        else:
            print("Excitation condition:", condition)
            raise Exception("Excition condition not implemented.")
 
    
 
    def get_thermal_ReducedDensityMatrix(self):
        """Returns equilibrium density matrix for a give temparature
        
        """
        
        H = self.get_Hamiltonian() 
        T = self.get_temperature()
        dat = numpy.zeros(H._data.shape,dtype=COMPLEX)
        
        with eigenbasis_of(H):
            
            if numpy.abs(T) < 1.0e-10:
                dat[0,0] = 1.0
            
            else:
            
                dsum = 0.0
                
                for n in range(H._data.shape[0]):
                    dat[n,n] = numpy.exp(-H.data[n,n]/(kB_intK*T))
                    dsum += dat[n,n]

                dat *= 1.0/dsum
            
            rdm = ReducedDensityMatrix(data=dat)
                
        
        return rdm  