"""*******************************************************************************


    Tests of the quantarhei.Manager class


*******************************************************************************
"""

import unittest

import numpy

from quantarhei import Manager, energy_units, set_current_units


class TestManager(unittest.TestCase):
    """Tests for the Manager class"""

    def setUp(self):
        pass

    def test_that_Manager_is_a_singleton(self):
        """Testing that Manager object is a singleton"""
        m = Manager()
        n = Manager()

        if m is not n:
            raise Exception()


class TestNmConversion(unittest.TestCase):
    def setUp(self):
        set_current_units()

    def tearDown(self):
        set_current_units()

    def test_zero_energy_converts_to_zero_in_nm_units(self):
        """convert_energy_2_current_u(0.0) must return 0.0 when units are nm"""
        with energy_units("nm"):
            m = Manager()
            result = m.convert_energy_2_current_u(0.0)
            self.assertEqual(result, 0.0)

    def test_zero_array_converts_to_zero_array_in_nm_units(self):
        """Zero array elements must stay zero in nm conversion, not become inf"""
        with energy_units("nm"):
            m = Manager()
            val = numpy.array([0.0, 1.0, 0.0])
            result = m.convert_energy_2_current_u(val)
            self.assertTrue(numpy.isfinite(result).all())
            self.assertEqual(result[0], 0.0)
            self.assertEqual(result[2], 0.0)

    def test_near_zero_subnormal_does_not_produce_inf_in_nm_units(self):
        """A subnormal float near zero must not invert to inf in nm conversion"""
        with energy_units("nm"):
            m = Manager()
            val = numpy.array([numpy.finfo(float).tiny])
            result = m.convert_energy_2_current_u(val)
            self.assertTrue(numpy.isfinite(result).all())

    def test_internal_to_nm_roundtrip(self):
        """convert_energy_2_internal_u(convert_energy_2_current_u(v)) == v for nonzero v"""
        with energy_units("nm"):
            m = Manager()
            val = numpy.array([100.0, 500.0, 1000.0])
            roundtrip = m.convert_energy_2_internal_u(m.convert_energy_2_current_u(val))
            numpy.testing.assert_allclose(roundtrip, val, rtol=1e-10)
