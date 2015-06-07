#edit the fields below and save for the benchmarking itinerary you want

#information needed:
#  -host names
#  -data sets
#  -number of iterations of each data set
#  -whether data should be downloaded from HTTP or not
#  -execution steps for each data set
#  -sources of scripts for each data set
#  -working directory on host

itinerary = {'hosts': {'cvpost045': {'dataSets': ['x2012_1_00912_S_43', \
                                                  'NGC3256Band3_43'], \
                                     'nIters': [2, 2], \
                                     'skipDownloads': [True, False], \
                                     'steps': ['both', 'im'], \
                                     'scriptSources': ['disk', 'web'], \
                                     'workDir': '/lustre/naasc/nbrunett/' + \
                                                'bench_code_devel/testing/' + \
                                                'test_remote_subprocess'}, \
                       'gauss': {'dataSets': ['x2012_1_00912_S_43', \
                                              'NGC3256Band3_43'], \
                                 'nIters': [2, 2], \
                                 'skipDownloads': [True, False], \
                                 'steps': ['both', 'im'], \
                                 'scriptSources': ['disk', 'web'], \
                                 'workDir': '/lustre/naasc/nbrunett/' + \
                                            'bench_code_devel/testing/' + \
                                            'test_remote_subprocess'}, \
                       'technomage': {'dataSets': ['x2012_1_00912_S_43', \
                                                   'NGC3256Band3_43'], \
                                      'nIters': [2, 2], \
                                      'skipDownloads': [True, False], \
                                      'steps': ['both', 'im'], \
                                      'scriptSources': ['disk', 'web'],\
                                      'workDir': '/lustre/naasc/nbrunett/' + \
                                                 'bench_code_devel/testing/' + \
                                                 'test_remote_subprocess'}}}
