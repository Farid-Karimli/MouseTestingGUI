import numpy as np

class FitsLaw:

    def __init__(self, target_width:float, distance_to_target:float):
        self.target_width = target_width
        self.distance_to_target = distance_to_target

    def calculate_original_law(self, time:float):
        ID = np.log2((2*self.distance_to_target)/self.target_width)
        MT = time
        return ID/MT
    

    