# -*- coding: utf-8 -*-
"""
Process functions to extract new features

Created on Fri Oct 31 15:35:20 2014

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

import processDicoms
from inputs_init import *
from display import *
import pylab      
import annot
from add_records import *

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
        
from sklearn.cluster import KMeans
from sklearn import datasets
import scipy.spatial.distance as dist
import networkx as nx
import itertools
from collections import Counter
import datetime


class newFeatures(object):
    """
    USAGE:
    =============
    newfeatures = newFeatures(load, display)
    """
    def __init__(self, load, display): 
        self.dataInfo = []
        self.records = AddRecords()
        # Create only 1 display
        self.loadDisplay = display
        self.load = load
        self.deltaS = {} 
        self.G=[]
    
        
    def extract_timepoints(self, series_path, phases_series):
        timepoints=[]
        print "\n Retrieving time points..."
        for i in range(len(self.load.DICOMImages)):
            abspath_PhaseID = series_path+os.sep+str(phases_series[i]) 
            print phases_series[i]
            # Get total number of files
            [len_listSeries_files, FileNms_slices_sorted_stack] = self.load.ReadDicomfiles(abspath_PhaseID)
            mostleft_slice = FileNms_slices_sorted_stack.slices[0]
            # Get dicom header, retrieve
            dicomInfo_series = dicom.read_file(abspath_PhaseID+os.sep+str(mostleft_slice)) 
            # (0008,0032) AT S Acquisition Time       # hh.mm.ss.frac
            ti = str(dicomInfo_series[0x0008,0x0032].value) 
            acquisitionTimepoint = datetime.time(hour=int(ti[0:2]), minute=int(ti[2:4]), second=int(ti[4:6]))
            timepoints.append( datetime.datetime.combine(datetime.date.today(), acquisitionTimepoint) )
        
        # Collecting timepoints in proper format
        self.t_delta = []
        self.t_delta.append(0)
        self.total_time = 0
        for i in range(len(self.load.DICOMImages)-1):
            current_time = timepoints[i+1]
            previous_time = timepoints[i]
            difference_time=current_time - previous_time
            timestop = divmod(difference_time.total_seconds(), 60)
            self.t_delta.append( self.t_delta[i] + timestop[0]+timestop[1]*(1./60))
            self.total_time = self.total_time+timestop[0]+timestop[1]*(1./60)
            
        # finally print t_delta
        print self.t_delta
        print "total_time"
        print self.total_time
        
        return 
            
    def extract_MRIsamp(self, series_path, phases_series, VOI_mesh, T2SeriesID): 
        """ Start pixVals for collection pixel values at VOI """
        pixVals = []
        iVals = []; jVals = []; kVals = [];
        # necessary to read point coords
        VOIPnt = [0,0,0]
        ijk = [0,0,0]
        pco = [0,0,0]
        
        #############################
        # Extract T1 DCE data
        #############################
        for i in range(len(self.load.DICOMImages)):           
            # find mapping to Dicom space  
            [transformed_T1, t_cube] = self.loadDisplay.dicomTransform(self.load.DICOMImages[i], self.load.image_pos_pat, self.load.image_ori_pat)
            # get lesion center in ijk
            center = VOI_mesh.GetCenter() 
            # extract pixID at location VOIPnt
            pixId = transformed_T1.FindPoint(center[0], center[1], center[2])
            im_pt = [0,0,0]
            transformed_T1.GetPoint(pixId,im_pt)     
            centerijk = [0,0,0]
            transformed_T1.ComputeStructuredCoordinates( im_pt, centerijk, pco)
            
            for j in range( VOI_mesh.GetNumberOfPoints() ):
                VOI_mesh.GetPoint(j, VOIPnt)      
                # extract pixID at location VOIPnt
                pixId = transformed_T1.FindPoint(VOIPnt[0], VOIPnt[1], VOIPnt[2])
                im_pt = [0,0,0]
                transformed_T1.GetPoint(pixId,im_pt)     
                ijk = [0,0,0]
                inorout = transformed_T1.ComputeStructuredCoordinates( im_pt, ijk, pco)
                if(inorout == 0):
                    pass
                else:
                    pixValx = transformed_T1.GetScalarComponentAsFloat( ijk[0], ijk[1], ijk[2], 0)
                    pixVals.append(pixValx)    
                    iVals.append(ijk[0])
                    jVals.append(ijk[1])
                    kVals.append(ijk[2])
                        
            # Now collect pixVals
            print "\nSaving %s" % 'DCE'+str(i)
            self.deltaS['DCE'+str(i)] = pixVals
            self.deltaS['i'+str(i)] = iVals            
            self.deltaS['j'+str(i)] = jVals            
            self.deltaS['k'+str(i)] = kVals            
            pixVals = []
            iVals = []; jVals = []; kVals = [];
            
        #############################             
        # Extract T2
        #############################
        # find mapping to Dicom space  
        if (T2SeriesID != 'NONE'): 
            [transformed_T2, t_cube] = self.loadDisplay.dicomTransform(self.load.T2Images, self.load.T2image_pos_pat, self.load.T2image_ori_pat)
        
            for j in range( VOI_mesh.GetNumberOfPoints() ):
                VOI_mesh.GetPoint(j, VOIPnt)      
                # extract pixID at location VOIPnt
                pixId = transformed_T2.FindPoint(VOIPnt[0], VOIPnt[1], VOIPnt[2])
                im_pt = [0,0,0]
                transformed_T2.GetPoint(pixId,im_pt)   
                ijk = [0,0,0]
                inorout = transformed_T2.ComputeStructuredCoordinates( im_pt, ijk, pco)
                if(inorout == 0):
                    pass
                else:
                    pixValx = transformed_T2.GetScalarComponentAsDouble( ijk[0], ijk[1], ijk[2], 0)
                    pixVals.append(pixValx)
                    iVals.append(ijk[0])
                    jVals.append(ijk[1])
                    kVals.append(ijk[2])
                        
            # Now collect pixVals
            print "\nSaving %s" % 'T2'
            self.deltaS['T2'] = pixVals
            self.deltaS['T2i'] = iVals            
            self.deltaS['T2j'] = jVals            
            self.deltaS['T2k'] = kVals            
            pixVals = []
            iVals = []; jVals = []; kVals = [];            
        else:
            self.deltaS['T2'] = []
            self.deltaS['T2i'] = []            
            self.deltaS['T2j'] = []            
            self.deltaS['T2k'] = [] 
            
        #############################
        ###### Extract time
        #############################
        self.extract_timepoints(series_path, phases_series)
        print self.t_delta
        
        return self.deltaS, self.t_delta, centerijk

        
    def generateNodesfromKmeans(self, x, y, z, pixVals, centerijk, T2SeriesID):
        global contourWidget
        
        X = zeros((len(x),3))
        X[:, 0] = x
        X[:, 1] = y
        X[:, 2] = z
        kmeans_estimators = {'k_means_20': KMeans(n_clusters=20, n_init=5, init='random')}
        for name, kmeans in kmeans_estimators.iteritems():
                   
            # PErform k-means clustering on x,y,z positions
            kmeans.fit(X)
            labels = kmeans.labels_
            print labels
    
            fig = plt.figure(1, figsize=(4, 3))
            ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)       
            ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels.astype(float))
        
            ax.w_xaxis.set_ticklabels([])
            ax.w_yaxis.set_ticklabels([])
            ax.w_zaxis.set_ticklabels([])
            
            kmeansnodes = kmeans.cluster_centers_
            nnodes = kmeans.n_clusters
            ax.set_xlim3d(min(kmeansnodes[:,0]), max(kmeansnodes[:,0]))
            ax.set_ylim3d(min(kmeansnodes[:,1]), max(kmeansnodes[:,1]))
            ax.set_zlim3d(min(kmeansnodes[:,2]), max(kmeansnodes[:,2]))
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            
        
        print 'K-means n_clusters: %d' % nnodes
        print 'K-means cluster centers: ' % kmeansnodes       
                 
        ############ process T1 PixVals from pixCluster
        pre_pixVals = pixVals['DCE0']
        early_pixVals = pixVals['DCE1']
        late_pixVals = pixVals['DCE4']
        
        # Get enhancement values from nodes clusters
        indNode = kmeans.predict(X) 
        preSI = zeros(nnodes)
        earlySI = zeros(nnodes)
        lateSI = zeros(nnodes)
        DCE2 = zeros(nnodes)
        DCE3 = zeros(nnodes)
        indNodecount = zeros(nnodes)
        pixSERClus=[]
        
        for k in range(len(indNode)):
            # acummulate pixvals assigned to nodes
            preSI[indNode[k]] += pre_pixVals[k]
            earlySI[indNode[k]] += early_pixVals[k]
            lateSI[indNode[k]] += late_pixVals[k]
            # process other points
            DCE2[indNode[k]] += pixVals['DCE2'][k]
            DCE3[indNode[k]] += pixVals['DCE3'][k]
            # increment points in node count            
            indNodecount[indNode[k]] += 1
            
        ############ process T2 PixVals from pixCluster
        if (T2SeriesID != 'NONE'): 
            x=pixVals['T2i']; y=pixVals['T2j']; z=pixVals['T2k'];
            T2pixVals = pixVals['T2']
            X = zeros((len(x),3))
            X[:, 0] = x
            X[:, 1] = y
            X[:, 2] = z
            
            kmeans_estimators = {'k_means_20': KMeans(n_clusters=20, n_init=5, init='random')}
            for name, kmeans in kmeans_estimators.iteritems():
                       
                # PErform k-means clustering on x,y,z positions
                kmeans.fit(X)
                labels = kmeans.labels_
                print labels
        
                fig = plt.figure(4, figsize=(4, 3))
                ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)       
                ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels.astype(float))
            
                ax.w_xaxis.set_ticklabels([])
                ax.w_yaxis.set_ticklabels([])
                ax.w_zaxis.set_ticklabels([])
                
                kmeansnodesT2 = kmeans.cluster_centers_
                nnodesT2 = kmeans.n_clusters
                ax.set_xlim3d(min(kmeansnodesT2[:,0]), max(kmeansnodesT2[:,0]))
                ax.set_ylim3d(min(kmeansnodesT2[:,1]), max(kmeansnodesT2[:,1]))
                ax.set_zlim3d(min(kmeansnodesT2[:,2]), max(kmeansnodesT2[:,2]))
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                
            print 'K-means n_clustersT2: %d' % nnodesT2
            print 'K-means cluster centersT2: ' % kmeansnodesT2    
            
            indNodeT2 = kmeans.predict(X) 
            indNodecountT2 = zeros(nnodesT2)
            print indNodeT2
            if(~any(indNodeT2)):
                print "NULLS"
                
            T2SI = zeros(nnodesT2)
            for k in range(len(indNodeT2)):
                # acummulate pixvals assigned to nodes
                T2SI[indNodeT2[k]] += T2pixVals[k]
                # increment points in node count            
                indNodecountT2[indNodeT2[k]] += 1
                
            ave_T2 = T2SI/indNodecountT2
            print "ave_T2:"
            print ave_T2 
        else:
            ave_T2=zeros(20)*nan
    
        ################################################
        # process node pixvalues    
        ave_pre_pixVals = preSI/indNodecount
        print "ave_pre_pixVals:"
        print ave_pre_pixVals
        ave_early_pixVals = earlySI/indNodecount
        ave_DCE2_pixVals = DCE2/indNodecount
        ave_DCE3_pixVals = DCE3/indNodecount
        print "ave_early_pixVals:" 
        print ave_early_pixVals
        ave_late_pixVals = lateSI/indNodecount
        print "ave_late_pixVals" 
        print ave_late_pixVals
        
        # gather SE ratios
        earlySE = (ave_early_pixVals-ave_pre_pixVals)/ave_pre_pixVals
        dce2SE = (ave_DCE2_pixVals-ave_pre_pixVals)/ave_pre_pixVals
        dce3SE = (ave_DCE3_pixVals-ave_pre_pixVals)/ave_pre_pixVals
        lateSE = (ave_late_pixVals-ave_pre_pixVals)/ave_pre_pixVals
        
        # produce curve type plots
        curveV = {}
        curveT = [str(b) for b in range(0,nnodes)] 
        fig, axes = plt.subplots(nrows=4, ncols=5, figsize=(12,10))
        bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
        left = .75
        bottom = .25
        k=0
        for i in range(4):
            for j in range(5):
                # classify curves as I,II,III
                if( lateSE[k] > 1.1*dce3SE[k] ): 
                    curveT[k] = "I"
                if( lateSE[k] < 1.1*dce3SE[k] and lateSE[k] < 1.1*dce2SE[k]):                     
                    curveT[k] = "II"
                    if ( lateSE[k] < 1.1*dce2SE[k] ): 
                        curveT[k] = "III"
                else:
                    curveT[k] = "I"
                # not plot
                curveV['n'+str(k)]=[0, earlySE[k], dce2SE[k], dce3SE[k], lateSE[k]]
                axes[i,j].plot(self.t_delta, curveV['n'+str(k)], color='blue', linestyle='solid', marker='o')
                axes[i,j].text(left, bottom, curveT[k], bbox=bbox_props)
                k+=1
        plt.plot()                
       
        ############ Collect clusters centers
        # Get final position for nodes
        print "\nGenerate measurement of dispersion from lesion center"
        d_euclideanNodes = zeros(nnodes)
        
        for k in range(nnodes):
            d_euclideanNodes[k] = dist.euclidean(kmeansnodes[k], centerijk)
            print "Node %i d_euclidean: %f" % (k, d_euclideanNodes[k])  
        
        return nnodes, curveT, earlySE, dce2SE, dce3SE, lateSE, ave_T2, [kmeansnodes, d_euclideanNodes]   
                
    
    def analyzeGraph(self, G):
        """ The structure of G can be analyzed using various graph-theoretic functions such as:"""
        #################
        ## Centrality
        #################
        # The degree centrality values are normalized by dividing by the maximum possible 
        # degree in a simple graph n-1 where n is the number of nodes in G.
        degreeC = nx.degree_centrality(G)
        print "\ndegreeC"
        print degreeC
        
        # Closeness centrality of a node \(u\) is the reciprocal of the sum of the shortest path distances from
        # \(u\) to all \(n-1\) other nodes. Since the sum of distances depends on the number of nodes in the graph, 
        # closeness is normalized by the sum of minimum possible distances \(n-1\).
        closenessC = nx.closeness_centrality(G, u=None, distance="d_euclid", normalized=True)
        print "\nclosenessC"
        print closenessC
        
        # Betweenness centrality of an edge \(e\) 
        # is the sum of the fraction of all-pairs shortest paths that pass through \(e\):
        betweennessC = nx.edge_betweenness_centrality(G, normalized=True)
        print "\nbetweennessC"
        print betweennessC
        
        #################
        ## Clustering and Components
        #################
        # Finds the number of triangles that include a node as one vertex.
        print "\nno_triangles"
        no_triangles = nx.triangles(G, nodes=None)
        print no_triangles
        
        print "\nno_con_comp"
        no_con_comp = nx.number_connected_components(G)
        print no_con_comp
        
        # find the mode
        modegreeC = Counter(degreeC).most_common(1)
        moclosenessC = Counter(closenessC).most_common(1)
        mobetweennessC = Counter(betweennessC).most_common(1)
        mono_triangles = Counter(no_triangles).most_common(1)
        
        print modegreeC
        print moclosenessC
        print mobetweennessC
        print mono_triangles
        
        return modegreeC, moclosenessC, mobetweennessC, mono_triangles, no_con_comp
    
    def createGraph(self, nnodes, nodelinks, prop):
        """ Create undirected graph from node list, and pass linkages as array of repeated node classes"""
        self.G = nx.Graph()
        self.G.add_nodes_from(range(0,nnodes))
        
        nodesCT1=[]; nodesCT2=[]; nodesCT3=[]; 
        for n,ct in enumerate(nodelinks):
            if ct == "I":
                print "CurveT I nodes:"
                print n,ct
                nodesCT1.append(n)
            if ct == "II":
                print "CurveT II nodes:"
                print n,ct
                nodesCT2.append(n)
            if ct == "III":
                print "CurveT III nodes:"
                print n,ct
                nodesCT3.append(n)
                
        if(len(nodesCT1) > 1):
          edges = list(itertools.permutations(nodesCT1,2))  
          self.G.add_edges_from(edges)
          
        if(len(nodesCT2) > 1):
          edges = list(itertools.permutations(nodesCT2,2))  
          self.G.add_edges_from(edges)
          
        if(len(nodesCT3) > 1):
          edges = list(itertools.permutations(nodesCT3,2))  
          self.G.add_edges_from(edges)
        
        # add node attributes based on list of attributes prop
        d_euclid = prop[1]
        nx.set_node_attributes(self.G, 'd_euclid', d_euclid)
        
        # draw
        fig = plt.figure(3, figsize=(4, 3))
        plt.clf()
        nx.draw(self.G)
        plt.show()
        
        return self.G
    
