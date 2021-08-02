# Hexcope - **Work in Progress**

3d printable hex pattern parabolic mirror for telescope \
20x20x20 cm parts \

## Primary mirror
19 x 20cm side hexagonal mirrors \
https://www.gifi.fr/product/id/557688/miroir-sticker-hexagonal-x-3

## Secondary mirror - **Work in Progress**
Allows for Newton setup (with basis central hex on) \

![Capture](https://github.com/Dethcount/hexcope/blob/main/img/snapshot_newton.png?raw=true)

or Ritchley-Chretien setup (with camera at basis center)

![Capture](https://github.com/Dethcount/hexcope/blob/main/img/snapshot.png?raw=true)

1 x 10cm radius round mirror \
https://www.gifi.fr/product/id/557686/miroir-sticker-rond-x-3

## Telescope basis
missing instrument plate and central hex for Newton setup

## Running scripts in Blender
Launch Blender (throw a terminal if you need to debug) \
in the Scripting tab open support.py and run it \
then open basis.py and run it

## Gcode files
DM_ is for Dagoma Magis 3d printer
DD_ is for Dagoma DiscoEasy200

## Scaling
Hexcope can be scaled by primary mirror radius hyperparameter "n" (number of hexagons) \
e.g : n = 4, f = 16 (= 1.6m) \
![Capture](https://github.com/Dethcount/hexcope/blob/main/img/snapshot_scaling.png?raw=true)
\
and by number of support arms \
e.g : support_arm_n = 6 \
![Capture](https://github.com/Dethcount/hexcope/blob/main/img/snapshot_scaling_arms.png?raw=true)

## Assembling
Primary mirror requires soldering PLA parts using filament \
https://youtu.be/Q-PgjTYsAFY

## Printing
(e.g: Dagoma DiscoEasy200) \
Layer height: 0.3mm \
Infill density: 10% \
Print speed: 75 mm/s \
Infill speed: 80 mm/s \
Outer wall speed: 50 mm/s \
Inner wall speed: 70 mm/s \
Top / Bottom speed: 70 mm/s \
Travel speed: 100 mm/s \
Initial layer speed: 15 mm/s \
Support: touching buildplate \
Build plate adhesion type: skirt \
Skirt line count: 3 \
Skirt distance: 2mm \

- Basis: 1.290kg, 480m, 68h30
    - 2 x plate bottom: 96g, 33m, 3h30
    - 1 x plate axis: 205g, 70m, 7h
    - 2 x plate top: 96g, 33m, 3h30
    - 2 x leg: 113g, 39m, 4h30  (support: everywhere)
    - 4 x foot: 10g, 4m, 0h30
    - 2 x arm: 79g, 27m, 3h30
    - 2 x wheel: 135g, 46m, 10h30 (print vertically, bottom up)
    - 2 x screw: 16g, 6m, 2h (0.1mm layer height)
    - 2 x screw cap: 9g, 4m, 2h30  (0.1mm layer height)
- Primary mirror (n=0, newton): 1152g, 396m, 59h
    - 2 x center half hex: 47g, 16m, 1h30
    - 16 x half hex: 67g, 23m, 3h30
- Secondary mirror support (f=16, arm_n=3, newton): 1,548kg, 552m, 192h
    - 3 x arm block: 177g, 60m, 6h30
    - 48 x arm: 19g, 7m, 3h30 (layer height: 0.1mm, support: disabled)
    - 3 x arm head: 35g, 12m, 1h30
    - 3 x spider arms: unknown
- Secondary mirror (f=16, arm_n=3, newton): 217g, 74m, 13h (disable support)
- Eyepiece support: unknown

## Current prototype state
![Capture](https://github.com/Dethcount/hexcope/blob/main/img/current_prototype_state.jpg?raw=true)
