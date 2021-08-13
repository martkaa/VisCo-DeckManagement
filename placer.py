import numpy as np
import math as m
import xlsxwriter as xls
import matplotlib.pyplot as plt
import dataHand as data
import copy

def placeCargosSingleLDA(cargos, LDA):
    
    j = len(LDA.cargos) + 2
    
    for cargo in cargos:

        if (cargo.hazards and LDA.takes_hazards or not cargo.hazards and LDA.takes_hazards or not cargo.hazards and not LDA.takes_hazards) and (cargo.risk and LDA.takes_risk or not cargo.risk and LDA.takes_risk or not cargo.risk and not LDA.takes_risk):        
        
            # check if area and weight available
            if LDA.space_available >= cargo.area  and not LDA.space_available == 0 and LDA.max_weight >= cargo.weight :

                # check if space available, set index of location
               for index, x in np.ndenumerate(LDA.measurements):
                    if x == 1:
                        x_cor, y_cor = index[1], index[0]

                        # check if entire cargo will fit 
                        length, width = cargo.length, cargo.width
                        end_x, end_y = x_cor + width, y_cor + length
                        end_x_space, end_y_space = end_x + 2, end_y + 2 # add space between cargos
                        
                        if end_x <= LDA.width and end_y <= LDA.length and np.all(LDA.measurements[y_cor:end_y,x_cor:end_x] == 1):
                        # space on shortest side
                            #if cargo.length < cargo.width:
                             #   if np.all(LDA.measurements[y_cor:end_y,x_cor:end_x_space] == 1):
                               #     LDA.measurements[y_cor:end_y,end_x:end_x_space] = -1

                           # elif width < length:
                            #    if np.all(LDA.measurements[y_cor:end_y_space,x_cor:end_x] == 1):
                             #       LDA.measurements[end_y:end_y_space,x_cor:end_x] = -2

                            #elif width == length:
                        # space on two sides
                            if np.all(LDA.measurements[y_cor:end_y_space,x_cor:end_x_space] == 1):
                                LDA.measurements[y_cor:end_y_space,x_cor:end_x_space] = -2

                                LDA.measurements[y_cor:end_y,x_cor:end_x] = j

                                j += 1  
                                cargo.coor = index
                                LDA.space_available -= cargo.area
                                LDA.max_weight -= cargo.weight
                                LDA.cargos.append(cargo)
                                cargos.remove(cargo)
                                break

                        else:
                            # try rotationg
                            temp = length
                            length = width
                            width = temp
                            
                            
                            end_x, end_y = x_cor + width , y_cor + length
                            end_x_space, end_y_space = end_x + 2, end_y + 2
                            
                            if end_x <= LDA.width and end_y <= LDA.length and np.all(LDA.measurements[y_cor:end_y,x_cor:end_x] == 1):
                            #space på kortside
                                #if length < width:
                                 #   if np.all(LDA.measurements[y_cor:end_y,x_cor:end_x_space] == 1):
                                  #      LDA.measurements[y_cor:end_y,end_x:end_x_space] = -1
                                #elif width < length:
                                #    if np.all(LDA.measurements[y_cor:end_y_space,x_cor:end_x] == 1):
                                 #       LDA.measurements[end_y:end_y_space,x_cor:end_x] = -2
                                #elif width == length:
                                if np.all(LDA.measurements[y_cor:end_y_space,x_cor:end_x_space] == 1):
                                    LDA.measurements[y_cor:end_y_space,x_cor:end_x_space] = -2
                                
                                    LDA.measurements[y_cor:end_y,x_cor:end_x] = j
                                    cargo.rotation = True
                                    j += 1
                                    cargo.coor = index
                                    LDA.space_available -= cargo.area
                                    LDA.max_weight -= cargo.weight
                                    LDA.cargos.append(cargo)
                                    cargos.remove(cargo)
                            
                                break
    return cargos, LDA

# placing list of cargos to list of LDAs 
def placeCargosManyLDAs(cargos_list, LDA_list):
    placed_LDAs = []
    rest_cargos = []
    for LDA in LDA_list:
        rest_cargos, LDA = placeCargosSingleLDA(cargos_list, LDA)   
        placed_LDAs.append(LDA)
    return placed_LDAs, rest_cargos

# Locations
# placing list of cargos to list of LDAS with locations in consideration
def placeCargosByLocation(location_list, cargos_list, LDA_list):
    rest = []
    for location in location_list:
        for LDA in LDA_list:
            if LDA.location == location.name:
                location.LDAs.append(LDA)
                location.deck = LDA.deck

        cargs_in_location = []
        space, weight = 0, 0
        for carg in cargos_list:
            if carg.location == location.name:
                cargs_in_location.append(carg)
                space += carg.area
                weight += carg.weight
        location.LDAs, temp = placeCargosManyLDAs(cargs_in_location, location.LDAs)
        for i in temp:
            rest.append(i)
            
    for location in location_list:
        location.LDAs, temp = placeCargosManyLDAs(rest, location.LDAs)

    return location_list, rest
        
