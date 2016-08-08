import os

class Mating:
    def __init__(self, func_data, num_matings):
        self.func_data = func_data
        self.num_matings = num_matings
        self.n_calls = 0
        self.name = "mating_{0}_topology_{1}_offspring_{2}.mol"
    def __call__(self, population):       
        parent_pool = population.select('mating')
        offspring_pop = Population(population.ga_tools)
        func = getattr(self, self.func_data.name)
        
        num_matings = 0
        for parents in parent_pool:         
            try:
                self.n_calls += 1
                offspring = func(*parents, **self.func_data.params)
                offspring_pop.add_members(offspring)
                num_matings += 1
                print('Mating number {0}. Finish when {1}.'.format(
                                num_matings, self.num_matings))
                if num_matings == self.num_matings:
                    break
            except:
                continue

        offspring_pop -= population
        return offspring_pop

    """
    The following mating operations apply to ``Cage`` instances    
    
    """

    def bb_lk_exchange(self, cage1, cage2):
        build_block1 = cage1.building_blocks[0]
        counterpart1 = next(x for x in cage2.building_blocks if 
                            type(build_block1) != type(x))
        build_block2 = cage1.building_blocks[1]
        counterpart2 = next(x for x in cage2.building_blocks if 
                            type(build_block2) != type(x))
        
        topologies = {type(x.topology) for x in (cage1, cage2)}

        offspring_pop = Population()
        for index, topology in enumerate(topologies):
                        
            offspring1 = Cage((build_block1, counterpart1), topology, 
                              os.path.join(os.getcwd(),
                              self.name.format(self.n_calls, index, 1)))
                              
            offspring2 = Cage((build_block2, counterpart2), topology,
                              os.path.join(os.getcwd(),
                              self.name.format(self.n_calls, index, 2)))
            offspring_pop.add_members((offspring1, offspring2))
            
        return offspring_pop
        
        
from ..population import Population
from ..molecular import BuildingBlock, Linker, Cage, Polymer