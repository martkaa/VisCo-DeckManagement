import numpy as np
import pandas as pd
import platform
import math as m

class Cargo:
    def __init__(self, ID, length, true_length, width, true_width, weight = 0, location = 0, hazards = False, risk = False, load_date = 0, load_off_date = 0, comment = '', description = ''):
        self.id = ID
        #self.length = m.ceil(length * 0.001)
        #self.width = m.ceil(width * 0.001)
        # for 0.5 units
        self.length = m.ceil(2.0 * (length * 0.001))
        self.width = m.ceil(2.0 * (width * 0.001))
        self.true_length = true_length
        self.true_width = true_width
        self.weight = weight
        self.location = location
        self.coor = {0, 0}
        self.area = self.length * self.width
        self.rotation = False
        self.hazards = hazards
        self.risk = risk
        self.load_date = load_date
        self.load_off_date = load_off_date
        self.comment = comment
        self.description = description

    def __repr__(self):
        return self.id

    
class LDA:
    def __init__(self, ID, measurements, location, deck, length, width, max_weight, hazards = False, risk = False):
        self.id = ID
        self.measurements = measurements
        self.location = location
        self.deck = deck
        self.length = length
        self.width = width
        self.max_weight = max_weight
        self.cargos = []
        self.takes_hazards = hazards
        self.takes_risk = risk
        self.space_available = np.sum(self.measurements)
        
    def __repr__(self):
        return self.id

class Location:
    def __init__(self, name):
        self.name = name
        self.LDAs = []
        self.cargos = []
        self.deck = ''
        self.backup = []
    
    def __repr__(self):
        return self.name

# load files of cargos
is_windows = any(platform.win32_ver())
if is_windows == True:
    # test
    #df = pd.read_excel(r'C:\Users\marte.aaberge\OneDrive - VisCO\code\test_cargo.xlsx')
    # 0.5 m
    #df_LDA = pd.read_excel(r'C:\Users\marte.aaberge\OneDrive - VisCO\code\Lda001-003_test_05m_units_2.xlsx')
    # 1 m
    #df = pd.read_excel(r'C:\Users\marte.aaberge\OneDrive - VisCO\code\LDAs_excel_test_4.xlsx')

    df = pd.read_excel(r'C:\Users\marte.aaberge\OneDrive - VisCO\code\cargos_altered_hazards_and_risk_3.xlsx')
    # 0.5 m
    df = pd.read_excel(r'C:\Users\marte.aaberge\OneDrive - VisCO\code\LDAs_05m_units.xlsx')
    # 1 m
    #df = pd.read_excel(r'C:\Users\marte.aaberge\OneDrive - VisCO\code\LDAs_excel_1m_unit.xlsx')
    

else:
    #test
    #df = pd.read_excel(r'/Users/marteaaberge/OneDrive - VisCO/code/test_cargo.xlsx')
    # 0.5 m
    #df_LDA = pd.read_excel(r'/Users/marteaaberge/OneDrive - VisCO/code/Lda001-003_test_05m_units_2.xlsx')
    # 1m
    #df_LDA = pd.read_excel(r'/Users/marteaaberge/OneDrive - VisCO/code/LDAs_excel_test_4.xlsx')

    df = pd.read_excel(r'/Users/marteaaberge/OneDrive - VisCO/code/cargos_altered_hazards_and_risk_3.xlsx')
    # 0.5 m
    df_LDA = pd.read_excel(r'/Users/marteaaberge/OneDrive - VisCO/code/LDAs_05m_units.xlsx')
    # 1 m
    #df_LDA = pd.read_excel(r'/Users/marteaaberge/OneDrive - VisCO/code/LDAs_excel_1m_unit.xlsx')

# Extract data from excel file and make valid cargo objects
# from dataFrame to dictionary

