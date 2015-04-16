""" Storage module for CASA benchmarking parameters.

This module is solely for storing information related to benchmarking the
typical group of data sets. The machine module depends on this module for finding
sources of scripts, raw data etc. but this module can be used in other contexts
too. It contains dictionaries for each data set which store information on:

  -calibration URLs
  -imaging URLs
  -uncalibrated data URLs
  -calibrated data URLs
  -uncalibrated data paths on lustre
  -calibrated data paths on lustre
  -uncalibrated data paths on the Mac RAID array (elric)
  -calibrated data paths on the Mac RAID array (elric)

Some data set variable names start with a meaningless "x" since variable names
can not start with numbers.
"""
##2012.1.00912##
#THIS DATA IS NOT ON THE SCIENCE PORTAL
#CASA 4.3
x2012_1_00912_S_43 = {'calibrationURL': \
                          '/lustre/naasc/nbrunett/benchmark/' + \
                          '2012.1.00912.S/430/' + \
                          '2012.1.00912.S_calibration4.3.py', \
                      'imagingURL': \
                          '/lustre/naasc/nbrunett/benchmark/' + \
                          '2012.1.00912.S/430/' + \
                          '2012.1.00912.S_imaging4.3.py', \
                      'uncalDataURL': \
                          None, \
                      'calDataURL': \
                          None, \
                      'lustreUncalDataPath': \
                          '/lustre/naasc/nbrunett/benchmark/2012.1.00912.S/' + \
                          '912_reduction.tgz', \
                      'lustreCalDataPath' : \
                          None, \
                      'macUncalDataPath': \
                          '/Volumes/elric/benchmark_raw_data/2012.1.00912.S/' + \
                          '912_reduction.tgz', \
                      'macCalDataPath': \
                          None}

#CASA 4.2
#THIS DATA IS NOT ON THE SCIENCE PORTAL
x2012_1_00912_S_42 = {'calibrationURL': \
                          '/lustre/naasc/nbrunett/benchmark/' + \
                          '2012.1.00912.S/422/' + \
                          '2012.1.00912.S_calibration4.2.py', \
                      'imagingURL': \
                          '/lustre/naasc/nbrunett/benchmark/' + \
                          '2012.1.00912.S/422/' + \
                          '2012.1.00912.S_imaging4.2.py', \
                      'uncalDataURL': \
                          None, \
                      'calDataURL': \
                          None, \
                      'lustreUncalDataPath': \
                          '/lustre/naasc/nbrunett/benchmark/2012.1.00912.S/' + \
                          '912_reduction.tgz', \
                      'lustreCalDataPath' : \
                          None, \
                      'macUncalDataPath': \
                          '/Volumes/elric/benchmark_raw_data/2012.1.00912.S/' + \
                          '912_reduction.tgz', \
                      'macCalDataPath': \
                          None}
##=============================================================================##

##2011.0.00099.S##
#THIS DATA IS NOT ON THE SCIENCE PORTAL
#CASA 4.0
x2011_0_00099_S_40 = {'calibrationURL': \
                          '/lustre/naasc/jcrossle/benchmark/scripts/' + \
                          '2011.0.00099.S_calibration_casa4p0.py', \
                      'imagingURL': \
                          '/lustre/naasc/jcrossle/benchmark/scripts/' + \
                          '2011.0.00099.S_imaging_casa4p0.py', \
                      'uncalDataURL': \
                          None, \
                      'calDataURL': \
                          None, \
                      'lustreUncalDataPath': \
                          '/lustre/naasc/jcrossle/benchmark/data/' + \
                          '2011.0.00099.S/2011.0.00099.S.tgz', \
                      'lustreCalDataPath': \
                          None, \
                      'macUncalDataPath': \
                          None, \
                      'macCalDataPath': \
                          None}
##=============================================================================##

