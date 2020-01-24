# Python-project-direction-identification  

ENSTAR robot: identify the direction of a sign  

This python file is just a prototye, it will be converted into C++ or C in order to control the robot.  

Identification_direction.py is the source file, and the 1/2.png is the sign.  

The steps for identification is followed:  

Step 0: transform  

Step 1: find the red triangle  

Step 2: find the correct circle nearest of the red triangle (through the ratio between the triangle and the circle)  

Step 3: analyse the direction (By gray value, the larger the gray value, the lighter the color) (modes or means)  

Problem: the sign in the picture may be an ellipse instead of a circle, so it's better to detect an ellipse.  

!!!!New Methode in using the library of ArUco (ArUco_detection_prototype.py)

# Step 1: En utilisant la bibliothèque d'ArUco, on obtient la position de la centre de la signe.
# Step 2: Trouver la cercle dont la rayon est correste
# Step 3: Comparer la valeur de gris de la deux semi-cercle (on compare seulent une partie mais pas toute la semi-cercle pour économiser du temps )
