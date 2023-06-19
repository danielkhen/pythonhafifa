import base64
import datetime
import os
import re
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def word_to_digit(word):
    digits = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }

    return False if word not in digits else digits[word]


# question 2
def list_sum(numbers):
    return 0 if len(numbers) == 0 else numbers[0] + list_sum(numbers[1:])


# question 3
def remove_vowels(string):
    return "".join(re.split("a|i|e|o|u", string))


# question 4
def count_zeros_and_eights(start, end):
    return 0 if start > end else str(start).count('0') + str(start).count('8') + count_zeros_and_eights(start + 1, end)


# question 5
def save_data(file_path, data):
    with open(file_path, 'w') as file:
        for obj in data:
            file.write('"' + obj + '"' if isinstance(obj, str) else str(obj))
            file.write(' ')


def parse(string):
    if string.isnumeric():
        return int(string)

    split = string.split('.')

    if len(split) == 2 and split[0].isnumeric() and split[1].isnumeric():
        return float(string)

    if string == 'True' or string == 'False':
        return string == 'True'

    return string[1:-1]


def load_data(file_path):
    with open(file_path, 'r') as file:
        return [parse(string) for string in file.read().split()]


# question 6
def days_until_next_birthday(date):
    today = datetime.date.today()

    if date > today:
        return date

    birthday_this_year = date.replace(year=today.year)

    if birthday_this_year > today:
        return (birthday_this_year - today).days

    birthday_next_year = date.replace(year=today.year + 1)

    return (birthday_next_year - today).days


# question 7
def copy_dir(source, destination, extensions):
    new_destination = destination + '/' + os.path.basename(source)

    os.mkdir(new_destination)

    for node in os.listdir(source):
        copy(source + '/' + node, new_destination, extensions)


def copy_file(source, destination, extensions):
    if extensions == "any" or os.path.splitext(source)[1] in extensions:
        with open(source, 'r') as source_file:
            contents = source_file.read()

        with open(destination + '/' + os.path.basename(source), 'w') as destination_file:
            destination_file.write(contents)


def copy(source, destination, extensions="any"):
    if os.path.isdir(source):
        copy_dir(source, destination, extensions)
    else:
        copy_file(source, destination, extensions)

#question 8
def decode_and_transfer_containers():
    connection_string = "BlobEndpoint=https://onboardingpractice.blob.core.windows.net/;QueueEndpoint=https://onboardingpractice.queue.core.windows.net/;FileEndpoint=https://onboardingpractice.file.core.windows.net/;TableEndpoint=https://onboardingpractice.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2023-06-19T18:38:31Z&st=2023-06-19T10:38:31Z&spr=https&sig=clPBtBd24RH2yN%2F%2FZ6YKXFHYz0UiMzZWZv4DttlJ8%2FA%3D"


    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    python_container_client = blob_service_client.get_container_client(container="python")
    decoded_container_client = blob_service_client.get_container_client(container="pythondecoded")

    for blob in python_container_client.list_blobs():
        blob_data = python_container_client.download_blob(blob.name).readall()
        decoded_data = base64.b64decode(blob_data)
        decoded_container_client.upload_blob(name=blob.name, data=decoded_data)




if __name__ == "__main__":
    decode_and_transfer_containers()
