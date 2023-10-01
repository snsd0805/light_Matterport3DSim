import csv
import json
import os
import sys
import numpy as np
import base64
import setting
from src.state import State

csv.field_size_limit(sys.maxsize)

class LightMatterSim():
    def __init__(self, features_file, batch_size):
        '''
            light wight matterport 3d simulator  
            only implement the makeAction and getState, etc.
            
            Inputs:
                features_file(str): the file path which contains image features 
                batch_size(int)
        '''
        self.__initilized = False
        self.__batch_size = batch_size
        self.__states = []

        # load features & viewpoint
        self.__features = self.__load_features(features_file)
        self.__navigable_viewpoints = self.__load_navigable_viewpoints()

        # initialization
        self.__initialize()
    
    def __initialize(self):
        self.__initilized = True
        self.__states = [ State() for i in range(self.__batch_size) ]
    
    def newEpisode(self, scans, viewpoints):
        '''
            New simulation episode.
            set up (batch_size) simulators

            Inputs:
                scans(list): a list of str(scan(enviroment) id ). 
                viewpoints(list): a list of str(viewpoint id)
            Outputs:
                None
        '''
        # if not initlized
        if not self.__initilized:
            self.__initialize() 
        
        # initilize the states
        for i in range(self.__batch_size):
            self.__states[i].step = 0
            self.__states[i].scan_id = scans[i]
            self.__states[i].viewpoint_id = viewpoints[i]

        self.populateNavigable()
    
    def populateNavigable(self):
        '''
            find all navigable viewpoint from the viewpoint which the agent at now
            save in each `states.navigableLocations`

            Inputs:
                None
            Outputs:
                None
        '''
        for i in range(self.__batch_size):
            scan = self.__states[i].scan_id
            viewpoint = self.__states[i].viewpoint_id
            view_index = self.__states[i].view_index
            # item in navigableLocations is (str). it's viewpoint_id
            self.__states[i].navigableLocations = \
                self.__navigable_viewpoints[scan][viewpoint][str(view_index)]

    
    def getStates(self):
        '''
            Return states in simulator

            Inputs:
                None
            Outputs:
                states(list of State)
        '''
        return self.__states
    
    def makeAction(self, indexes):
        '''
            Make actions for simulators

            Inputs:
                indexes(list of int): actions
            Outputs:
                None
        '''
        for i in range(self.__batch_size):
            navigable_size = len(self.__states[i].navigableLocations)
            assert indexes[i] <=  navigable_size, \
                "Invalid action index. {} navigable action but get {}".format(navigable_size, indexes[i])
            
            self.__states[i].step += 1
            self.__states[i].viewpoint_id = self.__states[i].navigableLocations[indexes[i]] 

        self.populateNavigable()

    def __load_features(self, infile):
        '''
            load image features from the TSV file
            
            Inputs:
                infile(str): filename. TSV file contain image features
            Outputs:
                features(dict): key is long_id(scan_id + viewpoint_id)
                                it has a list of features (36, 2048).
        '''
        features = {}
        print("load features from {}...".format(infile))
        with open(infile, "rt") as fp:
            # read TSV file
            reader = csv.DictReader(fp, delimiter='\t', fieldnames=setting.TSV_FIELDNAMES)
            for item in reader:
                scan_id = item['scanId']
                viewpoint_id = item['viewpointId']

                # use long id as key to select what viewpoint's feature you want to get
                long_id = scan_id + '_' + viewpoint_id

                # (36, 2048)
                feature = item['features'] = np.frombuffer(base64.b64decode(item['features']),
                        dtype=np.float32).reshape((setting.VIEWPOINT_SIZE, setting.FEATURE_SIZE))

                features[long_id] = feature
        print("loaded {} viewpoints' features.\n".format(len(features)))
        return features

    def __load_navigable_viewpoints(self):
        '''
            load navigable vewpoints path from navigate/*.json files
            navigable_viewpoints contains all navigable points from any other viewpoint

            Inputs:
                None
            Outputs:
                navigable_viewpoints(dict): key is the `scan`, `from` viewpoint and `view index`. 
                                            it will show the next navigable viewpoint to choose.
                                            use like: navigable_viewpoints['1pXnuDYAj8r']['2c...455']['5']                     
        '''
        # load scans list
        assert os.path.isfile('navigate/scans.txt'), "You should donwload https://snsd0805.com/data/navigate.zip"
        with open('navigate/scans.txt') as fp:
            scans = [ scan.strip() for scan in fp.readlines() ]
        
        # load navigate/*.json
        navigatable_viewpoints = {}
        for scan in scans:
            with open('navigate/{}.json'.format(scan)) as fp:
                data = json.load(fp)
                navigatable_viewpoints[scan] = data
        return navigatable_viewpoints
    
    