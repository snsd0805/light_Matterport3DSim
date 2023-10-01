from src.lightMatterSim import LightMatterSim
import setting

if __name__ == '__main__':
    sim = LightMatterSim(setting.FEATURES_FILE, 1)
    sim.newEpisode(['1LXtFkjw3qL'], ['187589bb7d4644f2943079fb949c0be9'])
    while 1:
        states = sim.getStates()
        print(states[0])

        action = int(input())
        sim.makeAction([action])
