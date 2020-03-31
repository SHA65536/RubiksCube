# RubiksCube
A RubiksCube Experiment by SHA2048

This is a personal project to explore an idea I had about affects of different algorithms on a Rubiks Cube.
If you repeat the same algorithm enough times on a rubiks cube it will return to it's original position.
The number of times you need to repeat the algorithm until the cube returns to it's original position  is dependant on the algorithm, and that is what I want to explore in this project.

### Installation 
To install simply clone the repository and run `pip install -r requirments.txt` To install all the dependencies of the project.

### Running
To start calculate the number of cycles needed to repeat the position, you should run `run.py`

### Visualization
Inside run.py there are some visualization funtions such as `makeGifFromString` that are used to visualize an algorithm.

### Instruction String
An Instruction string is a string of letters that represent movements of the cube.
A lower case letter means clockwise and an uppercase letter means counter-clockwise.
The different letters represent different sides: R - Right L - Left U - Up D - Down F - Face B - Back
So 'Rbr' would mean moving the right side counter-clockwise, backside clockwish, and the right side clockwise.