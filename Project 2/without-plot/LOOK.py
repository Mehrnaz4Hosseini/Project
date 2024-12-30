import random

# LOOK algorithm implementation
def look_disk_scheduling(requests, head, direction):
    
    requests.sort()  # Sort the requests
    seek_sequence = []
    total_seek_time = 0
    response_times = []
    
    # Separate requests into those less than and greater than the head
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    
    if direction == "left":
        # Process requests to the left of the head first
        for r in reversed(left):
            seek_sequence.append(r)
            total_seek_time += abs(head - r)
            response_times.append(total_seek_time)
            head = r
        # Process requests to the right of the head
        for r in right:
            seek_sequence.append(r)
            total_seek_time += abs(head - r)
            response_times.append(total_seek_time)
            head = r
    
    elif direction == "right":
        # Process requests to the right of the head first
        for r in right:
            seek_sequence.append(r)
            total_seek_time += abs(head - r)
            response_times.append(total_seek_time)
            head = r
        # Process requests to the left of the head
        for r in reversed(left):
            seek_sequence.append(r)
            total_seek_time += abs(head - r)
            response_times.append(total_seek_time)
            head = r
    
    # Calculate average response time
    avg_response_time = sum(response_times) / len(requests)
    
    return seek_sequence, total_seek_time, avg_response_time



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

seek_sequence, total_seek_count, avg_response_time = look_disk_scheduling(requests, initial_position, direction)

#We can see the requests and seek sequences, but because the large amount of requests(100000) we comment this part.
#print("Requests: ", requests)
#print("Seek sequence: ", seek_sequence)
print("Total seek count: ", total_seek_count)
print("Average response time: ", avg_response_time)