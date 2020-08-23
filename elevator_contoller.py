""" Add docstring """
from typing import Dict, List, Text, Union
from elevator import Elevator

class Error(Exception):
  """Base class for other exceptions."""
  pass

class NotReady(Error):
  """Raised when non of the elevators are available to take request."""
  pass

class InValidElevator(Error):
  """Raised when a Incorrect elevator id is recieved."""


class ElevatorController:
    """
    ElevatorSystem - Class that contains array of Elevator objects
    self.number_of_elevators = total number of elevators in the system
    self.floor_max = top floor
    self.floor_min = bottom most floor
    self.request_queue = request queue for each lift

    """
    def __init__(self, number_of_elevators: int,
                 floor_min: int, floor_max: int, request_queue: List[int], elevator_positions: List[int] = []) -> None:
      self.number_of_elevators = number_of_elevators
      self.floor_max = floor_max
      self.floor_min = floor_min
      self.elevators = []
      self.request_queue = request_queue

      # safegaurd in case no initial positining of lift is given
      # all start from min floor in that case.
      if len(elevator_positions) == 0:
        elevator_positions = [0] * number_of_elevators

      # create a list of Elevator objects
      for itr in range(0, number_of_elevators):
        new_elevator = Elevator(itr, floor_min, floor_max, elevator_positions[itr])
        self.elevators.append(new_elevator)

    def process_request(self) -> List[List[Text]]:
      """This method is to select elevator and process request."""
      if self.request_queue:
        first_floor = sorted(self.request_queue)[0]
        distance = []
        try:
          # Find optimal elevator.
          elevator_found = False
          for elevator in self.elevators:
            # if the elevator is not running.
            if not elevator.is_running:
              elevator_found = True
              distance.append(abs(elevator.current_floor - first_floor))
            else:
              distance.append(999)
          if not elevator_found:
            raise NotReady('Elevator not ready to process request.')
        except NotReady:
          print ('All the elevators are running and cannot take request at the moment. '
                 'Please try after some time.')
          return [['NOT_READY']]

        # find the elevator with minimum distance for the first floor.
        selected_elevator_num = distance.index(min(distance))
        elevator_selected = self.elevators[selected_elevator_num]

        # assign service queue and set direction
        elevator_selected.requested_floors = self.request_queue
        print('selected eleveator_id = {} which is onfloor = {}'.format(
          elevator_selected.elevtor_num, elevator_selected.current_floor))
        elevator_selected.is_running = True
        return elevator_selected.process_request()
      else:
        raise ValueError('Incorrect Floors')

    def elevator_monitor(self, elevator_id: int) -> Dict[Text, Union[Text, int]]:
      """This method will fetch the elevator status based on elevator id."""
      if elevator_id > self.number_of_elevators or elevator_id < 0:
        raise InValidElevator('Incorrect Elevator Id')
      return self.elevators[elevator_id].get_current_status()

