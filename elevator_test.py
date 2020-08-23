import unittest
from elevator import Elevator


class TestElevator(unittest.TestCase):
  """ Tests for Elevator class. """
  def setUp(self) -> None:
    self.elevator_obj = Elevator(
      elevtor_num=0, floor_min=-1, floor_max=10, current_floor=0)

  def test_process_request(self):
    """ Test to check the functionality of process_request method."""
    self.elevator_obj.requested_floors = [2, 3]
    expected_output = [['UP_1', 'UP_1', 'OPEN_DOOR', 'CLOSE_DOOR'],
                       ['UP_1', 'OPEN_DOOR', 'CLOSE_DOOR']]
    self.assertListEqual(self.elevator_obj.process_request(), expected_output)

    self.elevator_obj.requested_floors = [0]
    expected_output = [['DOWN_1', 'DOWN_1', 'DOWN_1', 'OPEN_DOOR', 'CLOSE_DOOR']]
    self.assertListEqual(self.elevator_obj.process_request(), expected_output)

  def test_process_request_mixed_requests(self):
    """ Test to check mixed floors as inputs."""
    self.elevator_obj.requested_floors = [2, 3, -1, 4, 0]
    expected_output = [['OPEN_DOOR', 'CLOSE_DOOR'], #floor0
                       ['UP_1', 'UP_1', 'OPEN_DOOR', 'CLOSE_DOOR'], #floor2
                       ['UP_1', 'OPEN_DOOR', 'CLOSE_DOOR'], #floor3
                       ['UP_1', 'OPEN_DOOR', 'CLOSE_DOOR'], #floor4
                       ['DOWN_1', 'DOWN_1', 'DOWN_1', 'DOWN_1', 'DOWN_1', 'OPEN_DOOR', 'CLOSE_DOOR']] #floor-1
    self.assertListEqual(self.elevator_obj.process_request(), expected_output)

  def test_process_request_other_direction(self):
    """current floor is 0 and request from other direction."""
    self.elevator_obj.requested_floors = [-1]
    expected_output = [['DOWN_1', 'OPEN_DOOR', 'CLOSE_DOOR']]
    self.assertListEqual(self.elevator_obj.process_request(), expected_output)

  def test_process_request_duplicate_floors(self):
    """Test to check multiple floors should be served once."""
    self.elevator_obj.requested_floors = [2, 2, 2, 3, 3]
    expected_output = [['UP_1', 'UP_1', 'OPEN_DOOR', 'CLOSE_DOOR'],
                       ['UP_1', 'OPEN_DOOR', 'CLOSE_DOOR']]
    self.assertListEqual(self.elevator_obj.process_request(), expected_output)

  def test_process_request_less_than_min_floor_requested(self):
    """Test to"""
    self.elevator_obj.requested_floors = [2, -2]
    with self.assertRaises(ValueError):
      self.elevator_obj.process_request()

  def test_process_request_greater_than_max_floor_requested(self):
    self.elevator_obj.requested_floors = [30]
    with self.assertRaises(ValueError):
      self.elevator_obj.process_request()


if __name__ == '__main__':
    unittest.main()