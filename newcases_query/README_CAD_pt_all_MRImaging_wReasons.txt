 *** THIS QUERY INCLUDES BENIGN BY ASSUMPTION, ALL BENIGN BY PATHOLOGY AND MALIGNANT (excluding unknown)
1) Query to list all CAD_pt with only MRI  exam_tp_int records with and associated procedure
 - interimg calculates length of years from imaging to present date '2015-05-05' 

SELECT 
  tbl_pt_mri_cad_record.cad_pt_no_txt, 
  tbl_pt_exam.mri_cad_status_txt, 
  tbl_pt_demographics.gender_int, 
  tbl_pt_demographics.anony_dob_datetime, 
  (DATE_PART('year', tbl_pt_exam.exam_dt_datetime) - DATE_PART('year', tbl_pt_demographics.anony_dob_datetime)) as age,
  tbl_pt_exam.exam_tp_int, 
  tbl_pt_exam.exam_dt_datetime, 
  (DATE_PART('year', tbl_pt_exam.exam_dt_datetime) - DATE_PART('year', '2015-05-05'::date)) as interimg,
  tbl_pt_exam.a_number_txt, 
  tbl_pt_exam.sty_indicator_add_eval_as_folup_yn, 
  tbl_pt_exam.sty_indicator_folup_after_pre_exam_yn, 
  tbl_pt_exam.sty_indicator_rout_screening_obsp_yn, 
  tbl_pt_exam.sty_indicator_high_risk_yn, 
  tbl_pt_exam.sty_indicator_high_risk_prior_high_risk_marker_yn, 
  tbl_pt_exam.sty_indicator_high_risk_prior_personal_can_hist_yn, 
  tbl_pt_exam.sty_indicator_pre_operative_extent_of_dis_yn, 
  tbl_pt_exam.sty_indicator_pre_neoadj_trtmnt_yn, 
  tbl_pt_exam.sty_indicator_post_operative_margin_yn, 
  tbl_pt_exam.sty_indicator_post_neoadj_trtmnt_yn, 
  tbl_pt_exam.sty_indicator_prob_solv_diff_img_yn, 
  tbl_pt_exam.sty_indicator_folup_recommend_yn
FROM 
  public.tbl_pt_mri_cad_record, 
  public.tbl_pt_exam, 
  public.tbl_pt_demographics
WHERE 
  tbl_pt_mri_cad_record.pt_id = tbl_pt_demographics.pt_id AND
  tbl_pt_demographics.pt_id = tbl_pt_exam.pt_id AND
  tbl_pt_exam.exam_tp_int = 'MRI' AND 
  tbl_pt_exam.sty_indicator_mri_guided_bio_yn = 'f'
ORDER BY
  tbl_pt_mri_cad_record.cad_pt_no_txt ASC;



RESULTS: 7207 rows on May 5, 2015
The result of this query is saved to file CAD_pt_all_MRImaging_wReasons.txt



a) first select cases where 
    - append to all list of patients in the time interval of the study (which you need to mention) *** reviewver comment
b) of those, filter by tbl_pt_exam.mri_cad_status_txt to include:
    - Malignant (criteria 1)
    - Benign by pathology (criteria 2)
    - Benign by assumption (criteria 4, 5)



The result of this filtering is saved to file CAD_pt_all_MRImaging_wReasons_wCADstatus.txt
=========================================================================
In the imaging interval, there were a total of 974+32 = 1006  patients
Of those, 710 (52 with prior_CA) were Benign by assumption (criteria 4, 5)
254 (22 with prior_CA) Benign by pathology (criteria 2) and
150 (18 with prior_CA) Malignant (criteria 1) 
= 240 + (16 excluded for othr reasons, see below)


-------
Unique number of patients in imaging interval either: 
 - Malignant (criteria 1) 
  - Benign by pathology (criteria 2) 
 - Benign by assumption (criteria 4, 5) 
 = 1002
       StudyID a_number             CADstatus prior_marker prior_CA
count     2729     2729                  2729         2729     2729
unique    1002     2729                     4            2        2
top        342  3380838  Benign by assumption            f        f
freq        14        1                  2257         2648     2403


