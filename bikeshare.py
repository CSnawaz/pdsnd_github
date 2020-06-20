
import time
import pandas as pd
import numpy as np
import click
from datetime import timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def choice(prompt, choices=('y', 'n')):
    """Return a valid input from the user given an array of possible answers.
    """

    while True:
        choice = input(prompt).lower().strip()
        # terminate the program if the input is end
        if choice == 'end':
            raise SystemExit
        # triggers if the input has only one name
        elif ',' not in choice:
            if choice in choices:
                break
        # triggers if the input has more than one name
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break

        prompt = ("\nSomething is not right. Please mind the formatting and "
                  "be sure to enter a valid option:\n>")

    return choice

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\nHey! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington).

    validity = False

    while True:


        city = str(input("\nPick a city - (Chicago, New York City or Washington): ").strip().lower())

        if city not in ("chicago", "new york city", "washington"):
            print("\nPlease check the city name.It seems incorrect.")
            continue
        else:
            print("\nGetting few more things to make ready the data you want to  see data for: '{}' ".format(city.title()))
            validation()
            break

    while True:
        month = str(input("\nFrom January to June, for what month do you "
                       "want do filter data? (Pick any (January to June))").strip().lower())

        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print("\nPlease check the month name.It seems incorrect . You can select all of them by typing 'all')")
            continue
        else:
            print("\n Applied for filter by: '{}' Getting few more things to make ready the data you want to  see ".format(month.title()))
            validation()
            break

    while True:
        day = str(input("\nType the name of day to filter. Pick any day (PS format should be- 'Monday'): ").strip().lower())

        if day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday" , "sunday", "all"):
            print("Please check the day.It seems incorrect . You can select all of them by typing 'all')")
            continue
        else:
            print("\nfiltering by: '{}' ".format(day.title()))
            validation()
            break

    print("\nYou have selected '{}' as city, '{}' as month, and '{}' as day. \nFiltering by your parameters....".format(city.title(), month.title(), day.title()))
    print()
    print('-'*50)
    return city, month, day

def validation():

    while True:
        validity = str(input("Is your input correct? Type 'y' to continue and 'n' to restart: \n").strip().lower())
        if validity not in ("y", "n"):
            print("\nInvalid Response. Try one more time!")
            continue
        elif validity == 'y':
            break
        else:
            get_filters()


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

    # convert the Start Time column to datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time and creating new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    # thus if user inputs proper month
    if month != 'all':
       # use the index of the months list to get the corresponding int "order is how months occur!"
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        # month outputted as integer
        month = months.index(month) + 1

        # month column is in type(integer)
        df = df[df['Month'] == month]


    # filtering by the day of week if applicable
    # thus if user inputs day name
    if day != 'all':
        # list of days must be in the order they appear!
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        # day = days.index(day) + 1

        # filter by day of week to create the new dataframe
        df = df[df['Day_of_Week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nDisplaying the statistics on the most frequent times of '
          'travel...\n')
    start_time = time.time()

    # look_up in dictionary
    look_up = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May',
        '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}

    # displays the most common month
    popular_month = df['Month'].mode()[0]
    month_in_string = look_up[str(popular_month)]
    print("- Most common month was: ", month_in_string)

    # displays the most common day
    popular_day = df['Day_of_Week'].mode()[0]
    print("- Most common day of the week was: {}".format(popular_day))

    # display the most common starting hour
    popular_hour = df['Hour'].mode()[0]
    print('- Most common start hour was:', popular_hour)


    print("\nIt took {} seconds." .format(time.time() - start_time))
    print('-'*50)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displays most commonly used start station

    start_station = df['Start Station'].mode()[0]
    print("-For the selected filters, the most common start station was : '{}'".format(start_station))

    # displays most commonly used end station

    end_station = df['End Station'].mode()[0]
    print("-For the selected filters, the most common end station was: '{}'".format(end_station))

    # displays most frequent combination of start station and end station trip

    pair_final = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).reset_index(name="counts")
    frequent_start_pair = pair_final['Start Station'][0]
    frequent_end_pair = pair_final['End Station'][0]

    print("- The start station for most frequent combination is '{}' and the end station is '{}'".format(frequent_start_pair, frequent_end_pair))
    print("\nIt took {} seconds." .format(time.time() - start_time))
    print('-'*50)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displays total travel time

    total_travel_time = df['Trip Duration'].sum()

    t2 = total_travel_time.astype('float64')
    time_in_duration = timedelta(seconds=t2)

    print("For your selected filters, the total travel time is : '{}' which converts to '{}' in duration. ".format(total_travel_time, time_in_duration))

    # displays mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time is: '{}' seconds ".format(mean_travel_time))

    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*50)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # displays counts of user types

    user_type_count = df["User Type"].value_counts()
    print(user_type_count)

    # displays counts of gender
    if "Gender" in df.columns:
        gender_count = df["Gender"].value_counts()
        #Reference "stackoveflow.com"
        # to count null values
        nan_values = df["Gender"].isna().sum()

        print("\nCount by Gender: \n{}\n \n*Note: there were '{}' NaN values for 'Gender' column".format(gender_count,nan_values))
    else:
        print("\nNo column named 'Gender' exists in the selected dataset")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:

        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("\nEarliest birth year is: '{}'. \nMost recent birth year is: '{}'. \nMost common birth year is: '{}'.".format(earliest, most_recent, most_common))

    else:
        print("\nNo column named 'Birth Year' exists in the selected dataset")

        print("\nThis took {} seconds.".format(time.time() - start_time))
        print('-'*50)


# Modified Version of the code in following url reference:
# Reference: https://knowledge.udacity.com/questions/26261


def raw_data(df):

    # initial input!
    display_raw_input = input("\nWould you like to see individual raw data? Enter 'yes' or 'no'\n").strip().lower()
    if display_raw_input in ("yes", "y"):
        i = 0

        # use while loop for the inputs that you want repeated!
        # thus should start here, not at the beginning of the code

        while True:
            # check if i is out of bounds, if upper limit is out of bounds,
            # then print from lower limit to length of dataframe rows
            if (i + 5 > len(df.index) - 1):
                # remember that the slicing is lower bound inclusive and upper bound exclusive!!
                # thus upper bound should be (len(df.index) --> won't print out that upper bound bc its exclusive)
                print(df.iloc[i:len(df.index), :])
                print("You've reached the end of the rows")
                break

            # if i is not out of bounds, then just print the dataframe normally
            print(df.iloc[i:i+5, :])
            i += 5

            # program temporarily halts at the input!
            # thus while loop does not get executed 100000 times (exaggerated) a second lol
            show_next_five_input = input("\nWould you like view the next five[5] rows? Enter 'yes' or 'no'\n").strip().lower()
            if show_next_five_input not in ("yes", "y"):
                break # break out of while loop above


def main():
    while True:
        click.clear()#clear the previous screen output
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = choice('\nWould you like to restart? Enter [y]yes or [n]no.\n')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()
