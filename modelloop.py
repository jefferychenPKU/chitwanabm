"""
Part of Chitwan Valley agent-based model.

Contains main model loop: Contains the main loop for the model. Takes input 
parameters read from runModel.py, and passes results of model run back.

Alex Zvoleff, azvoleff@mail.sdsu.edu
"""

import time
import copy

import numpy as np

from chitwanABM import rcParams

if rcParams['model.use_psyco'] == True:
    import psyco
    psyco.full()

timezero = rcParams['model.timezero']
endtime = rcParams['model.endtime']
timestep = rcParams['model.timestep']
timesteps = np.arange(timezero, endtime, timestep)

def main_loop(region):
    """This function contains the main model loop. Passed to it is a list of 
    regions, which contains the person, household, and neighborhood agents to 
    be used in the model, and the land-use parameters."""

    # saved_data will store the results of each timestep.
    saved_data = []
    
    # Save the starting time of the model to use in printing elapsed time while 
    # it runs.
    modelrun_starttime = time.time()
    print "\n******************************************************************************"
    print "Model run starttime:", time.strftime("%I:%M:%S %p")

    for t in timesteps:
        print "\ttimestep: ", str(t)

        # This could easily be written to handle multiple regions, although 
        # currently there is only one, for all of Chitwan.
        region.births(t)
        region.deaths(t)
        region.migration(t)
        #region.marriages(t)
        #region.update_landuse(t)

        region.increment_age()
            
        saved_data.append(copy.deepcopy(region))
        
        num_persons = region.census()
        print "\tNumber of person agents:", str(num_persons)
        print "Elapsed time: ", elapsed_time(modelrun_starttime)

    print "Finished model run. Total elapsed time: ", elapsed_time(modelrun_starttime)

    return saved_data

def elapsed_time(start_time):
    elapsed = int(time.time() - start_time)
    hours = elapsed / 3600
    minutes = (elapsed - hours * 3600) / 60
    seconds = elapsed - hours * 3600 - minutes * 60
    return "%ih %im %is" %(hours, minutes, seconds)
