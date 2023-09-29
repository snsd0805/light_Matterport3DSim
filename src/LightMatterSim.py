import csv
import sys
import numpy as np
import base64

csv.field_size_limit(sys.maxsize)

TSV_FIELDNAMES = ['scanId', 'viewpointId', 'image_w','image_h', 'vfov', 'features']
FEATURES_FILE = 'img_features/ResNet-152-imagenet.tsv'

VIEWPOINT_SIZE = 36
FEATURE_SIZE = 2048

class LightMatterSim():
    def __init__(self, features_file):
        '''
            light wight matterport 3d simulator  
            only implement the makeAction and getState, etc.
            
            Inputs:
                features_file(str): the file path which contains image features 
        '''
        self.features = self.load_features(FEATURES_FILE)

    def load_features(self, infile):
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
            reader = csv.DictReader(fp, delimiter='\t', fieldnames=TSV_FIELDNAMES)
            for item in reader:
                scan_id = item['scanId']
                viewpoint_id = item['viewpointId']

                # use long id as key to select what viewpoint's feature you want to get
                long_id = scan_id + '_' + viewpoint_id

                # (36, 2048)
                feature = item['features'] = np.frombuffer(base64.b64decode(item['features']),
                        dtype=np.float32).reshape((VIEWPOINT_SIZE, FEATURE_SIZE))

                features[long_id] = feature
        print("loaded {} viewpoints.\n".format(len(features)))
        return features

if __name__ == "__main__":
    sim = LightMatterSim(FEATURES_FILE)