import random

# SCAN algorithm implementation
def scan_disk_scheduling(requests, head, direction, disk_size):

    requests.sort()  
    seek_sequence = []
    total_seek_count = 0
    response_times = []
    
    # Separate requests into those less than and greater than the initial head position
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    
    # Serve requests based on direction
    if direction == "left":
        for r in reversed(left):
            seek_sequence.append(r)
            total_seek_count += abs(head - r)
            head = r
        # Once we reach the beginning of the disk, move to the other end
        if right:
            total_seek_count += head  # Seek to the beginning (0)
            head = 0
        for r in right:
            seek_sequence.append(r)
            total_seek_count += abs(head - r)
            response_times.append(total_seek_count)
            head = r

    elif direction == "right":
        for r in right:
            seek_sequence.append(r)
            total_seek_count += abs(head - r)
            response_times.append(total_seek_count)
            head = r

        if left:
            total_seek_count += abs(head - (disk_size - 1)) 
            head = disk_size - 1
        for r in reversed(left):
            seek_sequence.append(r)
            total_seek_count += abs(head - r)
            response_times.append(total_seek_count)
            head = r
    
    avg_response_time = sum(response_times) / len(requests)

    return seek_sequence, total_seek_count, avg_response_time


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

seek_sequence, total_seek_count, avg_response_time = scan_disk_scheduling(requests, initial_position, direction, N)


#We can see the requests and seek sequences, but because the large amount of requests(100000) we comment this part.
#print("Requests: ", requests)
#print("Seek sequence: ", seek_sequence)
print("Total seek count: ", total_seek_count)
print("Average response time: ", avg_response_time)