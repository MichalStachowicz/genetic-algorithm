from classes import *
from datetime import datetime

from database import insert_to_db
from config import name, NUMBER_GENERATIONS, num_mutated


start_time = datetime.now()

if __name__ == '__main__':
    pop = Population()
    best = []
    data = []
    print(f"Energy of structures {name} in the starting population:")
    pop.fill_up(0)
    pop.energy_calculator()
    data.append(pop.individuals)

    # Write population to db
    for individual in pop.individuals:
        temp_energy, temp_ngen, temp_status = individual.to_db()
        insert_to_db(temp_energy, temp_ngen, temp_status)

    for g in range(NUMBER_GENERATIONS):
        print(f"Energy of structures {name} in generation nr {g + 1}/{NUMBER_GENERATIONS}:")
        pop.purge()
        pop.fill_up(g + 1)

        for _ in range(num_mutated):
            pop.choice_by_roulette().mutation()
        pop.crossover()
        pop.energy_calculator()

        for individual in pop.individuals:
            temp_energy, temp_ngen, temp_status = individual.to_db()
            insert_to_db(temp_energy, temp_ngen, temp_status)

        best.append(pop.individuals[0].get_energy())

    print('Duration: {}'.format(datetime.now() - start_time))
