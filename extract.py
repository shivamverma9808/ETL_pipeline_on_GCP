import csv
from faker import Faker
import random
import string
from google.cloud import storage

# Specify number of employees to generate
num_employees = 100

# Create Faker instance
fake = Faker()

# Define the character set for the password
password_characters = string.ascii_letters + string.digits + 'm'

# Generate employee data and save it to a CSV file
with open('employee_data.csv', mode='w', newline='') as file:
    fieldnames = ['first_name', 'last_name', 'job_title', 'department', 'email', 'address', 'phone_number', 'salary', 'password']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for _ in range(num_employees):
        writer.writerow({
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "job_title": fake.job().replace(",", " "),       # ✅ remove commas
            "department": fake.job().replace(",", " "),      # ✅ remove commas
            "email": fake.email(),
            "address": fake.city().replace("\n", " "),       # ✅ remove line breaks
            "phone_number": fake.phone_number(),
            "salary": fake.random_number(digits=5),
            "password": ''.join(random.choice(password_characters) for _ in range(8))
        })

# Upload the CSV file to a GCS bucket
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client(project="stellar-builder-379618")  # ✅ Fixed with your project ID
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f'File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.')

# Set your GCS bucket name and destination file name
bucket_name = 'bkt-employee_data'   
source_file_name = 'employee_data.csv'
destination_blob_name = 'employee_data.csv'

# Upload the CSV file to GCS
upload_to_gcs(bucket_name, source_file_name, destination_blob_name)
