#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# @file   StrippingOptions.py
# @author Albert Puig (albert.puig@cern.ch)
# @date   27.10.2014
# =============================================================================
"""Options for configuring the Stripping in DaVinci."""


__all__ = ['get_stripping_options', 'get_available_options']


def get_stripping_options(stripping_version, year):
    """Get stripping (DaVinci) options.

    :param stripping_version: Version of the Stripping to run.
    :type stripping_version: str
    :param year: Year of the stripping.
    :type year: int

    :returns: Configuration options.
    :rtype: dict (or None if not found)

    """
    return _stripping_opt.get((stripping_version, year), None)


def get_available_options():
    """Get list of available options.

    :returns: List of available stripping configurations.
    :rtype: list

    """
    return _stripping_opt.keys()


_stripping_opt = {}

_stripping_opt[('Stripping20r1p3', 2011)] = {'davinci_version': 'v32r2p14',
                                             'davinci_appconfig': 'v3r193',
                                             'stripping_options': '$APPCONFIGOPTS/DaVinci/DV-Stripping20r1p3-Stripping-MC-NoPrescaling.py '
                                                                  '$APPCONFIGOPTS/DaVinci/DataType-2011.py '
                                                                  '$APPCONFIGOPTS/DaVinci/InputType-DST.py '
                                                                  '$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py'}

_stripping_opt[('Stripping20r0p3', 2012)] = {'davinci_version': 'v32r2p14',
                                             'davinci_appconfig': 'v3r193',
                                             'stripping_options': '$APPCONFIGOPTS/DaVinci/DV-Stripping20r0p3-Stripping-MC-NoPrescaling.py '
                                                                  '$APPCONFIGOPTS/DaVinci/DataType-2012.py '
                                                                  '$APPCONFIGOPTS/DaVinci/InputType-DST.py '
                                                                  '$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py'}

_stripping_opt[('Stripping20r0p3KpipiGammaFiltered', 2012)] = {'davinci_version': 'v32r2p14',
                                                              'davinci_appconfig': 'v3r193',
                                                              'davinci_rdconfig': 'v1r14',
                                                              'stripping_options': '$RDCONFIGOPTS/FilterBu2Kpipigamma.py '
                                                                                   '$APPCONFIGOPTS/DaVinci/DataType-2012.py '
                                                                                   '$APPCONFIGOPTS/DaVinci/InputType-DST.py '
                                                                                   '$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py'}

# EOF