-------
Unique number of patients Benign by assumption (criteria 4, 5) 
 = 733
       StudyID a_number             CADstatus prior_marker prior_CA
count     2257     2257                  2257         2257     2257
unique     733     2257                     1            2        2
top        342  3380838  Benign by assumption            f        f
freq        14        1                  2257         2188     1986


-------
Patients Benign by assumption (criteria 4, 5) with prior prior_CA 
 = 65
       StudyID a_number             CADstatus prior_marker prior_CA
count     1986     1986                  1986         1986     1986
unique     668     1986                     1            2        1
top        342  3380838  Benign by assumption            f        f
freq        14        1                  1986         1920     1986
['1', '2', '3', '5', '6', '9', '14', '17', '18', '19', '21', '35', '38', '43', '44', '49', '51', '54', '55', '66', '68', '70', '74', '76', '77', '79', '85', '91', '101', '102', '105', '107', '109', '114', '119', '120', '121', '122', '125', '127', '128', '130', '133', '134', '135', '138', '139', '140', '142', '144', '145', '146', '147', '149', '150', '151', '152', '153', '154', '155', '157', '159', '160', '161', '163', '165', '166', '167', '170', '171', '172', '174', '176', '178', '180', '182', '191', '193', '194', '195', '197', '198', '199', '200', '201', '203', '204', '205', '206', '207', '209', '211', '212', '219', '221', '223', '224', '226', '228', '231', '236', '238', '241', '242', '243', '244', '246', '250', '251', '253', '255', '256', '257', '259', '260', '261', '263', '264', '265', '266', '268', '270', '271', '272', '274', '275', '276', '279', '280', '281', '282', '283', '284', '285', '286', '291', '292', '294', '301', '306', '307', '312', '313', '315', '316', '318', '320', '322', '325', '326', '329', '330', '331', '332', '335', '339', '340', '342', '344', '348', '350', '351', '352', '353', '354', '355', '360', '361', '362', '363', '366', '369', '370', '371', '372', '373', '376', '377', '379', '381', '386', '387', '388', '389', '390', '392', '393', '394', '395', '397', '398', '400', '401', '402', '403', '404', '406', '409', '410', '418', '419', '420', '422', '423', '424', '425', '427', '428', '429', '432', '433', '439', '441', '442', '445', '448', '451', '452', '454', '456', '457', '459', '460', '462', '463', '465', '467', '469', '470', '471', '473', '475', '476', '478', '480', '481', '482', '483', '485', '486', '489', '490', '492', '493', '495', '496', '501', '503', '504', '506', '507', '509', '510', '511', '513', '514', '515', '517', '518', '519', '520', '521', '522', '523', '524', '525', '526', '527', '528', '529', '530', '531', '532', '533', '535', '536', '537', '538', '539', '540', '543', '544', '545', '546', '547', '549', '551', '552', '553', '554', '555', '557', '558', '559', '561', '564', '566', '567', '568', '569', '571', '573', '575', '576', '580', '581', '582', '583', '584', '586', '588', '589', '590', '591', '594', '595', '598', '599', '601', '606', '608', '609', '616', '622', '625', '626', '629', '638', '644', '646', '647', '649', '652', '656', '657', '658', '660', '661', '662', '663', '664', '668', '671', '674', '675', '677', '684', '686', '689', '706', '727', '729', '734', '736', '737', '743', '752', '774', '790', '805', '821', '837', '839', '852', '876', '877', '880', '887', '889', '892', '896', '897', '898', '899', '902', '903', '904', '906', '908', '911', '912', '913', '916', '917', '924', '925', '926', '928', '929', '930', '932', '933', '935', '936', '938', '942', '945', '947', '948', '949', '951', '953', '954', '956', '958', '960', '962', '963', '965', '966', '968', '969', '970', '972', '977', '983', '984', '987', '988', '989', '992', '993', '994', '1002', '1004', '1006', '1007', '1010', '1011', '1015', '1016', '1018', '1019', '1020', '1021', '1022', '1025', '1026', '1027', '1030', '1042', '1065', '1068', '1075', '1078', '1081', '1090', '2001', '2003', '2004', '2057', '2060', '2068', '2076', '2077', '2078', '3001', '3002', '3004', '3006', '3007', '3011', '3012', '3013', '3020', '3027', '3034', '3035', '3036', '3038', '3039', '3042', '3046', '3047', '3051', '3060', '3079', '3085', '3086', '3090', '3094', '3098', '3099', '4001', '4004', '4007', '4022', '4028', '4034', '4035', '4038', '4042', '4053', '4056', '4058', '4081', '4082', '4083', '4084', '4088', '4093', '4094', '5034', '5064', '5076', '5080', '5090', '6000', '6021', '6023', '6066', '6069', '6075', '6093', '6102', '6103', '6105', '6106', '6111', '6113', '6116', '6117', '6118', '6119', '6121', '6123', '6125', '6126', '6128', '6129', '6130', '6132', '6133', '6136', '6137', '6141', '6142', '6148', '6150', '6151', '6163', '6172', '6176', '6178', '6181', '6184', '6185', '6188', '6189', '6190', '6194', '6196', '6197', '6198', '6200', '6201', '6202', '6204', '6205', '6208', '6210', '6211', '6213', '6218', '6220', '6224', '6228', '6234', '6239', '6240', '6252', '7009', '7011', '7014', '7018', '7023', '7028', '7032', '7036', '7037', '7041', '7042', '7043', '7045', '7047', '7048', '7049', '7051', '7052', '7053', '7054', '7056', '7057', '7059', '7060', '7064', '7068', '7069', '7072', '7073', '7074', '7075', '7076', '7078', '7081', '7082', '7083', '7084', '7085', '7088', '7089', '7092', '7093', '7096', '7097', '7098', '7100', '7105', '7107', '7109', '7110', '7113', '7115', '7117', '7118', '7121', '7122', '7123', '7124', '7127', '7128', '7129', '7131', '7132', '7133', '7134', '7135', '7136', '7137', '7138', '7139', '7140', '7142', '7143', '7144', '7148', '7149', '7150', '7151', '7162', '7164', '7165', '7174', '7180', '7184', '7185', '7187', '7188', '7191', '7192', '7196', '7198', '7199', '7209', '7212', '7217', '7219', '7223']