def extractCargoData(df):
    dict_from_df = df.to_dict(orient='index')

    list_of_cargos_obj = []
    list_of_cargos_names = []
    list_of_locations = []
    list_of_invalid_cargos = []
    for key in dict_from_df:
        cargo = dict_from_df[key] # dict of a single cargo's properties
        
        # Check if cargos are valid
        if type(cargo["Item ID "]) == str and type(cargo['Length (mm)']) != str and not np.isnan(cargo['Length (mm)']) and type(cargo['Width (mm)']) != str and type(cargo["Weight (Kg)"]) != str and not np.isnan(cargo['Weight (Kg)']) and type(cargo["Where item is to be located"]) ==  str:
            # Avoid several cargos with same name
            if cargo["Item ID "] not in list_of_cargos_names:
                carg_obj = Cargo(cargo["Item ID "], cargo['Length (mm)'], cargo['Length (mm)'], cargo['Width (mm)'], cargo['Width (mm)'] , cargo["Weight (Kg)"], cargo["Where item is to be located"], cargo["Hazards"], cargo["Risk"], cargo["Projected load Date"], cargo["Projected  off load Date"], cargo['Comments'], cargo['Discription of Item to be loaded'])
                list_of_cargos_obj.append(carg_obj)
                list_of_cargos_names.append(cargo["Item ID "])

            loc_obj = cargo["Where item is to be located"]
            if loc_obj not in list_of_locations:
                list_of_locations.append(loc_obj)
        else:
            list_of_invalid_cargos.append(cargo["Item ID "])
                
    # Make location objects
    list_of_loc_obj = []
    for loc in list_of_locations:
        list_of_loc_obj.append(Location(loc))
    print(len(list_of_loc_obj))
    return list_of_cargos_obj, list_of_invalid_cargos, list_of_loc_obj

# Extract LDA data from excel sheet, make valid LDAs
def extractLDAData(df):
    dict_from_df_LDA = df_LDA.to_dict(orient='index')

    list_of_LDA_obj = []
    for key in dict_from_df_LDA:
        lda = dict_from_df_LDA[key]

        temp_matrix = lda["Measurements"]
        to_matrix = np.fromstring(temp_matrix, dtype=int, sep=',')
        length, width = lda["Y"], lda["X"]
        to_matrix = to_matrix.reshape(length, width)
        lda_obj = LDA(lda["Item ID"], to_matrix, lda["Where"], lda["Deck"], lda["Y"], lda["X"], lda['Max weight'], lda["Hazards"], lda["Risk"])
        list_of_LDA_obj.append(lda_obj)

    return list_of_LDA_obj

# sorts list of cargos based on location with heaviest first
def sortCargos(list_of_cargos_obj): 
    sorted_by_area = sorted(cargos_list, key=lambda x: x.area, reverse=True)
    sorted_by_weight = sorted(list_of_cargos_obj, key=lambda x: x.weight, reverse=True)
    sorted_by_location = sorted(sorted_by_weight, key=lambda x: x.location)
    sorted_by_hazards = sorted(sorted_by_location, key=lambda x: x.hazards, reverse=True)
    sorted_by_hazards_and_risk = sorted(sorted_by_hazards, key=lambda x: x.risk, reverse=True)
    return list_of_cargos_obj, sorted_by_area, sorted_by_weight, sorted_by_location, sorted_by_hazards_and_risk

# should be sorted based on area
def sortLDA(LDA_list): 
    smallest_first = sorted(LDA_list, key=lambda x: x.space_available)
    biggest_first = sorted(LDA_list, key=lambda x: x.space_available, reverse=True)
    hazards_first = sorted(smallest_first, key=lambda x: x.takes_hazards, reverse=True)
    risk_and_hazards = sorted(hazards_first, key=lambda x: x.takes_risk, reverse=True)
    return LDA_list, smallest_first, biggest_first, risk_and_hazards




#MAIN
cargos_list, invalid_cargos, list_of_locations = extractCargoData(df)
LDA_list = extractLDAData(df_LDA)
print("There are ", len(cargos_list), "valid cargos in this dataset.")
print("There are ", len(invalid_cargos), "invalid cargos in this dataset.")

unsorted_cargos, sorted_by_area, sorted_by_weight , sorted_by_location, sorted_by_hazards_and_risk = sortCargos(cargos_list)
unsorted_LDAs, LDA_sorted_smallest, LDA_sorted_biggest,  LDA_risk_and_hazards  = sortLDA(LDA_list)
