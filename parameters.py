"""Storage module for CASA benchmarking parameters.

This module is solely for storing information related to benchmarking the
typical group of data sets. The machine module depends on this module for
finding sources of scripts, raw data etc. but this module can be used in other
contexts too. Some data set variable names start with a meaningless "x" since
variable names can not start with numbers.

The dictionaries are organized by the source of data/scripts from "online",
"lustre" and "elric". Then each of those sub-dictionaries contain the URL/path
to the calScript, imScript, uncalData and calData from that source.
"""
##2012.1.00912##
#THIS DATA IS NOT ON THE SCIENCE PORTAL
#CASA 4.3
x2012_1_00912_S_43 = {'online': \
                          {'calScript': \
                               None, \
                           'imScript': \
                               None, \
                           'uncalData': \
                               None, \
                           'calData': \
                               None}, \
                      'lustre': \
                          {'calScript': \
                               '/lustre/naasc/jcrossle/benchmark/' + \
                               '2012.1.00912.S/430/' + \
                               '2012.1.00912.S_calibration4.3.py', \
                           'imScript': \
                               '/lustre/naasc/jcrossle/benchmark/' + \
                               '2012.1.00912.S/430/' + \
                               '2012.1.00912.S_imaging4.3.py', \
                           'uncalData': \
                               '/lustre/naasc/jcrossle/benchmark/' + \
                               '2012.1.00912.S/' + \
                               '912_reduction.tgz', \
                           'calData': \
                               None}, \
                      'elric': \
                          {'calScript': \
                               '/Volumes/elric/benchmark_raw_data/' + \
                               '2012.1.00912.S/430/' + \
                               '2012.1.00912.S_calibration4.3.py', \
                           'imScript': \
                               '/Volumes/elric/benchmark_raw_data/' + \
                               '2012.1.00912.S/430/' + \
                               '2012.1.00912.S_imaging4.3.py', \
                           'uncalData': \
                               '/Volumes/elric/benchmark_raw_data/' + \
                               '2012.1.00912.S/' + \
                               '912_reduction.tgz', \
                           'calData': \
                               None}}

#CASA 4.2
#THIS DATA IS NOT ON THE SCIENCE PORTAL
x2012_1_00912_S_42 = {'online': \
                          {'calScript': \
                               None, \
                           'imScript': \
                               None, \
                           'uncalData': \
                               None, \
                           'calData': \
                               None}, \
                      'lustre': \
                          {'calScript': \
                               '/lustre/naasc/jcrossle/benchmark/' + \
                               '2012.1.00912.S/422/' + \
                               '2012.1.00912.S_calibration4.2.py', \
                           'imScript': \
                               '/lustre/naasc/jcrossle/benchmark/' + \
                               '2012.1.00912.S/422/' + \
                               '2012.1.00912.S_imaging4.2.py', \
                           'uncalData': \
                               '/lustre/naasc/jcrossle/benchmark/' + \
                               '2012.1.00912.S/' + \
                               '912_reduction.tgz', \
                           'calData': \
                               None}, \
                      'elric': \
                          {'calScript': \
                               '/Volumes/elric/benchmark_raw_data/' + \
                               '2012.1.00912.S/422/' + \
                               '2012.1.00912.S_calibration4.2.py', \
                           'imScript': \
                               '/Volumes/elric/benchmark_raw_data/' + \
                               '2012.1.00912.S/422/' + \
                               '2012.1.00912.S_imaging4.2.py', \
                           'uncalData': \
                               '/Volumes/elric/benchmark_raw_data/' + \
                               '2012.1.00912.S/' + \
                               '912_reduction.tgz', \
                           'calData': \
                               None}}
##=============================================================================##

##2011.0.00099.S##
#THIS DATA IS NOT ON THE SCIENCE PORTAL
#CASA 4.0
x2011_0_00099_S_40 = {'online': \
                          {'calScript': \
                               None, \
                           'imScript': \
                               None, \
                           'uncalData': \
                               None, \
                           'calData': \
                               None}, \
                      'lustre': \
                          {'calScript': \
                               '/lustre/naasc/jcrossle/benchmark/scripts/' + \
                               '2011.0.00099.S_calibration_casa4p0.py', \
                           'imScript': \
                               '/lustre/naasc/jcrossle/benchmark/scripts/' + \
                               '2011.0.00099.S_imaging_casa4p0.py', \
                           'uncalData': \
                               '/lustre/naasc/jcrossle/benchmark/data/' + \
                               '2011.0.00099.S/2011.0.00099.S.tgz', \
                           'calData': \
                               None}, \
                      'elric': \
                          {'calScript': \
                               None, \
                           'imScript': \
                               None, \
                           'uncalData': \
                               None, \
                           'calData': \
                               None}}