-------
Unique number of patients Benign by pathology (criteria 2) 
 = 260
       StudyID a_number            CADstatus prior_marker prior_CA
count      296      296                  296          296      296
unique     260      296                    1            2        2
top       3046  7128025  Benign by pathology            f        f
freq         3        1                  296          290      265


-------
Patients  Benign by pathology (criteria 2) with prior prior_CA 
 = 25
       StudyID a_number            CADstatus prior_marker prior_CA
count      265      265                  265          265      265
unique     235      265                    1            2        1
top       3046  7128025  Benign by pathology            f        f
freq         3        1                  265          259      265
['2', '16', '25', '37', '66', '68', '102', '103', '111', '121', '127', '129', '133', '135', '140', '168', '180', '189', '199', '203', '205', '232', '252', '266', '272', '282', '331', '334', '339', '352', '355', '363', '376', '384', '393', '400', '407', '409', '422', '424', '426', '427', '428', '454', '456', '460', '462', '465', '469', '476', '483', '514', '522', '529', '533', '537', '542', '552', '560', '561', '566', '567', '576', '580', '591', '592', '595', '599', '603', '608', '619', '642', '645', '651', '664', '665', '677', '685', '690', '692', '707', '710', '718', '720', '729', '731', '732', '736', '742', '743', '752', '758', '765', '793', '794', '796', '799', '800', '827', '839', '840', '843', '850', '856', '858', '875', '876', '885', '896', '897', '898', '900', '904', '918', '920', '922', '924', '934', '937', '944', '952', '956', '962', '966', '975', '985', '993', '1004', '1006', '1018', '1021', '1022', '1024', '1025', '1026', '1045', '1059', '1062', '1074', '1081', '1087', '2007', '2016', '2075', '3005', '3020', '3031', '3033', '3046', '3054', '3057', '3065', '3066', '3070', '3077', '3081', '3097', '4012', '4019', '4041', '4044', '4045', '4052', '4072', '4082', '4090', '4092', '4095', '4097', '5004', '5007', '5012', '5029', '5037', '5039', '5043', '5044', '5049', '5050', '5051', '5063', '5068', '5077', '5097', '6053', '6069', '6071', '6076', '6079', '6084', '6087', '6090', '6094', '6095', '6096', '6101', '6102', '6103', '6129', '6132', '6139', '6148', '6150', '6165', '6174', '6180', '6183', '6184', '6211', '6214', '6217', '6218', '6219', '6244', '7003', '7024', '7025', '7029', '7030', '7043', '7053', '7066', '7074', '7087', '7097', '7110', '7127', '7160', '7161', '7162', '7173', '7189', '7193', '7201', '7220']


