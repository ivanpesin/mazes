<!-- omit in toc -->
# Mazes

Python implementations for maze generation, visualization, and solving.

## Intro

TODO:

Source: http://weblog.jamisbuck.org/under-the-hood/

- [Intro](#intro)
- [Syntax](#syntax)
- [Examples](#examples)
  - [Recursive split](#recursive-split)
  - [Recursive backtracking](#recursive-backtracking)
  - [Hunt-and-kill](#hunt-and-kill)
- [TODO](#todo)

## Syntax

```
usage: maze_client.py [-h] [-a A] [--algs] [-d D] [-n N] [-w W]

Creates an NxN maze using the specified algorithm.

optional arguments:
  -h, --help            show this help message and exit
  -a A                  maze generation algorithm
  --algs                list supported maze generation algorithms
  -d D                  simulation delay in seconds, can be a fraction
  --start_delay START_DELAY
                        delay on start, can be a fraction
  -n N                  maze dimention
  -w W                  tile width
  --start START START   maze entrance coordinates
  --finish FINISH FINISH
                        maze exit coordinates
```

## Examples

### Recursive split

Recursive splitting 50/50 and opening a randomly positioned door:

`$ python3 maze_client.py -n 10 -w 30 -d 0.2`

![](images/maze-split-halves.gif)

Recursive splitting at a random point and opening a randomly positioned door:

`$ python3 maze_client.py -n 10 -w 30 -d 0.2 -a 2`

![](images/maze-split-random.gif)

### Recursive backtracking

`$ python3 maze_client.py -n 10 -w 30 -d 0.2 -a 2`

![](images/maze-recursive-bt.gif)

### Hunt-and-kill

Does not require backtracking, thus generates less windy passages

`$ python3 maze_client.py -n 10 -w 30 -a 3 -d 0.15 --start 4 4 --finish 9 4`

![](images/maze-hunt-and-kill.gif)

## TODO

- [x] Fix wall chipping
- [x] Add starting and finishing locations for the maze solver
- [x] Hunt and kill alg
- [ ] Growing tree alg
- [ ] Binary tree alg
- [ ] ASCII representation for mazes
- [ ] Options to skip maze generation and solving animations