#!/usr/bin/env python3

import sys
import mapgen

_ploth = 60
_plotw = 80

def within_range(a, b, r):
    return abs(b-a) <= r

def plot(xs, ys, l1="x", l2="y"):
    points = sorted(list(zip(xs,ys)))
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]

    ytick = max(ys)/_ploth
    xtick = max(xs)/_plotw

    # if our xtick and ytick are within 20% of each other, make them the same
    bigtick = max(xtick,ytick)
    smltick = min(xtick,ytick)
    if bigtick/smltick - 1 < .2:
        tick = max(ytick,xtick)
        xtick = ytick = tick

    plot_tick(xs, ys, xtick, ytick, l1, l2)

def plot_tick(xs, ys, xtick, ytick, l1="x", l2="y"):
    print("Each X character is %.4f, each Y character is %.4f" % (xtick, ytick))
    print('\t'+l2)
    rows = int(max(ys)/ytick)+1
    for i in range(rows+1):
        index = (rows-i)*ytick
        print("%.2f\t|" % index, end='')
        s = ''
        for j in range(len(ys)):
            if within_range(ys[j], index, ytick/2):
                s += '-'*(int(xs[j]/xtick)-len(s)-1) + '*'
        print(s)

    num_ticks = int(_plotw/10) # int(max(xs)*xtick)+1
    print('\t+'+'|'.join(['-'*9]*num_ticks)+'|', l1)
    print(''.join(["%10.2f" % (i*10*xtick) for i in range(_plotw//10+1)]))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        freqs = mapgen.freqs
        amps  = mapgen.amps
    else:
        freqs = []
        amps  = []
        for s in sys.argv[1:]:
            s1, s2 = s.split(',',2)
            freqs.append(float(s1))
            amps.append(float(s2))

    plot(freqs, amps, l1="Frequency", l2="Amplitude")
