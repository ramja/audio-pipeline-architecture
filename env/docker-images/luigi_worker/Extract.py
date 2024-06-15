#!/usr/bin/python

import sys
from graph_tool import load_graph


import numpy



for gFile in sys.argv[1:]:
    
    


    g=load_graph(gFile)
    v_pitchr=g.vertex_properties["pitchr"]
    v_name=g.vertex_properties["name"]
    v_group=g.vertex_properties["group"]
    v_intensity=g.vertex_properties["intensity"]
    v_weight=g.vertex_properties["weight"]
    e_weight=g.edge_properties["weight"]



    m=numpy.matrix(numpy.zeros((10000,5)))
    i=0
    mem=10000
    for v in g.vertices(): 
        m[i,0]=v_weight[v]     
        m[i,1]=v_pitchr[v]
        m[i,2]=v_intensity[v]
        m[i,3]=v_group[i]
        i=i+1
        if (v_group[v] == 0 and i!=0):
            mem=i-1
    i=0    
    for e in g.edges():
        m[i,4]=e_weight[e]
        i=i+1
        
    numpy.savetxt(gFile[:-8]+".dat",  m[0:mem,], fmt='%10.5f', delimiter=',')   # X is an array