# write to file:

def writeToFile(placed_cargos_list):
    LDA_id = "LDA001"
    workbook = xls.Workbook('deckManagement.xlsx')
    worksheet = workbook.add_worksheet()
    
    # Start from the first cell.
    # Rows and columns are zero indexed.
    row = 0
    col = 0
    
    # iterating through content list
    worksheet.write(row, col, LDA_id)
    for item in placed_cargos_list :
    
        # write operation perform
        worksheet.write(row, col, LDA_id)
        worksheet.write(row, col + 1, item.id)
        coordinates = ','.join([str(coor) for coor in item.coor])
        #worksheet.write(row, col + 2, coordinates)
        worksheet.write(row, col + 3, item.rotation)
    
        # incrementing the value of row by one with each iteratons.
        row += 1
        
    workbook.close()

def writeALLToFile(LDA_list):
    workbook = xls.Workbook('deckManagement_test_6_05.xlsx')
    worksheet = workbook.add_worksheet()
    workbook.set_properties({
    'title':    'LDA, Cargo ID, coordinates, rotation, length, width, weight'})
    
    # Start from the first cell.
    # Rows and columns are zero indexed.
    row = 0
    col = 0
    for LDA in LDA_list:
        placed_cargos = LDA.cargos
    # iterating through content list
    #worksheet.write(row, col, LDA_id)
        for item in placed_cargos :
    
            # write operation perform
            worksheet.write(row, col, LDA.id)
            worksheet.write(row, col + 1, item.id)
            coordinates = ','.join([str(coor) for coor in item.coor])
            worksheet.write(row, col + 2, coordinates)
            worksheet.write(row, col + 3, item.rotation)
            worksheet.write(row, col + 4, item.length)
            worksheet.write(row, col + 5, item.width)
            worksheet.write(row, col + 6, item.weight)
        
            # incrementing the value of row by one with each iteratons.
            row += 1
        
    workbook.close()

def writeLocationsToFile(locations_list):
    workbook = xls.Workbook('deckManagement_placement_file.xlsx')
    #workbook = xls.Workbook('fase3.xlsx')
    worksheet = workbook.add_worksheet()
    
    row = 0
    col = 0
    format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
    format3 = workbook.add_format({'num_format': 'mm/dd/yy'})
    format4 = workbook.add_format({'num_format': 'd-m-yyyy'})
    format5 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm'})
    format6 = workbook.add_format({'num_format': 'd mmm yyyy'})
    format7 = workbook.add_format({'num_format': 'mmm d yyyy hh:mm AM/PM'})

    first_row_format = workbook.add_format({'bold': True, 'bg_color':'yellow','align':'center', 'valign':'vcenter'})
    align_format = workbook.add_format({'align':'center', 'valign':'vcenter'})

    worksheet.write(row, col, "Location")
    worksheet.write_comment(row, col, "Name of Location on platform.")
    worksheet.write(row, col + 1, "LDA ID")
    worksheet.write_comment(row, col + 1, "ID of LDA.")
    worksheet.write(row, col + 2, "Item ID")
    worksheet.write_comment(row, col + 2, "ID of Cargo.")
    worksheet.write(row, col + 3, "Coordinates")
    worksheet.write_comment(row, col + 3, "Coordinates (X,Y) of upper left corner of cargo. X is horizontal, Y i vertical.")
    worksheet.write(row, col + 4, "Rotation")
    worksheet.write_comment(row, col + 4, "True if it's rotated relative to standard orientaton.")
    worksheet.write(row, col + 5, "Length (mm)")
    worksheet.write_comment(row, col + 5, "Length (vertical) measures of cargo (mm).")
    worksheet.write(row, col + 6, "Width (mm)")
    worksheet.write_comment(row, col + 6, "Width (horizontal) measures of cargo (mm).")
    worksheet.write(row, col + 7, "Weight (kg)")
    worksheet.write_comment(row, col + 7, "Cargo weight (kg).")
    worksheet.write(row, col + 8, "Load date")
    worksheet.write_comment(row, col + 8, "Planned Load date of cargo to LDA.")
    worksheet.write(row, col + 9, "Load off date")
    worksheet.write_comment(row, col + 9, "Planned dispatch of cargo.")
    worksheet.write(row, col + 10, "Comments")
    worksheet.write_comment(row, col + 10, "Comments from original data sheet.")
    worksheet.write(row, col + 11, "Description")
    worksheet.write_comment(row, col + 11, "Description from original data sheet.")
    

    worksheet.set_column(1,9,15,align_format)
    worksheet.set_row(0,25,first_row_format)
    worksheet.set_column(0,0,20)
    worksheet.set_column(10,12,40)
   
    
    for location in locations_list:
        for LDA in location.LDAs:
            placed_cargos = LDA.cargos
        # iterating through content list
        #worksheet.write(row, col, LDA_id)
            for item in placed_cargos :
                try:
                    worksheet.write(row + 1, col, location.name)
                    worksheet.write(row + 1, col + 1, LDA.id)
                    worksheet.write(row + 1, col + 2, item.id)
                    #coordinates = ','.join([str(coor) for coor in item.coor])
                    coordinates = ','.join([str(coor/2) for coor in item.coor])
                    worksheet.write(row + 1, col + 3, coordinates)
                    worksheet.write(row + 1, col + 4, item.rotation)
                    worksheet.write(row + 1, col + 5, item.true_length) 
                    worksheet.write(row + 1, col + 6, item.true_width)
                    worksheet.write(row + 1, col + 7, item.weight)
                    worksheet.write(row + 1, col + 8, item.load_date, format3)
                    worksheet.write(row + 1, col + 9, item.load_off_date, format3)
                    worksheet.write(row + 1, col + 10, item.comment)
                    worksheet.write(row + 1, col + 11, item.description)
                    
                except:
                    pass
                # incrementing the value of row by one with each iteratons.
                row += 1
    worksheet.freeze_panes(1, 0)
    workbook.close()

