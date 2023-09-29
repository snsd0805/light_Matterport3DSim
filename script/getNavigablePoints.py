# this script must run in docker which has MatterSim enviroment
# It's may get all viewpoint's navigable locations from simulation
# and this is the reference code: https://github.com/peteanderson80/Matterport3DSimulator/blob/589d091b111333f9e9f9d6cfd021b2eb68435925/scripts/precompute_img_features.py

import MatterSim
import sys
import math
import os
import json
import numpy as np
import time
# Simulator image parameters 
WIDTH=640
HEIGHT=480
VFOV=60

GRAPHS = 'connectivity/'
VIEWPOINT_SIZE = 36 # Number of discretized views from one viewpoint
FEATURE_SIZE = 2048

def load_scans():
    with open(GRAPHS+'scans.txt') as f:
        scans = [scan.strip() for scan in f.readlines()]
    print("loaded {} scans".format(len(scans)))
    return scans

def load_viewpoints(scans):
    viewpoints = {scan: [] for scan in scans}
    counter = 0
    for scan in scans:
        with open(GRAPHS+scan+'_connectivity.json')  as j:
            data = json.load(j)
            for item in data:
                if item['included']:
                    viewpoints[scan].append(item['image_id'])
                    counter += 1
    print("loaded {} viewpoints".format(counter))
    return viewpoints


if __name__ == "__main__":

    # start a simulator
    sim = MatterSim.Simulator()
    sim.setCameraResolution(WIDTH, HEIGHT)
    sim.setCameraVFOV(math.radians(VFOV))
    sim.setDiscretizedViewingAngles(True)
    sim.setBatchSize(1)
    sim.initialize()

    # get all the scans & viewpoints in the simulator
    scans = load_scans()
    viewpoints = load_viewpoints(scans)

    # loop to get state from all viewpoints and view index
    scan_counter = 0
    process_counter = 0
    for scan in scans:

        # check whether the file exist
        scan_counter += 1
        print("{} {}/{}".format(scan, scan_counter, len(scans)))
        if os.path.isfile('./navigate/{}.json'.format(scan)):
            print("navigate/{}.json exist. skip scanning".format(scan))
            continue

        # loop scan(enviroment)
        navigableLocations = {}
        for viewpoint in viewpoints[scan]:
            navigableLocations[viewpoint] = {
                i: [] for i in range(VIEWPOINT_SIZE)
            }
            # loop view index (36)
            for ix in range(VIEWPOINT_SIZE):
                if ix == 0:
                    sim.newEpisode([scan], [viewpoint], [0], [math.radians(-30)])
                elif ix % 12 == 0:
                    sim.makeAction([0], [1.0], [1.0])   # turn right & lift up
                else:
                    sim.makeAction([0], [1.0], [0])

                state = sim.getState()[0]

                # save all navigation viewpoint
                for node in state.navigableLocations:
                    navigableLocations[viewpoint][ix].append(
                        node.viewpointId
                    )

        # save navigable viewpoint into file
        with open("navigate/{}.json".format(scan), 'w') as fp:
            json.dump(navigableLocations, fp)
        process_counter += 1

        # some memory problem but i cannot solve now.
        # so this program may stop when processed 40 enviroments.
        # the user need to restart this to process all enviroment to get all files.
        if process_counter == 40:
            print("Due to memory problem. This process need to stop.")
            print("You can run this program more times until this program scanning all nodes")
            print("Now: {}/{} completed".format(scan_counter, len(scans)))
            exit()