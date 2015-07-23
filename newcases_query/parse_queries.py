# -*- coding: utf-8 -*-
"""
Script that reads in a list of PostgreSQL - Date Difference in Months - prequery between imaging records and procedure available in biomatrix
1) selects cases only when difference = 0 < monthsdiff < 3 (i.e procedure within 3 months after imaging)

Created on Wed Apr 08 10:02:20 2015

@ author (C) Cristina Gallego, University of Toronto
----------------------------------------------------------------------
 """
import os, os.path
import sys
from sys import argv, stderr, exit
import numpy as np
import dicom
import psycopg2
import pandas as pd

from query_mydatabase import *
from base import Base, engine

from sqlalchemy.orm import sessionmaker


if __name__ == '__main__':    
    # Get Root folder ( the directory of the script being run)
    path_rootFolder = os.path.dirname(os.path.abspath(__file__))
    print path_rootFolder

    #############################
    ###### 1) Querying Research database for all imaging available '2001-08- to '2013-08' with procedures
    #############################       
    # Open filename list
    file_ids = open("CADpt_records_w_procedure_monthsdiff.txt","r")
    file_ids.seek(0)
    
    file_outids = open("CADpt_records_w_procedure_monthsdiff_within3mths.txt","w")   
   
    # this gets header
    line = file_ids.readline()
    print line
    # then get first case
    line = file_ids.readline()
    print line

    # form lists of patients and studies
    CAD_pts_within3mths = []
    access_numbers_within3mths = []
    
    while ( line ) : 
        # Get the line:     
        fileline = line.split('|')
        StudyID = int(fileline[0])
        examdateID = fileline[1] 
        a_number_txt = fileline[2]
        mri_cad_status_txt = fileline[3]
        proc_dt_datetime = fileline[4] 
        monthsdiff = fileline[5]
        interimg = fileline[6]
        if( fileline[5] ): monthsdiff = int(fileline[5])
        if (fileline[6] != '\n'): interimg = int(fileline[6])
    
        print "\n-------\n"+line
        if(interimg and interimg <= 0 and interimg >= -12 and monthsdiff != '\n' and monthsdiff >= 0  and monthsdiff <= 3 ):
                CAD_pts_within3mths.append(StudyID)
                access_numbers_within3mths.append(a_number_txt)
                file_outids.write(line) # write to file to process later                
                print "yes"
        
        line = file_ids.readline()
             
    # To get a unique collection of items is to use a set. Sets are unordered collections of distinct objects.
    file_outids.close()
    file_ids.close()
    allCAD_pts_within3mths = list(set(CAD_pts_within3mths))
    print "\n-------\nNumber of patients in imaging interval = %d" % len(allCAD_pts_within3mths)
    print sort(allCAD_pts_within3mths)
    
    allaccess_numbers_within3mthss = list(set(access_numbers_within3mths)) # this returns 815 patients
    print "\n-------\nNumber of studies in imaging interval = %d" % len(allaccess_numbers_within3mthss)


    #############################
    ###### 2) Of those imaging available '2001-08- to '2013-08' with procedures, select BIRADS 3,4,5 for specific lesions
    #############################    
    file_outids = open("CADpt_records_w_procedure_monthsdiff_within3mths.txt","r")
    file_outids.seek(0)
    
    file_lesionsids = open("accessions_BIRADS345_CADpt_records_w_procedure_monthsdiff_within3mths.txt","w")  
    
    # then get first case
    line = file_outids.readline()
    print line
     
    # Create the database: the Session. 
    queryBio = Query()
    lesions_CADpts = []   
    CAD_pts = []
    CAD_pts_accessions = []
        
    # form lists of patients and studies    
    while ( line ) : 
        # Get the line:     
        fileline = line.split('|')
        StudyID = fileline[0]
        examdateID = fileline[1] 
        a_number_txt = fileline[2]
        mri_cad_status_txt = fileline[3]
        proc_dt_datetime = fileline[4] 
        
        print "Executing SQL connection..."  
        # Create the session database: the Session. 
        Session = sessionmaker()
        Session.configure(bind=engine)  # once engine is available
        session = Session() #instantiate a Session
         
        # Format query reprocdateID
        redateID = datetime.date(int(examdateID[0:4]), int(examdateID[5:7]), int(examdateID[8:10]))
        # display GUI
        #guiinfo = queryBio.QuerymyDatabase_byid(StudyID, redateID)
        # no gui collect stats 
        # first query only exam/procedure info
        queryBio.queryDatabasewNoGui(session, StudyID, redateID)
        session.close()
        
        #catch mass records
        if(queryBio.is_mass):
            print "\n-------\nFound Mass lesion..."
            massframe = pd.DataFrame(data=array( queryBio.is_mass ))
            massframe.columns = list(queryBio.colLabelsmass)
            massframe = massframe.drop_duplicates()
            massframe.index = range(len(massframe))
            print massframe
            
            for k in range(len(massframe)):
                birads = massframe['finding.all_birads_scr_int'][k]
                            
                if (birads >=3):
                    CAD_pts.append(StudyID)
                    CAD_pts_accessions.append(a_number_txt)
                    lesions_CADpts.append(  str(massframe.iloc[k].values.tolist()) )
                    file_lesionsids.write( StudyID+'\t'+a_number_txt+'\t'+examdateID+'\t'+"mass"+'\t'+str(massframe.iloc[k].values.tolist())+'\n' ) # write to file to process later     
            
        #catch nonmass records
        if(queryBio.is_nonmass):
            print "\n-------\nFound Non-mass lesion..."
            nonmassframe = pd.DataFrame(data=array( queryBio.is_nonmass ))
            nonmassframe.columns = list(queryBio.colLabelsnonmass)
            nonmassframe = nonmassframe.drop_duplicates()
            nonmassframe.index = range(len(nonmassframe))
            print nonmassframe
            
            for k in range(len(nonmassframe)):
                birads = nonmassframe['finding.all_birads_scr_int'][k]
            
                if (birads >=3):
                    CAD_pts.append(StudyID)
                    CAD_pts_accessions.append(a_number_txt)
                    lesions_CADpts.append( str(nonmassframe.iloc[k].values.tolist())  )
                    file_lesionsids.write( StudyID+'\t'+a_number_txt+'\t'+examdateID+'\t'+"nonmass"+'\t'+str(nonmassframe.iloc[k].values.tolist())+'\n' ) # write to file to process later     
                                    
        # read next line       
        line = file_outids.readline()
        print "\n===========================\n"
        print line
        
        
    # To get a unique collection of items is to use a set. Sets are unordered collections of distinct objects.
    print "\n-------\nFinalizing..."
    file_outids.close()
    file_lesionsids.close()
    
    allCAD_pts = list(set(CAD_pts))
    print "\n-------\nNumber of patients in imaging interval = %d" % len(allCAD_pts)
    print sort(allCAD_pts)
    
    allaccessions_CADpts = list(set(CAD_pts_accessions))
    print "\n-------\nNumber of accesssions imaging interval = %d" % len(allaccessions_CADpts)
    
    alllesions_CADpts = list(set(lesions_CADpts))
    print "\n-------\nNumber of lesions BIRADS 3,4,5,6 in imaging interval = %d" % len(lesions_CADpts)


    #############################
    ###### 2) Process the end of query
    #############################    
    # first for all lesions queried, drop duplicates
    df_lesions_CADpt = pd.read_table("accessions_BIRADS345_CADpt_records_w_procedure_monthsdiff_within3mths.txt")
    df_lesions_CADpt = df_lesions_CADpt.drop_duplicates()
    df_lesions_CADpt.columns=['CAD_StudyID','accessionN','dateID','CAD_MorNM','lesioninfo']
    df_lesions_CADpt.index = range(len(df_lesions_CADpt['CAD_StudyID']))
    df_lesions_CADpt.describe()
    df_lesions_CADpt.to_csv('lesions.csv')
