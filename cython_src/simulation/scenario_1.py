# from house.loads import *
# from house.battery import *
# from house.house import *
# from simulation.simulation import *
#
#
# # Continuous loads
# fridge = ContinuousLoad(power_consumption=90)
# freezer = ContinuousLoad(power_consumption=90)
# heating = ContinuousLoad(power_consumption=2400)
#
# # Timed loads
# television = TimedLoad(60, time(19), 10800, pd.DateOffset())
# computer = TimedLoad(800, time(20), 3600, pd.DateOffset())
# cooker = TimedLoad(4000, time(19), 2700, pd.DateOffset())
# hood = TimedLoad(150, time(19), 2700, pd.DateOffset())
#
#
# # Staggered loads
# washing_machine1 = StaggeredLoad(power_consumption=1000,
#                                  original_start_time=None,
#                                  cycle_duration=)
# washing_machine2 = StaggeredLoad(power_consumption=1000,
#                                  original_start_time=None,
#                                  cycle_duration=,)
# tumble_drier = StaggeredLoad(power_consumption=2600,
#                              original_start_time=None,
#                              cycle_duration=,
#                              constraints=[{'type': 'ineq',
#                                            'fun': lambda _: tumble_drier.start_time - (washing_machine1.start_time + washing_machine1.cycle_duration)},
#                                           {'type': 'ineq',
#                                            'fun': lambda _: 86400 - (tumble_drier.start_time + tumble_drier.cycle_duration)}])
# dish_washer = StaggeredLoad(power_consumption=900,
#                             original_start_time=None,
#                             cycle_duration=)
#
