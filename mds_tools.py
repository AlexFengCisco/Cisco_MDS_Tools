'''
Created on Nov 20, 2018

@author: alfeng
'''

from ciscoconfparse import CiscoConfParse
import time
import mds_sh_run_files as SF





class MDS_Tools():
    '''
    Note: this parse will automatically ignore ! which is means memo in cisco classic configuration ,
so when parse fcdomain fcid database , all alias will be ignored 

    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        pass
    
    def compare_fcid_database(self,cfg_file_01,cfg_file_02):
        
        
        cfg_parse_01 = self.parse_cfg_file(cfg_file_01)
        cfg_parse_02 = self.parse_cfg_file(cfg_file_02)
        
        fcdomain_list_01=[]
        for obj_fcdomain_list_01 in cfg_parse_01.find_all_children("cdomain fcid database"):
            fcdomain_list_01.append(obj_fcdomain_list_01)
         
        fcdomain_list_02=[]
        for obj_fcdomain_list_02 in cfg_parse_02.find_all_children("cdomain fcid database"):
            fcdomain_list_02.append(obj_fcdomain_list_02)   
        
        fcdomain_count_01=len(fcdomain_list_01[1:]) 
        fcdomain_count_02=len(fcdomain_list_02[1:])
        
        #print "MDS 01 fcdomain list count is :" + str(fcdomain_count_01)
        #print "MDS 02 fcdomain list count is :" + str(fcdomain_count_02)
        
        missed_fcid_list=[]
        
        if fcdomain_count_01>fcdomain_count_02:
            missed_mds="MDS 02"
            #print "for 1 in 2 check "
            for fcdomain_item_01 in fcdomain_list_01[1:]:
                if fcdomain_item_01 in fcdomain_list_02[1:]:
                    pass
                else:
                    #print "Missed fcid in MDS 01 "+fcdomain_item_01
                    missed_fcid_list.append(fcdomain_item_01)
        else:
            missed_mds="MDS 01"
            #print "for 2 in 1 check"
            for fcdomain_item_02 in fcdomain_list_02[1:]:
                if fcdomain_item_02 in fcdomain_list_01[1:]:
                    pass
                else:
                    #print "Missed fcid in MDS 02 "+fcdomain_item_02
                    missed_fcid_list.append(fcdomain_item_02)
        return (missed_mds,missed_fcid_list)
    
    
    def compare_zone_active(self,cfg_file_01,cfg_file_02):
        
        '''
        Assume all MDS switches has same active zone ,just compare miss * part , or miss zone member part
        
        in case of low performance , strongly recommend use show zone active file to reduce the compute time , usually , 5000 zones compare time is 10 minutes
        '''
        zone_active_dbs_01=self.parse_zone_active_dbs(cfg_file_01)
        zone_active_dbs_02=self.parse_zone_active_dbs(cfg_file_02)
        
        
        cfg_parse_01 = CiscoConfParse(zone_active_dbs_01.splitlines())
        cfg_parse_02 = CiscoConfParse(zone_active_dbs_02.splitlines())
        
        #cfg_parse_01 = self.parse_cfg_file(cfg_file_01)
        #cfg_parse_02 = self.parse_cfg_file(cfg_file_02)
        
        zone_list=[]
        for obj_zone_list in cfg_parse_01.find_objects("zone name"):
            zone_list.append(obj_zone_list.text)
        
        total=len(zone_list)
        progressing = 0
        init_percent = 0
            
        print "Zone Database Count : "+ str(len(zone_list))
        
        error_zones=[]
        
        for zone in zone_list:
            zone01_members = cfg_parse_01.find_all_children(zone)
            zone02_members = cfg_parse_02.find_all_children(zone)
            #print zone
            #print zone01_members
            #print zone02_members
           
    
            if zone01_members  == zone02_members :
                pass
                #print "SAME  zone name = "+zone
            else:
                error_zonename= "DIFF zone name = "+zone
                error_sw1_member = "MDS sw01 "+str(zone01_members)
                error_sw2_member =  "MDS sw02 "+str(zone02_members)
                error_zones.append([error_zonename,error_sw1_member,error_sw2_member])
                #print error_zones
               
            progressing+=1
            if str(float(progressing)/total)[2] == str(init_percent) :
                print "Analyzing  Percent "+str(float(progressing)/total)[2]+'0%'
                init_percent+=1
            
            
        return error_zones
    
    def compare_zone_active_01(self,cfg_file_01,cfg_file_02):
        
        '''
        Assume all MDS switches has same active zone ,just compare miss * part , or miss zone member part
        
        in case of low performance , strongly recommend use show zone active file to reduce the compute time , usually , 5000 zones compare time is 10 minutes
        '''
        zone_active_dbs_01=self.parse_zone_active_dbs(cfg_file_01)
        zone_active_dbs_02=self.parse_zone_active_dbs(cfg_file_02)
        
        zone_active_dbs_01_lines=zone_active_dbs_01.splitlines()
        zone_active_dbs_02_lines=zone_active_dbs_02.splitlines()
        
        print type(zone_active_dbs_01_lines)
        #for i in zone_active_dbs_01_lines:
            #print i
        '''
        cfg_parse_01 = CiscoConfParse(zone_active_dbs_01.splitlines())
        cfg_parse_02 = CiscoConfParse(zone_active_dbs_02.splitlines())
        
        #cfg_parse_01 = self.parse_cfg_file(cfg_file_01)
        #cfg_parse_02 = self.parse_cfg_file(cfg_file_02)
        
        
        
        zone_list=[]
        for obj_zone_list in cfg_parse_01.find_objects("zone name"):
            zone_list.append(obj_zone_list.text)
        
        total=len(zone_list)
        progressing = 0
        init_percent = 0
            
        print "Zone Database Count : "+ str(len(zone_list))
        
        error_zones=[]
        
        for zone in zone_list:
            zone01_members = cfg_parse_01.find_all_children(zone)
            zone02_members = cfg_parse_02.find_all_children(zone)
            #print zone
            #print zone01_members
            #print zone02_members
           
    
            if zone01_members  == zone02_members :
                pass
                #print "SAME  zone name = "+zone
            else:
                error_zonename= "DIFF zone name = "+zone
                error_sw1_member = "MDS sw01 "+str(zone01_members)
                error_sw2_member =  "MDS sw02 "+str(zone02_members)
                error_zones.append([error_zonename,error_sw1_member,error_sw2_member])
                #print error_zones
               
            progressing+=1
            if str(float(progressing)/total)[2] == str(init_percent) :
                print "Analyzing  Percent "+str(float(progressing)/total)[2]+'0%'
                init_percent+=1
            
         '''   
        return #error_zones
    
    def parse_cfg_file(self,cfg_file):
        
        cfg= open(cfg_file).read().splitlines()
        cfg_parse = CiscoConfParse(cfg)
        
        return cfg_parse
    
    def parse_zone_active_dbs(self,sh_run):
        
        cfg= open(sh_run).read()

        #print type(cfg)

        zone_db_index=[]
        index_zone_active=-1
        while True:
            index_zone_active=cfg.find('Active Zone Database',index_zone_active+1)
            index_zone_full=cfg.find('Full Zone Database',index_zone_active+1)
            if index_zone_active == -1 :
                break
            zone_db_index.append([index_zone_active,index_zone_full])
           
        #print zone_db_index
        
        zone_active_DBs=''
        
        for index in zone_db_index:
            zone_active_db=cfg[index[0]:index[1]-1]
            zone_active_DBs=zone_active_DBs+zone_active_db
        
        
        return zone_active_DBs
    
start_time=time.time()    

tool=MDS_Tools()
result=tool.compare_zone_active_01(SF.MDS_SH_RUN_01,SF.MDS_SH_RUN_02)

# try new git branch

print 'try new branch'

##### test comapre zone active 
'''
result = tool.compare_zone_active(SF.MDS_SH_RUN_01,SF.MDS_SH_RUN_02)
for item in result:
    print "error zone name "+item[0]
    print "sw01 error zone member" + item[1]
    print "sw01 error zone member" + item[2]
    print ('='*200)
'''
##### test compare fcid database
'''
result= tool.compare_fcid_database(SF.MDS_SH_RUN_01,SF.MDS_SH_RUN_02)

error_mds=result[0]
missed_list=result[1]


print "error switch is "+error_mds
print "missed fcid list below "
for item in missed_list:
    print item
'''
##### end test compare fcid database    
    
end_time=time.time()-start_time
print "Process took "+str(end_time)+" seconds"
