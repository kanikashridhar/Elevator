import unittest
from elevator_contoller import ElevatorController


class TestElevatorController(unittest.TestCase):
  """ Tests for Elevator Controller class. """
  def setUp(self) -> None:
    self.ec_obj = ElevatorController(
      number_of_elevators=3, floor_min=-1, floor_max=10, request_queue=[])

  def test_controller_setup(self):
    self.assertEqual(self.ec_obj.number_of_elevators, 3)
    self.assertEqual(self.ec_obj.floor_min, -1)
    self.assertEqual(self.ec_obj.floor_max, 10)

  def test_process_request(self):
    # elevator=0 will process the request
    self.ec_obj.request_queue = [2, 3]
    expected_output = [['UP_1', 'UP_1', 'OPEN_DOOR', 'CLOSE_DOOR'],
                       ['UP_1', 'OPEN_DOOR', 'CLOSE_DOOR']]
    self.assertListEqual(self.ec_obj.process_request(), expected_output)

    # elevator=1 will process the request
    self.ec_obj.request_queue = [0]
    expected_output = [['OPEN_DOOR', 'CLOSE_DOOR']]
    self.assertListEqual(self.ec_obj.process_request(), expected_output)

    # elevator=0 will process the request
    self.ec_obj.request_queue = [4]
    expected_output = [['UP_1', 'OPEN_DOOR', 'CLOSE_DOOR']]
    self.assertListEqual(self.ec_obj.process_request(), expected_output)

    # elevator=0 will process the request, already on the floor
    self.ec_obj.request_queue = [4]
    expected_output = [['OPEN_DOOR', 'CLOSE_DOOR']]
    self.assertListEqual(self.ec_obj.process_request(), expected_output)

    # elevator=1 will process the request
    self.ec_obj.request_queue = [5, 0]
    expected_output = [['OPEN_DOOR', 'CLOSE_DOOR'],
                       ['UP_1', 'UP_1', 'UP_1', 'UP_1', 'UP_1', 'OPEN_DOOR', 'CLOSE_DOOR']]
    self.assertListEqual(self.ec_obj.process_request(), expected_output)

    # elevator=2 will process the request
    self.ec_obj.request_queue = [-1]
    expected_output = [['DOWN_1', 'OPEN_DOOR','CLOSE_DOOR']]
    self.assertListEqual(self.ec_obj.process_request(), expected_output)

    # elevator=2 will process the request
    self.ec_obj.request_queue = [0]
    expected_output = [['UP_1', 'OPEN_DOOR', 'CLOSE_DOOR']]
    self.assertListEqual(self.ec_obj.process_request(), expected_output)

    # Elevator monitor to return elevator2 status
    expected_elevator_2_status = {
      'door': 'Close',
       'running': False,
       'direction': 'Up',
       'current_floor': 0}
    self.assertDictEqual(self.ec_obj.elevator_monitor(2), expected_elevator_2_status)

  def test_process_none_of_elevators_available(self):
    dummy_ec_obj = ElevatorController(
      number_of_elevators=2, floor_min=-1, floor_max=10, request_queue=[])
    # Both the elevators are in running state.
    dummy_ec_obj.request_queue = [0]
    dummy_ec_obj.elevators[0].is_running = 1
    dummy_ec_obj.elevators[1].is_running = 1
    self.assertEqual(dummy_ec_obj.process_request(), [['NOT_READY']])

  def test_process_request_duplicate_floors(self):
    self.ec_obj.request_queue = [2, 2, 2]
    expected_output = [['UP_1', 'UP_1', 'OPEN_DOOR', 'CLOSE_DOOR']]
    self.assertListEqual(self.ec_obj.process_request(), expected_output)

  def test_process_request_raises_exception(self):
    self.ec_obj.request_queue = [2, -2]
    with self.assertRaises(ValueError):
      self.ec_obj.process_request()
