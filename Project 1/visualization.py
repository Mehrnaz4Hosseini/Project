import json
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read_json_file(json_file):
    """Read the JSON file and return the simulation data."""
    with open(json_file, mode='r') as file:
        data = json.load(file)
    return data

def plot_segmentation_memory_usage(simulation_log, frame_func):
    """Visualize the memory usage in segmentation simulation."""
    fig, ax = plt.subplots()
    time_data = []
    free_memory_data = []
    allocated_memory_data = []

    def update_plot(frame):
        """Update the plot with the current simulation state."""
        state = simulation_log[frame]
        time_data.append(state["time"])
        free_memory_data.append(state["free_memory"])
        allocated_memory = sum([process["needed_memory"] for process in state["allocated_or_in_memory"]])
        allocated_memory_data.append(allocated_memory)

        ax.clear()
        ax.set_title('Segmentation Memory Usage Over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Memory (Units)')
        ax.plot(time_data, free_memory_data, label="Free Memory", color="green")
        ax.plot(time_data, allocated_memory_data, label="Allocated Memory", color="red")
        ax.legend(loc='upper right')
        ax.set_xlim(0, max(time_data) + 1)
        ax.set_ylim(0, max(allocated_memory_data) + 100)

    ani = animation.FuncAnimation(fig, update_plot, frames=len(simulation_log), repeat=False, interval=500)
    frame_func(fig)

def plot_paging_memory_usage(simulation_log, frame_func):
    """Visualize the memory usage in paging simulation."""
    fig, ax = plt.subplots()
    time_data = []
    free_pages_data = []
    allocated_pages_data = []

    def update_plot(frame):
        """Update the plot with the current simulation state."""
        state = simulation_log[frame]
        time_data.append(state["time"])
        free_pages_data.append(state["free_pages"])
        allocated_pages = sum([len(process["allocated_pages"]) for process in state["allocated_processes"]])
        allocated_pages_data.append(allocated_pages)

        ax.clear()
        ax.set_title('Paging Memory Usage Over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Pages')
        ax.plot(time_data, free_pages_data, label="Free Pages", color="green")
        ax.plot(time_data, allocated_pages_data, label="Allocated Pages", color="red")
        ax.legend(loc='upper right')
        ax.set_xlim(0, max(time_data) + 1)
        ax.set_ylim(0, max(allocated_pages_data) + 2)

    ani = animation.FuncAnimation(fig, update_plot, frames=len(simulation_log), repeat=False, interval=500)
    frame_func(fig)

def display_plot_on_tkinter_window(fig, window):
    """Embed the plot into the Tkinter window using canvas."""
    canvas = FigureCanvasTkAgg(fig, master=window)  
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.get_tk_widget().pack()

def visualize_simulation_results(json_file, algorithm_type, window):
    """Visualize the simulation results for either Segmentation or Paging."""
    simulation_log = read_json_file(json_file)

    if algorithm_type == "Segmentation":
        plot_segmentation_memory_usage(simulation_log, lambda fig: display_plot_on_tkinter_window(fig, window))
    elif algorithm_type == "Paging":
        plot_paging_memory_usage(simulation_log, lambda fig: display_plot_on_tkinter_window(fig, window))
    else:
        print("Unknown algorithm type!")

def on_algorithm_choice(event, window, json_file_segmentation, json_file_paging):
    """Handle algorithm choice and start the visualization."""
    choice = algorithm_choice.get()
    if choice == 1:
        visualize_simulation_results(json_file_segmentation, "Segmentation", window)
    elif choice == 2:
        visualize_simulation_results(json_file_paging, "Paging", window)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    json_file_segmentation = "Project 1/segmentation/segmentation_simulation_log.json"
    json_file_paging = "Project 1/paging/paging_simulation_log.json"

    # Set up the Tkinter window
    window = tk.Tk()
    window.title("Memory Allocation Simulation Visualization")

    # Create a label and dropdown menu for choosing the algorithm
    label = ttk.Label(window, text="Choose Memory Allocation Algorithm:")
    label.pack()

    algorithm_choice = tk.IntVar()
    dropdown = ttk.Combobox(window, textvariable=algorithm_choice, values=[1, 2], state="readonly")
    dropdown.set("1")  # Default choice is Segmentation
    dropdown.bind("<<ComboboxSelected>>", lambda event: on_algorithm_choice(event, window, json_file_segmentation, json_file_paging))
    dropdown.pack()

    window.mainloop()
