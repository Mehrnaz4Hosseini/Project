import random

# C-SCAN algorithm implementation
def c_scan_disk_scheduling(requests, head, direction, disk_size):

    requests.sort()  
    seek_sequence = []
    total_seek_time = 0
    response_times = []
    
    # Separate requests into those less than and greater than the initial head position
    right = [r for r in requests if r >= head]
    left = [r for r in requests if r < head]
    
    # Serve requests based on direction
    if direction == "right":
        for r in right:
            seek_sequence.append(r)
            total_seek_time += abs(head - r)
            response_times.append(total_seek_time)
            head = r
        
        if left:
            total_seek_time += abs(head - (disk_size - 1))  # Seek to the end of the disk
            head = 0  # Jump to the start
            total_seek_time += disk_size - 1  # jump from end to start
        
        # Process the remaining requests on the left
        for r in left:
            seek_sequence.append(r)
            total_seek_time += abs(head - r)
            response_times.append(total_seek_time)
            head = r
    
    elif direction == "left":
        for r in reversed(left):
            seek_sequence.append(r)
            total_seek_time += abs(head - r)
            response_times.append(total_seek_time)
            head = r
        
        if right:   
            total_seek_time += head  # Seek to the beginning (0)
            head = disk_size - 1  # Jump to the end
            total_seek_time += disk_size - 1  # jump from start to end
        
        # Process the remaining requests on the right
        for r in reversed(right):
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

seek_sequence, total_seek_count, avg_response_time = c_scan_disk_scheduling(requests, initial_position, direction, N)

#We can see the requests and seek sequences, but because the large amount of requests(100000) we comment this part.
#print("Requests: ", requests)
#print("Seek sequence: ", seek_sequence)
print("Total seek count: ", total_seek_count)
print("Average response time: ", avg_response_time)
