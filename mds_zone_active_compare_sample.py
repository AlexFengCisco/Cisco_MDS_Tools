'''
Created on Nov 20, 2018

@author: alfeng
'''
import mds_tools as MT
import mds_sh_run_files as SF
import time

start_time=time.time()    

tool=MT.MDS_Tools()

result = tool.compare_zone_active(SF.MDS_SH_RUN_01,SF.MDS_SH_RUN_02)

for item in result:
    print "error zone name "+item[0]
    print "sw01 error zone member" + item[1]
    print "sw01 error zone member" + item[2]
    print ('='*200)
    
end_time=time.time()-start_time    
print "process during "+str(end_time)+"seconds"



if __name__ == '__main__':
    pass