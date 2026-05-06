import pandas as pd
import sys
import os

def clean_data(input_csv_path, output_csv_path):
    print(f"Loading data from {input_csv_path}...")
    try:
        df = pd.read_csv(input_csv_path, na_values=['null'])
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)

    print("Cleaning data...")
    # Drop rows with critical missing values
    df.dropna(subset=['Date', 'Time', 'Pickup Location', 'Drop Location'], inplace=True)
    
    # Fill missing ratings with mean
    if 'Driver Ratings' in df.columns:
        df['Driver Ratings'].fillna(df['Driver Ratings'].mean(), inplace=True)
    if 'Customer Rating' in df.columns:
        df['Customer Rating'].fillna(df['Customer Rating'].mean(), inplace=True)

    # Format Date and Time
    df['pickup_date'] = df['Date'].astype(str)
    df['pickup_time'] = df['Time'].astype(str)
    
    # Create a temporary datetime for feature engineering
    temp_datetime = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
    df.dropna(subset=['pickup_date', 'pickup_time'], inplace=True)

    # Feature Engineering
    df['pickup_hour'] = temp_datetime.dt.hour
    df['pickup_day_of_week'] = temp_datetime.dt.dayofweek

    # Rename columns to match backend schema
    rename_mapping = {
        'Booking ID': 'ride_id',
        'Pickup Location': 'pickup_location',
        'Drop Location': 'drop_location',
        'Booking Value': 'fare_amount',
        'Ride Distance': 'trip_distance',
        'Booking Status': 'booking_status',
        'Driver Ratings': 'driver_rating',
        'Customer Rating': 'customer_rating',
        'Vehicle Type': 'vehicle_type',
        'Payment Method': 'payment_method',
        'Reason for cancelling by Customer': 'cancellation_reason'
    }
    df.rename(columns=rename_mapping, inplace=True)

    # Fill NaNs for fare_amount and trip_distance
    df['fare_amount'] = pd.to_numeric(df['fare_amount'], errors='coerce').fillna(0.0)
    df['trip_distance'] = pd.to_numeric(df['trip_distance'], errors='coerce').fillna(0.0)
    
    # Strip quotes from ride_id
    df['ride_id'] = df['ride_id'].str.replace('"', '')

    # Select only required columns
    cols_to_keep = ['ride_id', 'pickup_date', 'pickup_time', 'pickup_location', 'drop_location', 'trip_distance', 'fare_amount', 'booking_status', 'vehicle_type', 'payment_method', 'cancellation_reason', 'driver_rating', 'customer_rating', 'pickup_hour', 'pickup_day_of_week']
    df = df[[c for c in cols_to_keep if c in df.columns]]

    print(f"Data cleaned. Saving to {output_csv_path}...")
    df.to_csv(output_csv_path, index=False)
    print("Done!")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "ncr_ride_bookings.csv")
    output_file = os.path.join(base_dir, "ncr_ride_bookings_cleaned.csv")
    
    if os.path.exists(input_file):
        clean_data(input_file, output_file)
    else:
        print(f"Input file not found at {input_file}. Please ensure the dataset is present.")
