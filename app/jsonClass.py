"""
This script is responsible for json manipulation which is further passed into D3.js 
"""
import json
import os
import string
import random
import sys
from graphMani import myGraph
import configParam

class genJSON():
    def __init__(self, filename):
        if ".dot" not in filename:
            filename = filename + ".dot"
        self.filename = filename
        self.config = configParam.configParam()
        self.directory = self.config.working_directory
        os.chdir(self.directory)
        ## check if filename.dot present in given directory
        if self.filename in os.listdir(self.directory):
            print("Success")
            self.importDOT()
        else:
            print("error")
        return
    
    def importDOT(self):
        # using the graphMani import the graph
        print(str(self.directory) + "/" + str(self.filename))
        self.graph = myGraph(str(self.directory) + "/" + str(self.filename))
        self.graph.saveAsType('json')
        print("successfully imported .dot")
        return
        
    def importJSON(self):
        self.saveName = self.filename[:-4]+'dump.json'
        if self.saveName in os.listdir(self.directory):
            return
        # importing the file graphjson.json 
        with open('graphjson.json','r') as fp:
            jsonfile = json.load(fp)

        newJson = {}

        #taking the nodes from the graph
        nodes = jsonfile['graph']['properties']['externLabel']['nodesValues']
        jnodes = []
        
        for n in nodes:
            node = {}
            inNode = self.graph.getInNodes()
            outNode = self.graph.getOutNodes()
            #adding the service name into the json format
            node['functions'] = nodes[n]
            # adding the dependants for a node into the json format
            node['dependants'] = inNode[nodes[n]]
            #decs = outNode[nodes[n]]
            # adding the dependencies for a node into the json format
            node['dependencies'] = outNode[nodes[n]]
            # adding the in nodes count
            node['inDegree'] = len(inNode[nodes[n]])
            # adding the out nodes count
            node['outDegree'] = len(outNode[nodes[n]])
            jnodes.append(node) 
            
        newJson["nodes"] = jnodes
        links = []
        # adding the links between the nodes
        for l in jsonfile['graph']['edges']:
            link = {}
            link['source'] = l[0]
            link['target'] = l[1]
            links.append(link)
        newJson["links"] = links
        data = json.dumps(newJson, indent = 2)
        # saving the new json format graph 
        os.chdir(self.directory)
        with open(self.saveName,'w') as f:
            f.write(data)
        return
        
    
    