##=============================================================================##

##NGC3256 Band 3
#CASA 4.3
NGC3256Band3_43 = {'online': \
                       {'calScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'NGC3256_Band3_Calibration_for_CASA_4.3', \
                        'imScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'NGC3256_Band3_Imaging_for_CASA_4.3', \
                        'uncalData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}, \
                   'lustre': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/lustre/naasc/SV/NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            '/lustre/naasc/SV/NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}, \
                   'elric': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}}

#CASA 4.2
NGC3256Band3_42 = {'online': \
                       {'calScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'NGC3256_Band3_Calibration_for_CASA_4.2', \
                        'imScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'NGC3256_Band3_Imaging_for_CASA_4.2', \
                        'uncalData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}, \
                   'lustre': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/lustre/naasc/SV/NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            '/lustre/naasc/SV/NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}, \
                   'elric': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}}

#CASA 4.1
NGC3256Band3_41 = {'online': \
                       {'calScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'NGC3256_Band3_Calibration_for_CASA_4.1', \
                        'imScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'NGC3256_Band3_Imaging_for_CASA_4.1', \
                        'uncalData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}, \
                   'lustre': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/lustre/naasc/SV/NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            '/lustre/naasc/SV/NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}, \
                   'elric': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}}

#CASA 4.0
NGC3256Band3_40 = {'online': \
                       {'calScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'NGC3256_Band3_Calibration_for_CASA_4.0', \
                        'imScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'NGC3256_Band3_Imaging_for_CASA_4.0', \
                        'uncalData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}, \
                   'lustre': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/lustre/naasc/SV/NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            '/lustre/naasc/SV/NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}, \
                   'elric': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}}

#CASA 3.4
NGC3256Band3_34 = {'online': \
                       {'calScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'NGC3256_Band3_Calibration_for_CASA_3.4', \
                        'imScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'NGC3256_Band3_Imaging_for_CASA_3.4', \
                        'uncalData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}, \
                   'lustre': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/lustre/naasc/SV/NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            '/lustre/naasc/SV/NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}, \
                   'elric': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                            'NGC3256_Band3_UnCalibratedMSandTables' + \
                            'ForReduction.tgz', \
                        'calData': \
                            '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                            'NGC3256_Band3_CalibratedData_CASA4.tgz'}}
##=============================================================================##

##TWHydra Band 7##
#CASA 4.3
TWHydraBand7_43 = {'online': \
                       {'calScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'TWHydraBand7_Calibration_4.3', \
                        'imScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'TWHydraBand7_Imaging_4.3', \
                        'uncalData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}, \
                   'lustre': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/lustre/naasc/SV/TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            '/lustre/naasc/SV/TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}, \
                   'elric': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}}

#CASA 4.2
TWHydraBand7_42 = {'online': \
                       {'calScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'TWHydraBand7_Calibration_4.2', \
                        'imScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'TWHydraBand7_Imaging_4.2', \
                        'uncalData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}, \
                   'lustre': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/lustre/naasc/SV/TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            '/lustre/naasc/SV/TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}, \
                   'elric': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}}

#CASA 4.1
TWHydraBand7_41 = {'online': \
                       {'calScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'TWHydraBand7_Calibration_4.1', \
                        'imScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'TWHydraBand7_Imaging_4.1', \
                        'uncalData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}, \
                   'lustre': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/lustre/naasc/SV/TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            '/lustre/naasc/SV/TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}, \
                   'elric': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}}

#CASA 4.0
TWHydraBand7_40 = {'online': \
                       {'calScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'TWHydraBand7_Calibration_4.0', \
                        'imScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'TWHydraBand7_Imaging_4.0', \
                        'uncalData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}, \
                   'lustre': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/lustre/naasc/SV/TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            '/lustre/naasc/SV/TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}, \
                   'elric': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}}

