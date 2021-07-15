# hexcope - **Work in Progress**

3d printable hex pattern parabolic mirror for telescope \
20x20x20 cm parts\

## primary mirror
19 x 20cm side hexagonal mirrors \
https://www.gifi.fr/product/id/557688/miroir-sticker-hexagonal-x-3

## secondary mirror - **Work in Progress**
Allows for Newton setup (with basis central hex on) \

![Capture](https://github.com/Dethcount/hexcope/blob/main/snapshot_newton.png?raw=true)

or Ritchley-Chretien setup (with camera at basis center)

![Capture](https://github.com/Dethcount/hexcope/blob/main/snapshot.png?raw=true)

1 x 10cm radius round mirror \
https://www.gifi.fr/product/id/557686/miroir-sticker-rond-x-3

## telescope basis
missing instrument plate and central hex for Newton setup

## running scripts in Blender
Launch Blender (throw a terminal if you need to debug) \
in the Scripting tab open support_v2_hex.py and run it \
then open basis.py and run it

## gcode files
DM_ is for Dagoma Magis 3d printer
DD_ is for Dagoma DiscoEasy200

## scaling
Hexcope can be scaled by primary mirror radius hyperparameter "n" (number of hexagons) \
e.g : n = 4, f = 16 (= 1.6m) \
![Capture](https://github.com/Dethcount/hexcope/blob/main/snapshot_scaling.png?raw=true)
\
and by number of support arms \
e.g : support_arm_n = 6 \
![Capture](https://github.com/Dethcount/hexcope/blob/main/snapshot_scaling_arms.png?raw=true)

## assembling
Primary mirror requires soldering PLA parts using filament \
https://youtu.be/Q-PgjTYsAFY
