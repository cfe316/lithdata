import numpy as np
from constants import mLi, kB

class LithiumProperties():

    def __init__(self):
        self.m = constants.mLi # this exactly matches the mass in SPARTA, air.vss. 
        heatVap = 147.0 / 6.022e23 # heat of vaporization in kJ per lithium atom (source?)
        kj_to_j = 1e3 # kilojoules to joules
        self.heat_vap = heatVap * kj_to_j

    def vapor_pressure(self, t_kelvin):
        """Lithium vapor pressure in Pascals

        Browning, P, and P. E. Potter. “Assessment of the Experimentally 
        Determined Vapour Pressures of the Liquid Alkali Metals.”
        In Handbook of Thermodynamic and Transport Properties of Alakali Metals, 
        349–58. Oxford: Blackwell Scientific Publications, 1985.

        Section by Ohse, Page 350, Equation (2)
        """
        c1 = 13.0719
        c2 = -18880.659
        c3 = -0.4942
        megapascals_to_pascals = 1e6
        p_megapascals = np.exp(c1 + c2 / t_kelvin + c3 * np.log(t_kelvin))
        pressure_pa = p_megapascals * megapascals_to_pascals
        return pressure_pa

    def vapor_density(self, t_kelvin):
        """Equilibrium lithium vapor density in #/m^3.

        Parameters: T in Kelvins
        """
        kB = constants.kB
        p = t_kelvin > 0
        res = np.zeros_like(t_kelvin)
        res[p] = self.vapor_pressure(t_kelvin[p]) / (kB * t_kelvin[p])
        density = res
        return density

    def langmuir_flux(self, temperature):
        kB = constants.kB
        temperature = 1.0 * np.array(temperature)
        """Calculates the equilibrium Langmuir flux in # m^{-2} s^{-1}."""
        density = self.vapor_density(temperature)
        flux = density * np.sqrt(kB * temperature / (2 * np.pi * self.m))
        return flux