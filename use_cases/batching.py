from octopus_client import OctopusClient 

import concurrent.futures

import pyarrow as pa
import pandas as pd

MAX_THRESHOLD = 1000000  

# Define your function to generate embedding
def generate_embedding(partition):
    # Your logic to generate embedding from partition data
    pass

# Function to split a pandas dataframe into halves
def split_dataframe(df, num_rows):
    mid_point = num_rows // 2
    return df.iloc[:mid_point], df.iloc[mid_point:]

# Example usage
def main():
    oc = OctopusClient("52.45.151.229", "8000", "hatem", "password")
    execution = oc.execute("MATCH (h)-[r]-(t) RETURN h, r, t", 20)

    # Poll until job finishes
    status = execution.poll():
    if status == 1:
       sys.exit(1)

    results = execution.output

    # Process partitions
    for partition in results:
        # Convert PyArrow dataframe to Pandas dataframe
        df = partition.to_pandas()

        num_rows = len(df)
        if num_rows >= MAX_THRESHOLD:
            # Split dataframe into halves
            df1, df2 = split_dataframe(df, num_rows)

            # Process halves in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(generate_embedding, [df1, df2])
        else:
            # Process partition as is
            generate_embedding(partition)

if __name__ == "__main__":
    main()


