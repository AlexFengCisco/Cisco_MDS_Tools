'''
Created on Nov 20, 2018

@author: alfeng
'''
import mds_tools as MT
import mds_sh_run_files as SF
import time

start_time=time.time()    

tool=MT.MDS_Tools()
result= tool.compare_fcid_database(SF.MDS_SH_RUN_01,SF.MDS_SH_RUN_02)

error_mds=result[0]
missed_list=result[1]

end_time=time.time()-start_time
print "missed switch is "+error_mds
print "missed fcid list below "
for item in missed_list:
    print item
print "process during "+str(end_time)+"seconds"


if __name__ == '__main__':
    pass