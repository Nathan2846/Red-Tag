"""
This is red_tag_classes. It provides the necessary classes to run the red_tag module, including 
Time, Employee, and Ride
"""
class Time:
    __slots__ = ['__hours','__minutes']
    def __init__(self, hours, minutes):
        self.__hours = hours
        self.__minutes = minutes
    def __str__(self):
        a_string = str(self.__hours) + ':' + str(self.__minutes)
        if self.__minutes == 0:
            a_string += '0'
        return a_string
    def time_to_seconds(self):
        """
        This will take a time and convert it to seconds for the purpose of doing math
        """
        seconds = (int(self.__hours) *3600) + (int(self.__minutes) * 60)
        return seconds
    def seconds_to_time(self, seconds):
        """
        This will take a time in seconds and return it to hours and minutes for reading purposes
        """
        hours = int (seconds/3600)
        remainder = seconds % 3600
        minutes = int (remainder/60)
        return hours, minutes
        
    def add(self, other):
        """
        This will return a new time object that is a result of the addition of parameters
        """
        sec_self = self.time_to_seconds()
        sec_other = other.time_to_seconds()

        result = sec_self + sec_other
        hours, minutes= self.seconds_to_time(result)

        return Time(hours, minutes)
    def subtract(self, other):
        """
        This will return a new time object that is a result of the subtraction of self - other
        """
        sec_self = self.time_to_seconds()
        sec_other = other.time_to_seconds()
        result = int(sec_self) - sec_other
        hours, minutes= self.seconds_to_time(result)

        return Time(hours, minutes)
    def __gt__(self, other):
        if self.__hours > other.__hours:
            return True
        elif self.__hours == other.__hours and self.__minutes > other.__minutes:
            return True
        return False
    def __lt__(self, other):
        if self.__hours < other.__hours:
            return True
        elif self.__hours == other.__hours and self.__minutes < other.__minutes:
            return True
        return False
    def __eq__(self, other):
        return self.__minutes == other.__minutes and self.__hours == other.__hours 
    
    def __hash__(self):
        return self.__minutes * self.__hours

class Employee:
    __slots__ = ['__name','__age','__shift_start','__shift_end','__break_status', '__break_window', '__pos', '__break_end', '__untrained_positions', '__is_lead']
    def __init__(self, name, age, start, end, is_lead):
        self.__name = name
        self.__age = age
        self.__shift_start = start
        self.__shift_end = end
        self.__break_status = False
        self.__break_window = []
        self.__pos = None
        self.__break_end = None
        self.__is_lead = is_lead # Make sure this is boolean when you pass it in

        #We will now compute the break window. It begins 5 hours from end of shift 
        #and ends 4.5 hours after start of shift. 18+ has window 1 hour from start and end
        #If the shift is less than 5 hours in duration, no break is required
        if Time.subtract(self.__shift_end, self.__shift_start) < Time(5,0):
            self.__break_window = [Time(0,0), Time(0,0)]
            self.__break_status = True
        if int(age)>=18:
            self.__break_window.append(Time.add(Time(1,30), self.__shift_start)) #Break begins 1.5 hours after start
            self.__break_window.append(Time.subtract(self.__shift_end, Time(1,30))) #Break ends 1.5 hours before end
            
        else:
            self.__break_window.append(Time.subtract(self.__shift_end, Time(5,0)))
            self.__break_window.append(Time.add(Time(4,30), self.__shift_start))
            
    def __repr__(self):
        result = "Here is the information for " + self.__name + "\n"
        result += "Age: " + str(self.__age) + "\nShift time: " + str(self.__shift_start) + "-"  + str(self.__shift_end) +"\n"
        if self.__break_status :
            print('end' , self.__break_end)
            result += "Break ended at: " + str(self.__break_end) + '\n'
        elif self.__break_status:
            result += "The lead does not take a break with everyone else\n"
        else:
            result += self.__name + " has not gone on break yet \n" + "Break window: " + str(self.__break_window[0]) + '-' + str(self.__break_window[1]) + '\n'
        
        try:
            result += "Current position: " + self.__pos + '\n'
        except TypeError:
            # Positions not set
            result += "Current position : Unset"
        return result

    def __str__(self):
        a_string = self.__name + ':' + str(self.__pos) + ':' + self.__age + ':' + str(self.__break_status)
        return a_string
    def set_pos(self,position):
        self.__pos = position
    def get_pos(self):
        return self.__pos
    def get_break_window(self):
        return self.__break_window
    def get_name(self):
        return self.__name
    def get_age(self):
        return self.__age
    def get_break_status(self):
        return self.__break_status
    def set_break_status(self, value):
        self.__break_status = value
    def get_shift_end(self):
        return self.__shift_end
    def set_break_end(self, value):
        self.__break_end = value
    def get_break_end(self):
        return self.__break_end
    def get_shift_start(self):
        return self.__shift_start
    def set_untrained_positions(self, value):
        self.__untrained_positions = value
    def get_untrained_positions(self):
        return self.__untrained_positions
    def get_lead(self):
        return self.__is_lead
    def train_on_position(self, position):
        while position.lower() in self.__untrained_positions:
            self.__untrained_positions.remove(position.lower())
    