#CASA 3.4
TWHydraBand7_34 = {'online': \
                       {'calScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'TWHydraBand7_Calibration_3.4', \
                        'imScript': \
                            'http://casaguides.nrao.edu/index.php?title=' + \
                            'TWHydraBand7_Imaging_3.4', \
                        'uncalData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            'https://almascience.nrao.edu/almadata/sciver/' + \
                            'TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}, \
                   'lustre': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/lustre/naasc/SV/TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            '/lustre/naasc/SV/TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}, \
                   'elric': \
                       {'calScript': \
                            None, \
                        'imScript': \
                            None, \
                        'uncalData': \
                            '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                            'TWHYA_BAND7_UnCalibratedMSAndTablesFor' + \
                            'Reduction.tgz', \
                        'calData': \
                            '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                            'TWHYA_BAND7_CalibratedData.tgz'}}
##=============================================================================##

##Antennae Band 7##
AntennaeBand7_43 = {'online': \
                        {'calScript': \
                             'http://casaguides.nrao.edu/index.php?title=' + \
                             'AntennaeBand7_Calibration_4.3', \
                         'imScript': \
                             'http://casaguides.nrao.edu/index.php?title=' + \
                             'AntennaeBand7_Imaging_4.3', \
                         'uncalData': \
                             'https://almascience.nrao.edu/almadata/sciver/' + \
                             'AntennaeBand7/' + \
                             'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                             'Reduction.tgz', \
                         'calData': \
                             'https://almascience.nrao.edu/almadata/sciver/' + \
                             'AntennaeBand7/' + \
                             'Antennae_Band7_CalibratedData.tgz'}, \
                     'lustre': \
                         {'calScript': \
                              None, \
                          'imScript': \
                              None, \
                          'uncalData': \
                              '/lustre/naasc/SV/AntennaeBand7/' + \
                              'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                              'Reduction.tgz', \
                          'calData': \
                              '/lustre/naasc/SV/AntennaeBand7/' + \
                              'Antennae_Band7_CalibratedData.tgz'}, \
                     'elric': \
                         {'calScript': \
                              None, \
                          'imScript': \
                              None, \
                          'uncalData': \
                              '/Volumes/elric/benchmark_raw_data/' + \
                              'AntennaeBand7/' + \
                              'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                              'Reduction.tgz', \
                          'calData': \
                              '/Volumes/elric/benchmark_raw_data/' + \
                              'AntennaeBand7/' + \
                              'Antennae_Band7_CalibratedData.tgz'}}

#CASA 4.2
AntennaeBand7_42 = {'online': \
                        {'calScript': \
                             'http://casaguides.nrao.edu/index.php?title=' + \
                             'AntennaeBand7_Calibration_4.2' , \
                         'imScript': \
                             'http://casaguides.nrao.edu/index.php?title=' + \
                             'AntennaeBand7_Imaging_4.2', \
                         'uncalData': \
                             'https://almascience.nrao.edu/almadata/sciver/' + \
                             'AntennaeBand7/' + \
                             'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                             'Reduction.tgz', \
                         'calData': \
                             'https://almascience.nrao.edu/almadata/sciver/' + \
                             'AntennaeBand7/' + \
                             'Antennae_Band7_CalibratedData.tgz'}, \
                     'lustre': \
                         {'calScript': \
                              None, \
                          'imScript': \
                              None, \
                          'uncalData': \
                              '/lustre/naasc/SV/AntennaeBand7/' + \
                              'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                              'Reduction.tgz', \
                          'calData': \
                              '/lustre/naasc/SV/AntennaeBand7/' + \
                              'Antennae_Band7_CalibratedData.tgz'}, \
                     'elric': \
                         {'calScript': \
                              None, \
                          'imScript': \
                              None, \
                          'uncalData': \
                              '/Volumes/elric/benchmark_raw_data/' + \
                              'AntennaeBand7/' + \
                              'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                              'Reduction.tgz', \
                          'calData': \
                              '/Volumes/elric/benchmark_raw_data/' + \
                              'AntennaeBand7/' + \
                              'Antennae_Band7_CalibratedData.tgz'}}

