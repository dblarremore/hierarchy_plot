import numpy as np
import networkx as nx
import SpringRank as sr

def write_circle(file,center,radius,stroke,fillcolor,strokecolor):
    file.write('<circle class="node" r="{}" style="fill: rgb({},{},{}); stroke: rgb({},{},{}); stroke-width:{}" cx="{}" cy="{}"/>\n'
               .format(radius,fillcolor[0],fillcolor[1],fillcolor[2],
                       strokecolor[0],strokecolor[1],strokecolor[2],
                       stroke,center[0],center[1]))
def write_arc(file,centerFrom,centerTo,anchor,width,color,opacity):
    file.write('<path d="M{} {} Q {} {} {} {}" stroke-width="{}" stroke="rgb({},{},{})" stroke-opacity="{}" fill="none"/>\n'
               .format(
                   centerFrom[0],centerFrom[1],
                   anchor[0],anchor[1],
                   centerTo[0],centerTo[1],
                   width,
                   color[0],color[1],color[2],
                   opacity))
def write_text(file,xy,myText,myClass,myRotate,myTranslate):
    file.write('<text x="{}" y="{}" class="{}" transform="translate({},{}) rotate({} {},{})">{}</text>\n'.format(
        xy[0],xy[1],
        myClass,
        myTranslate[0],myTranslate[1],
        myRotate,xy[0],xy[1],
        myText))
def write_line(file,myStart,myFinish,stroke,color,opacity):      
    file.write('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke-width="{}" stroke="rgb({},{},{})" stroke-opacity="{}"/>\n'.format(
        myStart[0],myStart[1],
        myFinish[0],myFinish[1],
        stroke,color[0],color[1],color[2],opacity))

def svg_circle(center,radius,stroke,fillcolor,strokecolor):
    circle =  '<circle class="node" r="{}" style="fill: rgb({},{},{}); stroke: rgb({},{},{}); stroke-width:{}" cx="{}" cy="{}"/>\n'.format(
        radius,fillcolor[0],fillcolor[1],fillcolor[2],
        strokecolor[0],strokecolor[1],strokecolor[2],
        stroke,center[0],center[1])
    return circle
def svg_line(myStart,myFinish,stroke,color,opacity):      
    line = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke-width="{}" stroke="rgb({},{},{})" stroke-opacity="{}"/>\n'.format(
        myStart[0],myStart[1],
        myFinish[0],myFinish[1],
        stroke,color[0],color[1],color[2],opacity)
    return line
def svg_text(xy,myText,myClass,myRotate,myTranslate):
    text = '<text x="{}" y="{}" class="{}" transform="translate({},{}) rotate({} {},{})">{}</text>\n'.format(
        xy[0],xy[1],
        myClass,
        myTranslate[0],myTranslate[1],
        myRotate,xy[0],xy[1],
        myText)
    return text
def svg_arc(centerFrom,centerTo,anchor,width,color,opacity):
    arc = '<path d="M{} {} Q {} {} {} {}" stroke-width="{}" stroke="rgb({},{},{})" stroke-opacity="{}" fill="none"/>\n'.format(
        centerTo[0],centerTo[1],
        anchor[0],anchor[1],
        centerFrom[0],centerFrom[1],
        width,
        color[0],color[1],color[2],
        opacity)
    return arc


