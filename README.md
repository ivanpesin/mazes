# mazes

Python implementations for maze generation, visualization, and solving.

## Syntax

```
usage: maze_client.py [-h] [-a A] [--algs] [-d D] [-n N] [-w W]

Creates an NxN maze using the specified algorithm.

optional arguments:
  -h, --help  show this help message and exit
  -a A        maze generation algorithm
  --algs      list supported maze generation algorithms
  -d D        simulation delay in seconds, can be a fraction
  -n N        maze dimention
  -w W        tile width
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
