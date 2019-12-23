# Python-project-direction-identification  

ENSTAR robot: identify the direction of a sign  

This python file is just a prototye, it will be converted into C++ or C in order to control the robot.  

Identification_direction.py is the source file, and the 2.png is the sign.  

The steps for identification is followed:  

Step 0: transform  

Step 1: find the red triangle  

Step 2: find the correct circle nearest of the red triangle (through the ratio between the triangle and the circle)  

Step 3: analyse the direction (By gray value, the larger the gray value, the lighter the color) (modes or means)  

Problem: the sign in the picture may be an ellipse instead of a circle, so it's better to detect an ellipse.  

