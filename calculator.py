from ase.calculators.siesta import Siesta
from ase.units import Ry

from main import name

calc = Siesta(label=name,
              xc='PBE',
              mesh_cutoff=200 * Ry,
              energy_shift=0.01 * Ry,
              basis_set='SZP',
              kpts=[12, 12, 1],
              pseudo_path='/home/czeski/Pobrane/siesta-4.1-b4/pseudo',
              fdf_arguments={'MaxSCFIterations': 500,
                             'DM.Tolerance': 1.E-5,
                             'DM.NumberPulay': 6,
                             'DM.NumberBroyden': 0,
                             'DM.MixingWeight': 0.1000000000,
                             'DM.OccupancyTolerance': 0.1000000000E-11,
                             'DM.NumberKick': 0,
                             'DM.KickMixingWeight': 0.5000000000,
                             'MD.NumCGsteps': 150,
                             'MD.TypeOfRun': 'CG',
                             'MD.VariableCell': 'F',
                             'WriteMullikenPop': 1,
                             'WriteDenchar': True,
                             'WriteKpoints': True,
                             'WriteForces': True,
                             'WriteDM': True,
                             'WriteXML': True,
                             'WriteEigenvalues': False,
                             'WriteCoorStep': True,
                             'WriteMDhistory': True,
                             'WriteMDXmol': True,
                             'WriteCoorXmol': True,
                             })
