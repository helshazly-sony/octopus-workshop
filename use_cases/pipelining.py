from octopus_client import OctopusClient 

import concurrent.futures
import pyarrow as pa
import pandas as pd
import queue

# Define your function to generate embedding
def generate_embedding(partition):
    # Your logic to generate embedding from partition data
    pass

# Function to fetch partitions and add them to a queue
def fetch_partitions(results, queue):
    while results.has_next():
        partition = results.fetch_next()
        queue.put(partition)

# Function to process partitions from the queue
def process_partitions(queue):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        # Continue processing partitions until the queue is empty
        while not queue.empty():
            partition = queue.get()
            future = executor.submit(generate_embedding, partition)
            futures.append(future)

        # Wait for all processing to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result() 
            except Exception as e:
                print(f"An error occurred: {e}")

# Example usage
def main():
    oc = OctopusClient("52.45.151.229", "8000", "hatem", "password")
    execution = oc.execute("MATCH (h)-[r]-(t) RETURN h, r, t", 20)

    # Poll until job finishes
    status = execution.poll():
    results = execution.output

    # Create a queue to hold partitions
    queue = queue.Queue()

    # Create threads for fetching and processing partitions
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Start the fetching thread
        fetching_thread = executor.submit(fetch_partitions, results, queue)
        # Start the processing thread
        processing_thread = executor.submit(process_partitions, queue)

        # Wait for both threads to finish
        concurrent.futures.wait([fetching_thread, processing_thread])

if __name__ == "__main__":
   main()
