#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# @file   BooleOptions.py
# @author Albert Puig (albert.puig@cern.ch)
# @date   26.10.2014
# =============================================================================
"""Options for configuring Boole."""


__all__ = ['get_boole_options', 'get_available_options']


def get_boole_options(digi_version, year):
    """Get digitization (Boole) options.

    :param digi_version: Digitization version.
    :type digi_version: str
    :param year: Year for which to get the options.
    :type year: int

    :returns: Configuration options.
    :rtype: dict (or None if not found)

    """
    year = int(year)
    return _boole_opt.get((digi_version, year), None)


def get_available_options():
    """Get list of available options.

    :returns: List of available options in (digi, year) format.
    :rtype: list of tuples

    """
    return _boole_opt.keys()


_boole_opt = {}
_boole_opt[('Digi13 with G4 dE/dx', 2012)] = {'boole_version': 'v26r3',
                                              'boole_appconfig': 'v3r164',
                                              'boole_options': '$APPCONFIGOPTS/Boole/Default.py '
                                                               '$APPCONFIGOPTS/Boole/DataType-2012.py '
                                                               '$APPCONFIGOPTS/Boole/Boole-SiG4EnergyDeposit.py '
                                                               '$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py'}

_boole_opt[('Digi13 with G4 dE/dx', 2011)] = {'boole_version': 'v26r3',
                                              'boole_appconfig': 'v3r171',
                                              'boole_options': '$APPCONFIGOPTS/Boole/Default.py '
                                                               '$APPCONFIGOPTS/Boole/DataType-2011.py '
                                                               '$APPCONFIGOPTS/Boole/Boole-SiG4EnergyDeposit.py '
                                                               '$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py'}
# EOF
