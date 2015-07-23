# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 16:48:07 2014

@ author (C) Cristina Gallego, University of Toronto
"""
import sys, os
import string
import datetime
from numpy import *

import datetime
from base import Base, engine
import database
import pandas as pd

from sqlalchemy.orm import sessionmaker

import wx
import wxTableBase

#!/usr/bin/env python
class Query(object):
    """
    USAGE:
    =============
    dbdata = QuerymyDatabase()
    """
    def __call__(self):       
        """ Turn Class into a callable object """
        Query()
        
        
    def __init__(self): 
        """ initialize QueryDatabase """
    

    def QuerymyDatabase_byid(self, StudyID, redateID):
        """
        run : Query by StudyID/AccesionN pair study to local folder
        
        Inputs
        ======
        StudyID : (int)    CAD StudyID
        redateID : (int)  CAD StudyID Data of exam (format yyyy-mm-dd)
        
        Output
        ======
        """               
        # Create the database: the Session. 
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)  # once engine is available
        session = self.Session() #instantiate a Session
        
        # Create first display
        """ Creates Table grid and Query output display Cad_Container"""
        self.app = wx.App(False)
        self.display = wxTableBase.Container(self.app)
        
        self.datainfo = []; self.is_mass=[];  self.is_nonmass=[]; self.pathology=[]; radreport=[];
        for cad, exam, finding, proc, patho in session.query(database.Cad_record, database.Exam_record, database.Exam_Finding, database.Procedure, database.Pathology).\
                     filter(database.Cad_record.pt_id==database.Exam_record.pt_id).\
                     filter(database.Exam_record.pt_exam_id==database.Exam_Finding.pt_exam_id).\
                     filter(database.Exam_record.pt_id==database.Procedure.pt_id).\
                     filter(database.Procedure.pt_procedure_id==database.Pathology.pt_procedure_id).\
                     filter(database.Cad_record.cad_pt_no_txt == str(StudyID)).\
                     filter(database.Exam_record.exam_dt_datetime == str(redateID)).all():
                         
           # print results
           if not cad:
               print "cad is empty"
           if not exam:
               print "exam is empty"
           if not finding:
               print "finding is empty"
           if not proc:
               print "proc is empty"
           if not patho:
               print "patho is empty"
                   
           self.datainfo.append([cad.cad_pt_no_txt, cad.latest_mutation_status_int,
              exam.exam_dt_datetime, exam.a_number_txt, exam.exam_img_dicom_txt, exam.mri_cad_status_txt, exam.comment_txt, exam.original_report_txt,
              finding.mri_mass_yn, finding.mri_nonmass_yn, finding.mri_foci_yn,
              proc.pt_procedure_id, proc.proc_dt_datetime, proc.proc_side_int, proc.proc_source_int, proc.proc_guid_int, proc.proc_tp_int, proc.original_report_txt])
           
           # Create rad report dataset
           radreport.append([ str(exam.original_report_txt), str(exam.comment_txt)])
           
           #iterate through patho keys
           pathodict = patho.__dict__
           pathokeys = pathodict.keys()
           pathoItems = pathodict.items()
           procpath=[]; procLabels=[];
           for k in range(len(pathokeys)):
               if( pathoItems[k][1] ):
                   procpath.append( pathoItems[k][1] )
                   procLabels.append( str(pathoItems[k][0]) )
           
           # add procedure lesion record table 
           self.pathology.append(procpath)
           rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(self.pathology))])
           # Add display query to wxTable    
           self.display.MassNonM_Container_initGUI(self.pathology, rowLabels, procLabels, "procedure/pathology")
           self.pathology=[];  
           
           # Find if it's mass or non-mass and process
           if (finding.mri_mass_yn):
               self.is_mass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_mass_margin_int, finding.mammo_n_mri_mass_shape_int, finding.t2_signal_int, finding.all_birads_scr_int])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_nonmass_yn):
               self.is_nonmass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_nonmass_dist_int, finding.mri_nonmass_int_enh_int, finding.t2_signal_int, finding.all_birads_scr_int ])
          
          ####### finish finding masses and non-masses
        
        ################### Send to table display  
        # add main CAD record table       
        colLabels = ("cad.cad_pt_no_txt", "cad.latest_mutation", "exam.exam_dt_datetime","exam.a_number_txt","exam.exam_img_dicom_txt","exam.mri_cad_status_txt","exam.comment_txt","exam.original_report", "finding.mri_mass_yn", "finding.mri_nonmass_yn", "finding.mri_foci_yn", "proc.pt_procedure_id", "proc.proc_dt_datetime", "proc.proc_side_int", "proc.proc_source_int", "proc.proc_guid_int", "proc.proc_tp_int", "proc.original_report_txt")
        rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(self.datainfo))])
        # Add display query to wxTable    
        self.display.Cad_Container_initGUI(self.datainfo, rowLabels, colLabels)
        
        # write output query to pandas frame.
        radreport_label = ("exam.original_report_txt", "exam.comment_txt")
        self.radreport = pd.DataFrame(data=array(radreport), columns=list(radreport_label))
           
        # write output query to pandas frame.
        self.d1 = pd.DataFrame(data=array(self.datainfo), columns=list(colLabels))
        
        # add mass lesion record table
        self.colLabelsmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_mass_margin_int", "finding.mammo_n_mri_mass_shape_int", "finding.t2_signal_int", "finding.all_birads_scr_int")
        rowLabelsmass = tuple(["%s" % str(x) for x in xrange(0,len(self.is_mass))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(self.is_mass, rowLabelsmass, self.colLabelsmass, "Masses")
        
        # add non-mass lesion record table
        self.colLabelsnonmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_nonmass_dist_int", "finding.mri_nonmass_int_enh_int", "finding.t2_signal_int", "finding.all_birads_scr_int")
        rowLabelsnonmass = tuple(["%s" % str(x) for x in xrange(0,len(is_nonmass))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(self.is_nonmass, rowLabelsnonmass, self.colLabelsnonmass, "NonMasses")
        
        # Finish the display and Show
        self.display.Centre()
        self.display.Show()
        self.app.MainLoop()    
        
        return 

    def queryDatabasewNoGui(self, session, StudyID, redateID):
        """
        run : Query by StudyID/AccesionN pair study to local folder
        
        Inputs
        ======
        StudyID : (int)    CAD StudyID
        redateID : (int)  CAD StudyID Data of exam (format yyyy-mm-dd)
        
        Output
        ======
        """
        
        self.datainfo = []; self.is_mass=[];  self.is_nonmass=[]; self.pathology=[]; 
        for cad, exam, finding, proc, patho in session.query(database.Cad_record, database.Exam_record, database.Exam_Finding, database.Procedure, database.Pathology).\
                     filter(database.Cad_record.pt_id==database.Exam_record.pt_id).\
                     filter(database.Exam_record.pt_exam_id==database.Exam_Finding.pt_exam_id).\
                     filter(database.Exam_record.pt_id==database.Procedure.pt_id).\
                     filter(database.Procedure.pt_procedure_id==database.Pathology.pt_procedure_id).\
                     filter(database.Cad_record.cad_pt_no_txt == str(StudyID)).\
                     filter(database.Exam_record.exam_dt_datetime == str(redateID)).all():
                         
           # print results
           if not cad:
               print "cad is empty"
           if not exam:
               print "exam is empty"
           if not finding:
               print "finding is empty"
           if not proc:
               print "proc is empty"
           if not patho:
               print "patho is empty"
                   
           self.datainfo.append([cad.cad_pt_no_txt, cad.latest_mutation_status_int,
              exam.exam_dt_datetime, exam.a_number_txt, exam.mri_cad_status_txt, exam.comment_txt,
              finding.mri_mass_yn, finding.mri_nonmass_yn, finding.mri_foci_yn,
              proc.pt_procedure_id, proc.proc_dt_datetime, proc.proc_side_int, proc.proc_source_int, proc.proc_guid_int, proc.proc_tp_int, proc.original_report_txt])
           
           #iterate through patho keys
           pathodict = patho.__dict__
           pathokeys = pathodict.keys()
           pathoItems = pathodict.items()
           procpath=[]; procLabels=[];
           for k in range(len(pathokeys)):
               if( pathoItems[k][1] ):
                   procpath.append( pathoItems[k][1] )
                   procLabels.append( str(pathoItems[k][0]) )
           
           # add procedure lesion record table 
           self.pathology.append(procpath)
           rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(self.pathology))])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_mass_yn):
               self.is_mass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_mass_margin_int, finding.mammo_n_mri_mass_shape_int, finding.t2_signal_int, finding.all_birads_scr_int])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_nonmass_yn):
               self.is_nonmass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_nonmass_dist_int, finding.mri_nonmass_int_enh_int, finding.t2_signal_int, finding.all_birads_scr_int ])
          
          ####### finish finding masses and non-masses
        
        # add mass lesion record table
        self.colLabelsmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_mass_margin_int", "finding.mammo_n_mri_mass_shape_int", "finding.t2_signal_int", "finding.all_birads_scr_int")

        # add non-mass lesion record table
        self.colLabelsnonmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_nonmass_dist_int", "finding.mri_nonmass_int_enh_int", "finding.t2_signal_int", "finding.all_birads_scr_int")
        
        return 
        
        
        
    def queryDatabasewNoGui_wReasons(self, session, StudyID, redateID):
        """
        run : Query by StudyID/AccesionN pair study to local folder
        
        Inputs
        ======
        StudyID : (int)    CAD StudyID
        redateID : (int)  CAD StudyID Data of exam (format yyyy-mm-dd)
        
        Output
        ======
        """
        
        self.datainfo = []; self.is_mass=[];  self.is_nonmass=[]; self.pathology=[]; 
        for cad, exam, finding, proc, patho in session.query(database.Cad_record, database.Exam_record, database.Exam_Finding, database.Procedure, database.Pathology).\
                     filter(database.Cad_record.pt_id==database.Exam_record.pt_id).\
                     filter(database.Exam_record.pt_exam_id==database.Exam_Finding.pt_exam_id).\
                     filter(database.Exam_record.pt_id==database.Procedure.pt_id).\
                     filter(database.Procedure.pt_procedure_id==database.Pathology.pt_procedure_id).\
                     filter(database.Cad_record.cad_pt_no_txt == str(StudyID)).\
                     filter(database.Exam_record.exam_dt_datetime == str(redateID)).all():
                         
           # print results
           if not cad:
               print "cad is empty"
           if not exam:
               print "exam is empty"
           if not finding:
               print "finding is empty"
           if not proc:
               print "proc is empty"
           if not patho:
               print "patho is empty"
                   
           self.datainfo.append([cad.cad_pt_no_txt, cad.latest_mutation_status_int,
              exam.exam_dt_datetime, exam.a_number_txt, exam.mri_cad_status_txt, exam.comment_txt,
              finding.mri_mass_yn, finding.mri_nonmass_yn, finding.mri_foci_yn,
              proc.pt_procedure_id, proc.proc_dt_datetime, proc.proc_side_int, proc.proc_source_int, proc.proc_guid_int, proc.proc_tp_int, proc.original_report_txt])
           
           #iterate through patho keys
           pathodict = patho.__dict__
           pathokeys = pathodict.keys()
           pathoItems = pathodict.items()
           procpath=[]; procLabels=[];
           for k in range(len(pathokeys)):
               if( pathoItems[k][1] ):
                   procpath.append( pathoItems[k][1] )
                   procLabels.append( str(pathoItems[k][0]) )
           
           # add procedure lesion record table 
           self.pathology.append(procpath)
           rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(self.pathology))])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_mass_yn):
               self.is_mass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_mass_margin_int, finding.mammo_n_mri_mass_shape_int, finding.t2_signal_int, finding.all_birads_scr_int])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_nonmass_yn):
               self.is_nonmass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_nonmass_dist_int, finding.mri_nonmass_int_enh_int, finding.t2_signal_int, finding.all_birads_scr_int ])
          
          ####### finish finding masses and non-masses
        
        # add mass lesion record table
        self.colLabelsmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_mass_margin_int", "finding.mammo_n_mri_mass_shape_int", "finding.t2_signal_int", "finding.all_birads_scr_int")

        # add non-mass lesion record table
        self.colLabelsnonmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_nonmass_dist_int", "finding.mri_nonmass_int_enh_int", "finding.t2_signal_int", "finding.all_birads_scr_int")
        
        return