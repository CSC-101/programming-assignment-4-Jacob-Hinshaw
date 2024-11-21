import fullreduced
import data
from data import CountyDemographics
from fullreduced import reduced_data

county_list = fullreduced.reduced_data
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

def filter_state(counties: list[CountyDemographics], state: str) -> list[CountyDemographics]:
    new = [county for county in counties if county.state == state]
    print(f"Filter: state == {state} ({len(new)} entries)")
    return new

def filter_gt(counties: list[CountyDemographics], field: str, number: float):
    #new = [county for county in counties if county.field > number]
    field_parts = field.split('.')

    def get_field_value(county: CountyDemographics):
        """Retrieve the value of the specified field from a CountyDemographics object."""
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

def filter_lt(counties: list[CountyDemographics], field: str, number: float):
    #new = [county for county in counties if county.field > number]
    field_parts = field.split('.')

    def get_field_value(county: CountyDemographics):
        """Retrieve the value of the specified field from a CountyDemographics object."""
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

    # Filter the counties based on the resolved field value
    new = [county for county in counties if (val := get_field_value(county)) is not None and val < number]
    print(f"Filter: {field} lt {number} ({len(new)} entries)")
    return new

def population_total(counties: list[CountyDemographics]):
    pop = 0
    for county in counties:
        pop += county.population.get("2014 Population", 0)
    print(f"2014 population: {pop}")
    return pop

def population_field(counties: list[CountyDemographics], field: str):
    field_parts = field.split('.')
    pop = 0
    pop_2014 = 0
    for county in counties:
        pop_2014 += county.population.get("2014 Population", 0)
    def get_field_value(county: CountyDemographics):
        """Retrieve the value of the specified field from a CountyDemographics object."""
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

#population_field(reduced_data, "ethnicities.Black Alone")
#population_total(reduced_data)
#county_list = filter_lt(reduced_data, "education.High School or Higher", 83)
#county_list = filter_gt(reduced_data, "education.High School or Higher", 83)
#county_list = filter_state(county_list, "AR")
#display(county_list)