-------
Patients  Benign by pathology (criteria 2) with prior_marker 
 = 6
       StudyID a_number            CADstatus prior_marker prior_CA
count      290      290                  290          290      290
unique     254      290                    1            1        2
top       3046  7128025  Benign by pathology            f        f
freq         3        1                  290          290      259
['2', '16', '25', '37', '66', '68', '102', '103', '111', '121', '127', '129', '133', '135', '140', '168', '180', '189', '199', '203', '205', '207', '232', '248', '252', '266', '272', '282', '299', '331', '334', '339', '352', '355', '357', '363', '376', '384', '393', '396', '400', '407', '409', '422', '424', '426', '427', '428', '436', '440', '442', '454', '456', '460', '462', '465', '469', '476', '483', '514', '522', '529', '533', '537', '542', '552', '560', '561', '566', '567', '576', '580', '591', '592', '595', '599', '603', '608', '619', '642', '645', '651', '663', '664', '665', '677', '685', '690', '692', '707', '710', '718', '720', '729', '731', '732', '736', '740', '742', '743', '752', '765', '793', '794', '799', '800', '827', '839', '840', '843', '850', '856', '858', '875', '876', '896', '897', '898', '900', '904', '918', '920', '922', '924', '934', '937', '944', '952', '956', '966', '975', '985', '993', '1004', '1006', '1018', '1021', '1022', '1024', '1025', '1026', '1045', '1057', '1059', '1062', '1074', '1081', '1087', '1095', '2003', '2007', '2016', '2070', '2075', '2078', '3005', '3020', '3021', '3031', '3033', '3039', '3045', '3046', '3054', '3057', '3065', '3066', '3070', '3077', '3081', '3092', '3097', '4002', '4011', '4012', '4019', '4023', '4041', '4044', '4045', '4052', '4072', '4082', '4090', '4092', '4095', '4097', '5004', '5007', '5012', '5029', '5037', '5039', '5043', '5044', '5049', '5050', '5051', '5063', '5068', '5077', '5097', '6043', '6053', '6069', '6071', '6076', '6079', '6084', '6087', '6090', '6093', '6094', '6095', '6096', '6101', '6102', '6129', '6132', '6139', '6148', '6150', '6165', '6174', '6180', '6183', '6209', '6211', '6214', '6217', '6218', '6219', '6244', '7003', '7024', '7025', '7029', '7030', '7043', '7053', '7066', '7074', '7087', '7097', '7110', '7127', '7160', '7161', '7162', '7173', '7189', '7193', '7201', '7220']
-------

-------
Unique number of patients  Malignant (criteria 1) 
 = 157
       StudyID   a_number  CADstatus prior_marker prior_CA
count      167        167        167          167      167
unique     157        167          1            2        2
top        667  ACC108250  Malignant            f        f
freq         2          1        167          161      143


-------
Patients Malignant (criteria 1) with prior prior_CA 
 = 20
       StudyID a_number  CADstatus prior_marker prior_CA