class Ride:
    """
    This is the ride class. It will contain field for positions, whcih will have a dict. with each position 
    mapped to a list of [current employee, lead permitted status, clerk permitted status]
    """
    __slots__ = ['__name','__mins','__pos_dict', '__optional_pos_dict', '__current_time', '__employees', '__break_order', '__position_availability']
    def __init__(self, name, mins):
        self.__name = name
        self.__mins = mins
        self.__pos_dict = {}
        self.__optional_pos_dict = {}
        self.__current_time = None

    def add_pos(self, name=None, lead_status=None, clerk_status=None, mandatory=True):
        if name == None or lead_status ==None or clerk_status == None:
            # One or more pieces of info are missing
            name = input ('Please enter the name of the position')
            clerk_status = ''
            while clerk_status.lower() != 'y' and clerk_status.lower() != 'n':
                clerk_status = input('Can a clerk occupy this position? Please enter Y or N')
            if clerk_status == 'y' or clerk_status == 'Y':
                clerk_status = True
            else:
                clerk_status = False
            
            lead_status = ''
            while lead_status.lower() != 'n' and lead_status.lower() != 'y':
                lead_status = input('Can a lead occupy this position? Please enter Y or N')
            if lead_status == 'y' or clerk_status == 'Y':
                lead_status = True
            else:
                lead_status = False
            
            mandatory = None
            while mandatory == None:
                mandatory = (input('Is this position mandatory? Enter Y or N:')).lower()
                if mandatory == 'y':
                    mandatory = True
                elif mandatory == 'n':
                    mandatory = False
        # All data has now either been collected or was part of the function call
        if mandatory:
            self.__pos_dict[name] = [None, lead_status, clerk_status]
        else:
            self.__optional_pos_dict[name] == [None, lead_status, clerk_status]

        return name


    def remove_pos(self,name):
        if name in self.__pos_dict:
            self.__pos_dict.pop(name)
        elif name in self.__opt_pos_dict:
            self.__opt_pos_dict.pop(name)
        else:
            print ('Position not found-please try again')
    def get_pos_dict(self):
        return self.__pos_dict
    def get_optional_pos_dict(self):
        return self.__optional_pos_dict
    def __str__(self):
        a_string = 'Name: ' + self.__name + ' mins: ' + str(self.__mins)
        return a_string
    def get_name(self):
        return self.__name
    def get_mins(self):
        return self.__mins
    def set_current_time(self, time):
        self.__current_time = time
    def get_current_time(self):
        return self.__current_time
    
    def set_employee_list(self, employees):
        self.__employees = employees

    def get_employee_list(self):
        return self.__employees
    
    def get_position_availability(self):
        return self.__position_availability
    
    def set_pos_dict(self, pos_dict):
        self.__pos_dict = pos_dict
    
    def set_optional_pos_dict(self, opt_pos_dict):
        self.__optional_pos_dict = opt_pos_dict

    def set_break_order (self, break_list):
        self.__break_order = break_list

    """
    This function returns a list of all the breaks that need completed in order
    """
    def make_break_list(self):
        duplicate = self.__employees.copy() #Create a duplicate of the employee list to work with
        return_list = []
        for _ in range(len(self._employees)):
            max_time = Time(24,00) #A maximum time value
            current_lowest_employee = 1 #This variable will hold the employee object with the first brak time
            lowest_index = 0 #This will be the index of the lowest employee
            for i in range(len(duplicate)):
                potential_employee = duplicate[i] #The current employee
                current_break_start = potential_employee.get_break_window()[0]
                if current_break_start < max_time and current_break_start != Time(0,0) and not potential_employee.get_break_status(): #HEY: The break dstatus bit of this logic may need work. It is meant to skip people who have already been onb break
                    #They need a break, and it is earlier than any other found thus far. Set all variables
                    max_time = current_break_start
                    current_lowest_employee = potential_employee
                    lowest_index = i
            if current_lowest_employee.get_name().lower() == 'lead': #TODO: Deasl with leads
                duplicate.pop(lowest_index) #Remove the lead, we don't need to deal with them
                continue #Continue on without adding them to the return_list
            return_list.append(current_lowest_employee) #Add the employee onto the end of the list
            if (len(duplicate))!= 0 :
                #Remove the employee from the duplicate
                duplicate.pop(lowest_index)

        self.__break_order = return_list
    
    #The following functions are used to manually create test data
    def add_to_dict(self,key, value):
        self.__pos_dict[key] = value
    def add_to_opt_dict(self, key, value):
        self.__optional_pos_dict[key] = value
    
    def calculate_position_availability(self):
    #Begin by getting all positions in one list
        all_positions = list(self.__pos_dict.keys()) + list(self.__optional_pos_dict.keys())

        position_availability = {}
        # Determine List of employees for each positions. Create a dictionary where the key is the position
        # and the value is the list of employees that can do it

        for position in all_positions:
            position_availability[position.lower()] = []
            for employee in self.__employees:
                if position.lower() not in employee.get_untrained_positions():
                    position_availability[position.lower()].append(employee.get_name())

        
        self.__position_availability = position_availability

"""
Tests for the time module
a = Time(3,0)
b = Time(4,30)
print (Time.add(a,b))
print(Time.subtract(b,a))

test_18 = Employee('Nineteen',19,Time(11,0), Time(3,0))
print(repr (test_18))
print (test_18)

### add minor labor laws, add getters as needed.
"""