import numpy as np

class FitsLaw:

    def __init__(self, target_width:float, distance_to_target:float):
        self.target_width = target_width
        self.distance_to_target = distance_to_target

        self.a = 0
        self.b = 0
        self.c = 0

        self.movement_amplitudes = []
        self.selection_coordinates = []

        self.f:tuple[int] = 0
        self.to:tuple[int] = 0
        self.select:tuple[int] = 0

        self.ae = 0
        self.dx = 0

        self.times = []

        self.ballistic_times = []
        self.time_to_select = []

    def __repr__(self) -> str:
        return f"from: {self.f}\nto: {self.to}\nselect: {self.select}\n"

    def calculate_original_law(self, time:float):
        ID = np.log2((self.distance_to_target)/self.target_width + 1)
        MT = time
        return ID/MT
    
    def distance(self, x1, y1, x2, y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5
    
    def calculate_a(self):
        self.a = self.distance(self.f[0], self.f[1], self.to[0], self.to[1])
    
    def calculate_b(self):
        self.b = self.distance(self.to[0], self.to[1], self.select[0], self.select[1])
    
    def calculate_c(self):
        self.c = self.distance(self.f[0], self.f[1], self.select[0], self.select[1])
    
    def update(self):
        self.calculate_a()
        self.calculate_b()
        self.calculate_c()
        dx:float = (self.c**2 - self.b**2 - self.a**2)/(2*self.a)
        self.movement_amplitudes += [self.a + dx]
        #print(self.movement_amplitudes)
        self.selection_coordinates += [dx]
        #print(self.selection_coordinates)

    def calculate_modified_law(self, time:float):
        # STD of dx
        std = np.std(self.selection_coordinates)
        # MEAN of ae
        mean = np.mean(self.movement_amplitudes)

        ID = np.log2((mean/(4.133*std)) + 1)
        MT = np.mean(self.times)

        return ID/MT
    

    def get_average_times(self):
        return np.mean(self.ballistic_times), np.mean(self.time_to_select)




