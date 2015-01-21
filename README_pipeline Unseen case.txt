
1) C:\Users\windows\Documents\repoCode-local\addnewLesion
- create a list of cases columns: id	StudyID 	MRN     Accession 	Examdate	ProcedureResults
- run processNewRecords.py to 
Get new cases, query BIOMATRIX, get images from PACS and create record in local database, segment and extract features
NOTE: remove stage1features from path, since declarative BASE in this pipeline is not biomatrix but Stage1Local.db
make sure local_database folder is on the path where mybase and mydatabase are defined

2) script will get scans from PACS by accession
- ask to select pre-contrast T1w and T2 series
- Loads volumes and asks for seeds of lesion location
- Based on seeds segments lesion
- uses segmentation to extract kinetic, morpho and texture properties on DCEMRI
- extracts texture and morphology from T2w scans

3) send lesion, mass/nonmass BIRADS info, features, annotations (if any) to databse