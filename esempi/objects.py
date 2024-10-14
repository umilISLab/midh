import numpy as np


class Animal:
    def __init__(self, name):
        self.name = name 
        self.energy = 0
        self.history = []
    
    def eat(self, food: int):
        self.energy += food 
        self.history.append(self.energy)
    
    def consume(self, energy: int):
        self.energy -= energy
        self.history.append(self.energy)
    
    def get_history(self):
        return self.history


class Predators(Animal):
    
    def hunt(self, food: Animal):
        if np.random.uniform() <= 0.4:
            self.eat(food.energy)
            food.energy = 0
        else:
            pass 
        
    