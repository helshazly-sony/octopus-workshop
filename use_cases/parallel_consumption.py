from octopus_client import OctopusClient 

import concurrent.futures

# Define your function to generate embedding
def generate_embedding(partition):
    # Your logic to generate embedding from partition data
    pass

# Example usage
def main():
    oc = OctopusClient("52.45.151.229", "8000", "hatem", "password")
    execution = oc.execute("MATCH (h)-[r]-(t) RETURN h, r, t", 20)

    # Poll until job finishes
    status = execution.poll():

    result = execution.output

    # Fetch partitions in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        partition_futures = [executor.submit(result.fetch_next()) for _ in range(20)]
        partitions = [future.result() for future in concurrent.futures.as_completed(partition_futures)]

    # Process partitions in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(generate_embedding, partitions)

if __name__ == "__main__":
    main()