count      143      143        143          143      143
unique     137      143          1            2        1
top        667  5264139  Malignant            f        f
freq         2        1        143          137      143
['27', '59', '114', '171', '178', '186', '190', '225', '229', '271', '276', '280', '283', '320', '323', '346', '366', '388', '396', '415', '455', '562', '571', '584', '586', '604', '613', '619', '635', '657', '667', '668', '683', '684', '687', '691', '700', '705', '713', '714', '719', '722', '724', '730', '735', '743', '744', '745', '747', '755', '760', '764', '776', '779', '781', '782', '791', '802', '803', '807', '813', '814', '815', '829', '830', '834', '837', '845', '846', '851', '853', '861', '862', '865', '867', '871', '883', '888', '943', '950', '967', '1008', '1044', '1054', '1071', '1079', '1099', '2025', '2049', '2073', '3000', '3005', '3055', '3078', '4023', '4064', '5001', '5002', '5046', '6018', '6024', '6033', '6035', '6039', '6040', '6042', '6044', '6046', '6068', '6072', '6073', '6100', '6105', '6110', '6116', '6140', '6145', '6148', '6202', '6207', '6215', '6236', '6248', '6256', '6342', '7002', '7018', '7033', '7063', '7068', '7076', '7086', '7104', '7159', '7169', '7172', '7184']

-------
Patients Malignant (criteria 1) with prior_marker 
 = 6
       StudyID   a_number  CADstatus prior_marker prior_CA
count      161        161        161          161      161
unique     151        161          1            1        2
top        667  ACC108250  Malignant            f        f
freq         2          1        161          161      137
['18', '27', '59', '114', '171', '178', '190', '225', '229', '271', '276', '280', '283', '299', '308', '320', '323', '346', '347', '358', '366', '383', '388', '396', '415', '438', '455', '562', '571', '584', '586', '604', '613', '619', '635', '657', '667', '668', '683', '687', '691', '700', '705', '713', '714', '719', '722', '724', '726', '730', '735', '743', '744', '745', '747', '755', '760', '764', '776', '779', '781', '782', '802', '803', '807', '812', '813', '814', '815', '829', '830', '834', '837', '844', '845', '846', '851', '853', '861', '865', '867', '883', '888', '943', '950', '967', '1008', '1044', '1054', '1071', '1079', '2025', '2049', '2068', '2071', '2073', '3000', '3005', '3033', '3055', '3078', '4023', '4025', '4064', '4069', '5001', '5002', '5046', '6005', '6018', '6024', '6026', '6030', '6033', '6035', '6037', '6039', '6040', '6042', '6044', '6046', '6068', '6072', '6073', '6100', '6105', '6110', '6116', '6140', '6145', '6148', '6202', '6207', '6215', '6236', '6248', '6256', '6342', '7002', '7018', '7033', '7063', '7068', '7076', '7077', '7086', '7104', '7159', '7169', '7172', '7184']



========================================================
NEWED ADDED CASES CATEGORY:
* add mri cad status
* cases with prior cancer history
* cases normal - BIRADS 3, had not other BIRADS>3 withing 2 years or other than benign procedure (based on biomatrix mri_cad_status field) to exclude all BIRADS 3 benig


========================================================
* cases excluded due to difficult segmentation: 3 patients
 59  -  Lesion_id = 3,   series  S33:      Patched Sag 3D spgr  (280 images)
 556 -  Lesion_id = 29,   series  S4:       Sag 2D SPGR F.S. Dynamic  (210 images)
 299 -  Lesion_id = 19,  series  S33:    Patched Sag 3D spgr  (280 images)
     -  Lesion_id = 20,  series  S33:    Patched Sag 3D spgr  (280 images)


* Other exluded 
68	8628	942112	     1664	20030618	005	['-50.500000','-151.899994','115.000000']	['0.000000','1.000000','0.000000','0.000000','0.000000','-1.000000']
201	13027	1223382	1535	20050818	S4	['100.585','-130.243','101.951']	['-0','1','0','-0','-0','-1']
225	5632	1215316	1563	20020220	S5	['82.099998','-148.699997','94.000000']	['0.000000','1.000000','0.000000','0.000000','0.000000','-1.000000']
234	6677	1240055	1566	20020827	S80	['-60.000000','-148.100006','108.000000']	['0.000000','1.000000','0.000000','0.000000','0.000000','-1.000000']
248	8563	1207930	25	20030605	S5	['-86.599998','-156.300003','101.000000']	['0.000000','1.000000','0.000000','0.000000','0.000000','-1.000000']
662 		# excluded because of cysts images 13 and 75
6011	4527	2550230	1118	20090206	S700	# LABC post chemotherapy
6013	5156	893821	1124	20090320	S600	# Right upper outer quadrant lumpectomy for DCIS
6019	8175	2618319	1133	20091010	# not clear
6033	6399	2596363	1152	2009-06-13	# DOES NOT EXIST


