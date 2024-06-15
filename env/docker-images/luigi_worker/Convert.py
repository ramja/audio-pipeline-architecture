#!/usr/bin/python

import sys
from graph_tool import load_graph

i=1
for gFile in sys.argv[1:]:
    
    
    with open("Output.log", "a") as text_file:

        g=load_graph(gFile)
        v_pitchr=g.vertex_properties["pitchr"]
        v_name=g.vertex_properties["name"]
        v_group=g.vertex_properties["group"]
        v_intensity=g.vertex_properties["intensity"]
        v_weight=g.vertex_properties["weight"]
        e_weight=g.edge_properties["weight"]


        text_file.write("%s\n" % gFile[:-8])
        print("%% %s" % gFile[:-8])
        d=dict()

        
        for v in g.vertices(): 
            if (i<30):
                d[v_name[v].replace(" ", "")]=i 
                if (v_group[v] ==1): 
                    if (v_weight[v]*v_pitchr[v]/10000<4):
                        vSize="s"
                    elif (v_weight[v]*v_pitchr[v]/10000<16):
                        vSize="m"
                    else:
                        vSize="b"  
                else:  
                    if (v_weight[v]*v_pitchr[v]/10000<100):
                        vSize="z"
                    elif (v_weight[v]*v_pitchr[v]/10000<1000):
                        vSize="n"
                    else:
                        vSize="g"  
                text_file.write('%d %s\n' % (i,vSize))
                print("v %d %s" % (i,vSize))
                i=i+1
            
        for e in g.edges():
            if (v_name[e.target()].replace(" ", "") in d):
                if (e_weight[e]<2):
                    eSize="s"
                elif (e_weight[e]<4):
                    eSize="m"
                else:
                    eSize="b"
                text_file.write(""" d %d %d %s \n""" % (d[v_name[e.source()].replace(" ", "")],d[v_name[e.target()].replace(" ", "")],eSize))
                print(""" d %d %d %s """ % (d[v_name[e.source()].replace(" ", "")],d[v_name[e.target()].replace(" ", "")],eSize))
            
text_file.close()
