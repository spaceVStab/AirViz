"""
This is the script responsible for graph imports, exports, manipulation
"""
from tulip import tlp
#from tulipgui import tlpgui
import os
import configParam

class myGraph(object):
    def __init__(self, graphLoc):
        print(graphLoc)
        #import the graph
        graph = tlp.loadGraph(graphLoc)
        self.config = configParam.configParam()
        self.graph = graph
        #get necessary properties 
        self.viewLayout = graph.getLayoutProperty("viewLayout")
        self.viewSize = graph.getSizeProperty("viewSize")
        self.viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
        self.viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
        self.viewColor = graph.getColorProperty("viewColor")
        self.viewLabelColor = graph.getColorProperty("viewLabelColor")
        self.viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
        self.viewBorderColor = graph.getColorProperty("viewBorderColor")
        self.viewLabel = graph.getStringProperty("viewLabel")
        self.viewShape = graph.getIntegerProperty("viewShape")
        self.viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
        self.viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
        self.viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
        self.viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")
        return
    
    def modifyMyGraph(self):
        self.viewBorderWidth.setAllEdgeValue(0.1)
        self.viewColor.setAllEdgeValue(tlp.Color.Blue)
        self.viewColor.setAllNodeValue(tlp.Color.Red)
        self.viewSrcAnchorShape.setAllEdgeValue(tlp.EdgeExtremityShape.Circle)
        self.viewTgtAnchorShape.setAllEdgeValue(tlp.EdgeExtremityShape.Cross)
        return
    
    def removeChildren(self):
        # this function removes the children or nodes which are single degrees
        for node in self.graph.getNodes():
            if self.graph.deg(node) == 1:
                for edge in self.graph.allEdges(node):
                    self.graph.delEdge(edge)
        for node in self.graph.getNodes():
            if self.graph.deg(node) == 0:
                self.graph.delNode(node)
        return
        
    def saveAsType(self, gtype, rmchild=False):
        # this function is responsible to export the graph as per type provided
        if rmchild is True:
            self.removeChildren()
        currDir = self.config.working_directory
        status = tlp.saveGraph(self.graph, currDir + "/graph"+gtype+"."+gtype)
        return status
    
    def getIDNodeMap(self):
        # this function retunrs the dictionary of IDs and their function names of nodes
        self.IdNode = {}
        for node in self.graph.getNodes():
            self.IdNode[node.id] = str(self.viewLabel[node])
        return self.IdNode
    
    def getInNodes(self):
        # this function is reponsible for returning the list of incoming nodes for a particular node
        self.inNodes = {}
        for node in self.graph.getNodes():
            innode = self.graph.getInNodes(node)
            innodelist = []
            for inn in innode:
                nodename  = self.viewLabel[inn]
                innodelist.append(str(nodename))
            self.inNodes[str(self.viewLabel[node])] = innodelist
        return self.inNodes
    
    
    def getOutNodes(self):
        # this function is responsible for returning the list of outgoing nodes for a particular node
        self.outNodes = {}
        for node in self.graph.getNodes():
            outnode = self.graph.getOutNodes(node)
            outnodelist = []
            for out in outnode:
                nodename  = self.viewLabel[out]
                outnodelist.append(str(nodename))
            self.outNodes[str(self.viewLabel[node])] = outnodelist
        return self.outNodes
    
    def graphToImg(self, name):
        #to output an image without displaying it
        #tlpself.modifyMyGraph()
        nodeLinkView = tlpgui.createView("Node Link Diagram view", self.graph, {}, False)
        currDir = os.getcwd()
        #returns true if image is generated
        status = nodeLinkView.saveSnapshot(currDir+"/"+name+".png", 1920, 1080)    
        return status
    