* Due to only 3 post contrast time points
838	2009	2523981	1376	# 3 time points
843	17736	2037776	1382	# same patient, only Ph2/3/4 available
6003	179	2503080	1198	# 3 dynamic runs post gadolinium contrast

========================================================
REMOVED
========================================================
* cases with older protocols:
    MASSES:  13 patients (19 lesions)
    18  -  Lesion_id = 1,  series  S44:    Patched Sag 3D spgr  (280 images)
        -  Lesion_id = 2,  series  S44:    Patched Sag 3D spgr  (280 images)
    261 -  Lesion_id = 8,   series  S3:     Sag 3D dynamic - NON-FAT SAT  (280 images)
    271 -  Lesion_id = 9,   series  S3:     Sag 3d bilateral dynamic - NON-FAT SAT  (280 images)
    272 -  Lesion_id = 10,  series  S4:     Sag 2D SPGR dynamic  (196 images)
    282 -  Lesion_id = 15,  series  S5:     Sag 2D SPGR  (132 images)
    299 -  Lesion_id = 19,  series  S33:    Patched Sag 3D spgr  (280 images)          
        -  Lesion_id = 20,  series  S33:    Patched Sag 3D spgr  (280 images)
    455 -  Lesion_id = 23,  series  S4:     Optional Sag 3D  (280 images)  
    556 -  Lesion_id = 25,  series  S3:     Sag 3d bilateral dynamic - FAT SAT  (280 images)
        -  Lesion_id = 26,  series  S3:     Sag 3d bilateral dynamic - FAT SAT  (280 images)
        -  Lesion_id = 27,  series  S3:     Sag 3d bilateral dynamic - FAT SAT  (280 images)
    837 -  Lesion_id = 127,  series  S44:  Patched Sag 3D spgr  (280 images)
    837 -  Lesion_id = 128,  series  S4:   Sag Vibrant Dry  (96 images)
        -  Lesion_id = 129,  series  S4:   Sag Vibrant Dry  (96 images)
    881 -  Lesion_id = 251,  series  S8:   SAG Vibrant SPECIAL  (100 images)
    559 -  Lesion_id = 294,  series  S8:   Sag Vibrant Dry 
    547 -  Lesion_id = 361,  series  S7:   Sag Vibrant Dry
        -  Lesion_id = 362,  series  S7:   Sag Vibrant Dry               


    - Lesions exluded due to old acquisition protocol:
    NONMASSES:  6 patients (8 lesions)
    59  -  Lesion_id = 3,   series  S33:      Patched Sag 3D spgr  (280 images)
    340 -  Lesion_id = 22,   series  S4:      Sag 3D spgr  (140 images)
    455 -  Lesion_id = 24,   series  S4:      Optional Sag 3D  (280 images)
    556 -  Lesion_id = 28,   series  S3:      Sag 3d bilateral dynamic  (280 images)
        -  Lesion_id = 29,   series  S4:      Sag 3d bilateral dynamic  (280 images)
    837 -  Lesion_id = 130,   series  S4:     Sag Vibrant Dry  (96 images)
        -  Lesion_id = 131,   series  S4:     Sag Vibrant Dry  (96 images)
    6052 -  Lesion_id = 264,   series  S4:     Sag 3D dynamic  (280 images)

* cases with BIRADS=0:
    203     -  Lesion_id = 535	4384800	01/12/2007	Left	nonmassB	FIBROCYSTIC but MRI is BIRADS 0 and imaging 4535858	27/12/2007 is Old 3D SPGR
    6114    -  Lesion_id = 509	6737175	09/02/2012	Left	nonmassB	Fibroadenoma    MRI in 2012 is BIRADS 0, more imaging ordered
    775     -  Lesion_id = 370	6916901	18/10/2011	NA	nonmassB	BenignbyFollowUp  BIRADS 0
            -  Lesion_id = 371	6916901	18/10/2011	NA	nonmassB	BenignbyFollowUp  BIRADS 0