#CASA 4.1
AntennaeBand7_41 = {'online': \
                        {'calScript': \
                             'http://casaguides.nrao.edu/index.php?title=' + \
                             'AntennaeBand7_Calibration_4.1' , \
                         'imScript': \
                             'http://casaguides.nrao.edu/index.php?title=' + \
                             'AntennaeBand7_Imaging_4.1', \
                         'uncalData': \
                             'https://almascience.nrao.edu/almadata/sciver/' + \
                             'AntennaeBand7/' + \
                             'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                             'Reduction.tgz', \
                         'calData': \
                             'https://almascience.nrao.edu/almadata/sciver/' + \
                             'AntennaeBand7/' + \
                             'Antennae_Band7_CalibratedData.tgz'}, \
                     'lustre': \
                         {'calScript': \
                              None, \
                          'imScript': \
                              None, \
                          'uncalData': \
                              '/lustre/naasc/SV/AntennaeBand7/' + \
                              'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                              'Reduction.tgz', \
                          'calData': \
                              '/lustre/naasc/SV/AntennaeBand7/' + \
                              'Antennae_Band7_CalibratedData.tgz'}, \
                     'elric': \
                         {'calScript': \
                              None, \
                          'imScript': \
                              None, \
                          'uncalData': \
                              '/Volumes/elric/benchmark_raw_data/' + \
                              'AntennaeBand7/' + \
                              'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                              'Reduction.tgz', \
                          'calData': \
                              '/Volumes/elric/benchmark_raw_data/' + \
                              'AntennaeBand7/' + \
                              'Antennae_Band7_CalibratedData.tgz'}}

#CASA 4.0
AntennaeBand7_40 = {'online': \
                        {'calScript': \
                             'http://casaguides.nrao.edu/index.php?title=' + \
                             'AntennaeBand7_Calibration_4.0', \
                         'imScript': \
                             'http://casaguides.nrao.edu/index.php?title=' + \
                             'AntennaeBand7_Imaging_4.0', \
                         'uncalData': \
                             'https://almascience.nrao.edu/almadata/sciver/' + \
                             'AntennaeBand7/' + \
                             'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                             'Reduction.tgz', \
                         'calData': \
                             'https://almascience.nrao.edu/almadata/sciver/' + \
                             'AntennaeBand7/' + \
                             'Antennae_Band7_CalibratedData.tgz'}, \
                     'lustre': \
                         {'calScript': \
                              None, \
                          'imScript': \
                              None, \
                          'uncalData': \
                              '/lustre/naasc/SV/AntennaeBand7/' + \
                              'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                              'Reduction.tgz', \
                          'calData': \
                              '/lustre/naasc/SV/AntennaeBand7/' + \
                              'Antennae_Band7_CalibratedData.tgz'}, \
                     'elric': \
                         {'calScript': \
                              None, \
                          'imScript': \
                              None, \
                          'uncalData': \
                              '/Volumes/elric/benchmark_raw_data/' + \
                              'AntennaeBand7/' + \
                              'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                              'Reduction.tgz', \
                          'calData': \
                              '/Volumes/elric/benchmark_raw_data/' + \
                              'AntennaeBand7/' + \
                              'Antennae_Band7_CalibratedData.tgz'}}

