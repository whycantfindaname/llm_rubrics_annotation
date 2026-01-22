"""
This simulation models a ride queue system with two types of tubes:
- Single-person tubes (S-tubes)
- Double-person tubes (D-tubes)

The system manages riders in a queue, assigning them to available tubes based on specific rules.
Riders with vowel-named IDs have a wait limit to prevent starvation.
Tubes take multiple turns to complete a ride, after which riders return to the queue.
"""
from collections import deque

class RideSimulator:
    """Simulates a ride facility scheduling system"""
    
    def __init__(self, riders, num_single_tubes, num_double_tubes, max_wait, single_ride_time, double_ride_time):
        """
        Initialize the ride simulator
        
        Args:
            riders: List of riders
            num_single_tubes: Number of single-person tubes
            num_double_tubes: Number of double-person tubes
            max_wait: Maximum wait count (unused)
            single_ride_time: Ride time for single-person tubes
            double_ride_time: Ride time for double-person tubes
        """
        # Set of vowel characters to identify vowel riders
        self.vowel_chars = set('AEIOU')
        # Queue of riders waiting for the ride
        self.rider_queue = deque(riders)
        # Wait count for vowel riders to prevent starvation
        self.vowel_rider_wait_count = {r: 0 for r in riders if r[0] in self.vowel_chars}
        
        # Initial configuration
        self.total_single_tubes = num_single_tubes
        self.total_double_tubes = num_double_tubes
        self.single_ride_time = single_ride_time
        self.double_ride_time = double_ride_time
        
        # Currently available tubes
        self.available_single_tubes = num_single_tubes
        self.available_double_tubes = num_double_tubes
        
        # List of running tubes, format: (tube_type, remaining_time, riders_list)
        self.running_tubes = []

    def is_vowel_rider(self, rider):
        """Check if rider ID starts with a vowel"""
        return rider[0] in self.vowel_chars

    def simulate_turn(self):
        """Simulate one turn of operation"""
        assigned = False
        current_queue = list(self.rider_queue)
        index = 0
        
        # Try to assign riders to tubes
        while index < len(current_queue) and not assigned:
            rider = current_queue[index]
            
            # Prioritize double-person tubes
            if self.available_double_tubes > 0:
                self.available_double_tubes -= 1
                # Double-person tubes need two riders
                riders_assigned = [self.rider_queue.popleft()]
                if self.rider_queue:
                    riders_assigned.append(self.rider_queue.popleft())
                # Add to running tubes list
                self.running_tubes.append(('d', self.double_ride_time, riders_assigned))
                assigned = True
            
            # Assign to single-person tubes
            elif self.available_single_tubes > 0:
                # Check if vowel rider hasn't waited too long
                if self.is_vowel_rider(rider) and self.vowel_rider_wait_count.get(rider, 0) < 2:
                    self.vowel_rider_wait_count[rider] += 1
                    index += 1
                else:
                    # Assign to single-person tube
                    self.available_single_tubes -= 1
                    self.rider_queue.popleft()
                    self.running_tubes.append(('s', self.single_ride_time, [rider]))
                    assigned = True
            else:
                break
        
        # Update remaining time for all running tubes
        for i in range(len(self.running_tubes) - 1, -1, -1):
            tube_type, remaining_time, riders = self.running_tubes[i]
            # Decrease remaining time
            self.running_tubes[i] = (tube_type, remaining_time - 1, riders)
            
            # Check if tube has completed the ride
            if self.running_tubes[i][1] <= 0:
                # Return riders to queue
                for rider in riders:
                    self.rider_queue.append(rider)
                    # Reset wait count for vowel riders
                    if rider in self.vowel_rider_wait_count:
                        self.vowel_rider_wait_count[rider] = 0
                
                # Remove completed tube
                del self.running_tubes[i]
                # Release tube resource
                if tube_type == 's':
                    self.available_single_tubes += 1
                else:
                    self.available_double_tubes += 1

    def display_status(self, turn, action=None):
        """Display current status of the simulation"""
        print(f"Turn {turn}:")
        if action:
            print(f"  Action: {action}")
        print(f"  Queue: {list(self.rider_queue)}")
        print(f"  Running Tubes: {[(t, rt, rs) for t, rt, rs in self.running_tubes]}")
        print(f"  Available Tubes: Single={self.available_single_tubes}, Double={self.available_double_tubes}")
        print("-" * 60)

    def run_simulation(self, num_turns):
        """Run the complete simulation"""
        for turn in range(1, num_turns + 1):
            # Display status at the start of the turn
            self.display_status(turn, "Starting turn")
            # Execute turn simulation
            self.simulate_turn()
            # Display updated status after turn actions
            self.display_status(turn, "After turn actions")


def main():
    """Main function to initialize and run the simulation"""
    # Generate rider list A-Z (22 riders)
    riders = list("ABCDEFGHIJKLMNOPQRSTUV")
    
    # Configuration parameters
    num_single_tubes = 5  # Number of single-person tubes
    num_double_tubes = 1   # Number of double-person tubes
    single_ride_time = 5   # Ride time for single-person tubes
    double_ride_time = 4   # Ride time for double-person tubes
    
    # Create and run the simulator
    simulator = RideSimulator(riders, num_single_tubes, num_double_tubes, 2, single_ride_time, double_ride_time)
    simulator.run_simulation(20)