========================================================
REPLACED WITH
========================================================
MASSES:   (19 lesions)
    -  Lesion_id = 1,  66	     4583735	    17/02/2008	BENIGN BREAST TISSUE     mass	[u'Right', Decimal('8'), Decimal('3'), None, u'Rapid', u'Plateau', u'II', u'N/A', u'Oval', u'Hypointense or not seen', 3]
    -  Lesion_id = 2,  121	     6714524	    22/02/2011	ADENOSIS     mass	[u'Right', Decimal('20'), Decimal('12'), None, u'N/A', u'N/A', None, u'N/A', u'Lobular', None, 4]
    -  Lesion_id = 8,  133	     7072006	    10/03/2012	Fibrocystic  mass     [u'Left', None, None, None, u'Rapid', u'Plateau', None, u'N/A', u'N/A', None, 4]
    -  Lesion_id = 9,  171	     4751079	    22/02/2009	InsituDuctal     mass	[u'Left', Decimal('5'), None, None, u'N/A', u'N/A', u'Other', u'N/A', u'N/A', None, 4]
    -  Lesion_id = 10, 205	     5085133	    17/04/2010	fibroepithelial      mass	[u'Left', Decimal('9'), Decimal('6'), None, u'Slow', u'Plateau', u'II', u'Smooth', u'Oval', u'Hyperintense', 4]
    -  Lesion_id = 15, 207	     4982884	    09/11/2009	mass	[u'Right', Decimal('9.2'), Decimal('6'), Decimal('5.3'), u'N/A', u'N/A', None, u'N/A', u'N/A', None, 4]
    -  Lesion_id = 19, 212	     4734525	    08/09/2008	Fibroadenoma     mass	[u'Left', Decimal('9'), Decimal('8'), Decimal('7'), u'N/A', u'Persistent', u'Ia', u'N/A', u'N/A', u'Hyperintense', 4]        
    -  Lesion_id = 20, 252	     5142106	    04/12/2009	FIBROADENOMA     mass	[u'Right', Decimal('7'), None, None, u'Rapid', u'Washout', None, u'N/A', u'N/A', u'Hypointense or not seen', 4]
    -  Lesion_id = 23, 376	     4609403	    04/04/2008	BENIGN HAMARTOMA     mass	[u'Left', Decimal('12'), None, None, u'Moderate to marked', u'Persistent', u'Ia', u'Smooth', u'Lobular', u'Slightly hyperintense', 4]
    -  Lesion_id = 25, 173	     5123923	    30/11/2009	DUCT PAPILLOMA       nonmass	[u'Right', Decimal('86'), Decimal('16'), None, u'N/A', u'N/A', None, u'N/A', u'N/A', None, 4]
    -  Lesion_id = 26, 189      5057674	    10/10/2009   nonmass	[u'Left', Decimal('11'), None, None, u'Rapid', u'Plateau', u'II', u'Linear', u'N/A', None, 4]
    -  Lesion_id = 27, 325	     4696948	    01/12/2008	FIBROCYSTIC  mass	[u'Right', None, None, None, u'N/A', u'N/A', None, u'N/A', u'N/A', None, 4]
    -  Lesion_id = 127, 352	4785776	19/01/2009	FIBROADENOMA     mass	[u'Right', Decimal('9'), Decimal('9'), Decimal('9'), u'N/A', u'Plateau', None, u'N/A', u'N/A', u'Slightly hyperintense', 4]
    -  Lesion_id = 128, 357	5137030	15/12/2009	FIBROCYSTIC      foci	[u'Left', None, None, None, u'N/A', u'N/A', None, u'N/A', u'N/A', None, 4]
    -  Lesion_id = 129, 473	7364625	19/12/2013	mass	[u'Left', Decimal('6'), Decimal('3'), Decimal('6'), u'N/A', u'Washout', None, u'N/A', u'N/A', None, 4]
    -  Lesion_id = 251, 388	7395410	26/02/2013	InvasiveDuctal       mass	[u'Right', Decimal('20'), Decimal('22'), Decimal('23'), u'N/A', u'N/A', None, u'N/A', u'Irregular', None, 5]
    -  Lesion_id = 294, 252	5142106	04/12/2009	FIBROADENOMA     mass	[u'Left', Decimal('7.4000'), None, None, u'Rapid', u'Washout', u'III', u'N/A', u'N/A', u'Hypointense or not seen', 4]
    -  Lesion_id = 361, 424	4644689	27/04/2008	mass	[u'Right', None, Decimal('11'), Decimal('12'), u'Rapid', u'Washout', None, u'Spiculated', u'N/A', None, 6]
    -  Lesion_id = 362, 442	4936886	13/03/2010	mass	[u'Right', Decimal('7'), Decimal('4'), Decimal('5'), u'N/A', u'N/A', None, u'N/A', u'Lobular', u'Slightly hyperintense', 4]



