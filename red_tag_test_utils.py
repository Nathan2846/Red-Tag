import red_tag
import red_tag_classes

def test_dict_list_match(employee_list, positions_dict, optional_positions_dict):
    for employee in employee_list:
        list_value = employee.get_pos() #The position of the meployee object
        if list_value.lower() == "break":
            continue
        try:
            dict_value = positions_dict[list_value][0] #The name of the employee at that dict key
        except:
            try: 
                dict_value = optional_positions_dict[list_value][0]
            except:
                print(list_value , " not found in either dict")
                return False
        
        if employee.get_name() != dict_value:
            print(employee, ' is out of compliance')
            return False
    return True
