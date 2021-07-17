# hexcope - **Work in Progress**

3d printable hex pattern parabolic mirror for telescope \
20x20x20 cm parts\

## primary mirror
19 x 20cm side hexagonal mirrors \
https://www.gifi.fr/product/id/557688/miroir-sticker-hexagonal-x-3

## secondary mirror - **Work in Progress**
Allows for Newton setup (with basis central hex on) \

![Capture](https://github.com/Dethcount/hexcope/blob/main/img/snapshot_newton.png?raw=true)

or Ritchley-Chretien setup (with camera at basis center)

![Capture](https://github.com/Dethcount/hexcope/blob/main/img/snapshot.png?raw=true)

1 x 10cm radius round mirror \
https://www.gifi.fr/product/id/557686/miroir-sticker-rond-x-3

## telescope basis
missing instrument plate and central hex for Newton setup

## running scripts in Blender
Launch Blender (throw a terminal if you need to debug) \
in the Scripting tab open support.py and run it \
then open basis.py and run it

## gcode files
DM_ is for Dagoma Magis 3d printer
DD_ is for Dagoma DiscoEasy200

## scaling
Hexcope can be scaled by primary mirror radius hyperparameter "n" (number of hexagons) \
e.g : n = 4, f = 16 (= 1.6m) \
![Capture](https://github.com/Dethcount/hexcope/blob/main/img/snapshot_scaling.png?raw=true)
\
and by number of support arms \
e.g : support_arm_n = 6 \
![Capture](https://github.com/Dethcount/hexcope/blob/main/img/snapshot_scaling_arms.png?raw=true)

## assembling
Primary mirror requires soldering PLA parts using filament \
https://youtu.be/Q-PgjTYsAFY

## printing
(e.g: Dagoma DiscoEasy200) \

- Basis: 1,217kg, 422m, 48h
    - 2 x plate bottom: 96g, 33m, 3h30
    - 1 x plate axis: 205g, 70m, 7h
    - 2 x plate top: 96g, 33m, 3h30
    - 2 x leg: 126g, 43m, 5h
    - 4 x foot: 10g, 4m, 0h30
    - 2 x arm: 128g, 44m, 5h30
    - 2 x wheel: 40g, 15m, 2h
- Primary mirror (n=0, newton): 592g, 204m, 27h
    - 2 x center half hex: 40g, 14m, 1h30
    - 16 x half hex: 32g, 11m, 1h30
- Secondary mirror support (f=16, arm_n=3, newton): 1,248kg, 462m, 57h
    - 3 x arm block: 87g, 30m, 3h30
    - 42 x arm: 21g, 8m, 1h
    - 3 x arm head: 35g, 12m, 1h30
    - 3 x spider arms: unknown
- Secondary mirror: unknown
- Eyepiece support: unknown