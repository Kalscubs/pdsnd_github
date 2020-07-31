import time
import pandas as pd
import numpy as np
import datetime as dt

"""  Sources used:  
     udacity.com, 
     https://docs.python.org/3/contents.html,
     https://www.w3schools.com/python/
     https://www.w3resource.com/python-exercises/
     https://www.geeksforgeeks.org/
     https://stackoverflow.com/
     https://datatofish.com/python-tutorials/
     https://pandas.pydata.org/pandas-docs/stable/reference/
"""

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# months list
months = ['january', 'february', 'march', 'april', 'may', 'june']
# weekdays list
weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday']


def ConvertSectoDayHrMin(n_seconds):
    """Takes number of seconds in the input and calculates and prints
       number of days, hrs, mins, and seconds.
    """

    numofdays = n_seconds // (24 * 3600)
    n_seconds = n_seconds % (24 * 3600)
    numofhours = n_seconds // 3600
    n_seconds %= 3600
    numofminutes = n_seconds // 60
    n_seconds %= 60
    numofseconds = n_seconds

    print(int(numofdays), "days,", int(numofhours), "hours,",
          int(numofminutes), "minutes, and",
          "{:.2f}".format(numofseconds), "seconds")


def validate(selection, category):
    """Takes user entered data and category (eg city, month, day of the week), and ask user to confirm and
       returns Y or N, based on user confirming to information.
    """
    # static prompt
    validation_prompt = "Please confirm 'Y' or 'N' >> "

    while True:
        print(f"\nYou have chosen to view data for {category}: {selection} ")
        user_confirmation = str(input(validation_prompt)).strip().upper()
        # if input is end, terminate the program
        if 'END' in user_confirmation:
            print('*' * 20, "Thank you, goodbye.", '-' * 20)
            raise SystemExit
        elif user_confirmation in ('Y', 'N'):
            break
        else:
            print("\n --- Please enter valid option. ---- \n\n\n")
    return user_confirmation


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    #  static strings to be used as prompt when request for input
    city_prompt = "\nPlease choose city(ies)  (separated by comma) would you like to see data for: Chicago, New York City, Washington\n>> "
    month_prompt = "\nPlease choose which month(s) from January to June (separated by comma) or 'all' you would like to see data for:\n>> "
    dow_prompt = "\nPlease choose the day(s) of the week from Sunday to Saturday (separated by commaa) or 'all' you would like to see data for:\n>> "

    print("\n\n", '*' * 20, "Hello! Let's explore some US bikeshare data!", '*' * 20, "\n")
    print("\n>>>>  Type 'end' at any time if you would like to exit the program. <<<<\n")
    print('=' * 80)

    # Collect user input for city
    while True:
        city = str(input(city_prompt))
        city = [i.strip().lower() for i in city.split(',')]

        # if input is end, terminate the program
        if 'end' in city:
            print('*' * 20, "Thank you, goodbye.", '-' * 20)
            raise SystemExit
        else:
            if list(filter(lambda x: x in CITY_DATA.keys(), city)) == city:
                user_confirmation = validate(city, 'city(ies)')
                if user_confirmation == 'Y':
                    break
                else:
                    print("\nLet's try this again!")
            else:
                print("\n --- Please enter valid option. ---- \n\n\n")

    # Collect user input for Month
    print('=' * 80)
    while True:
        month = str(input(month_prompt))
        month = [i.strip().lower() for i in month.split(',')]
        # if input is end, terminate the program
        if 'end' in month:
            print('*' * 20, "Thank you, goodbye.", '-' * 20)
            raise SystemExit
        elif 'all' in month:
            month = months
            user_confirmation = validate(month, 'Month')
            if user_confirmation == 'Y':
                break
            else:
                print("\nLet's try this again!")
        else:
            if list(filter(lambda x: x in months, month)) == month:
                user_confirmation = validate(month, 'Month')
                if user_confirmation == 'Y':
                    break
                else:
                    print("\nLet's try this again!")
            else:
                print("\n --- Please enter valid option. ---- \n\n\n")

    # Collect user input for Day(s) of the week
    print('=' * 80)
    while True:
        day = str(input(dow_prompt))
        day = [i.strip().lower() for i in day.split(',')]

        # if input is end, terminate the program
        if 'end' in day:
            print('*' * 20, "Thank you, goodbye.", '-' * 20)
            raise SystemExit
        elif 'all' in day:
            day = weekdays
            user_confirmation = validate(day, 'Day of the Week')
            if user_confirmation == 'Y':
                break
            else:
                print("\nLet's try this again!")
        else:
            if list(filter(lambda x: x in weekdays, day)) == day:
                user_confirmation = validate(day, 'Day of the Week')
                if user_confirmation == 'Y':
                    break
                else:
                    print("\nLet's try this again!")
            else:
                print("\n --- Please enter valid option. ---- \n")

    # Print Summary
    print('=' * 80)
    print("\n\n", '=' * 40, "Summary of your selection:", '=' * 40, "\n")
    print("City(ies): ", city, "\n")
    print("Month(s): ", month, "\n")
    print("Day(s) of the week: ", day, "\n")
    print('=' * 100)
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

    # Load Data
    print("\nLoading Data Based On Your Selection of City(ies), Month(s), and Day(s) of the week.....")

    #  capture start time
    start_time = time.time()

    # read data from csv file and filter the data according to the selected city/cities
    df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city), sort=True)

    # reorganize DataFrame columns after a cities concat as these columns will be used
    # for other functions.
    try:
        df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                 'Trip Duration', 'Start Station',
                                 'End Station', 'User Type', 'Gender',
                                 'Birth Year'])
    except:
        print("Message:  Reindex did not work!")
        pass

    # Convert and create new columns to show statistics results
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour


    # filter the data according to month into new DataFrame
    df = pd.concat(map(lambda month: df[df['Month'] ==
                       (months.index(month)+1)], month))

    # filter the data according to weekday into new DataFrame
    df = pd.concat(map(lambda day: df[df['Weekday'] ==
                       (day.title())], day))

    # calculate and print processing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)
    return df  # return dataframe based on filtered data


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # determine the most common month
    most_common_month = df['Month'].mode()[0]

    # display name of the month by taking numeric representation and match to index position in the months list.
    # In the month list January is represented by 0, meanwhile pandas January is represented by 1.
    print('Most popular travel month is: ', str(months[most_common_month - 1]).title())

    # determine and print the most common day of week
    print('Most popular day of the week is: ', str(df['Weekday'].mode()[0]))

    # determine and print the most common day of week
    print('Most popular start hour is: ', str(df['Start Hour'].mode()[0]))

    # calculate and print processing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Determine and print the most commonly used start station
    print("Most popular start station is: ", str(df['Start Station'].mode()[0]))

    # Determine and print the most commonly used end station
    print("Most popular end station is: ", str(df['End Station'].mode()[0]))

    # Determine and print most frequent combination of start station and end station trip
    # Create new column, start and end combination , in the dataframe.
    df['Start-End Stations Combination'] = (df['Start Station'] + ' --> ' + df['End Station'])
    print("Most popular start-end stations combination is: ", str(df['Start-End Stations Combination'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is: ")
    ConvertSectoDayHrMin(total_travel_time)


    # calculate and display mean travel time
    # function ConvertSectoDayHrMin calculates and prints days, hrs, mins, secs
    mean_travel_time = df['Trip Duration'].mean()
    print("\nThe mean travel time is: ")
    ConvertSectoDayHrMin(mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # calculate and display user types distribution
    print(f"User Types Distribution:\n\n{df['User Type'].value_counts(dropna=False).to_string()}")

    # calculate and display gender types distribution
    print("\nGender Type Distribution:\n")
    # check Gender column to see if least 1 record has value (ie not NAN).  If true then calculate and prints counts.
    if (df['Gender'].notna().values.any()):
        print(df['Gender'].value_counts(dropna=False).to_string())
    else:
        print("Oops...Gender data not available for the selected criteria")

    # calculate and display earliest, most recent, and most common year of birth
    print("\nEarliest, Most Recent, and Most Common Year of birth:\n")
    # check Birth Year column to see if least 1 record has value (ie not NAN).  If true then calculate and prints counts.
    if (df['Birth Year'].notna().values.any()):
        print("Earliest Year of Birth (ie oldest person): ", str(int(df['Birth Year'].min())))
        print("Most Recent Year of Birth (ie youngest person): ", str(int(df['Birth Year'].max())))
        print("Most Common Year of Birth: ", str(int(df['Birth Year'].mode()[0])))
    else:
        print("Oops...Birth Year data not available for the selected criteria")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def raw_data(df):
    """Displays bikeshare raw data."""

    # predefined prompt questions
    raw_data_init_prompt = "\nEnter 'Y' if you like to see raw data (5 lines at a time, sorted by Start Time, Desc), " \
                           "otherwise press enter to skip\n>> "

    raw_data_continue_prompt = "\nEnter 'Y' to see next 5 lines, otherwise press enter to skip\n>> "

    # Initial question to confirm with user on whether to see raw data or not
    raw_data_user_answer = str(input(raw_data_init_prompt)).strip().upper()
    if raw_data_user_answer == 'Y':
        # sort dataframe based on start time column, starting with most recent (desc)
        df = df.sort_values(['Start Time'], ascending=False)
        current_position = 0  # holds current position of record to be used to display specific records
        while True:
            for i in range(current_position, len(df.index)):
                print("\n")
                print(df.iloc[current_position:current_position + 5].to_string())
                current_position += 5

                # Only ask question if current position has not reached length of df.index.
                if current_position < len(df.index):
                    # ask question if want to see next 5 records
                    raw_data_user_answer = str(input(raw_data_continue_prompt)).strip().upper()
                    if raw_data_user_answer == 'Y':
                        continue
                    else:   # user does not want to see additional records
                        print("Ending raw data display. \n")
                        print('-' * 60)
                        break
                else:  # This is executed if reached to the last record)
                        print("End of data....\n")
                        print('-' * 60)
                        break
            break
    else:
        print("Skipping raw data display. \n")
        print('-' * 60)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input("\nEnter 'Y' to restart, else just enter to exit.\n>> ")
        if restart.lower() != 'y':
            print("\n\n", '*' * 20, "Good Bye!!!!!", '*' * 20, "\n")
            break



if __name__ == "__main__":
    main()
