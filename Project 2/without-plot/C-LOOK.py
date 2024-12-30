import random
import matplotlib.pyplot as plt

# C-LOOK algorithm implementation
def c_look(requests, head, direction):

    requests.sort()  # Sort the requests
    seek_sequence = []
    seek_count = 0
    response_times = []

    # Separate requests into those less than and greater than the head
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    if direction == 'right':
        # Service the right side first
        for r in right:
            seek_sequence.append(r)
            seek_count += abs(head - r)
            response_times.append(seek_count)
            head = r

        # Jump to the beginning of the left requests (circular movement)
        if left:
            seek_count += abs(head - left[0])  # Jump cost
            head = left[0]

        # Service the left side
        for r in left:
            seek_sequence.append(r)
            seek_count += abs(head - r)
            response_times.append(seek_count)
            head = r

    elif direction == 'left':
        # Service the left side first
        for r in reversed(left):
            seek_sequence.append(r)
            seek_count += abs(head - r)
            response_times.append(seek_count)
            head = r

        # Jump to the end of the right requests (circular movement)
        if right:
            seek_count += abs(head - right[-1])  # Jump cost
            head = right[-1]

        # Service the right side
        for r in reversed(right):
            seek_sequence.append(r)
            seek_count += abs(head - r)
            response_times.append(seek_count)
            head = r

    average_response_time = sum(response_times) / len(requests)

    return seek_sequence, seek_count, average_response_time


# Set up a normal distribution for cylinder numbers
N = int(input("Number of cylinders: "))  # Number of cylinders
mean = N / 2
std_dev = N / 5

# Initial position of the disk head
initial_position = int(input("Initial position of the disk head: "))

#Direction
direction = input("Specify the head direction (right or left): ")

# Number of requests
num_requests = 100000
requests = [int(min(max(random.gauss(mean, std_dev), 0), N)) for _ in range(num_requests)]

seek_sequence, total_seek_count, avg_response_time = c_look(requests, initial_position, direction)

#We can see the requests and seek sequences, but because the large amount of requests(100000) we comment this part.
#print("Requests: ", requests)
#print("Seek sequence: ", seek_sequence)
print("Total seek count: ", total_seek_count)
print("Average response time: ", avg_response_time)
