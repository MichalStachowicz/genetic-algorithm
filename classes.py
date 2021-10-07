import random
from ase import Atoms
import numpy as np

from config import POP_SIZE, num_selected, n_atoms
from functions import init_struct, Vector
from calculator import calc


class Individual:
    def __init__(self, structure: Atoms, n_gen: int) -> None:
        """ Individual constructor

        Args:
            structure (ase.atoms.Atoms) : Atom
            n_gen (int) : Number of the generation
        """
        self.calc = calc
        self.init_structure = structure
        self.energy = 0.0
        self.ngen = n_gen
        self.status = 'Random'

    def next_gen(self) -> None:
        """
        Updates the generation number
        """
        self.ngen = self.ngen + 1

    def calc_energy(self) -> None:
        """
        Calculates the energy of the individual
        """
        try:
            self.init_structure.calc = calc
            self.energy = self.init_structure.get_potential_energy()
        except:
            print("energy calculation failed")
            self.energy = +1000.
        self.next_gen()

    def mutation(self) -> None:
        positions = self.init_structure.get_positions()
        new = [n + (random.random() - 0.5) for n in positions]
        self.init_structure.set_positions(new)
        self.status = 'Mutation'

    def get_init_structure(self) -> Atoms:
        """Returns the structure of the individual

        Returns:
            ase.atoms.Atoms: Structure of the individual
        """
        return self.init_structure.copy()

    def get_energy(self) -> float:
        """Returns the energy of the individual

        Returns:
            float: Energy of the structure
        """
        return self.energy

    def get_ngen(self) -> int:
        """Returns the generation number from which the individual came

        Returns:
            int: Generation number
        """
        return self.ngen

    def get_position(self) -> Vector:
        """Returns Atoms positions.

        Returns:
            numpy.ndarray: Vector of Atoms positions
        """
        return self.init_structure.get_positions()

    def get_status(self) -> str:
        """Returns where the individual came from

        Returns:
            str: Origin of the individual
        """
        return self.status

    def set_status(self, status) -> None:
        """
        Sets new individual status
        """
        self.status = status

    def to_db(self):
        """
        Returns the energy, number of generation and status of the individual
        """
        return self.energy, self.ngen, self.status


class Population:
    def __init__(self) -> None:
        self.population_size = POP_SIZE
        self.individuals = []
        self.n_selected = num_selected

    def add_individual(self, individual: Atoms) -> None:
        """Adds a new individual to the population provided it is not full

        Args:
            individual (ase.atoms.Atoms): Structure
        """
        if len(self.individuals) < self.population_size:
            self.individuals.append(individual)

    def fill_up(self, n_gen: int) -> None:
        """ Fills the population with new individuals until it is full

        Returns:
            Sorted population of individuals
        """

        while len(self.individuals) < self.population_size:
            self.individuals.append(Individual(init_struct(), n_gen))

    def purge(self) -> None:
        """
        Removes the worst individuals.
        """
        self.individuals = self.individuals[:self.n_selected]

    def energy_calculator(self) -> None:
        """
        Calculates the energies of each individual in the population, then sorts them and displays.
        """
        for individual in self.individuals:
            individual.calc_energy()
        self.individuals = sorted(self.individuals, key=lambda x: x.energy)

        # Printing sorted energy
        for individual in self.individuals:
            print(individual.get_energy())

    def choice_by_roulette(self) -> Atoms:
        """ Choice the Individual using Choice by the roulette.

        Returns:
            Chosen individual
        """

        individuals = self.individuals

        individuals = individuals[1:]  # Delete the best individual because it's untouchable

        # Totally population fitness
        population_sum = sum([individual.get_energy() for individual in individuals])

        # Each individual probability
        individuals_prob = [individual.get_energy() / population_sum for individual in individuals]

        n = np.arange(0, len(individuals))
        chosen_num = np.random.choice(n, p=individuals_prob)

        return individuals[chosen_num]

    def crossover(self) -> None:
        """
        Takes two random structures and swaps their random atom positions
        """
        while True:

            # Draw 2 individuals
            rand_ind1 = random.randint(1, POP_SIZE - 1)
            rand_ind2 = random.randint(1, POP_SIZE - 1)

            if rand_ind1 == rand_ind2:
                continue
            # Draw atom to swap
            rand_atom1 = random.randint(0, n_atoms - 1)
            rand_atom2 = random.randint(0, n_atoms - 1)

            # Swap atoms positions
            temp = self.individuals[rand_ind1].get_init_structure()[rand_atom1].position
            self.individuals[rand_ind1].get_init_structure()[rand_atom1].position = self.individuals[rand_ind2].get_init_structure()[rand_atom2].position
            self.individuals[rand_ind2].get_init_structure()[rand_atom2].position = temp

            # Set status of individual as Crossover
            self.individuals[rand_ind1].set_status("Crossover")
            self.individuals[rand_ind2].set_status("Crossover")
            break

