# SandPy - WIP
A zen garden simulation using real-time physics. A sandbox will fill with particles which can then be raked using the mouse. This project uses the game engine Panda3D because of its integration with Bullet, a robust physics engine.  

Currently the simulation doesn't have enough 'sand' since the framerate suffers as the amount of particles increase. The particles also do not stack as one would expect since the collision objects are spherical. 
![SandPy GIF](https://user-images.githubusercontent.com/84789250/121971906-7ab13680-cd3f-11eb-978e-ae0c8debaa2a.gif)

A solution to the stacking issue would be to create a set of irregularly-shaped particles that are then generated in random amounts in the box, however this would not solve the performance issues. I am considering replacing the particle-based system with voxels and using a smaller amount of physics-based particles only to sell the illusion.


Created using Python 3.9 and Panda3D 1.10.9.
