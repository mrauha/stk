import os
import numpy as np

class Mutation:
    """
    Carries out mutations operations on a population.

    Instances of the ``Population`` class delegate mating operations to
    instances of this class. They do this by calling:
        
        >>> mutant_pop = pop.gen_mutants()
        
    which returns a new population consisting of molecules generated by
    performing mutation operations on members of ``pop``. This class
    invokes an instance of the ``Selection`` class to select molecules 
    for mutations. Both an instance of this class and the ``Selection``
    class are held in the `ga_tools` attribute of a ``Population`` 
    instance.
    
    This class is initialized with a ``FunctionData`` instance. The 
    object holds the name of the mutation function to be used by the
    population as well as any additional parameters the function may 
    require. Mutation functions should be defined as methods within this
    class.
    
    Members of this class are also initialized with an integer which
    holds the number of mutation operations to be performed each
    generation.
    
    Attributes
    ----------
    func_data : FunctionData
        The ``FunctionData`` object holding the name of the function
        chosen for mutation and any additional paramters and 
        corresponding values the function may require.
    
    num_mutations : int
        The number of mutations thats need to be performed each
        generation.
    
    n_calls : int
        The total number of times an instance of ``Mutation`` has been
        called during its lifetime.
    
    name : str
        A template string for naming ``MacroMolecule`` instances 
        produced during mutation.    
    
    """
    
    def __init__(self, func_data, num_mutations):
        self.func_data = func_data
        self.num_mutations = num_mutations
        self.n_calls = 0
        self.name = "mutation_{0}.mol"
    
    def __call__(self, population):
        """
        Carries out mutation operations on the supplied population.
        
        This function initially selects members of the population to
        be mutated. These are then mutated. This goes on until
        either all possible molecules have been mutated or the required
        number of successful mutation operations have been performed.
        
        The mutants generated are returned together in a ``Population`` 
        instance. Any molecules that are created as a result of mutation 
        that match a molecule present in the original population are 
        removed.

        Parameters
        ----------
        population : Population
            The population who's members are to be mutated.
            
        Returns
        -------
        Population
            A population with all the mutants generated held in the
            `members` attribute. This does not include mutants which
            correspond to molecules already present in `population`.            

        """
        
        parent_pool = population.select('mutation')
        mutant_pop = Population(population.ga_tools)
        func = getattr(self, self.func_data.name)
        
        num_mutations = 0
        for parent in parent_pool:
            try:
                self.n_calls += 1
                mutant = func(parent, **self.func_data.params)
                mutant_pop.members.append(mutant)
                num_mutations += 1
                print('Mutation number {0}. Finish when {1}.'.format(
                                num_mutations, self.num_mutations))
                if num_mutations == self.num_mutations:
                    break

            except:
                continue

        mutant_pop -= population
            
        return mutant_pop


    def random_bb(self, cage, database):
        """
        Substitutes a building-block* with a random one from a database.
        
        Parameters
        ----------
        cage : Cage
            The cage who's building-block* will be exchanged. Note that
            the cage is not destroyed. It is used a template for a new
            cage.
            
        database : str
            The full path of the database from which a new 
            building-block* is to be found.
            
        Returns
        -------
        Cage
            A cage instance generated by taking all attributes of `cage`
            except its building-block* which is replaced by a random 
            building-block* from `database`.
        
        """
        
        bb_file = np.random.choice(os.listdir(database))
        bb_file = os.path.join(database, bb_file)
        bb = BuildingBlock(bb_file)
        lk = next(x for x in cage.building_blocks if 
                                                isinstance(x, Linker))        
        return Cage((bb, lk), type(cage.topology), 
                    cage.optimize.func_name,
            os.path.join(os.getcwd(), self.name.format(self.n_calls)))
        
from ..population import Population
from ..molecular import BuildingBlock, Linker, Cage, Polymer