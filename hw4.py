import sys

import fullreduced
import county_demographics
import data
from data import CountyDemographics
from fullreduced import reduced_data


#this file uses the reduced data but that can be changed here and in line 162
county_list = fullreduced.reduced_data


# This function displays the current state of the filtered list of county demographics
def display(counties: list[CountyDemographics]) -> None:
    print(f"{len(counties)} entries")
    for county in counties:
        print(f"{county.county}, {county.state}")
        print(f"        Population: {county.population.get('2014 Population', 'N/A')}")
        print("        Age:")
        print(f"               < 5: {county.age.get('Percent Under 5 Years', 'N/A')}%")
        print(f"               < 18: {county.age.get('Percent Under 18 Years', 'N/A')}%")
        print(f"               > 65: {county.age.get('Percent 65 and Older', 'N/A')}%")
        print("        Education")
        print(f"                >= High School: {county.education.get('High School or Higher', 'N/A')}%")
        print(f"                >= Bachelor's: {county.education.get("Bachelor's Degree or Higher", 'N/A')}%")
        print("        Ethnicity Percentages")
        for ethnicity, percentage in county.ethnicities.items():
            print(f"                {ethnicity}: {percentage}%")
        print("        Income")
        print(f"                Median Household: {county.income.get('Median Household Income', 'N/A')}")
        print(f"                Per Capita: {county.income.get('Per Capita Income', 'N/A')}")
        print(f"                Below Poverty Level: {county.income.get('Persons Below Poverty Level', 'N/A')}%")
        print()

# This function will filter out any county that is not from the specified state
def filter_state(counties: list[CountyDemographics], state: str) -> list[CountyDemographics]:
    new = [county for county in counties if county.state == state]
    print(f"Filter: state == {state} ({len(new)} entries)")
    return new

# this function will filter out any county that does not have the given demographic above the given percentage.
def filter_gt(counties: list[CountyDemographics], field: str, number: float):
    #new = [county for county in counties if county.field > number]
    field_parts = field.split('.')

    def get_field_value(county: CountyDemographics):
        value = county
        try:
            for part in field_parts:
                if isinstance(value, dict):
                    value = value[part]
                else:
                    value = getattr(value, part)
            return value
        except (KeyError, AttributeError):
            return None

    new = [county for county in counties if (val := get_field_value(county)) is not None and val > number]
    print(f"Filter: {field} gt {number} ({len(new)} entries)")
    return new

# this function will filter out any county that does not have the given demographic below the given percentage.
def filter_lt(counties: list[CountyDemographics], field: str, number: float):
    #new = [county for county in counties if county.field > number]
    field_parts = field.split('.')

    def get_field_value(county: CountyDemographics):
        value = county
        try:
            for part in field_parts:
                if isinstance(value, dict):
                    value = value[part]
                else:
                    value = getattr(value, part)
            return value
        except (KeyError, AttributeError):
            return None

    new = [county for county in counties if (val := get_field_value(county)) is not None and val < number]
    print(f"Filter: {field} lt {number} ({len(new)} entries)")
    return new

# This function tells the total population for all of the counties in the current state of the data
def population_total(counties: list[CountyDemographics]):
    pop = 0
    for county in counties:
        pop += county.population.get("2014 Population", 0)
    print(f"2014 population: {pop}")
    return pop

# This function tells the total population for all of the counties in the current state of the data that qualify for the given demographic
def population_field(counties: list[CountyDemographics], field: str):
    field_parts = field.split('.')
    pop = 0
    pop_2014 = 0
    for county in counties:
        pop_2014 += county.population.get("2014 Population", 0)
    def get_field_value(county: CountyDemographics):
        value = county
        try:
            for part in field_parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    value = getattr(value, part)
            return value
        except (KeyError, AttributeError):
            return 0

    for county in counties:
        value = get_field_value(county)
        if isinstance(value, (int, float)):
            pop += value
    print(f"2014 {field} population: {pop * pop_2014}")

# This function gives the percent total 2014 population that fits the given demographic.
def population_percent(counties: list[CountyDemographics], field: str):
    field_parts = field.split('.')
    total_population = sum(county.population.get("2014 Population", 0) for county in counties)
    weighted_percent = 0

    def get_field_value(county: CountyDemographics):
        value = county
        try:
            for part in field_parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    value = getattr(value, part)
            return value
        except (KeyError, AttributeError):
            return 0

    for county in counties:
        value = get_field_value(county)
        if isinstance(value, (int, float)):
            county_population = county.population.get("2014 Population", 0)
            weighted_percent += (value / 100) * county_population

    overall_percent = (weighted_percent / total_population) * 100 if total_population > 0 else 0
    print(f"2014 {field} percentage: {overall_percent}%")


#population_percent(reduced_data, "income.Persons Below Poverty Level")
#population_field(reduced_data, "ethnicities.Black Alone")
#population_total(reduced_data)
#county_list = filter_lt(reduced_data, "education.High School or Higher", 83)
#county_list = filter_gt(reduced_data, "education.High School or Higher", 83)
#county_list = filter_state(county_list, "AR")
#display(county_list)

# This function applies the given functions to reduced_data from a file in the command line.
def main():
    if len(sys.argv) != 2:
        print("Error: Please provide an operations file as a command-line argument.")
        sys.exit(1)

    operations_file = sys.argv[1]

    try:
        with open(operations_file, 'r') as file:
            operations = file.readlines()
    except FileNotFoundError:
        print(f"Error: Unable to open the file '{operations_file}'.")
        sys.exit(1)

    county_list = fullreduced.reduced_data

    for line_num, operation in enumerate(operations, start=1):
        line = operation.strip()
        if not line:
            continue

        try:
            parts = line.split(':')
            command = parts[0]

            if command == "display":
                display(county_list)
            elif command == "filter-state":
                state = parts[1]
                county_list = filter_state(county_list, state)
            elif command == "filter-gt":
                field, number = parts[1], float(parts[2])
                county_list = filter_gt(county_list, field, number)
            elif command == "filter-lt":
                field, number = parts[1], float(parts[2])
                county_list = filter_lt(county_list, field, number)
            elif command == "population-total":
                population_total(county_list)
            elif command == "population":
                field = parts[1]
                population_field(county_list, field)
            elif command == "percent":
                field = parts[1]
                population_percent(county_list, field)
            else:
                print(f"Error: Unknown operation on line {line_num}. Skipping.")
        except (IndexError, ValueError) as e:
            print(f"Error: Malformed operation on line {line_num}. Skipping.")

if __name__ == "__main__":
    main()