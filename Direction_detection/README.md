1)ENSTAR robot: identify the direction of a sign

This python file is just a prototye, it will be converted into C++ or C in order to control the robot.

Identification_direction.py is the source file, and the 1/2.png is the sign.

The steps for identification is followed:

!!!!New Methode in using the library of ArUco (ArUco_detection_prototype.py)

Step 1: Using the ArUco library, we obtain the position of the center of the sign. Step 2: Find the circle with the correct radius Step 3: Compare the gray value of the two semi-circle (we only compare a part but not the whole semi-circle to save time)

Other methodes (not valid) Step 0: transform
Step 1: find the red triangle
Step 2: find the correct circle nearest of the red triangle (through the ratio between the triangle and the circle)
Step 3: analyse the direction (By gray value, the larger the gray value, the lighter the color) (modes or means)
Problem: the sign in the picture may be an ellipse instead of a circle, so it's better to detect an ellipse.
