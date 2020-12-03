"""
This python file tests the conversion from a esriFieldTypeDate to a human-readable format.
"""

import os
import time

import pickle
import pandas as pd


def readable_date(df):
    """Converts the Date column in a DataFrame to a more readable format.
    
    Parameters
    ----------
    df : Pandas DataFrame instance
        DataFrame containing a "Date" column.

    Returns
    -------
    None

    """
    df["Date"] = df["Date"].apply(lambda t: time.ctime(t / 1000.0))


if __name__ == "__main__":
    # Extract the data and create a Pandas DataFrame object.
    data_path = (
        "/Users/administrator/Documents/Projects/abq_crime/data/processed_data.pkl"
    )
    extracted_data = pickle.load(open(data_path, "rb"))
    data_columns = [
        "Object_ID",
        "Location",
        "Description",
        "Date",
        "Latitude",
        "Longitude",
    ]
    dataset = pd.DataFrame(extracted_data, columns=data_columns)

    # Convert the date to a more readable formrat.
    time_start = time.time()
    readable_date(dataset)
    time_end = time.time()

    # Print some examples.
    print(dataset["Date"].head())
    print("Entire operation took {} seconds.".format(time_end - time_start))
