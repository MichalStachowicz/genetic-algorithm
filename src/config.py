"""
    STRUCTURE
"""
name = 'C2'
# Chemical species of the structure
species = ['C']
# Quantity of chemical species in elemental cell
quantity = [2]
# Number of atoms in cell
n_atoms = sum(quantity)
# Thickness of the structure
thickness = 5

"""
    POPULATION
"""
# Number of structures in population
POP_SIZE = 4
# Number of generations
NUMBER_GENERATIONS = 3

"""
    NATURAL SELECTION
"""
# Percentage of best individuals passing to the next generation
prob = 0.5
# Number of individual's passing to next generation
num_selected = int(prob*POP_SIZE)
# Percentage of individuals in which the mutation occurs
prob = 0.2
# Number of individuals to mutation
num_mutated = int(prob*num_selected)