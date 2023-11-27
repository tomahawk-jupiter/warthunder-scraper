import pandas as pd
import json
import re


def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)


def clean_csv(input_file, output_file):
    df = pd.read_csv(input_file)
    df['plane_name'] = df['plane_name'].apply(remove_non_ascii)
    df.to_csv(output_file, index=False)


def remove_duplicates_and_create_json(csv_file, json_file):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Remove duplicate rows
    df_no_duplicates = df.drop_duplicates()

    # Convert NaN values to empty strings in the DataFrame
    df_no_duplicates = df_no_duplicates.applymap(
        lambda x: '' if pd.isna(x) else x)

    # Write cleaned data to a new CSV file
    df_no_duplicates.to_csv(csv_file, index=False)

    # Convert the DataFrame to a list of dictionaries
    json_data = df_no_duplicates.to_dict(orient='records')

    # Write the list of dictionaries to a JSON file
    with open(json_file, 'w') as json_output:
        json.dump(json_data, json_output, indent=2)


if __name__ == "__main__":
    input_file = 'raw-data.csv'
    output_file = 'clean-data.csv'
    json_file = 'clean-data.json'

    clean_csv(input_file, output_file)
    print(f"Cleaning completed. Cleaned data saved to {output_file}")

    remove_duplicates_and_create_json(output_file, json_file)
    print(
        f"Duplicate removal and JSON creation completed. Cleaned data saved to {output_file}, JSON data saved to {json_file}")
