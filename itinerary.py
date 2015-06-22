"""Storage module for CASA benchmarking with the run_benchmarks.py script.

Purpose
-------
This module is used to store the machines, data sets, stages and numbers of
iterations that make up all of the benchmarking that will be carried out with
the run_benchmarks.py script. It is also setup to be the way the user actually
tells run_benchmarks.py what to run so editing this module's source file
(itinerary.py) is the first step in automated, parallel, benchmarking of
machines on the internal NRAO network.

Editing for Use with run_benchmarks.py
--------------------------------------
The first step of using run_benchmarks.py is to actually edit this module's
source file. When a copy of the CASA-Guides-Script-Extractor repository is
cloned, this module has an example itinerary already filled out. The easiest
way to make sure that dictionary is filled out properly is to just follow the
form of the example that it starts with. All of the values for each host (e.g.
dataSets, nIters, skipDownloads, etc.) are the inputs that will be used when
using the machine class included in this repository. It may help to review the
help docstring for the machine class to understand what is needed for each of
those values.
"""
itinerary = {'hosts': {'cvpost045': {'dataSets': ['x2012_1_00912_S_43', \
                                                  'NGC3256Band3_43'], \
                                     'nIters': [2, 2], \
                                     'skipDownloads': [True, False], \
                                     'steps': ['both', 'im'], \
                                     'scriptsSources': ['disk', 'web'], \
                                     'workDir': '/lustre/naasc/nbrunett/' + \
                                                'bench_code_devel/testing/' + \
                                                'test_remote_subprocess'}, \
                       'gauss': {'dataSets': ['x2012_1_00912_S_43', \
                                              'NGC3256Band3_43'], \
                                 'nIters': [2, 2], \
                                 'skipDownloads': [True, False], \
                                 'steps': ['both', 'im'], \
                                 'scriptsSources': ['disk', 'web'], \
                                 'workDir': '/lustre/naasc/nbrunett/' + \
                                            'bench_code_devel/testing/' + \
                                            'test_remote_subprocess'}, \
                       'technomage': {'dataSets': ['x2012_1_00912_S_43', \
                                                   'NGC3256Band3_43'], \
                                      'nIters': [2, 2], \
                                      'skipDownloads': [True, False], \
                                      'steps': ['both', 'im'], \
                                      'scriptsSources': ['disk', 'web'],\
                                      'workDir': '/lustre/naasc/nbrunett/' + \
                                                 'bench_code_devel/testing/' + \
                                                 'test_remote_subprocess'}}}
