# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:48:41 2015

@ author (C) Cristina Gallego, University of Toronto
--------------------------------------------------------------------
 """

import os, os.path
import sys
import string
from sys import argv, stderr, exit
import vtk
from numpy import *

# to query biomatrix only needed
from sqlalchemy.orm import sessionmaker
import database
from base import Base, engine

from mylocalbase import mynewengine
import mylocaldatabase
from query_mydatabase import *
from sendNew2_mydatabase import *

###
from add_newrecords import *


if __name__ == '__main__':    
    # Get Root folder ( the directory of the script being run)
    path_rootFolder = os.path.dirname(os.path.abspath(__file__))
    print path_rootFolder
       
    # Open filename list
    file_ids = open("allLesions_view.txt","r")
    file_ids.seek(0)
    
    line = file_ids.readline()
    print line
    line = file_ids.readline()
    print line
       
    while ( line ) : 
        # Get the line: id  	Study #	MRN	ProcedDate	Path-In situ ca	Path-Invasive ca
        fileline = line.split()
        lesion_id = int(fileline[0] )
        StudyID = fileline[1] 
        accessionN = fileline[2]  
        dateID = fileline[3]
        findingside = fileline[4]
        MorNM = fileline[5]
        Diagnosis = fileline[6]
        BorM = MorNM[-1]
        
        #############################
        #print "\n Adding record radiology"
        #SendNew2DB = SendNew()
        #radioinfo = SendNew2DB.queryRadioData(StudyID, dateID)
        #radioinfo = radioinfo.iloc[0]
        #SendNew2DB.addRecordDB_radiology(lesion_id, radioinfo)        
        
        ############# Query biomatrix
        print "Executing SQL connection..."
        # Format query StudyID
        if (len(StudyID) >= 4 ): fStudyID=StudyID
        if (len(StudyID) == 3 ): fStudyID='0'+StudyID
        if (len(StudyID) == 2 ): fStudyID='00'+StudyID
        if (len(StudyID) == 1 ): fStudyID='000'+StudyID
            
        try:
            biomtx_Session = sessionmaker()
            biomtx_Session.configure(bind=engine)  # once engine is available
            sessionbiomtx = biomtx_Session() #instantiate a Session
            
            queryBio = QuerymyDatabase()
            redateID = datetime.date(int(dateID[6:10]), int(dateID[3:5]), int(dateID[0:2]))
            radiologyinfo = queryBio.queryBiomatrixBIRADSage(sessionbiomtx, fStudyID, redateID)
            sessionbiomtx.close()
            
        except Exception:
            print "Not able to query biomatrix"
            pass
        
        # extract right BIRADS
        typeLesion = MorNM[:-1]
        if (findingside == 'R'):    sideLesion = 'Right'
        elif (findingside == 'L'):    sideLesion = 'Left'
        else: sideLesion = radiologyinfo['finding.side_int'].iloc[0]
                
        print(radiologyinfo[['finding.mri_mass_yn', 'finding.mri_nonmass_yn', 'finding.side_int']])
        checkside = radiologyinfo[ radiologyinfo['finding.side_int'] == sideLesion ]
        
        checkrow = []
        if( typeLesion == 'mass'):
            checkrow = checkside[ checkside['finding.mri_mass_yn'] == True ]
        if( typeLesion == 'nonmass'):
            checkrow = checkside[ checkside['finding.mri_nonmass_yn'] == True ]
    
        BIRADS = checkrow['finding.all_birads_scr_int'].iloc[0]            
        print BIRADS
        
        Session = sessionmaker()
        Session.configure(bind=mynewengine) 
        session = Session()
        
        for lesion in session.query(mylocaldatabase.Lesion_record).\
                filter(mylocaldatabase.Lesion_record.lesion_id == str(lesion_id)):
            # print results
            if not lesion:
                print "lesion is empty"
            else:
                print lesion

        lesion.BIRADS = int(BIRADS)
        lesion.anony_dob_datetime = radiologyinfo['pt.anony_dob_datetime'].iloc[0]
        session.flush()
        session.commit()
        session.close()
        line = file_ids.readline()
        print line
