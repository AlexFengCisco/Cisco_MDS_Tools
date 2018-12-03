'''
Created on Nov 20, 2018

@author: alfeng
'''
import time
import mds_tools as MT
import mds_sh_run_files as SF





if __name__ == '__main__':

    start_time = time.time()

    tool = MT.MdsTools()
    result = tool.compare_fcid_database(SF.MDS_SH_RUN_01, SF.MDS_SH_RUN_02)
    print "Switch MDS_01 fcid count is " + str(result[0])
    print "missed fcid list below "
    for item in result[3]:
        print item

    print "Switch MDS_02 fcid count is " + str(result[2])
    print "missed fcid list below "
    for item in result[1]:
        print item

    end_time = time.time() - start_time
    print "process during " + str(end_time) + "seconds"