#cargos_sorted_location, cargos_sorted_weight, cargos_sorted_area, sorted_by_hazards_and_risk = data.sortCargos(data.cargos_list)

def writephase4_and_5(locations_list):
    workbook = xls.Workbook('result_phase_4_5.xlsx')
    #workbook = xls.Workbook('fase3.xlsx')
    worksheet = workbook.add_worksheet()
    
    row = 0
    col = 0

    first_row_format = workbook.add_format({'bold': True, 'bg_color':'yellow','align':'center', 'valign':'vcenter'})
    align_format = workbook.add_format({'align':'center', 'valign':'vcenter'})
    #left_format = workbook.add_format({'align':'left', 'valign':'vleft'})

    worksheet.write(row, col, "Location")
    worksheet.write_comment(row, col, "Name of Location on platform.")
    worksheet.write(row, col + 1, "LDA ID")
    worksheet.write_comment(row, col + 1, "ID of LDA.")
    worksheet.write(row, col + 2, "Item ID")
    worksheet.write_comment(row, col + 2, "ID of Cargo.")
    worksheet.write(row, col + 3, "Desired location")
    worksheet.write_comment(row, col + 3, "The cargo's desired location.")
    worksheet.write(row, col + 4, "LDA takes hazards")
    worksheet.write_comment(row, col + 4, "If LDA allows cargos with hazards.")
    worksheet.write(row, col + 5, "Cargo hazards")
    worksheet.write_comment(row, col + 5, "If cargo has hazards.")
    worksheet.write(row, col + 6, "LDA takes risk")
    worksheet.write_comment(row, col + 6, "If LDA allows cargos with risk.")
    worksheet.write(row, col + 7, "Cargo risk")
    worksheet.write_comment(row, col + 7, "If cargo has risk.")

    worksheet.set_column(1,2,15,align_format)
    worksheet.set_column(4,7,15,align_format)
    worksheet.set_row(0,25,first_row_format)
    worksheet.set_column(0,0,20)
    worksheet.set_column(3,3,20)
    
    for location in locations_list:
        for LDA in location.LDAs:
            placed_cargos = LDA.cargos
        # iterating through content list
        #worksheet.write(row, col, LDA_id)
            for item in placed_cargos :
                try:
                    worksheet.write(row + 1, col, location.name)
                    worksheet.write(row + 1, col + 1, LDA.id)
                    worksheet.write(row + 1, col + 2, item.id)
                    worksheet.write(row + 1, col + 3, item.location)
                    worksheet.write(row + 1, col + 4, LDA.takes_hazards)
                    worksheet.write(row + 1, col + 5, item.hazards)
                    worksheet.write(row + 1, col + 6, LDA.takes_risk)
                    worksheet.write(row + 1, col + 7, item.risk)    
                except:
                    pass
                # incrementing the value of row by one with each iteratons.
                row += 1
    worksheet.freeze_panes(1, 0)
    workbook.close()

