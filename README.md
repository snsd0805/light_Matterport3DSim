# Light Matterport3DSim
## Requirement
- download features

    Matterport3DSim has generated image features using Caffe and it provided [features](https://github.com/peteanderson80/Matterport3DSimulator/tree/589d091b111333f9e9f9d6cfd021b2eb68435925#precomputing-resnet-image-features) to download.

    Features are saved in tsv format in the `img_features` directory.

## Get navigable viewpoints
You can run `python3 script/getBavugabkePoints.py` to get all navigable viewpoints in simulation but you must run this program in the docker container which support the original `Matterport3DSim`.

These viewpoints will be saved in json file in `navigate/` directory.

Without running the script, You can directly download these files at this [link](https://snsd0805.com/data/navigate.zip) 

