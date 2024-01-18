import boto3
import ray
from concurrent.futures import ThreadPoolExecutor

config={
        "service_name": "s3",
        "s3_endpoint": "http://local-s3-service.ezdata-system.svc.cluster.local:30000",
        "s3_access_key": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJnWUxXc3FYODRFMTNONHJRWlYybUZYakl6RDMyODdjMmFSZDkwempVTDdnIn0.eyJleHAiOjE3MDQ5ODAyMzEsImlhdCI6MTcwNDk3ODQzMSwiYXV0aF90aW1lIjoxNzA0OTAxMzczLCJqdGkiOiIwNzU3ZWMwOC03MjIyLTRiNGEtOTRiNi05MDRmNTQ2OTVjZmEiLCJpc3MiOiJodHRwczovL2tleWNsb2FrLmhwZS1hcHBzLWRldjMtZXphZi5jb20vcmVhbG1zL1VBIiwic3ViIjoiN2U1NDJmMzgtODBmYy00MWIzLWEwYzctZjhhYzIxZjEzYzYyIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoidWEiLCJub25jZSI6IkZBN2Y2LVItLURtcFRpeEdhTTZYbC1sc3JlV3JQZkpZTTN4cHBreEVhSTQiLCJzZXNzaW9uX3N0YXRlIjoiM2IwMTExMDgtNWNhNy00MTNmLWI2MmItOTg5ZDk3ZTNjZmU2IiwiYWNyIjoiMSIsInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIHByb2ZpbGUgZW1haWwiLCJzaWQiOiIzYjAxMTEwOC01Y2E3LTQxM2YtYjYyYi05ODlkOTdlM2NmZTYiLCJ1aWQiOiI2MDAwIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJnaWQiOiI1MDA1IiwibmFtZSI6ImhwZWRlbW8gdXNlcjAxIiwiZ3JvdXBzIjpbInVhLWVuYWJsZWQiLCJvZmZsaW5lX2FjY2VzcyIsImFkbWluIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXVhIl0sInByZWZlcnJlZF91c2VybmFtZSI6ImhwZWRlbW8tdXNlcjAxIiwiZ2l2ZW5fbmFtZSI6ImhwZWRlbW8iLCJwb3NpeF91c2VybmFtZSI6ImhwZWRlbW8tdXNlcjAxIiwiZmFtaWx5X25hbWUiOiJ1c2VyMDEiLCJlbWFpbCI6ImhwZWRlbW8udXNlcjAxQGhwZS5jb20ifQ.NA00q09RT6i8TZzRhKKEe7gtYruzyF7eFhl3qb4FMNhl6BaTnqCHQGddDVOKMk7688zuQECPNN3sWWLf26-kA0U8KZSw8ZfUwK8WNDEn39jhYypMf-DHNNe5XCBMNpnYrBjhHKQMgqTZoc6A_9QtPXnY0Sz9dkSUCwrFfSh0CpLzVwPmA7dPZlu9vPozYWf1qMblMAp80vQRLzZJVpdx5gwR9RCp0t6LAbw9Q9buwCzu6EPyMK8RByGNdhqhkUXqR5txZTZU3L3lpChfDTErVLCxe0lbBvi7RGO8L0uLRHQPSUQrWe6HoYC6i00oMGljRUl213Qa9YR5Dly2Rx_WJg",
        "s3_secret_key": "s3",
        "s3_bucket": "experiments",
       }


# Create an S3 client
client= boto3.client(
        service_name=config.get("service_name"),
        aws_access_key_id=config.get("s3_access_key"),
        aws_secret_access_key=config.get("s3_secret_key"),
        endpoint_url=config.get("s3_endpoint"),
        verify=False
        )

print(client)
#Print Buckets
print(client.list_buckets())
#client.create_bucket(Bucket=config.get("s3_bucket"))

print("========BUCKET OBJECTS", client.list_objects(Bucket=config.get("s3_bucket")))

# Number of workers to use
num_loops = 10

# Number to calculate sum of squares up to
N = 100

# Define the function that calculates the sum of squares
def calculate_sum_of_squares(n):
    return sum(i * i for i in range(1, n + 1))

# Function to distribute the computation and write results
def distributed_task(worker_id, n):
    try:
        # Calculate the result
        result = calculate_sum_of_squares(n)
        
        # Save the result to a local file
        result_file = f"result_{worker_id}.txt"
        with open(result_file, "w") as f:
            f.write(str(result))
        
        # Upload the result file to S3
        # s3_key = f"{s3_bucket}/{result_file}"
        s3_key = f"{result_file}"
        print("result_file:", result_file, "||", "s3_bucket:", config.get("s3_bucket"), "||", "s3_key:", s3_key)
        
        with open(f"{result_file}", "rb") as data:
            client.upload_fileobj(data, config.get("s3_bucket"), s3_key)   
        
        client.download_file(config.get("s3_bucket"), s3_key,"./")
        return s3_key
    except Exception as e:
        return str(e)

# Launch distributed tasks using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=num_loops) as executor:
    task_futures = [executor.submit(distributed_task, i, N) for i in range(num_loops)]
    print("task_futures:", list(task_futures))

print("CUSTOM S3 PATH JOB ENDED")