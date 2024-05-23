import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
VALID_ANSWER = ['yes', 'no', 'y' ,'n']

valid_ans = False
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    # Select City to filter by. If invalid city selected, repeat question
    valid_ans = False
    while valid_ans == False:
        c = input("Please enter your city of choice. Select from Chicago, New York City or Washington: ")
        city = c.lower() 
        if city not in CITY_DATA:
            print("The city selected is not valid. Please try again")
        else:
            print("You have selected, {}".format(city))
            valid_ans = True

    #  Select Month to filter by. If invalid month selected, repeat question
    valid_ans = False
    while valid_ans == False:
        m = input("Please select month (all, january, february, ... , june): ")
        month = m.lower()
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        if month not in months:
            print("The month selected is not valid. Please try again")
        else:
            print("You have selected, {}".format(month))
            valid_ans = True

    # Select Day to filter by. If invalid day selected, repeat question
    valid_ans = False
    while valid_ans == False:
        d = input("Please select day (all, monday, tuesday, ... , sunday): ")
        day = d.lower()
        days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        if day not in days:
            print("The day selected is not valid. Please try again")
        else:
            print("You have selected, {}".format(day))
            valid_ans = True
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
        # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df
    


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    #convert month integer to name
    pop_month_name = calendar.month_name[popular_month]
    print('the most popular month for bike rental in {} is {}'.format(city, pop_month_name))
        
    df['day'] = df['Start Time'].dt.day
    popular_day = df['day_of_week'].mode()[0]
    print('the most popular day for bike rental in {} is {}'.format(city, popular_day))
        
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('the most popular hour for bike rental in {} is {}00 hrs'.format(city, popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    pop_start_station = df['Start Station'].mode()[0]
    print('the most popular starting point in {} is {}'.format(city, pop_start_station))

    pop_end_station = df['End Station'].mode()[0]
    print('the most popular destination in {} is {}'.format(city, pop_end_station))

    df['trip'] = df["Start Station"] + ' to ' + df["End Station"]
    pop_trip = df['trip'].mode()[0]
    print('the most popular trip in {} is {}'.format(city, pop_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum() / 3600 # convert seconds into hours
    print('the total time of trips taken for the current selection is {} hours'.format(total_travel_time))


    mean_travel_time = df['Trip Duration'].mean() / 60 # convert seconds into minutes
    print('the mean time of trips taken for the current selection is is {} minutes'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    print('User Type Count\n')
    user_type_count = df['User Type'].value_counts()
    print(user_type_count)
    print('-'*30)

    print('User Gender Count\n')
    if city == 'washington':
        print('No gender data available')
    else:      
        user_type_count = df['Gender'].value_counts()
        print(user_type_count)
        print('-'*30)

    print('Birth Year Stats\n')
    if city == 'washington':
        print('No birth year data available')
    else:
        common_year = df['Birth Year'].mode()[0].astype('int64')
        print('the most common birth year for the current selection is {}\n'.format(common_year))
        print(df['Birth Year'].describe()[['min', 'max']].astype('int64', errors='ignore'))

        print('-'*30)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def display_raw_data(df):
    """ Ask User if they would like to display raw data
        If no end functiona. If yes print raw data 5 lines at time, Confirming with user each time if they would like to continue"""
    i = 0
    valid_ans = False
    while valid_ans == False:
        r = input("Would you like to see the raw data. Yes or No: ") # TO DO: convert the user input to lower case using lower() function
        raw = r.lower()
        if raw not in VALID_ANSWER:
            print("The answer selected is not valid. Please answer yes or no: ")
        else:
            valid_ans = True    
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i+5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
            print('-'*40)
            r = input("Would you like to see 5 more lines of raw data. Yes or No: ") # TO DO: convert the user input to lower case using lower() function
            raw = r.lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        print('Hello! Let\'s explore some US bikeshare data!')
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, city, month, day)
        station_stats(df, city)   
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != ('yes' or 'y'):
            break


if __name__ == "__main__":
	main()
