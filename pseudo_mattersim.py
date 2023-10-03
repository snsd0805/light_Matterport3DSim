import json

class PseudoViewPoint:
    def __init__(self, viewpoint):
        self.ix = viewpoint.ix
        self.rel_distance = viewpoint.rel_distance
        self.rel_elevation = viewpoint.rel_elevation
        self.rel_heading = viewpoint.rel_heading
        self.viewpointId = viewpoint.viewpointId
        self.x = viewpoint.x
        self.y = viewpoint.y
        self.z = viewpoint.z

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
        #self.location
        self.sync_heading_and_elevation()
        
    def sync_heading_and_elevation(self):
        self.heading = self.headings_by_views[self.viewIndex]
        self.elevation = self.elevation_by_view[self.viewIndex]
        
    def update_view(self, heading, elevation):
        if heading != 0:
            self.viewIndex += heading
            if self.viewIndex%12==0:
                self.viewIndex -= 12
        if elevation != 0:
            self.viewIndex += 12
        self.sync_heading_and_elevation()
    
    
class PseudoSimulator:
    def __init__(self):
        self.state = PseudoSimState()
        self.routes = None
        
    def initial_heading_to_view_idx(self, initial_heading):
        heading = round(initial_heading/math.radians(30))
        if heading == 12:
            heading = 0
        return 12 + heading
    
    def setRenderingEnabled(x):
        pass
    
    def setDiscretizedViewingAngles(x):
        pass
    
    def setCameraResolution(x, y):
        pass
    
    def setCameraVFOV(x):
        pass
    
    def initialize():
        pass
    
    def load_cache():
        pass
        
    def makeAction(index, heading, elevation):
        new_node_id = navigableLocations[self.state.node_id][str(self.state.viewIndex)][index]
        if self.state.node_id != new_node_id:
            self.state.node_id = new_node_id
            self.state.navigableLocations = self.routes[new_node_id]
        self.state.update_view(heading, elevation)
    
    def getState():
        return [self.state]
    
    def newEpisodes(scanId, node_id, heading, elevation):
        self.routes = json.load(open(f'navigate/{scanId}.json'))
        navigableLocations = self.routes[node_id]
        viewIndex = self.initial_heading_to_view_idx(initial_heading)
        self.state.update(scanId, node_id, viewIndex, navigableLocations)
        