#CASA 3.4
AntennaeBand7_34 = {'online': \
                        {'calScript': \
                             'http://casaguides.nrao.edu/index.php?title=' + \
                             'AntennaeBand7_Calibration_3.4', \
                         'imScript': \
                             'http://casaguides.nrao.edu/index.php?title=' + \
                             'AntennaeBand7_Imaging_3.4', \
                         'uncalData': \
                             'https://almascience.nrao.edu/almadata/sciver/' + \
                             'AntennaeBand7/' + \
                             'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                             'Reduction.tgz', \
                         'calData': \
                             'https://almascience.nrao.edu/almadata/sciver/' + \
                             'AntennaeBand7/' + \
                             'Antennae_Band7_CalibratedData.tgz'}, \
                     'lustre': \
                         {'calScript': \
                              None, \
                          'imScript': \
                              None, \
                          'uncalData': \
                              '/lustre/naasc/SV/AntennaeBand7/' + \
                              'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                              'Reduction.tgz', \
                          'calData': \
                              '/lustre/naasc/SV/AntennaeBand7/' + \
                              'Antennae_Band7_CalibratedData.tgz'}, \
                     'elric': \
                         {'calScript': \
                              None, \
                          'imScript': \
                              None, \
                          'uncalData': \
                              '/Volumes/elric/benchmark_raw_data/' + \
                              'AntennaeBand7/' + \
                              'Antennae_Band7_UnCalibratedMSandTablesFor' + \
                              'Reduction.tgz', \
                          'calData': \
                              '/Volumes/elric/benchmark_raw_data/' + \
                              'AntennaeBand7/' + \
                              'Antennae_Band7_CalibratedData.tgz'}}
##=============================================================================##

##IRAS 16293 Band 9##
#CASA 4.3
IRASBand9_43 = {'online': \
                    {'calScript': \
                         'http://casaguides.nrao.edu/index.php?title=' + \
                         'IRAS16293_Band9_-_Calibration_for_CASA_4.3', \
                     'imScript': \
                         'http://casaguides.nrao.edu/index.php?title=' + \
                         'IRAS16293_Band9_-_Imaging_for_CASA_4.3', \
                     'uncalData': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'IRAS16293B9/IRAS16293_Band9_UnCalibratedMS.tgz', \
                     'calData': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'IRAS16293B9/IRAS16293_Band9_CalibratedMS_FIXED.tgz'}, \
                'lustre': \
                    {'calScript': \
                         None, \
                     'imScript': \
                         None, \
                     'uncalData': \
                         '/lustre/naasc/SV/IRAS16293B9/' + \
                         'IRAS16293_Band9_UnCalibratedMS.tgz', \
                     'calData': \
                         '/lustre/naasc/SV/IRAS16293B9/' + \
                         'IRAS16293_Band9_CalibratedMS_FIXED.tgz'}, \
                'elric': \
                    {'calScript': \
                         None, \
                     'imScript': \
                         None, \
                     'uncalData': \
                         '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                         'IRAS16293_Band9_UnCalibratedMS.tgz', \
                     'calData': \
                         '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                         'IRAS16293_Band9_CalibratedMS_FIXED.tgz'}}

#CASA 4.2
IRASBand9_42 = {'online': \
                    {'calScript': \
                         'http://casaguides.nrao.edu/index.php?title=' + \
                         'IRAS16293_Band9_-_Calibration_for_CASA_4.2', \
                     'imScript': \
                         'http://casaguides.nrao.edu/index.php?title=' + \
                         'IRAS16293_Band9_-_Imaging_for_CASA_4.2', \
                     'uncalData': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'IRAS16293B9/IRAS16293_Band9_UnCalibratedMS.tgz', \
                     'calData': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'IRAS16293B9/IRAS16293_Band9_CalibratedMS_FIXED.tgz'}, \
                'lustre': \
                    {'calScript': \
                         None, \
                     'imScript': \
                         None, \
                     'uncalData': \
                         '/lustre/naasc/SV/IRAS16293B9/' + \
                         'IRAS16293_Band9_UnCalibratedMS.tgz', \
                     'calData': \
                         '/lustre/naasc/SV/IRAS16293B9/' + \
                         'IRAS16293_Band9_CalibratedMS_FIXED.tgz'}, \
                'elric': \
                    {'calScript': \
                         None, \
                     'imScript': \
                         None, \
                     'uncalData': \
                         '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                         'IRAS16293_Band9_UnCalibratedMS.tgz', \
                     'calData': \
                         '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                         'IRAS16293_Band9_CalibratedMS_FIXED.tgz'}}

#CASA 4.0
IRASBand9_40 = {'online': \
                    {'calScript': \
                         'http://casaguides.nrao.edu/index.php?title=' + \
                         'IRAS16293_Band9_-_Calibration_for_CASA_4.0', \
                     'imScript': \
                         'http://casaguides.nrao.edu/index.php?title=' + \
                         'IRAS16293_Band9_-_Imaging_for_CASA_4.0', \
                     'uncalData': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'IRAS16293B9/IRAS16293_Band9_UnCalibratedMS.tgz', \
                     'calData': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'IRAS16293B9/IRAS16293_Band9_CalibratedMS_FIXED.tgz'}, \
                'lustre': \
                    {'calScript': \
                         None, \
                     'imScript': \
                         None, \
                     'uncalData': \
                         '/lustre/naasc/SV/IRAS16293B9/' + \
                         'IRAS16293_Band9_UnCalibratedMS.tgz', \
                     'calData': \
                         '/lustre/naasc/SV/IRAS16293B9/' + \
                         'IRAS16293_Band9_CalibratedMS_FIXED.tgz'}, \
                'elric': \
                    {'calScript': \
                         None, \
                     'imScript': \
                         None, \
                     'uncalData': \
                         '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                         'IRAS16293_Band9_UnCalibratedMS.tgz', \
                     'calData': \
                         '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                         'IRAS16293_Band9_CalibratedMS_FIXED.tgz'}}
##=============================================================================##

##2011.0.00367.S##
#THIS DATA IS NOT ON THE SCIENCE PORTAL
#CASA 3.3
x2011_0_00367_S_33 = {'online': \
                          {'calScript': \
                               None, \
                           'imScript': \
                               None, \
                           'uncalData': \
                               None, \
                           'calData': \
                               None}, \
                      'lustre': \
                          {'calScript': \
                               '/export/lustre/jcrossle/benchmark/scripts/' + \
                               '2011.0.00367.S_sb_calibration.py', \
                           'imScript': \
                               '/export/lustre/jcrossle/benchmark/scripts/' + \
                               '2011.0.00367.S_calibration_image.py', \
                           'uncalData': \
                               '/export/lustre/jcrossle/benchmark/data/' + \
                               '2011.0.00367.S.tgz', \
                           'calData': \
                               None}, \
                      'elric': \
                          {'calScript': \
                               None, \
                           'imScript': \
                               None, \
                           'uncalData': \
                               None, \
                           'calData': \
                               None}}
##=============================================================================##

##M100 Band 3##
#CASA 3.3
M100Band3_33 = {'online': \
                    {'calScript': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'M100Band3/M100_Band3_Calibration.py', \
                     'imScript': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'M100Band3/M100_Band3_Imaging.py', \
                     'uncalData': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'M100Band3/' + \
                         'M100_Band3_UnCalibratedMSAndTablesFor' + \
                         'Reduction.tgz', \
                     'calData': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'M100Band3/M100_Band3_CalibratedData.tgz'}, \
                'lustre': \
                    {'calScript': \
                         '/lustre/naasc/SV/M100Band3/' + \
                         'M100_Band3_Calibration.py', \
                     'imScript': \
                         '/lustre/naasc/SV/M100Band3/' + \
                         'M100_Band3_Imaging.py', \
                     'uncalData': \
                         '/lustre/naasc/SV/M100Band3' + \
                         'M100_Band3_UnCalibratedMSAndTablesForReduction.tgz', \
                     'calData': \
                         '/lustre/naasc/SV/M100Band3' + \
                         'M100_Band3_CalibratedData.tgz'}, \
                'elric': \
                    {'calScript': \
                         '/Volumes/elric/benchmark_raw_data/M100Band3' + \
                         'M100_Band3_Calibration.py', \
                     'imScript': \
                         '/Volumes/elric/benchmark_raw_data/M100Band3' + \
                         'M100_Band3_Imaging.py', \
                     'uncalData': \
                         '/Volumes/elric/benchmark_raw_data/M100Band3' + \
                         'M100_Band3_UnCalibratedMSAndTablesForReduction.tgz', \
                     'calData': \
                         '/Volumes/elric/benchmark_raw_data/M100Band3' + \
                         'M100_Band3_CalibratedData.tgz'}}
##=============================================================================##

##SgrA Band 6##
#CASA 3.3
SgrABand6_33 = {'online': \
                    {'calScript': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'SgrABand6/SgrA_Band6_Calibration.py', \
                     'imScript': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'SgrABand6/SgrA_Band6_Imaging.py', \
                     'uncalData': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'SgrABand6/' + \
                         'SgrA_Band6_UnCalibratedMSAndTablesForReduction.tgz', \
                     'calData': \
                         'https://almascience.nrao.edu/almadata/sciver/' + \
                         'SgrABand6/' + \
                         'SgrA_Band6_CalibratedData.tgz'}, \
                'lustre': \
                    {'calScript': \
                         '/lustre/naasc/SV/SgrABand6/' + \
                         'SgrA_Band6_Calibration.py', \
                     'imScript': \
                         '/lustre/naasc/SV/SgrABand6/' + \
                         'SgrA_Band6_Imaging.py', \
                     'uncalData': \
                         '/lustre/naasc/SV/SgrABand6/' + \
                         'SgrA_Band6_UnCalibratedMSAndTablesForReduction.tgz', \
                     'calData': \
                         '/lustre/naasc/SV/SgrABand6/' + \
                         'SgrA_Band6_CalibratedData.tgz'}, \
                'elric': \
                    {'calScript': \
                         '/Volumes/elric/benchmark_raw_data/SgrABand6' + \
                         'SgrA_Band6_Calibration.py', \
                     'imScript': \
                         '/Volumes/elric/benchmark_raw_data/SgrABand6' + \
                         'SgrA_Band6_Imaging.py', \
                     'uncalData': \
                         '/Volumes/elric/benchmark_raw_data/SgrABand6' + \
                         'SgrA_Band6_UnCalibratedMSAndTablesForReduction.tgz', \
                     'calData': \
                         '/Volumes/elric/benchmark_raw_data/SgrABand6' + \
                         'SgrA_Band6_CalibratedData.tgz'}}
##=============================================================================##
