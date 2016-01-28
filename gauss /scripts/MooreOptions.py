#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# @file   MooreOptions.py
# @author Albert Puig (albert.puig@cern.ch)
# @date   27.10.2014
# =============================================================================
"""Trigger (Moore) options."""


__all__ = ['get_moore_options', 'get_available_options']


def get_moore_options(tck, year):
    """Get trigger (Moore) options.

    :param tck: TCK to run.
    :type tck: str
    :param year: Year of simulation.
    :type year: int

    :returns: Configuration options.
    :rtype: dict (or None if not found)

    """
    return _moore_opt.get((tck, year), None)


def get_available_options():
    """Get list of available options.

    :returns: List of available TCKs.
    :rtype: list

    """
    return _moore_opt.keys()


_moore_opt = {('0x409f0045', 2012): {'moore_version': 'v14r8p1',
                                     'moore_appconfig': 'v3r164',
                                     'moore_options': '$APPCONFIGOPTS/Moore/MooreSimProductionWithL0Emulation.py '
                                                      '$APPCONFIGOPTS/Conditions/TCK-0x40990042.py '
                                                      '$APPCONFIGOPTS/Moore/DataType-2012.py '
                                                      '$APPCONFIGOPTS/L0/L0TCK-0x0045.py', },
              ('0x40760037', 2011): {'moore_version': 'v12r8g3',
                                     'moore_appconfig': 'v3r171',
                                     'moore_lblogin': 'x86_64-slc5-gcc43-opt',
                                     'moore_options': '$APPCONFIGOPTS/Moore/MooreSimProductionWithL0Emulation.py '
                                                      '$APPCONFIGOPTS/Conditions/TCK-0x40760037.py '
                                                      '$APPCONFIGOPTS/Moore/DataType-2011.py '
                                                      '$APPCONFIGOPTS/L0/L0TCK-0x0037.py', }, }

# EOF
