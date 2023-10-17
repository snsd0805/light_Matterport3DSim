import json
import math
from datetime import datetime


class PseudoViewPoint:
    
    def __init__(self, inp):
        if type(inp) is str:
            self.from_node_id(inp)
        else:
            self.from_viewpoint(inp)
        
        
    def from_viewpoint(self, viewpoint):
        self.ix = viewpoint['ix']
        self.rel_distance = viewpoint['rel_distance']
        self.rel_elevation = viewpoint['rel_elevation']
        self.rel_heading = viewpoint['rel_heading']
        self.viewpointId = viewpoint['viewpointId']
        self.x = viewpoint['x']
        self.y = viewpoint['y']
        self.z = viewpoint['z']
        
    def from_node_id(self, viewpointId):
        self.viewpointId = viewpointId




class PseudoSimState:
    def __init__(self, state=None):
        self.headings_by_views = [0.0, 0.5235987755982988, 1.0471975511965976, 1.5707963267948966, 2.0943951023931953, 2.617993877991494, 3.141592653589793, 3.665191429188092, 4.1887902047863905, 4.71238898038469, 5.235987755982988, 5.759586531581287, 0.0, 0.5235987755982988, 1.0471975511965976, 1.5707963267948966, 2.0943951023931953, 2.617993877991494, 3.141592653589793, 3.665191429188092, 4.1887902047863905, 4.71238898038469, 5.235987755982988, 5.759586531581287, 0.0, 0.5235987755982988, 1.0471975511965976, 1.5707963267948966, 2.0943951023931953, 2.617993877991494, 3.141592653589793, 3.665191429188092, 4.1887902047863905, 4.71238898038469, 5.235987755982988, 5.759586531581287]
        self.elevation_by_views = [-0.5235987755982988, -0.5235987755982988, -0.5235987755982988, -0.5235987755982988, -0.5235987755982988, -0.5235987755982988, -0.5235987755982988, -0.5235987755982988, -0.5235987755982988, -0.5235987755982988, -0.5235987755982988, -0.5235987755982988, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5235987755982988, 0.5235987755982988, 0.5235987755982988, 0.5235987755982988, 0.5235987755982988, 0.5235987755982988, 0.5235987755982988, 0.5235987755982988, 0.5235987755982988, 0.5235987755982988, 0.5235987755982988, 0.5235987755982988]
    
        if state is not None:
            self.update(state)
    
    def update_from_state(self, state):
        pseudo_state_dict = {}
        pseudo_state_dict['viewIndex'] = state.viewIndex
        pseudo_state_dict['step'] = state.step
        pseudo_state_dict['scanId'] = state.scanId
        pseudo_state_dict['navigableLocations'] = [PseudoViewPoint(loc) for loc in state.navigableLocations]
        pseudo_state_dict['location'] = PseudoViewPoint(state.location)
        pseudo_state_dict['heading'] = state.heading
        pseudo_state_dict['elevation'] = state.elevation
        
        for key, value in pseudo_state_dict.items():
            setattr(self, key, value)
            
    def update(self, scanId, node_id, viewIndex, navigableLocations, step=0):
        self.viewIndex = viewIndex
        self.step = step
        self.scanId = scanId
        self.navigableLocations = navigableLocations
        self.node_id = node_id
        self.location = PseudoViewPoint(node_id)
        self.sync_heading_and_elevation()
        
    def sync_heading_and_elevation(self):
        self.heading = self.headings_by_views[self.viewIndex]
        self.elevation = self.elevation_by_views[self.viewIndex]
        
    def update_view(self, heading, elevation):
        if heading != 0:
            self.viewIndex += int(heading)
            if self.viewIndex%12==0:
                self.viewIndex -= 12
        if elevation != 0:
            self.viewIndex += int(12 * elevation)
        self.sync_heading_and_elevation()
    
    
class PseudoSimulator:
    def __init__(self, route_root, debug_log=False):
        self.state = PseudoSimState()
        self.routes = None
        self.debug_log = debug_log
        self.route_root = route_root
        if self.debug_log:
            self.log_fp = open(f"{datetime.now()}_pseudo_sim.log", "w")
        
    def initial_heading_to_view_idx(self, initial_heading):
        heading = round(initial_heading/math.radians(30))
        if heading == 12:
            heading = 0
        return 12 + heading
    
    def setRenderingEnabled(self, x):
        pass
    
    def setDiscretizedViewingAngles(self, x):
        pass
    
    def setCameraResolution(self, x, y):
        pass
    
    def setCameraVFOV(self, x):
        pass
    
    def initialize(self):
        pass
    
    def load_cache():
        pass
    
    def log_state(self):
        for k in ['scanId', 'node_id', 'viewIndex', 'heading', 'elevation']:
            self.log_fp.write(f"{k}: {self.state.__dict__[k]}\n")
        
    def makeAction(self, index, heading, elevation):
        index, heading, elevation = index[0], heading[0], elevation[0]
        navigableLocations = self.routes[self.state.node_id][self.state.viewIndex]
        new_node_id = navigableLocations[index].viewpointId
        if self.state.node_id != new_node_id:
            self.state.node_id = new_node_id
        
        self.state.update_view(heading, elevation)
        self.state.navigableLocations = self.routes[new_node_id][self.state.viewIndex]
        
        if self.debug_log:
            self.log_fp.write(f"makeAction called: {index}, {heading}, {elevation}\n")
            self.log_state()
    
    def getState(self):
        return [self.state]
    
    def node_to_pseudoviewpoint(self, view):
        return [PseudoViewPoint(node) for node in view]

    def views_to_pseudoviewpoint(self, views):
        return [self.node_to_pseudoviewpoint(view) for view in views]

    def load_routes(self, routes):
        ret = {}
        for node_id, views in routes.items():
            ret[node_id] = self.views_to_pseudoviewpoint(views)
        return ret

    def newEpisode(self, scanId, node_id, heading, elevation):
        scanId, node_id, heading, elevation = scanId[0], node_id[0], heading[0], elevation[0]
        #self.routes = json.load(open(f'navigate/{scanId}.json'))
        
        #make it load_routes
        raw_routes = json.load(open(f'{self.route_root}/{scanId}.json'))
        self.routes = self.load_routes(raw_routes)
        
        if (heading, elevation) == (0, math.radians(-30)): #some stupid workaround
            viewIndex = 0
        else:
            viewIndex = self.initial_heading_to_view_idx(heading)
            
        navigableLocations = self.routes[node_id][viewIndex]
        self.state.update(scanId, node_id, viewIndex, navigableLocations)
        
        if self.debug_log:
            self.log_fp.write("newEpisode called\n")
            self.log_state()
        
