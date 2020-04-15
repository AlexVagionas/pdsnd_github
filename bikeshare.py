import time
import calendar as cal
import random as rnd
from pprint import pprint
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get the city from user
    city = input('Choose a city between Chicago, New York City and Washington: ').lower()

    # if no .csv file exist for the city prompt the user for input again
    while city not in CITY_DATA:
        print('We apologise but no such city exists in our database!')
        city = input('Please try one of the aforementioned cities: ').lower()

    # get time filter options from user. available filters: month, day, both, all
    time_filter = input('\nWould you like to filter by month, day, both or not at all? '
                        'Type \"none\" for no time filter.\n').lower()

    # if incorrect filter specified prompt the user for input again
    while time_filter not in ('month', 'day', 'both', 'none'):
        time_filter = input('Invalid filter! Please try again: ').lower()

    # no time filter is applied
    if time_filter == 'none':
        return city, 'All', 'All'

    # is the month filter applied?
    if time_filter in ('month', 'both'):
        # get the month from user
        month = input('\nChoose a month from January to June: ').title()

        # if month is not from January to July or "all" promt the user for input again
        while month not in cal.month_name[1:7]:
            month = input('Please enter a valid month: ').title()

        if time_filter == 'month':
            # only month filter is applied
            print('-'*40)
            return city, month, 'All'

    # is the day filter applied?
    if time_filter in ('day', 'both'):
        # get the day from user
        day = input('\nChoose a day of the week: ').title()

        # if day is not a valid day or "all" promt the user for input again
        while day not in cal.day_name:
            day = input('Please enter a valid day: ').title()

        if time_filter == 'day':
            # only day filter is applied
            print('-'*40)
            return city, 'All', day

    # both time filters are applied
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = [m for m in cal.month_name[1:7]]
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (DataFrame) df    - Pandas DataFrame containing city data filtered by month and day
        (str)       month - name of the month for which data were filtered by, or "All"
                            if no filter is applied
        (str)       day   - name of the day for which data were filtered by, or "All"
                            if no filter is applied
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'All':
        most_popular_month = cal.month_name[df['month'].mode()[0]]
        print('Most Popular Month: ' + most_popular_month)

    # display the most common day of week
    if day == 'All':
        most_popular_day = df['day_of_week'].mode()[0]
        print('Most Popular Day: ' + most_popular_day)

    # extract start hour from Start Time
    df['start_hour'] = df['Start Time'].dt.hour

    # display the most common start hour
    most_popular_start_hour = df['start_hour'].mode()[0]
    print('Most Popular Start Hour: {}'.format(most_popular_start_hour))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station: ' + most_popular_start_station)

    # display most commonly used end station
    most_popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station: ' + most_popular_end_station)

    # create trip column from start and end stations
    df['Trip'] = df['Start Station'] + ' -> ' + df['End Station']

    # display most frequent combination of start station and end station trip
    most_popular_trip = df['Trip'].mode()[0]
    print('Most Popular Trip: ' + most_popular_trip)

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: {}'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time : {}'.format(mean_travel_time))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Types:\n{}'.format(df['User Type'].value_counts()))

    # Display counts of gender
    print('\nGenders:\n{}'.format(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
    earlist_birth = df['Birth Year'].min()
    most_recent_birth = df['Birth Year'].max()
    most_common_birth = df['Birth Year'].mode()[0]

    print('\nBirth Year Statistics:')
    print('Earlist Year of Birth: {}'.format(earlist_birth))
    print('Most Recent Year of Birth: {}'.format(most_recent_birth))
    print('Most Common Year of Birth: {}'.format(most_common_birth))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def get_rand_rows(df, n):
    """
    Extracts n random rows from DataFrame

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (int) n - number of rows to be extracted
    Returns:
        (DataFrame) df_part - Pandas DataFrame containing only the exctracted rows
    """

    # get total number of rows in DataFrame
    nrows, _ = df.shape

    # create list of n random integers to index the DataFrame
    idx_list = [rnd.randint(0, nrows - 1) for i in range(n)]

    # extract n random rows from DataFrame
    df_part = df.iloc[idx_list]

    return df_part


def individual_data(df):
    """Displays individual data of bikeshare users."""

    # get 5 random rows from DataFrame
    df_part = get_rand_rows(df, 5)

    # remove 1st columns
    df_part = df_part.drop(df.columns[0], axis=1)

    # display extracted rows
    for row in df_part.iterrows():
        pprint(row[1].to_dict())


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # print(df.head())
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            disp_individual_data = input(
                '\nWould you like to see individual trip data? Enter yes or no.\n')
            if disp_individual_data.lower() != 'yes':
                break
            individual_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