# place cargos and display result depending on list of cargos and LDAs
def result(loc, cargos_list, LDA_list):
    loc_list, rest_cargos = placeCargosByLocation(loc, cargos_list, LDA_list)
    sum  = 0
    labs = ["space/unavailable","available"]
    for loc in loc_list:
        print(loc.name)
        
        for lda in loc.LDAs:
            weight = 0
            #print(lda.id, lda.cargos)
            #print(lda.measurements)
            sum += len(lda.cargos)
            #print("Weight remaining:", lda.max_weight)
            for carg in lda.cargos:
                weight += carg.weight
                print(carg.id, carg.length, carg.width, carg.location)
            
            # plot
            i = 2
            names = [x.id for x in lda.cargos]
            labels = labs.append(names)
            plt.title(lda.id)
            plt.pcolormesh(lda.measurements, edgecolors='k')
            ax = plt.gca()
            ax.set_aspect('equal')
            plt.colorbar(orientation='vertical')
            ax.invert_yaxis()
            #plt.show()
            
    print("Total cargos placed: ", sum, "Not placed: ", len(rest_cargos))
    #for i in rest_cargos:
     #   print(i, i.length, i.width, i.weight)

    writeLocationsToFile(loc_list)

#result(data.list_of_locations, data.sorted_by_area, data.LDA_sorted_smallest)
#result(data.list_of_locations, data.sorted_by_hazards_and_risk, data.LDA_risk_and_hazards)


def optimizeResult(locations, cargos, LDAs):
    
    cargo_sort = ['Unsorted', 'Area', 'Weight', 'Location', 'Risk and Hazards']
    LDA_sort = ['Unsorted', 'Smallest', 'Biggest', 'Risk and Hazards']
    
    print("There are ", len(cargos), "valid cargos in this dataset.")
    result = []
    rest_cargos = []
    result_dict = {}
    lowest_rest = len(cargos)
    optimal_loc_list = -1
    list_cargos_sorted = data.sortCargos(cargos) # sort by [location, weight, area]
    list_LDAs_sorted = data.sortLDA(LDAs) # sort by [smallest first, biggest first

    n = 0
    l = 0
    c = 0
    for cargo_list in list_cargos_sorted:
        
        for LDA_list in list_LDAs_sorted:
            
            temp_cargos = copy.deepcopy(cargo_list)
            temp_LDAs = copy.deepcopy(LDA_list)
            blank_locations = copy.deepcopy(locations)
            list_loc, rest = placeCargosByLocation(blank_locations, temp_cargos, temp_LDAs)
            result.append(list_loc)
            rest_cargos.append(rest)
            result_dict[n] = list_loc
            if len(rest) <= lowest_rest:
                lowest_rest = len(rest)
                optimal_loc_list = n

            print("Iteration ", n, 'cargo sorted by', cargo_sort[c], 'LDA sorted by ', LDA_sort[l], "rest cargos: ", len(rest))
            n += 1
            l += 1
            if l == len(LDA_sort):
                l = 0
        c += 1
   
    writeLocationsToFile(result[optimal_loc_list])
    writephase4_and_5(result[optimal_loc_list])
    
    return result[optimal_loc_list], rest_cargos

optimal_solution, rest_list = optimizeResult(data.list_of_locations, data.cargos_list, data.LDA_list)

# writes to excel file the result of rest cargos depending on sortation of cargo and LDA list
def writeResultSortedLists(rest_cargos):
    workbook = xls.Workbook('deckManagement_results_1.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell.
    # Rows and columns are zero indexed.
    row = 0
    col = 0
    
    first_row_format = workbook.add_format({'bold': True, 'bg_color':'yellow','align':'center', 'valign':'vcenter'})
    align_format = workbook.add_format({'align':'center', 'valign':'vcenter'})

    worksheet.write(row, col, "CargoList sorted")
    worksheet.write_comment(row, col, "What the CargoList is sorted by.")
    worksheet.write(row, col + 1, "LDAList sorted")
    worksheet.write_comment(row, col + 1, "What the LDAList is sorted by.")
    worksheet.write(row, col + 2, "Remaining cargos")
    worksheet.write_comment(row, col + 2, "Numer of cargos that have not been placed on the platform.")

    worksheet.set_row(0,25,first_row_format)
    worksheet.set_column(0,3,20,align_format)
    
   
    #worksheet.set_column()
    cargo_sort = ['Unsorted', 'Area', 'Weight', 'Location', 'Risk and Hazards']
    LDA_sort = ['Unsorted', 'Smallest', 'Biggest', 'Risk and Hazards']
    c = 0
    l = 0
    for rest in rest_cargos:

        # write operation perfor
        try:
            worksheet.write(row + 1, col, cargo_sort[c])
            worksheet.write(row + 1, col + 1, LDA_sort[l])
            worksheet.write(row + 1, col + 2, len(rest))
        except:
            pass
        # incrementing the value of row by one with each iteratons.
        row += 1
        l += 1
        if l == len(LDA_sort):
            l = 0
            c += 1

    worksheet.freeze_panes(1, 0)
    workbook.close()

writeResultSortedLists(rest_list)
