#imports the necessary libraries
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
days = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('Are you looking at Chicago, New York City, or Washington?  ').title())
            if city == "Washington" or city =="Chicago" or city == "New York City":
                break
            print("Try again (check for exact spelling)")
        except:
            print("Try again")


    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
       try:
           month = str(input('What month (type "All" for all months or "January", "February", "March", etc...)?  ').title())
           if month in months:
               break
           print("\nTry again (check for exact spelling and note that there is no data after June)")
       except:
           print("Try again")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
       try:
           day = str(input('What day of the week (type "All" for all days of the week or "Monday", "Tuesday", "Wednesday", etc...)?  ').title())
           if day in days:
               break
           print("\nTry again (check for exact spelling)")
       except:
           print("Try again")

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

    #if statement to call correct file based on user input
    if city == "Washington":
        filename = 'washington.csv'
    elif city == "New York City":
        filename = 'new_york_city.csv'
    elif city == "Chicago":
        filename = 'chicago.csv'

    df = pd.read_csv(filename)

    #try statements in case 'Gender' column is missing in the files. The column is created with NaN values
    try:
        df[['Gender']] = df[['Gender']].fillna(value='Unknown')
    except:
        df["Gender"] = np.nan

    #creation of new time columns based on dates
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['week_day'] = df['Start Time'].dt.day_name()
    df['month'] = df['Start Time'].dt.month_name()
    df['hour'] = df['Start Time'].dt.hour

    #creation of station to station trips
    df['combo_station'] = df['Start Station'] + ' -> TO -> ' + df['End Station']

    #fills NaNs with 'Unknown' value
    df[['Gender']] = df[['Gender']].fillna(value='Unknown')
    df[['User Type']] = df[['User Type']].fillna(value='Unknown')

    #if 'All' is inputted by the user, then the following statement avoids filters
    if month != 'All':
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['week_day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if df['month'].nunique() > 1:
        print("The most common month is:", df['month'].mode()[0])
    else:
        print("Most common month not shown since month filter is applied")


    # TO DO: display the most common day of week
    if df['week_day'].nunique() > 1:
        print("The most common day is:", df['week_day'].mode()[0])
    else:
        print("Most common day not shown since day filter is applied")

    # TO DO: display the most common start hour
    print("The most common hour is:", df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most common start station is:", df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("The most common end station is:", df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print("The most common combination of start station and end station trip is:\n", df['combo_station'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()

    print("The total travel time:", time.strftime('%H:%M:%S', time.gmtime(total_duration)),'(H:M:S)')

    # TO DO: display mean travel time
    avg_time = df['Trip Duration'].mean()

    print("The average travel time:", time.strftime('%H:%M:%S', time.gmtime(avg_time)),'(H:M:S)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The count of each user type:\n", df['User Type'].value_counts())


    # TO DO: Display counts of gender
    print("\nThe count of each gender:\n", df['Gender'].value_counts())



    # TO DO: Display earliest, most recent, and most common year of birth
    #try statement added because a file may not have the birth year included in the data
    try:
        print("\nThe earliest birth year:", int(df['Birth Year'].min()))
        print("The most recent birth year:", int(df['Birth Year'].max()))
        print("The most common birth year:", int(df['Birth Year'].mode()))

    except:
        print("\nNote: no birth year data is available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
    #counter is utilized to ensure when users want to see more data, its five rows at a time
        i = 0
        j = 5
        while True:
            raw_dat = input('\nWould you like to see 5 new or additional lines of raw data? Enter yes or no.\n')
            if raw_dat.lower() != 'yes':
               break
            elif raw_dat.lower() == 'yes':
                print('\nNote: values of column 1 are the orginal row numbers from the file before filtering\n')
                print(df.iloc[i:j])
                i += 5
                j += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
