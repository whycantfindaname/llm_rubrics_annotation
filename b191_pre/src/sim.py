from collections import deque

class TubeRideSimulation:
    """
    The simulation manages a queue of riders waiting for single and double inner tubes at a water park. 
    Riders are prioritized for double tubes if available. For single tubes, riders whose names start 
    with a vowel will hesitate and let others pass up to two times before taking a tube. Once a rider 
    or pair of riders gets a tube, they occupy it for a set duration, after which they return to the 
    back of the line and the tube becomes available again. The simulation runs for a specified number 
    of turns, tracking the state of the line, active rides, and tube availability.
    """

    def __init__(self, riders, num_single_tubes, num_double_tubes, max_wait_skips, single_ride_time, double_ride_time):
        self.riders = riders
        self.vowels = set('AEIOU')
        self.line = deque(riders)
        # Track how many times a vowel rider has skipped a single tube
        self.wait_skips = {r: 0 for r in riders if r[0] in self.vowels}
        self.num_single_tubes = num_single_tubes
        self.num_double_tubes = num_double_tubes
        self.max_wait_skips = max_wait_skips
        self.single_ride_time = single_ride_time
        self.double_ride_time = double_ride_time
        self.available_single_tubes = num_single_tubes
        self.available_double_tubes = num_double_tubes
        self.active_rides = []

    def is_vowel_rider(self, rider):
        """Check if the rider's name starts with a vowel."""
        return rider[0] in self.vowels

    def run_turn(self):
        """
        Simulate a single turn. 
        Assigns tubes to riders if available and updates active rides.
        Returns a description of the action taken.
        """
        assigned = False
        action_taken = "No riders assigned to tubes."
        temp_line = list(self.line)
        i = 0
        
        # Try to assign a tube to riders in the line
        while i < len(temp_line) and not assigned:
            rider = temp_line[i]
            
            # Priority: Check for double tubes first
            if self.available_double_tubes > 0:
                self.available_double_tubes -= 1
                # Take two riders for the double tube
                riders_in_double = [self.line.popleft()]
                if self.line:
                    riders_in_double.append(self.line.popleft())
                
                self.active_rides.append(('double', self.double_ride_time, riders_in_double))
                action_taken = f"Assigned double tube to {riders_in_double}."
                assigned = True
                
            # Check for single tubes
            elif self.available_single_tubes > 0:
                # Vowel riders hesitate if they haven't waited enough
                if self.is_vowel_rider(rider) and self.wait_skips.get(rider, 0) < self.max_wait_skips:
                    self.wait_skips[rider] += 1
                    i += 1 # Skip this rider
                else:
                    self.available_single_tubes -= 1
                    self.line.popleft() 
                    self.active_rides.append(('single', self.single_ride_time, [rider]))
                    action_taken = f"Assigned single tube to {[rider]}."
                    assigned = True
            else:
                # No tubes available
                break

        # Update active rides (decrement time, return returned riders to line)
        for i in range(len(self.active_rides) - 1, -1, -1):
            tube_type, time_remaining, riders_list = self.active_rides[i]
            self.active_rides[i] = (tube_type, time_remaining - 1, riders_list)
            
            if self.active_rides[i][1] <= 0:
                # Ride finished
                for r in riders_list:
                    self.line.append(r)
                    if r in self.wait_skips:
                        self.wait_skips[r] = 0 # Reset skip count
                
                del self.active_rides[i]
                
                if tube_type == 'single':
                    self.available_single_tubes += 1
                else:
                    self.available_double_tubes += 1
                    
        return action_taken

    def display_status(self, turn):
        """Display the current state of the simulation."""
        print(f"  Line: {list(self.line)}")
        # Format active rides for display
        rides_display = [(t, tm, r) for t, tm, r in self.active_rides]
        print(f"  Active Rides: {rides_display}")

    def run(self, num_turns):
        """Run the simulation for a specified number of turns."""
        for turn in range(1, num_turns + 1):
            print(f"Turn {turn} Start:")
            self.display_status(turn)
            
            action = self.run_turn()
            
            print(f"  Action: {action}")
            print("-" * 40)

def main():
    riders = list("ABCDEFGHIJKLMNOPQRSTUV")
    num_single = 5
    num_double = 1
    single_time = 5
    double_time = 4
    
    simulation = TubeRideSimulation(riders, num_single, num_double, 2, single_time, double_time)
    simulation.run(20)
