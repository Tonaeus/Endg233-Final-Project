# Group Number: 42
# Member 1: Tony Tran, 30141007
# Member 2: Sarim Sheikh, 30143892

import numpy as np
import matplotlib.pyplot as plt

class Country:
    """A country used to create a country object.

        Attributes:
            name (str): String that represents the country's name
    """
    def __init__(self, name, proportion):
        self.name = name
        self.proportion = proportion 
        
    def most_area_print(self):
        ''' A function that prints the name and area of the country with the greatest area
    
        Parameters: None
        Return: None
        ''' 
        print(f'The largest country in the region is {self.name} and its approximate proportion relative to the region is {self.proportion}.')

    def least_area_print(self):
        ''' A function that prints the name and area of the country with the least area
    
        Parameters: None
        Return: None
        ''' 
        print(f'The smallest country in the region is {self.name} and its approximate proportion relative to the region is {self.proportion}.')

def operation_menu():
    ''' A function that request user desired data or if they want to quit.
    
    Parameters: None
    Return: None
    '''
    print()
    print('OPTION MENU')
    print('1 - A list of countries within a sub-region and their population density')
    print('2 - A pie chart of the region\'s countries area contribution percentages')
    print('3 - A bar graph of the region\'s mean endangered species')
    print('4 - A line graph comparing 2 countries population and their average')
    print('5 - The country within the region with the most and least area proportion')
    print('6 - The country within the region with the most and least total endangered species')
    print('7 - The country within the region with the largest and lowest population growth')
    print('0 - To select a different region')
    print()

def finding_countries(selected_region, data_for_country):
    ''' A function that creates a list of the countries within the region index.

    Parameters: selected_region -- the region that the user wishes to look up data for
                data_for_country -- a set of data containing the countries name and which region it belongs to
    Return: region_country_index -- a list containing the index of the countries within the region
    '''
    region_country_index = [list(data_for_country).index(region) for region in data_for_country if region[1] == selected_region]
    return region_country_index

def region_countries(country_index, data_with_name):
    ''' A function that creates a list with the names of the countries in the region.

    Parameters: country_index -- the index of the countries within the region
                data_with_name -- any data containing the names of countries in alphabetical order
    Return: name_list -- a list of all the names of the countries in the region
    '''
    names_list = [data_with_name[index][0] for index in country_index]
    return names_list

def most_least(inputted_list):
    ''' A function that finds the maximum and minimum value of given list

    Parameter: inputted_list -- a list containing values ranging from a small one to a large one
    Return: max_value -- largest value in the list
            min_value -- smallest value in the list
    '''
    size_list = np.array([inputted_list])
    max_value = np.amax(size_list)
    min_value = np.amin(size_list)
    return max_value, min_value

