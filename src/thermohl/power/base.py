"""Generic radiative cooling term."""

from typing import Union

import numpy as np

from thermohl.air import kelvin

_dT = 1.0E-03


class PowerTerm:
    """Base class for power term."""

    def __init__(self, **kwargs):
        pass

    def value(self, T: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        r"""Compute power term value in function of temperature.

        Usually this function should be overridden in children classes; if it is
        not the case it will just return zero.

        Parameters
        ----------
        T : float or np.ndarray
            Conductor temperature (C).

        Returns
        -------
        float or np.ndarray
            Power term value (W.m\ :sup:`-1`\ ).

        """
        return np.zeros_like(T)

    def derivative(self, T: Union[float, np.ndarray], dT: float = _dT) -> Union[float, np.ndarray]:
        r"""Compute power term derivative regarding temperature in function of temperature.

        Usually this function should be overriden in children classes; if it is
        not the case it will evaluate the derivative from the value method with
        a second-order approximation.

        Parameters
        ----------
        T : float or np.ndarray
            Conductor temperature (C).
        dT : float, optional
            Temperature increment. The default is 1.0E-03.

        Returns
        -------
        float or np.ndarray
            Power term derivative (W.m\ :sup:`-1`\ K\ :sup:`-1`\ ).

        """
        return (self.value(T + dT) - self.value(T - dT)) / (2. * dT)


class RadiativeCooling(PowerTerm):
    """Generic power term for radiative cooling."""

    def __init__(
            self,
            Ta: Union[float, np.ndarray],
            D: Union[float, np.ndarray],
            epsilon: Union[float, np.ndarray],
            sigma: float = 5.67E-08,
            **kwargs
    ):
        r"""Init with args.

        Parameters
        ----------
        Ta : float or np.ndarray
            Ambient temperature (C).
        D : float or np.ndarray
            External diameter (m).
        epsilon : float or np.ndarray
            Emissivity.
        sigma : float, optional
            Stefan-Boltzmann constant in W.m\ :sup:`-2`\ K\ :sup:`4`\ . The
            default is 5.67E-08.

        Returns
        -------

        """
        self.Ta = kelvin(Ta)
        self.D = D
        self.epsilon = epsilon
        self.sigma = sigma

    def value(self, T: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        r"""Compute radiative cooling using the Stefan-Boltzmann law.

        Parameters
        ----------
        T : float or np.ndarray
            Conductor temperature (C).

        Returns
        -------
        float or np.ndarray
            Power term value (W.m\ :sup:`-1`\ ).

        """
        return np.pi * self.sigma * self.epsilon * self.D * (kelvin(T)**4 - self.Ta**4)

    def derivative(self, T: Union[float, np.ndarray], dT: float = _dT) -> Union[float, np.ndarray]:
        r"""Analytical derivative of value method.

        Parameters
        ----------
        T : float or np.ndarray
            Conductor temperature (C).

        Returns
        -------
        float or np.ndarray
            Power term derivative (W.m\ :sup:`-1`\ K\ :sup:`-1`\ ).

        """
        return 4. * np.pi * self.sigma * self.epsilon * self.D * T**3
