# Elevator
This code represents an Elevator system which consists of 
1) Elevator controller 
2) ‘n’ number of elevators.

![Screenshot](elevator.png)

```
An Elevator can perform following tasks:-  
1) Go up and down and track the current floor.
2) Accept requests from the elevator controller from inside or outside of the elevator.
3) Given a list of floors, intelligently decides the direction and cater next floor request.
4) Provide its current status such as door is open or closed, elevator's current floor, is it running or not.              
5) Throws an error if the requested floor is less than min and greater than max floors.

Elevator controller can perform following tasks:-
1) Elevator controller accepts multiple requests and chooses the best among n elevators.
2) Elevator controller provides elevator monitor which returns the current status of any given elevator.

Sample request:-
Two people requested to stop at floors 2 and 3
Elevator-1 current_floor = 0

Output returned is:-
[UP_1, UP_1, UP_1, OPEN_DOOR, CLOSE_DOOR]
[UP_1, OPEN_DOOR, CLOSE_DOOR]

```

How to Run:
```
Ensure you have python3 installed in your system.
Download code from git repo. Move to code folder.
1) Create and activate a python3 virtualenv.
    python3 -m venv venv
    source venv/bin/activate
2)  Execute unit test cases for elevator and elevator controller. 
    a) python -m unittest elevator_controller_test 
    b) python -m unittest elevator_test 
Change inputs if required in the testcases files.(elevator_test.py and elevator_controller_test.py)
```

Assumptions and Future work:
```
1) We need to enhance the system to use better cost functions. The algorithm used to determine the cost of moving 
   an elevator (up and down) considers the first nearest requested floor for cost calculation.
2) The Code assumes that only a stopped elevator can accept the request. Future work is to push the requested floors 
   request to the moving elevators also. The proposed algorithm will fetch one of the moving elevator which is moving in the same 
   direction and is nearest to the requested floor. This approach will require to handle concurrent access of the requested_floors 
   list with the use of locks.
3) Need to improve upon error handling.
4) Expose elevator API and have a docker image for the solution. 
```