#   results for CADStudys n= 1617     
#           CAD_StudyID
#    count  1617.000000
#    mean   3050.942486
#    std    2636.048132
#    min       2.000000
#    25%     672.000000
#    50%    2046.000000
#    75%    6071.000000
#    max    7231.000000
 
    CAD_StudyID = []
    CAD_MorNM = []
    CAD_BIRADS = []
    list_CADlesions = pd.DataFrame()      
    ithlesion = 0
    
    # form lists of patients and studies    
    for k in range(len(df_lesions_CADpt)):
        # Get the line:     
        StudyID = int( df_lesions_CADpt['CAD_StudyID'][k] )
        MorNM = df_lesions_CADpt['CAD_MorNM'][k]
        lesioninfo = df_lesions_CADpt['lesioninfo'][k].split(',')
        BIRADS = int(list(lesioninfo[10])[1])
         
        if( StudyID not in CAD_StudyID):
            CAD_StudyID.append(StudyID) 
            CAD_MorNM.append(MorNM)
            CAD_BIRADS.append(BIRADS)
            list_CADlesions = list_CADlesions.append(  pd.DataFrame({'StudyID' : StudyID, 'MorNM': MorNM, 'BIRADS' : BIRADS}, index=[ithlesion]) ) 
            print list_CADlesions.irow(ithlesion)
            ithlesion += 1
    
    print "\n-------\nNumber of patients with a mass/nonmass BIRADS 3,4,5,6 in imaging interval = %d" % len(CAD_StudyID)
 
    hist(CAD_BIRADS)   
    
    ########
    ## process only selected
    print list_CADlesions
    list_CADlesions.to_csv('list_CADlesions.csv')
        
