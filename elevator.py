"""Elevator class to represent each Elevator"""
import time
from utils import elevator_helper as eh
from typing import Dict, List, Text, Union

class Elevator:
    """
    Elevator class represents a single Elevator
    The Elevator can  Move up and down, can decide which direction to move based on input request and current_floor.
    The Elevator can keep a state of doors i.e open and close door.
    """
    def __init__(self,
                 elevtor_num: int, floor_min: int, floor_max: int, current_floor: int = 0) -> None:
      self.elevtor_num = elevtor_num
      self.floor_max = floor_max
      self.floor_min = floor_min
      self.is_running = False
      self._door_open = True
      self.current_floor = current_floor
      self.direction = 1 # 1 for up, -1 for down
      self.requested_floors = []
      self._path = []
      self._traversed_path = []

    def get_door_status(self):
      return self._door_open

    def _open_door(self):
      self._door_open = True
      self._path.append('OPEN_DOOR')

    def _close_door(self):
      self._door_open = False
      self._path.append('CLOSE_DOOR')

    def process_destination_floor(self):
      self._open_door()
      # wait for passengers to move out.
      time.sleep(1)
      self._close_door()
      self._traversed_path.append(self._path)
      self._path = []


    def execute_request(self, list_of_request: List[int]):
      while True:
        self.is_running = True
        # if current floor in not in the boundary.
        if self.current_floor < self.floor_min or self.current_floor > self.floor_max:
          raise ValueError("InValid Floor")
        if self.current_floor in list_of_request:
          # Remove all occurences of the matching floor.
          list_of_request = list(filter((self.current_floor).__ne__, list_of_request))
          # stop the lift, as it has reached one of its destination
          self.is_running = False
          self.process_destination_floor()

        if len(list_of_request) == 0:
          # if we have processed all list of request - break
          break
        self.move_one_step()

    def move_one_step(self):

      # move_one_step : moves Elevator one step up or down based on direction
      self.current_floor = self.current_floor + self.direction
      # direction can have value of 1 for up or -1 for down
      if self.direction == 1:
        move = 'UP_1'
      elif self.direction == -1:
        move = 'DOWN_1'
      else:
        move = 'UNKNOWN_MOVE'
      self._path.append(move)


    def process_request(self) -> List[Text]:
      """
        This method will be called by elevator_controller to handle cases wherein
        someone requested to go to a floor from outside or when someone requested from inside.
      """
      print("Requested Floors = {}, current lift position = {}".format(
        self.requested_floors, self.current_floor))
      floors_in_up_direction, floors_in_down_direction = eh.calculate_service_in_directions(
        self.requested_floors, self.current_floor)
      # If there is nothing to process in either direction start moving in opposite direction.
      if len(floors_in_up_direction) == 0:
        self.direction = -1
      elif len(floors_in_down_direction) == 0:
        self.direction = 1
      else:
        # calculate cost and then decide direction, this strategy can be optimised
        # currently it just checks the first request for cost calculation
        # cost_up is the distance between first up floor and current floor
        cost_up = abs(floors_in_up_direction[0] - self.current_floor)
        # cost_down = distance between first down floor and current floor
        cost_down = abs(floors_in_down_direction[0] - self.current_floor)
        # choose direction
        self.direction = 1 if cost_up <= cost_down else -1

      for turn in range(0,2):
        # execute for both the directions.
        if self.direction == -1:
          self.execute_request(floors_in_down_direction)
        else:
          self.execute_request(floors_in_up_direction)
        # reverse the direction
        self.direction = - self.direction

      # all done, reset the lift parameters
      value_to_return = self._traversed_path
      self.reset_lift_params()
      return value_to_return

    def get_current_status(self) -> Dict[Text, Union[Text, int]]:
      return ({'door':'Open' if self._door_open else 'Close',
               'running': self.is_running,
               'direction': 'Up' if self.direction == 1 else 'Down',
               'current_floor': self.current_floor})

    def reset_lift_params(self) -> None:
        # when request finishes reset the direction
        self.direction = 1
        self.is_running = False
        self.requested_floors = []
        self._path = []
        self._traversed_path = []