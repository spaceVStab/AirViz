"""
Main application script for version 1
"""
import json
import sys
from flask import Flask, render_template, request, jsonify
import networkx as nx
from networkx.readwrite import json_graph
from jsonClass import genJSON
import configParam
import os

app = Flask(__name__)
config = configParam.configParam()


# change the filename accordingly; make sure the file is in the same folder as that of this script
FILENAME = config.FILENAME

@app.route('/')
def index():
    INPUT_DIR = config.working_directory
    os.chdir(INPUT_DIR)
    if FILENAME not in os.listdir(INPUT_DIR):
        pass
    
    JSONFILE = FILENAME[:-4] + "dump.json"
    
    # if corresponding dump.json is not there in directory, it will be created using the classes genJSON
    if JSONFILE not in os.listdir(INPUT_DIR):
        myjson = genJSON(filename=FILENAME)
        myjson.importJSON()
        
    with open(JSONFILE,'r') as fp:
        jsonfile = json.load(fp)
    data = {'graphData': jsonfile}
    return render_template("index.html", data = data)

#this function is for the simple paths determination between two nodes
@app.route('/paths', methods=['GET','POST'])
def process():
    # importing the value of source and target using ajax from the web browser
    source = request.form['source']
    target = request.form['target']
    print(source, target, file=sys.stdout)

    ## importing the graph using networkx 
    if source and target:
        with open(str(FILENAME[:-4] + "dump.json"),'r') as fp:
            jsonfile = json.load(fp)
        graph = json_graph.node_link_graph(jsonfile, directed=True)
        #mapping the ID and name of nodes for simplicity
        nodeIDFuncMap = {}
        for f in graph.nodes():
            nodeIDFuncMap[graph.node[f]['functions']] = f

        # getting the source and target IDS
        sourceID = nodeIDFuncMap[str(source)]
        targetID = nodeIDFuncMap[str(target)]
        totalPaths = nx.all_simple_paths(graph, source = sourceID, target=targetID)

        nodeList = []
        totalNodes = []
        # creating the list of nodes involved in the paths
        for p in totalPaths:
            for n in p:
                if n not in totalNodes:
                    totalNodes.append(n)
        for n in totalNodes:
            l = {}
            l["id"] = n
            nodeList.append(l)

        # creating the list for total links present
        linkList2 = []
        totalPaths = nx.all_simple_paths(graph, source = sourceID, target=targetID)
        for p in totalPaths:
            for i in range(len(p)-1):
                link = {}
                link["source"] = p[i]
                link["target"] = p[i+1]
                linkList2.append(link)
        path = {"nodes":nodeList, "links":linkList2}
        data = json.dumps(path, indent = 2)

        #saving the simple path for reference as path.json
        with open('path.json','w') as f:
            f.write(data)

        # returning the json format 
        return jsonify(path)
    return jsonify({"error":"Missing Data!!"})                      

if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True)