# -*- coding: utf-8 -*-
"""
Get new cases from PACS only and query BIOMATRIX

Created on Mon Aug 11 09:19:14 2014

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

from query_database import *
import processDicoms

from dictionaries import my_aet, hostID, data_loc, local_port, clinical_aet, clinical_IP, clinical_port, remote_aet, remote_IP, remote_port
import dcmtk_routines as dcmtk

from inputs_init import *
from display import *
from segment import *
from features_dynamic import *
from features_morphology import *
from features_texture import *
from features_T2 import *
import pylab      

 
from sqlalchemy import Column, Integer, String
import datetime
from mybase import myengine
import mydatabase
from sqlalchemy.orm import sessionmaker
from add_records import *
from sendNew2_mydatabase import *


def getScans(data_loc, img_folder, fileline, PatientID, StudyID, AccessionN, oldExamID):
    """
    run : getScans(path_rootFolder, PatientID, StudyID, AccessionN):

    Inputs
    ======
    path_rootFolder: (string)   Automatically generated based on the location of file 
    
    PatientID : (int)    MRN
    
    StudyID : (int)    CAD StudyID
    
    AccessionN : (int)  CAD AccessionN
    
    database : (bool) [True]   whether to check database for info about study.
    
    Output
    ====== 
    """
    try:
        dcmtk.check_MRI_MARTEL(data_loc, remote_aet, remote_port, remote_IP, local_port, PatientID, StudyID, AccessionN)
        if(oldExamID==False):
            dcmtk.pull_MRI_MARTEL(data_loc, img_folder, remote_aet, remote_port, remote_IP, local_port, PatientID, StudyID, AccessionN, countImages=False)
        else:
            ExamID = fileline[4]
            dcmtk.pull_MRI_MARTELold(data_loc, img_folder, remote_aet, remote_port, remote_IP, local_port, PatientID, StudyID, AccessionN, ExamID, countImages=False)
            
    except (KeyboardInterrupt, SystemExit):
        dcmtk.check_pacs(data_loc, img_folder,  clinical_aet , clinical_port, clinical_IP, local_port, PatientID, StudyID, AccessionN)
        dcmtk.pull_pacs(data_loc, img_folder, clinical_aet, clinical_port, clinical_IP, local_port, PatientID, StudyID, AccessionN)
    except (KeyboardInterrupt, SystemExit):
        print 'Unable to find study in MRI_MARTEL or AS0SUNB --- Abort'
        sys.exit()
        
    return  
    
    
if __name__ == '__main__':    
    # Get Root folder ( the directory of the script being run)
    path_rootFolder = os.path.dirname(os.path.abspath(__file__))
    print path_rootFolder
       
    # Open filename list
    print sys.argv[1]
    file_ids = open(sys.argv[1],"r")
    file_ids.seek(0)
    
    for k in range(1):
        line = file_ids.readline()
    print line
       
    while ( line ) : 
        # Get the line: id  	Study #	MRN	ProcedDate	Path-In situ ca	Path-Invasive ca
        fileline = line.split()
        lesion_id = int(fileline[0] )
        StudyID = fileline[1] 
        PatientID = fileline[2]  
        procdateID = fileline[3]
        Diagnosis = fileline[4:]
        print Diagnosis
        
        #############################
        ###### 1) Querying Research database for clinical, pathology, radiology data
        #############################
        SendNew2DB = SendNew()
        [img_folder, cond, BenignNMaligNAnt, Diagnosis, rowCase] = SendNew2DB.queryNewDatabase(StudyID, procdateID, Diagnosis)        
        
        AccessionN = SendNew2DB.casesFrame['exam.a_number_txt'].iloc[0]
        DicomExamNumber = SendNew2DB.casesFrame['exam.exam_img_dicom_txt'].iloc[0]
        dateID = SendNew2DB.casesFrame['exam.exam_dt_datetime'].iloc[0]
        if 'proc.proc_side_int' in SendNew2DB.casesFrame.keys():
            finding_side = SendNew2DB.casesFrame['proc.proc_side_int'].iloc[0]
        else:
            finding_side = 'NA'
        
        #############################
        ###### 2) Get Scans from pacs
        #############################
        getScans(data_loc, img_folder, fileline, PatientID, StudyID, AccessionN, oldExamID=False)
        
        ## continue to next case
        line = file_ids.readline()
        print line
       
    file_ids.close()