##NGC3256 Band 3
#CASA 4.3
NGC3256Band3_43 = {'calibrationURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'NGC3256_Band3_Calibration_for_CASA_4.3', \
                   'imagingURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'NGC3256_Band3_Imaging_for_CASA_4.3', \
                   'uncalDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/' + \
                       'NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'calDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/' + \
                       'NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz', \
                   'lustreUncalDataPath': \
                       '/lustre/naasc/SV/NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'lustreCalDataPath': \
                       '/lustre/naasc/SV/NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz', \
                   'macUncalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'macCalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz'}

#CASA 4.2
NGC3256Band3_42 = {'calibrationURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'NGC3256_Band3_Calibration_for_CASA_4.2', \
                   'imagingURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'NGC3256_Band3_Imaging_for_CASA_4.2', \
                   'uncalDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/' + \
                       'NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'calDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/' + \
                       'NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz', \
                   'lustreUncalDataPath': \
                       '/lustre/naasc/SV/NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'lustreCalDataPath': \
                       '/lustre/naasc/SV/NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz'}

#CASA 4.1
NGC3256Band3_41 = {'calibrationURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'NGC3256_Band3_Calibration_for_CASA_4.1', \
                   'imagingURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'NGC3256_Band3_Imaging_for_CASA_4.1', \
                   'uncalDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/' + \
                       'NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'calDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/' + \
                       'NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz', \
                   'lustreUncalDataPath': \
                       '/lustre/naasc/SV/NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'lustreCalDataPath': \
                       '/lustre/naasc/SV/NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz', \
                   'macUncalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'macCalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz'}

#CASA 4.0
NGC3256Band3_40 = {'calibrationURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'NGC3256_Band3_Calibration_for_CASA_4.0', \
                   'imagingURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'NGC3256_Band3_Imaging_for_CASA_4.0', \
                   'uncalDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/' + \
                       'NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'calDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/' + \
                       'NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz', \
                   'lustreUncalDataPath': \
                       '/lustre/naasc/SV/NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'lustreCalDataPath': \
                       '/lustre/naasc/SV/NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz', \
                   'macUncalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'macCalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz'}

#CASA 3.4
NGC3256Band3_34 = {'calibrationURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'NGC3256_Band3_Calibration_for_CASA_3.4', \
                   'imagingURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'NGC3256_Band3_Imaging_for_CASA_3.4', \
                   'uncalDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/' + \
                       'NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'calDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/' + \
                       'NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz', \
                   'lustreUncalDataPath': \
                       '/lustre/naasc/SV/NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'lustreCalDataPath': \
                       '/lustre/naasc/SV/NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz', \
                   'macUncalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                       'NGC3256_Band3_UnCalibratedMSandTablesForReduction.tgz', \
                   'macCalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/NGC3256/' + \
                       'NGC3256_Band3_CalibratedData_CASA4.tgz'}
##=============================================================================##

##TWHydra Band 7##
#CASA 4.3
TWHydraBand7_43 = {'calibrationURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'TWHydraBand7_Calibration_4.3', \
                   'imagingURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'TWHydraBand7_Imaging_4.3', \
                   'uncalDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'calDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz', \
                   'lustreUncalDataPath': \
                       '/lustre/naasc/SV/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'lustreCalDataPath': \
                       '/lustre/naasc/SV/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz', \
                   'macUncalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'macCalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz'}

#CASA 4.2
TWHydraBand7_42 = {'calibrationURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'TWHydraBand7_Calibration_4.2', \
                   'imagingURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'TWHydraBand7_Imaging_4.2', \
                   'uncalDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'calDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz', \
                   'lustreUncalDataPath': \
                       '/lustre/naasc/SV/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'lustreCalDataPath': \
                       '/lustre/naasc/SV/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz', \
                   'macUncalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'macCalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz'}

#CASA 4.1
TWHydraBand7_41 = {'calibrationURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'TWHydraBand7_Calibration_4.1', \
                   'imagingURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'TWHydraBand7_Imaging_4.1', \
                   'uncalDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'calDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz', \
                   'lustreUncalDataPath': \
                       '/lustre/naasc/SV/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'lustreCalDataPath': \
                       '/lustre/naasc/SV/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz', \
                   'macUncalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'macCalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz'}

#CASA 4.0
TWHydraBand7_40 = {'calibrationURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'TWHydraBand7_Calibration_4.0', \
                   'imagingURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'TWHydraBand7_Imaging_4.0', \
                   'uncalDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'calDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz', \
                   'lustreUncalDataPath': \
                       '/lustre/naasc/SV/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'lustreCalDataPath': \
                       '/lustre/naasc/SV/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz', \
                   'macUncalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'macCalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz'}

#CASA 3.4
TWHydraBand7_34 = {'calibrationURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'TWHydraBand7_Calibration_3.4', \
                   'imagingURL': \
                       'http://casaguides.nrao.edu/index.php?title=' + \
                       'TWHydraBand7_Imaging_3.4', \
                   'uncalDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'calDataURL': \
                       'https://almascience.nrao.edu/almadata/sciver/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz', \
                   'lustreUncalDataPath': \
                       '/lustre/naasc/SV/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'lustreCalDataPath': \
                       '/lustre/naasc/SV/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz', \
                   'macUncalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                       'TWHYA_BAND7_UnCalibratedMSAndTablesForReduction.tgz', \
                   'macCalDataPath': \
                       '/Volumes/elric/benchmark_raw_data/TWHya/' + \
                       'TWHYA_BAND7_CalibratedData.tgz'}
##=============================================================================##

##Antennae Band 7##
AntennaeBand7_43 = {'calibrationURL': \
                        'http://casaguides.nrao.edu/index.php?title=' + \
                        'AntennaeBand7_Calibration_4.3', \
                    'imagingURL': \
                        'http://casaguides.nrao.edu/index.php?title=' + \
                        'AntennaeBand7_Imaging_4.3', \
                    'uncalDataURL': \
                        'https://almascience.nrao.edu/almadata/sciver/' + \
                        'AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'calDataURL': \
                        'https://almascience.nrao.edu/almadata/sciver/' + \
                        'AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz', \
                    'lustreUncalDataPath': \
                        '/lustre/naasc/SV/AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'lustreCalDataPath': \
                        '/lustre/naasc/SV/AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz', \
                    'macUncalDataPath': \
                        '/Volumes/elric/benchmark_raw_data/AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'macCalDataPath': \
                        '/Volumes/elric/benchmark_raw_data/AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz'}

#CASA 4.2
AntennaeBand7_42 = {'calibrationURL': \
                        'http://casaguides.nrao.edu/index.php?title=' + \
                        'AntennaeBand7_Calibration_4.2' , \
                    'imagingURL': \
                        'http://casaguides.nrao.edu/index.php?title=' + \
                        'AntennaeBand7_Imaging_4.2', \
                    'uncalDataURL': \
                        'https://almascience.nrao.edu/almadata/sciver/' + \
                        'AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'calDataURL': \
                        'https://almascience.nrao.edu/almadata/sciver/' + \
                        'AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz', \
                    'lustreUncalDataPath': \
                        '/lustre/naasc/SV/AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'lustreCalDataPath': \
                        '/lustre/naasc/SV/AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz', \
                    'macUncalDataPath': \
                        '/Volumes/elric/benchmark_raw_data/AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'macCalDataPath': \
                        '/Volumes/elric/benchmark_raw_data/AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz'}

#CASA 4.1
AntennaeBand7_41 = {'calibrationURL': \
                        'http://casaguides.nrao.edu/index.php?title=' + \
                        'AntennaeBand7_Calibration_4.1' , \
                    'imagingURL': \
                        'http://casaguides.nrao.edu/index.php?title=' + \
                        'AntennaeBand7_Imaging_4.1', \
                    'uncalDataURL': \
                        'https://almascience.nrao.edu/almadata/sciver/' + \
                        'AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'calDataURL': \
                        'https://almascience.nrao.edu/almadata/sciver/' + \
                        'AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz', \
                    'lustreUncalDataPath': \
                        '/lustre/naasc/SV/AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'lustreCalDataPath': \
                        '/lustre/naasc/SV/AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz', \
                    'macUncalDataPath': \
                        '/Volumes/elric/benchmark_raw_data/AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'macCalDataPath': \
                        '/Volumes/elric/benchmark_raw_data/AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz'}

#CASA 4.0
AntennaeBand7_40 = {'calibrationURL': \
                        'http://casaguides.nrao.edu/index.php?title=' + \
                        'AntennaeBand7_Calibration_4.0', \
                    'imagingURL': \
                        'http://casaguides.nrao.edu/index.php?title=' + \
                        'AntennaeBand7_Imaging_4.0', \
                    'uncalDataURL': \
                        'https://almascience.nrao.edu/almadata/sciver/' + \
                        'AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'calDataURL': \
                        'https://almascience.nrao.edu/almadata/sciver/' + \
                        'AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz', \
                    'lustreUncalDataPath': \
                        '/lustre/naasc/SV/AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'lustreCalDataPath': \
                        '/lustre/naasc/SV/AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz', \
                    'macUncalDataPath': \
                        '/Volumes/elric/benchmark_raw_data/AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'macCalDataPath': \
                        '/Volumes/elric/benchmark_raw_data/AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz'}

#CASA 3.4
AntennaeBand7_34 = {'calibrationURL': \
                        'http://casaguides.nrao.edu/index.php?title=' + \
                        'AntennaeBand7_Calibration_3.4', \
                    'imagingURL': \
                        'http://casaguides.nrao.edu/index.php?title=' + \
                        'AntennaeBand7_Imaging_3.4', \
                    'uncalDataURL': \
                        'https://almascience.nrao.edu/almadata/sciver/' + \
                        'AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'calDataURL': \
                        'https://almascience.nrao.edu/almadata/sciver/' + \
                        'AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz', \
                    'lustreUncalDataPath': \
                        '/lustre/naasc/SV/AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'lustreCalDataPath': \
                        '/lustre/naasc/SV/AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz', \
                    'macUncalDataPath': \
                        '/Volumes/elric/benchmark_raw_data/AntennaeBand7/' + \
                      'Antennae_Band7_UnCalibratedMSandTablesForReduction.tgz', \
                    'macCalDataPath': \
                        '/Volumes/elric/benchmark_raw_data/AntennaeBand7/' + \
                        'Antennae_Band7_CalibratedData.tgz'}
##=============================================================================##

##IRAS 16293 Band 9##
#CASA 4.3
IRASBand9_43 = {'calibrationURL': \
                    'http://casaguides.nrao.edu/index.php?title=' + \
                    'IRAS16293_Band9_-_Calibration_for_CASA_4.3', \
                'imagingURL': \
                    'http://casaguides.nrao.edu/index.php?title=' + \
                    'IRAS16293_Band9_-_Imaging_for_CASA_4.3', \
                'uncalDataURL': \
                    'https://almascience.nrao.edu/almadata/sciver/' + \
                    'IRAS16293B9/IRAS16293_Band9_UnCalibratedMS.tgz', \
                'calDataURL': \
                    'https://almascience.nrao.edu/almadata/sciver/' + \
                    'IRAS16293B9/IRAS16293_Band9_CalibratedMS_FIXED.tgz', \
                'lustreUncalDataPath': \
                    '/lustre/naasc/SV/IRAS16293B9/' + \
                    'IRAS16293_Band9_UnCalibratedMS.tgz', \
                'lustreCalDataPath': \
                    '/lustre/naasc/SV/IRAS16293B9/' + \
                    'IRAS16293_Band9_CalibratedMS_FIXED.tgz', \
                'macUncalDataPath': \
                    '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                    'IRAS16293_Band9_UnCalibratedMS.tgz', \
                'macCalDataPath': \
                    '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                    'IRAS16293_Band9_CalibratedMS_FIXED.tgz'}

#CASA 4.2
IRASBand9_42 = {'calibrationURL': \
                    'http://casaguides.nrao.edu/index.php?title=' + \
                    'IRAS16293_Band9_-_Calibration_for_CASA_4.2', \
                'imagingURL': \
                    'http://casaguides.nrao.edu/index.php?title=' + \
                    'IRAS16293_Band9_-_Imaging_for_CASA_4.2', \
                'uncalDataURL': \
                    'https://almascience.nrao.edu/almadata/sciver/' + \
                    'IRAS16293B9/IRAS16293_Band9_UnCalibratedMS.tgz', \
                'calDataURL': \
                    'https://almascience.nrao.edu/almadata/sciver/' + \
                    'IRAS16293B9/IRAS16293_Band9_CalibratedMS_FIXED.tgz', \
                'lustreUncalDataPath': \
                    '/lustre/naasc/SV/IRAS16293B9/' + \
                    'IRAS16293_Band9_UnCalibratedMS.tgz', \
                'lustreCalDataPath': \
                    '/lustre/naasc/SV/IRAS16293B9/' + \
                    'IRAS16293_Band9_CalibratedMS_FIXED.tgz', \
                'macUncalDataPath': \
                    '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                    'IRAS16293_Band9_UnCalibratedMS.tgz', \
                'macCalDataPath': \
                    '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                    'IRAS16293_Band9_CalibratedMS_FIXED.tgz'}

#CASA 4.0
IRASBand9_40 = {'calibrationURL': \
                    'http://casaguides.nrao.edu/index.php?title=' + \
                    'IRAS16293_Band9_-_Calibration_for_CASA_4.0', \
                'imagingURL': \
                    'http://casaguides.nrao.edu/index.php?title=' + \
                    'IRAS16293_Band9_-_Imaging_for_CASA_4.0', \
                'uncalDataURL': \
                    'https://almascience.nrao.edu/almadata/sciver/' + \
                    'IRAS16293B9/IRAS16293_Band9_UnCalibratedMS.tgz', \
                'calDataURL': \
                    'https://almascience.nrao.edu/almadata/sciver/' + \
                    'IRAS16293B9/IRAS16293_Band9_CalibratedMS_FIXED.tgz', \
                'lustreUncalDataPath': \
                    '/lustre/naasc/SV/IRAS16293B9/' + \
                    'IRAS16293_Band9_UnCalibratedMS.tgz', \
                'lustreCalDataPath': \
                    '/lustre/naasc/SV/IRAS16293B9/' + \
                    'IRAS16293_Band9_CalibratedMS_FIXED.tgz', \
                'macUncalDataPath': \
                    '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                    'IRAS16293_Band9_UnCalibratedMS.tgz', \
                'macCalDataPath': \
                    '/Volumes/elric/benchmark_raw_data/IRAS16293Band9/' + \
                    'IRAS16293_Band9_CalibratedMS_FIXED.tgz'}
##=============================================================================##

##2011.0.00367.S##
#THIS DATA IS NOT ON THE SCIENCE PORTAL
#CASA 3.3
x2011_0_00367_S_33 = {'calibrationURL': \
                          '/export/lustre/jcrossle/benchmark/scripts/' + \
                          '2011.0.00367.S_sb_calibration.py', \
                      'imagingURL': \
                          '/export/lustre/jcrossle/benchmark/scripts/' + \
                          '2011.0.00367.S_calibration_image.py', \
                      'uncalDataURL': \
                          None, \
                      'calDataURL': \
                          None, \
                      'lustreUncalDataPath': \
                          '/export/lustre/jcrossle/benchmark/data/' + \
                          '2011.0.00367.S.tgz', \
                      'lustreCalDataPath': \
                          None, \
                      'macUncalDataPath': \
                          None, \
                      'macCalDataPath': \
                          None}
##=============================================================================##

##M100 Band 3##
#CASA 3.3
M100Band3_33 = {'calibrationURL': \
                    'https://almascience.nrao.edu/almadata/sciver/M100Band3/' + \
                    'M100_Band3_Calibration.py', \
                'imagingURL': \
                    'https://almascience.nrao.edu/almadata/sciver/M100Band3/' + \
                    'M100_Band3_Imaging.py', \
                'uncalDataURL': \
                    'https://almascience.nrao.edu/almadata/sciver/M100Band3/' + \
                    'M100_Band3_UnCalibratedMSAndTablesForReduction.tgz', \
                'calDataURL': \
                    'https://almascience.nrao.edu/almadata/sciver/M100Band3/' + \
                    'M100_Band3_CalibratedData.tgz', \
                'lustreUncalDataPath': \
                    '/lustre/naasc/SV/M100Band3' + \
                    'M100_Band3_UnCalibratedMSAndTablesForReduction.tgz', \
                'lustreCalDataPath': \
                    '/lustre/naasc/SV/M100Band3' + \
                    'M100_Band3_CalibratedData.tgz', \
                'macUncalDataPath': \
                    None, \
                'macCalDataPath': \
                    None}
##=============================================================================##

##SgrA Band 6##
#CASA 3.3
SgrABand6_33 = {'calibrationURL': \
                    'https://almascience.nrao.edu/almadata/sciver/SgrABand6/' + \
                    'SgrA_Band6_Calibration.py', \
                'imagingURL': \
                    'https://almascience.nrao.edu/almadata/sciver/SgrABand6/' + \
                    'SgrA_Band6_Imaging.py', \
                'uncalDataURL': \
                    'https://almascience.nrao.edu/almadata/sciver/SgrABand6/' + \
                    'SgrA_Band6_UnCalibratedMSAndTablesForReduction.tgz', \
                'calDataURL': \
                    'https://almascience.nrao.edu/almadata/sciver/SgrABand6/' + \
                    'SgrA_Band6_CalibratedData.tgz', \
                'lustreUncalDataPath': \
                    '/lustre/naasc/SV/SgrABand6/' + \
                    'SgrA_Band6_UnCalibratedMSAndTablesForReduction.tgz', \
                'lustreCalDataPath': \
                    '/lustre/naasc/SV/SgrABand6/' + \
                    'SgrA_Band6_CalibratedData.tgz', \
                'macUncalDataPath': \
                    None, \
                'macCalDataPath': \
                    None}
##=============================================================================##
