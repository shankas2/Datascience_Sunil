from configparser import ConfigParser
from collections import defaultdict
import os
import math


# Creating our classes 
class calculatingPeople:
    '''
    This class is responsible for calculating the total number of people 
    in the apartment, including the number of guests.
    '''
    def __init__(self, apartment_type, number_of_guests):
        self.no_of_bedrooms = apartment_type
        self.no_of_guests = number_of_guests
        self.members = defaultdict(int)

    def __getitem__(self, key):
        '''Access the total no of members in the house'''
        return self.members[key]

    def __setitem__(self, val):
        '''Add more guests to the house'''
        self.members['guests'] += val
        return self.members

    def __str__(self):
        return f'The class dict is {self.members}'
    
    def __repr__(self):
        return f'The class dict is {self.members}'

    def initialMembers(self):
        '''
        This method is used to calculate the initial members in the family without guests.
        '''

        if self.no_of_bedrooms == 2:
            self.members['original_members'] = 3
            self.members['guests'] = self.no_of_guests
            return self.members
        else:
            self.members['original_members'] = 5
            self.members['guests'] = self.no_of_guests
            return self.members

    def addGuests(self, val):
        self.members['guests'] += val
        return self.members


class waterConsumed:
    '''
    Water consumed by the apartment given how many people are there in the building.
    '''
    def __init__(self, members, corporation_water_by_parts, borewell_water_by_parts, each_person_water_in_liters):
        self.members = members
        self.corporation_water_by_parts = corporation_water_by_parts
        self.borewell_water_by_parts = borewell_water_by_parts
        self.total_water_parts = self.corporation_water_by_parts + self.borewell_water_by_parts
        self.each_person_water_in_liters = each_person_water_in_liters
        self.water_consumed_by_family = defaultdict(int)

    def __str__(self):
        return f'water consumed by the family is {self.water_consumed_by_family}'

    def __repr__(self):
        return f'water consumed by the family is {self.water_consumed_by_family}'
        
    def initial_water_consumed(self):
        total_number_of_members = self.members['original_members'] + self.members['guests']
        self.water_consumed_by_family['initial_water_allotted'] = self.members['original_members'] * self.each_person_water_in_liters * 30
        self.water_consumed_by_family['initial_water_allotted_by_corporation'] = (
            (self.water_consumed_by_family['initial_water_allotted'] // self.total_water_parts) * self.corporation_water_by_parts)
        self.water_consumed_by_family['initial_water_allotted_by_borewell'] = self.water_consumed_by_family['initial_water_allotted'] - self.water_consumed_by_family['initial_water_allotted_by_corporation']
        return self.water_consumed_by_family

    def water_consumed_by_guests(self, average_water_consumed_by_single_guest_in_liters):
        water_consumed_by_guests = self.members['guests'] * average_water_consumed_by_single_guest_in_liters
        self.water_consumed_by_family['water_consumed_by_guests'] = water_consumed_by_guests
        return self.water_consumed_by_family


class bill:
    '''
    Total bill for the apartment given the water consumed.
    '''

    def __init__(self, 
        water_consumed_by_family,
        corporation_water_rate_per_liter_in_rs,
        borewell_water_rate_per_liter_in_rs,
        tanker_water_rate_upto_500,
        tanker_water_rate_501_1500,
        tanker_water_rate_1501_3000,
        tanker_water_rate_3000_plus):
    
    
        self.water_consumed_by_family = water_consumed_by_family
        self.corporation_water_rate_per_liter_in_rs = corporation_water_rate_per_liter_in_rs
        self.borewell_water_rate_per_liter_in_rs = borewell_water_rate_per_liter_in_rs
        self.tanker_water_rate_upto_500 = tanker_water_rate_upto_500
        self.tanker_water_rate_501_1500 = tanker_water_rate_501_1500
        self.tanker_water_rate_1501_3000 = tanker_water_rate_1501_3000
        self.tanker_water_rate_3000_plus = tanker_water_rate_3000_plus


    def bill_generation(self):
        corporation_water_bill = self.water_consumed_by_family['initial_water_allotted_by_corporation'] * self.corporation_water_rate_per_liter_in_rs
        borewell_water_bill = self.water_consumed_by_family['initial_water_allotted_by_borewell'] * self.borewell_water_rate_per_liter_in_rs
        if self.water_consumed_by_family['water_consumed_by_guests'] == 0:
            print('Total Water bill generated without guests in the house')
            print('------------------------------------------------------')
            return corporation_water_bill + borewell_water_bill

        else:
            total_water_tank_parts = self.water_consumed_by_family['water_consumed_by_guests'] // 100
            base_bill = corporation_water_bill + borewell_water_bill + 500 * self.tanker_water_rate_upto_500
            print('Total water bill generated with guests is .....')
            print('\n')

            if total_water_tank_parts <= 5:
                return corporation_water_bill + borewell_water_bill + total_water_tank_parts * 100 * self.tanker_water_rate_upto_500
            if total_water_tank_parts <= 15 and total_water_tank_parts > 5:
                return  base_bill + (total_water_tank_parts - 5) * self.tanker_water_rate_501_1500 
            if total_water_tank_parts <= 30 and total_water_tank_parts > 15:
                return  base_bill + 1000 * self.tanker_water_rate_501_1500 + (total_water_tank_parts - 15) * self.tanker_water_rate_1501_3000
            if total_water_tank_parts > 30:
                return  base_bill + 1000 * self.tanker_water_rate_501_1500 + 1500 * self.tanker_water_rate_1501_3000 + (total_water_tank_parts - 30) * self.tanker_water_rate_3000_plus
            



def run():
    # Getting our data from the config parser
    config = ConfigParser()
    config.read('configuration.ini')
    apartment_type = int(config['DEFAULT']['apartment_type'])
    corporation_water_by_parts = int(config['DEFAULT']['corporation_water_by_parts'])
    borewell_water_by_parts = int(config['DEFAULT']['borewell_water_by_parts'])
    number_of_guests = int(config['DEFAULT']['number_of_guests'])
    each_person_water_in_liters = int(config['DEFAULT']['each_person_water_in_liters'])
    average_water_consumed_by_single_guest_in_liters = int(config['DEFAULT']['average_water_consumed_by_single_guest_in_liters'])
    corporation_water_rate_per_liter_in_rs = float(config['DEFAULT']['corporation_water_rate_per_liter_in_rs'])
    borewell_water_rate_per_liter_in_rs = float(config['DEFAULT']['borewell_water_rate_per_liter_in_rs'])
    tanker_water_rate_upto_500 = float(config['DEFAULT']['tanker_water_rate_upto_500'])
    tanker_water_rate_501_1500 = float(config['DEFAULT']['tanker_water_rate_501_1500'])
    tanker_water_rate_1501_3000 = float(config['DEFAULT']['tanker_water_rate_1501_3000'])
    tanker_water_rate_3000_plus = float(config['DEFAULT']['tanker_water_rate_3000_plus'])

    people_dict = calculatingPeople(apartment_type, number_of_guests)
    people_dict.initialMembers()

    print(people_dict.members)

    while True:
        val = int(input('Do you want to add guests, if yes enter the val, else enter 99 to generate bill...'))
        if val != 99:
            people_dict.addGuests(val)
            print(f'Total number of guests added to the house are {people_dict["guests"]}')

        else:
            print('Generating the bill.......')
            break
    water_consumed = waterConsumed(people_dict.members, corporation_water_by_parts, borewell_water_by_parts, each_person_water_in_liters)
    water_consumed.initial_water_consumed()
    water_consumed.water_consumed_by_guests(average_water_consumed_by_single_guest_in_liters)

    print('water consumption info....\n')
    print(water_consumed)
    print('----------------------------')

    bill_generated = bill(water_consumed.water_consumed_by_family,
        corporation_water_rate_per_liter_in_rs,
        borewell_water_rate_per_liter_in_rs,
        tanker_water_rate_upto_500,
        tanker_water_rate_501_1500,
        tanker_water_rate_1501_3000,
        tanker_water_rate_3000_plus)
    
    total_bill = bill_generated.bill_generation()
    print(f'Total bill generated is {total_bill}')

if __name__ == '__main__':
    run()