NONMASSES:  (8 lesions)
    -  Lesion_id = 3,   27	   7171944	15/08/2012	nonmass	STROMAL FIBROSIS      [u'Right', None, None, None, u'N/A', u'N/A', None, u'Linear', u'N/A', None, 4]
    -  Lesion_id = 22,  127	4696964	11/09/2008	FIBROADENOMA     nonmass	[u'Left', Decimal('13'), Decimal('8'), None, u'N/A', u'Persistent', u'Ia', u'Regional', u'N/A', u'Hyperintense', 4]
    -  Lesion_id = 24,  180	4632561	25/10/2008	BENIGN BREAST TISSUE.        nonmass	[u'Left', Decimal('0'), Decimal('0'), Decimal('0'), u'N/A', u'N/A', u'Ia', u'Focal', u'Clumped', None, 4]
    -  Lesion_id = 28,  409	6696680	24/04/2011	BENIGN        mass	[u'Left', None, None, None, u'N/A', u'N/A', None, u'N/A', u'N/A', u'Slightly hyperintense', 4]
    -  Lesion_id = 29, 266	5254958	16/07/2010	FIBROCYSTIC      nonmass	[u'Right', Decimal('18'), Decimal('6'), Decimal('4'), u'N/A', u'Persistent', None, u'Linear', u'N/A', u'Hypointense or not seen', 4]
    -  Lesion_id = 130, 212	4734525	08/09/2008	nonmass	[u'Right', Decimal('25'), None, None, u'Rapid', u'Persistent', u'Ia', u'Linear', u'N/A', u'Hypointense or not seen', 4]
    -  Lesion_id = 131, 199	4362726	18/05/2007	ATYPICAL LOBULAR HYPERPLASIA     mass	[u'Left', Decimal('11.2000'), Decimal('10'), None, u'N/A', u'Persistent', u'Ia', u'Irregular', u'N/A', u'Hyperintense', 4]
    -  Lesion_id = 264, 277	5077098	22/09/2009	InsituDuctal     nonmass	[u'Left', Decimal('14'), Decimal('10'), Decimal('5'), u'N/A', u'N/A', u'Other', u'N/A', u'N/A', u'Hypointense or not seen', 5]

* cases with BIRADS=0:
    -  Lesion_id = 535	498	5043973	11/09/2009	foci	[u'Left', None, None, None, u'N/A', u'N/A', None, u'N/A', u'N/A', None, 4]
    -  Lesion_id = 509	944	7742881	23/05/2014	ADH and DCIS  
    -  Lesion_id = 370	519	4937737	14/05/2009	mass	FLAT EPITHELIAL ATYPIA     [u'Left', Decimal('5'), None, None, u'Moderate to marked', u'Plateau', None, u'Irregular', u'Irregular', None, 4]   
    -  Lesion_id = 371	536	7786869	06/05/2014	mass	FIBROADENOMA     [u'Right', None, None, None, u'N/A', u'Persistent', u'Ia', u'N/A', u'Oval', u'Hypointense or not seen', 4]

