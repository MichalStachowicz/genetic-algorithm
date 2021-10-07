import random
from ase import Atoms
from pyxtal import pyxtal
import numpy as np


from config import species, quantity, thickness


Vector = np.ndarray


def dist(v1: Vector, v2: Vector) -> float:
    """Returns distance two atoms

    Args:
        v1 (numpy.ndarray): First vector
        v2 (numpy.ndarray): Second vector

    Returns:
        float: Distance of two vectors
    """

    d = np.sqrt(
        (v1[0] - v2[0]) * (v1[0] - v2[0]) + (v1[1] - v2[1]) * (v1[1] - v2[1]) + (v1[2] - v2[2]) * (v1[2] - v2[2]))
    return d


def check_dist(number_atoms: int, positions: Vector, d_min: float, d_max: float) -> bool:
    """Restrict of the distance between atoms

    Args:
        number_atoms (int): Number of atoms
        positions (list[float]): Atom positions
        d_min (float): Minimum allowable distance
        d_max (float): Maximum allowable distance

    Returns:
        bool: Returns True if conditions are fulfilled anyway False
    """

    flag = True
    for i in range(number_atoms):
        for j in range(number_atoms):
            if i != j:
                distance = dist(positions[i], positions[j])
                if (distance < d_min) or (distance > d_max):
                    flag = False
    return flag


def init_struct() -> Atoms:
    """Initialization of the random structure

    Returns:
        ase.atoms.Atoms: Structure
    """

    atoms_out = None

    number_attempts = 2000  # no of attempts
    d_min = 1.0  # min distance
    d_max = 3.5  # max distance

    for i in range(number_attempts):
        group_id = random.randrange(80) + 1  # randrange(230) + 1
        my_crystal = pyxtal()

        try:
            my_crystal.from_random(2, group_id, species, quantity, thickness=thickness)
        except:
            continue

        atoms = my_crystal.to_ase()
        positions = atoms.get_positions()
        number_atoms = len(atoms.get_chemical_symbols())

        flag = check_dist(number_atoms, positions, d_min, d_max)

        if flag:
            atoms_out = atoms
            break
    return atoms_out
