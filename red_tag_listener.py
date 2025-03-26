"""
This is a master listener for red_tag
It is designed to parse incoming messages from the server and handle them appropriately for this 
specific ride instance. 
This code is designed to be run as a seperate thread in the red_tag program
so that supervisors can directly interact with ride staffing
"""