def main():
    # Import all 3 csv
    country_data = np.genfromtxt('Country_Data.csv', delimiter = ',', skip_header = True, dtype = None, encoding = 'UTF-8')
    threatened_species = np.genfromtxt('Threatened_Species.csv', delimiter = ',', skip_header = True, dtype = None, encoding = 'UTF-8')
    population_data = np.genfromtxt('Population_Data.csv', delimiter = ',', skip_header = True, dtype = None, encoding = 'UTF-8')

    # User region and operation selection

        # Taking in region input and verifying them
    region_list = sorted(list({region[1] for region in country_data}))
    user_region = ''
    while user_region not in region_list:
        print('Regions: {}, {}, {}, {}, and {}.'.format(region_list[0], region_list[1],region_list[2],region_list[3],region_list[4]))
        user_region = input("Enter a region to extrapolate data from or type 'quit' to quit: ")
        if user_region in region_list:
            # Creating a list for the country index and name
            countries_index_list = finding_countries(user_region, country_data)
            countries_name_list = region_countries(countries_index_list, population_data)

            operation_menu()

                # Taking in option input and verifying them
            valid_option = [str(x) for x in range(8)]
            user_option = ''

            while True:
                user_option = input('Enter an option: ')
                
                if user_option not in valid_option:
                    print('Enter in a valid option.\n')
                    continue

                # Return users to the original menu to select another region to look up data
                elif user_option == '0':
                    user_region = ''
                    print()
                    break

                # The print statements showing each countries within a region population density
                elif user_option == '1':
                    sub_region_list = sorted(list({region[2] for region in country_data if region[1] == user_region}))
                    sub_region_format = ', '.join(sub_region_list[:-1] + ['and'] + sub_region_list[-1:])
                    edit_sub_region = sub_region_format.replace(' and,', ' and')

                    print('Sub-Regions:', edit_sub_region, end = '.\n')

                    user_sub_region = ''
                    while True:
                        user_sub_region = input('Enter a sub-region: ')
                        if user_sub_region not in sub_region_list:
                            print('Enter in a valid sub-region.\n')
                            continue

                        print()
                        for index in countries_index_list:
                            if country_data[index][2] == user_sub_region:
                                print('{}: {} people per sq km'.format(country_data[index][0], round(population_data[index][21] / country_data[index][3], 3)))
                        break

                # The pie chart displaying the relative size of each country in a region
                elif user_option == '2':
                    total_region_size = sum([country_data[index][3] for index in countries_index_list]) # The total region area

                    # Creating a list of the countries' name with an area greater than 1% of the overall and another list of their sizes
                    country_size_list = [country_data[index][3] for index in countries_index_list if (country_data[index][3] / total_region_size * 100) >= 1]
                    country_name_list = [country_data[index][0] for index in countries_index_list if (country_data[index][3] / total_region_size * 100) >= 1]

                    # Finding the area total of the countries that is not atleast 1% of the region overall area, and adding it to the country size list
                    country_size_list.append(sum([country_data[index][3] for index in countries_index_list if (country_data[index][3] / total_region_size * 100) < 1]))
                        # Adding the name 'Others' to account for the name element in country size list when plotting
                    country_name_list.append('Others')

                    # Generating the pie chart and showing it
                    plt.figure(1)
                    plt.pie(country_size_list, autopct = '%1.1f%%', labels = country_name_list, labeldistance = 1.15)
                    plt.title(f'Countries in {user_region} Relative Area Distribution', fontsize = 20)
                    plt.legend(country_name_list, loc='center left', bbox_to_anchor=(-0.35, .5))
                    
                    plt.show()

                ### Make a mean bar graph
                elif user_option == '3':
                    number_of_countries = len(countries_index_list) # Finding the number of countries in the region to use as a parameter in the loop
                    
                    # Creating lists for the different types of subspecies
                    total_plant_species = []
                    total_fish_species = []
                    total_bird_species = []
                    total_mammal_species = []

                    i = 0   # Definig the parameter for the loop

                    # Loop which adds all the different supspecies into their corresponding lists from the different countries in the region
                    while i in range(number_of_countries):
                        total_plant_species.append(threatened_species[countries_index_list[i]][1])
                        total_fish_species.append(threatened_species[countries_index_list[i]][2])
                        total_bird_species.append(threatened_species[countries_index_list[i]][3])
                        total_mammal_species.append(threatened_species[countries_index_list[i]][4])
                        i += 1
                    
                    # Finding the averages of all the different sub species in the sub-species lists and rounding them too the two decimal place
                    average_plant_species = round(np.average(np.array(total_plant_species)), 2)
                    average_fish_species = round(np.average(np.array(total_fish_species)), 2)
                    average_bird_species = round(np.average(np.array(total_bird_species)), 2)
                    average_mammal_species = round(np.average(np.array(total_mammal_species)), 2)

                    # Generating the bar graph and showing it
                    array_species_name = np.array(['Plants', 'Fish', 'Birds', 'Mammals'])
                    array_species_average = np.array([average_plant_species, average_fish_species, average_bird_species, average_mammal_species])
                    plt.bar(array_species_name,array_species_average, color = ['green','blue','orange','brown'], width = 0.5)
                    plt.title(f'Average Number of Endangered Species in {user_region}')
                    plt.xlabel('Type of Species')
                    plt.ylabel('Number of Species')
                    plt.show()

                ### Make a mean line graph
                elif user_option == '4':
                    list_country_names = []                 # An empty list for the country names in a region

                    # Loop which adds the country names into the empty list
                    for index in countries_index_list:
                        list_country_names.append(country_data[index][0])

                    country_format = ', '.join(list_country_names[:-1] + ['and'] + list_country_names[-1:])
                    edit_country = country_format.replace(' and,', ' and')

                    print('Country names:', edit_country, end = '.\n') # Printing all the country names in the region

                    # Prompts for the inputs from the user to pick two countries within a region to get the comparasion population data for
                    user_country_name1 = ''
                    user_country_name2 = ''
                    
                    x = True                    
                    while x == True:
                        
                        # Checks that the input is valid
                        while True:
                            user_country_name1 = str(input('\nWhat is the first country from the region you want to compare: '))
                            if user_country_name1 not in list_country_names:
                                print('You must enter a valid country name from the region.')
                                continue
                            else: 
                                break
                        
                        # Checks that the input is valid and is not the same as the first input
                        while True:
                            user_country_name2 = str(input('\nWhat is the second country from the region you want to compare: '))
                            if user_country_name2 not in list_country_names or user_country_name1 == user_country_name2:
                                print('You must enter a valid country name or a differnt country name from the region.')
                                continue
                            else: 
                                break
                
                        # Creating both independent and dependent coordinate values
                        index_country_name1 = list_country_names.index(user_country_name1)
                        index_country_name2 = list_country_names.index(user_country_name2)
                        array_index_population1 = countries_index_list[index_country_name1]
                        array_index_population2 = countries_index_list[index_country_name2]
                        change_in_years = np.array([2000, 2004, 2008, 2012, 2016, 2020])
                        change_in_population1 = np.array([population_data[array_index_population1][1], population_data[array_index_population1][5], population_data[array_index_population1][9], population_data[array_index_population1][13], population_data[array_index_population1][17], population_data[array_index_population1][21]])
                        change_in_population2 = np.array([population_data[array_index_population2][1], population_data[array_index_population2][5], population_data[array_index_population2][9], population_data[array_index_population2][13], population_data[array_index_population2][17], population_data[array_index_population2][21]])
                        array_average_pop = np.divide((change_in_population1 + change_in_population2), [2])

                        # Plotting line graph
                        plt.xticks(change_in_years)
                        plt.title('Population Growth')
                        plt.xlabel('Years')
                        plt.ylabel('Population')
                        plt.plot(change_in_years, change_in_population1, ls = '-.', c = 'orangered', marker = 'o', label = f'{user_country_name1}')
                        plt.plot(change_in_years, change_in_population2, ls = '-.', c = 'cyan', marker = 'o', label = f'{user_country_name2}')
                        plt.plot(change_in_years, array_average_pop, ls = '-.', c = 'lime', marker = 'o', label = 'Average')
                        plt.legend()
                        plt.show()
                        x = False
                        
                        # Resetting inputs variable
                        user_country_name1 = ''
                        user_country_name2 = ''

                # Find the country that has the biggest proportion and the country that has the smallest proportion in the region
                elif user_option == '5':
                    total_region_size = sum([country_data[index][3] for index in countries_index_list]) # The total region area

                    country_size_list2 = [country_data[index][3] for index in countries_index_list] # Creating a list with all the areas of the countries in the region
                    b_area, s_area = most_least(country_size_list2) # Finding the largest and smallest areas

                    # Finding the proportion for the 2 areas
                    b_proportion = round((b_area / total_region_size), 5)
                    s_proportion = round((s_area / total_region_size), 5)
                    
                    # Finding the largest and smallest country that corresponds to the areas from above
                    b_country = region_countries(countries_index_list, country_data)[country_size_list2.index(b_area)]
                    s_country = region_countries(countries_index_list, country_data)[country_size_list2.index(s_area)]
                    
                    # Creating country objects for the largest and smallest country
                    largest_country = Country(b_country, b_proportion)
                    smallest_country = Country(s_country, s_proportion)
                    
                    # Printing out the data for the largest and smallest country
                    largest_country.most_area_print()
                    smallest_country.least_area_print()

                # Find the country that has the highest amount of total endangered species and the country that has the lowest amount of total endangered species in the region
                elif user_option == '6':
                    country_tot_endspec = [sum(list(country)[1:]) for country in threatened_species if country[0] in countries_name_list] # Creating a list of the total endangered species
                    
                    most_end, least_end = most_least(country_tot_endspec) # Finding the most and least total amount of endangered spcies in a country within the region

                    # Finding the name of the countries with the most and least endangered species
                    most_end_country = threatened_species[countries_index_list[country_tot_endspec.index(most_end)]][0]
                    least_end_country = threatened_species[countries_index_list[country_tot_endspec.index(least_end)]][0]
                    
                    # Printing out the statements for user
                    print(f'The country with the most total endangered species in {user_region} is {most_end_country} with a total of {most_end}.')
                    print(f'The country with the least total endangered species in {user_region} is {least_end_country} with a total of {least_end}.')

                # Find the country with the greatest population growth from 2000 to 2020 and the country with the least population growth from 2000 to 2020 in the region
                elif user_option == '7':
                    # Creating 2 list of populations in the year of 2000 and 2021 for the countries within the region
                    pop_2020 = [country[21] for country in population_data if country[0] in countries_name_list]
                    pop_2000 = [country[1] for country in population_data if country[0] in countries_name_list]

                    pop_change = list(np.array(pop_2020) - np.array(pop_2000)) # Creating a list of all the population changes

                    most_growth, least_growth = most_least(pop_change) # Determining the greatest and least population changes

                    # Find the name of the countries with the most and least population growth
                    most_growth_country = population_data[countries_index_list[pop_change.index(most_growth)]][0]
                    least_growth_country = population_data[countries_index_list[pop_change.index(least_growth)]][0]

                    # Printing out the statements for user
                    print(f'The country that had the largest population growth would be {most_growth_country} and its population changed by {most_growth}.')
                    print(f'The country that had the lowest population growth would be {least_growth_country} and its population changed by {least_growth}.')
                    
                operation_menu()

        # Continuous loop until the user enters in a valid region or quits
        elif user_region == 'quit':
            break
        else:
            print('Enter in a valid region.\n')
            continue

if __name__ == '__main__':
    main()