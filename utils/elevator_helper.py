import typing
from typing import List, Tuple

def calculate_service_in_directions(requested_floors: List[int],
                                    current_floor: int) -> Tuple[List[int], List[int]]:
  """
  Creates two list from a input requested_floors list.
  floors_in_up_direction - contains all the floor number which are above the current_floor
  floors_in_down_direction - all floor which are below which are below the current_floor
  """
  requested_list = sorted(requested_floors)
  floors_in_up_direction = [val for val in requested_list if val >= current_floor]
  floors_in_down_direction = [val for val in requested_list if val < current_floor]
  floors_in_down_direction = floors_in_down_direction[::-1]
  return floors_in_up_direction, floors_in_down_direction