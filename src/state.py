'''
This is source code about state

struct SimState: std::enable_shared_from_this<SimState>{
    //! Building / scan environment identifier
    std::string scanId;

    //! Number of frames since the last newEpisode() call
    unsigned int step = 0;
    
    //! RGB image (in BGR channel order) from the agent's current viewpoint
    cv::Mat rgb;
    
    //! Depth image taken from the agent's current viewpoint
    cv::Mat depth;
    
    //! Agent's current 3D location
    ViewpointPtr location;
    
    //! Agent's current camera heading in radians           (we don't need it)
    double heading = 0;
    
    //! Agent's current camera elevation in radians         (we don't need it)
    double elevation = 0;
    
    //! Agent's current view [0-35] (set only when viewing angles are discretized)
    //! [0-11] looking down, [12-23] looking at horizon, [24-35] looking up
    unsigned int viewIndex = 0;
    
    //! Vector of nearby navigable locations representing state-dependent action candidates, i.e.
    //! viewpoints you can move to. Index 0 is always to remain at the current viewpoint.
    //! The remaining viewpoints are sorted by their angular distance from the centre of the image.
    std::vector<ViewpointPtr> navigableLocations;
}
 '''
class State():
    def __init__(self):
        self.scan_id = ""
        self.viewpoint_id = ""              # it's in state.location
        self.step = 0
        self.rgb = None
        self.depth = None
        self.view_index = 0
        self.navigableLocations = []
    
    def __str__(self):
        ans = ""
        ans += "scan_id: {}\n".format(self.scan_id)
        ans += "viewpoint_id: {}\n".format(self.viewpoint_id)
        ans += "step: {}\n".format(self.step)
        ans += "rgb: {}\n".format(self.rgb)
        ans += "depth: {}\n".format(self.depth)
        ans += "view_indexe {}\n".format(self.view_index)
        ans += "navigableLocations:\n"
        for node in self.navigableLocations:
            ans += "    {}\n".format(node)
        ans += "\n\n"
        return ans 