class RankSVG:
    def __init__(self, path, width=600, aspectRatio=9/5, swirl=1/4, pad=230, text_offset=180, text_size=12, node_size=3):
        self.path = path
        self.width = int(width)
        self.height = int(width*aspectRatio)
        self.aspectRatio = aspectRatio
        self.swirl = swirl
        self.pad = pad
        self.text_offset = text_offset
        self.text_size = text_size
        self.node_size = node_size
        
        self.nodes = []
        self.node2center = {}
        self.node2size = {}
        
        self.edges = []
        self.set_head()    
    
    def get_anchor(self,fr,to):
        anchor_y = (1-self.swirl)*fr + self.swirl*to;
        anchor_x = (self.width/2)+np.sign(to-fr)*np.abs(to-fr)/self.aspectRatio;
        return [anchor_x,anchor_y]
    
    def set_head(self):
        self.head = '<svg width="{}" height="{}" id="{}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'.format(self.width,self.height,'v1') + '''
        <style>
            .sans { font: 12px sans-serif; }
            .grey { stroke: rgb(150,150,150); stroke-width:0.5;}
        </style>
        '''
    
    def set_nodes(self,nodes):
        for node in nodes:
            self.nodes.append(node)
            self.node2center[node] = 0
            self.node2size[node] = self.node_size
        
    def add_edge(self,edge):
        self.edges.append(edge.copy())
        
    def get_nodes(self):
        return self.nodes
    
    def set_node_centers(self,node2center):
        for key in node2center.keys():
            self.node2center[key] = [self.width/2,
                                     np.interp(node2center[key],
                                               (np.min(list(node2center.values())),
                                                np.max(list(node2center.values()))),
                                               (self.height-self.pad,self.pad))]
    
    def set_node_sizes(self,node2size):
        for key in node2size.keys():
            self.node2size[key] = node2size[key]
            
    def set_axis_label(self,axis_label):
        self.axis_label = axis_label
            
    def write_nodes(self,f):
        for node in self.nodes:
            circle = svg_circle(
                center=self.node2center[node],
                radius=self.node2size[node],
                stroke=1.5,
                fillcolor=[100,100,100],
                strokecolor=[255,255,255])
            f.write(circle)
            
    def write_center_line(self,f):
        center_line = svg_line(
            [self.width/2,
             np.min(list(self.node2center.values()))-self.pad/4],
            [self.width/2,
             np.max(list(self.node2center.values()))+self.pad/4],
            stroke=0.5,
            color=np.array([150,150,150]),
            opacity=1)
        f.write(center_line)
    
    def label_nodes(self,f):
        self.write_label_lines(f)
        self.write_label_text(f)
    
    def write_label_lines(self,f):
        for node in self.nodes:
            label_line = svg_line(
                self.node2center[node],
                np.array(self.node2center[node])+np.array([self.text_offset,0]),
                stroke=0.5,
                color=np.array([150,150,150]),
                opacity=1)
            f.write(label_line)
    
    def write_label_text(self,f):
        for node in self.nodes:
            text = svg_text(self.node2center[node],
                            myText=node,
                            myTranslate=[self.text_offset,self.text_size/4],
                            myRotate=0,myClass="sans")
            f.write(text)
            
    def label_axis(self,f):
        axis_text = svg_text(
            [self.width/2-4,self.pad-10],self.axis_label,
            'sans',-90,[0,0])
        f.write(axis_text)
    
    def write_under_edges(self,f):
        rgb = np.array([0,0,0])
        for edge in self.edges:
            if 'width' in edge.keys():
                w = edge['width']
            else:
                w = 2
            under_arc = svg_arc(self.node2center[edge['fr']],
                          self.node2center[edge['to']],
                          self.get_anchor(self.node2center[edge['fr']][1],
                                          self.node2center[edge['to']][1]),
                          width=w+2,
                          color=np.array([255,255,255]),
                          opacity=1)
            f.write(under_arc)
    
    def write_edges(self,f):
        rgb = np.array([0,0,0])
        for edge in self.edges:
            if 'width' in edge.keys():
                w = edge['width']
            else:
                w = 2
            if 'color' in edge.keys():
                c = edge['color']
            else:
                c = np.array([100,100,100])
            if 'alpha' in edge.keys():
                alph = edge['alpha']
            else:
                alph = 0.3
            arc = svg_arc(self.node2center[edge['fr']],
                          self.node2center[edge['to']],
                          self.get_anchor(self.node2center[edge['fr']][1],
                                          self.node2center[edge['to']][1]),
                          width=w,
                          color=c,
                          opacity=alph)
            f.write(arc)
    
    def dump(self):
        f = open(self.path,'w')
        f.write(self.head)
        self.write_center_line(f)
        # self.label_nodes(f)
        # self.label_axis(f)
        # self.write_under_edges(f)
        self.write_edges(f)
        self.write_nodes(f)
        f.write('</svg>')
        f.close()

def nx2rankfigure(nxG,filepath='viz.svg'):
    nodes = list(nxG.nodes())
    A = nx.to_numpy_array(nxG,
                          nodelist=nxG.nodes(),
                          weight='weight')
    positions = sr.get_scaled_ranks(A)
    
    svg = RankSVG(filepath)
    svg.set_nodes(nodes)
    
    node2center = dict()
    for idx,name in enumerate(nodes):
        node2center[name] = positions[idx]
    svg.set_node_centers(node2center)
    
    edges = []
    for i,iname in enumerate(nodes):
        for j,jname in enumerate(nodes):
            if i==j:
                continue
            if A[i,j]==0:
                continue
            edge = dict()
            edge['fr'] = iname
            edge['to'] = jname
            edge['weight'] = A[i,j]
            # If you want color, put it here!
            if positions[i] >= positions[j]:
                edge['color'] = np.array([255,0,0])
            else:
                edge['color'] = np.array([0,0,255])
            svg.add_edge(edge.copy())
    svg.dump()
    