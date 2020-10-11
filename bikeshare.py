import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# 'all' is first because months are 1-indexed
VALID_MONTH = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

# 'all' is last because days are 0-indexed
VALID_DAY = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def ask_user(prompt, valid_choices):
    """
    Asks the user a prompt, and then waits for a valid response
    
    Args:
        prompt (str): The prompt to ask the user
        valid_choices (list, dict): Set of valid responses
    
    Returns:
        str: The user's valid response
    """
    rsp = input(prompt).lower()
    while rsp not in valid_choices:
        rsp = input(f'Invalid input. {prompt}')

    return rsp

def line_break():
    print('-'*40)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ask_user('What city do you want to analyze (Chicago, New York City, or Washington)? ', CITY_DATA)

    # get user input for month (all, january, february, ... , june)
    month = ask_user('What month do you want to analyze (January - June or All)? ', VALID_MONTH)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ask_user('What day do you want to analyze (Monday - Sunday or All)? ', VALID_DAY)

    s = f'Analyzing data for {city.title()}'
    if month != 'all':
        s += f' in {month.title()}'
    if day != 'all':
        s += f' on {day.title()}s'
    print(s)
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
    df = pd.read_csv(CITY_DATA[city])
    # changing Start Time column from str to datetime, creating additional columns for months, weeks, and hours
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.dayofweek
    df['Hour'] = df['Start Time'].dt.hour
    #filter data if necessary
    if month != 'all':
        df = df[df['Month'] == VALID_MONTH.index(month)]
    if day != 'all':
        df = df[df['Day'] == VALID_DAY.index(day)]

    #insert fake gender and birth year values for Washington
    if city == 'washington':
        df['Gender'] = 'N/A'
        df['Birth Year'] = 'N/A'

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = VALID_MONTH[df['Month'].mode()[0]]
    print('Most popular month:', popular_month.title())

    # display the most common day of week
    popular_day = VALID_DAY[df['Day'].mode()[0]]
    print('Most popular day:', popular_day.title())

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print('Most popular hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    line_break()


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + ', ' + df['End Station']
    popular_start_and_end_station = df['Station Combination'].mode()[0]
    print('Most popular station combination:', popular_start_and_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    line_break()


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in seconds
    print ('Total travel time:', df['Trip Duration'].sum(), 'seconds') 


    # display mean travel time
    print ('Average travel time:', df['Trip Duration'].mean(), 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    line_break()


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f'User count:\n{df["User Type"].value_counts()}\n')

    # Display counts of gender
    print(f'Gender:\n{df["Gender"].value_counts()}\n')

    # Display earliest, most recent, and most common year of birth
    print('Earliest birth year:', df['Birth Year'].min())
    print('Most recent birth year:', df['Birth Year'].max())
    print('Most common birth year:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    line_break()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        i = 0
        rsp = ask_user('Would you like to see the first 5 rows of raw data? (yes/no) ', ['yes', 'no'])
        while rsp.lower() == 'yes':
            print(df.iloc[i : i+5])
            i += 5
            if i >= len(df.index):
                print('You have reached the end of the requested data')
                break
            rsp = ask_user('Would you like to see the next 5 rows of raw data? (yes/no) ', ['yes', 'no'])

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
