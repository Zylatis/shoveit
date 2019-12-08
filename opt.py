import math 
import numpy as np 
import copy
import time
from numba import jit, prange
# http://hjemmesider.diku.dk/~pisinger/codes.html
# https://onlinelibrary.wiley.com/doi/abs/10.1111/itor.12094
# http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0101-74382015000100001

# Pinched from GFG but couldn't use their full one because for some reason it didn't work for rectangles
@jit(nopython=True)
def largestRectangleArea( heights):
      stack = [-1]
      maxArea = 0

      for i in range(len(heights)):
          # we are saving indexes in stack that is why we comparing last element in stack
          # with current height to check if last element in stack not bigger then
          # current element
          while stack[-1] != -1 and heights[stack[-1]] >= heights[i]:
              lastElementIndex = stack.pop()
              maxArea = max(maxArea, heights[lastElementIndex] * (i - stack[-1] - 1))
          stack.append(i)

      # we went through all elements of heights array
      # let's check if we have something left in stack
      while stack[-1] != -1:
          lastElementIndex = stack.pop()
          maxArea = max(maxArea, heights[lastElementIndex] * (len(heights) - stack[-1] - 1))

      return maxArea
@jit(nopython=True)
def largestRectangle(M):
	nrows, ncols = M.shape
	hist = np.zeros(ncols)
	max_area = 0.
	for r in range(nrows):
		hist += M[r,:]
		zero_locs = np.where(M[r,:]==0)
		hist[zero_locs] = 0
		area = largestRectangleArea(hist)
		max_area = max(area, max_area)
	return max_area

def add_item(grid, item_size, all_coords, labelled_grid):
	# Lots of optimisations can be done here in terms of checking against existing placements
	# For now let's just ensure we don't start at any points occupied by existing items. That
	# won't fully prevent collisions but will be a good start
	l,w = item_size
	occupied = set(zip(*np.where(grid == 0.)))
	available = sorted(occupied ^ all_coords)
	test_grid = grid.copy()
	overall_max_free_area = 0
	placement = (0,0)
	box_l, box_w = grid.shape
	for coord in available:
		x,y = coord
		if (test_grid[x:x+l,y:y+w].all() == 1.) and (x+l < box_l) and (y+w < box_w):

			test_grid[x:x+l,y:y+w] = 0
			max_free_area = largestRectangle(test_grid)# + 1./largestRectangle(1.-test_grid)
			if max_free_area > overall_max_free_area:
				overall_max_free_area = max_free_area
				placement = coord

	if placement == ():
		print("Failed to place item")
	else:
		x,y = placement
		grid[x:x+l,y:y+w] = 0
		labelled_grid[x:x+l,y:y+w] = np.max(labelled_grid)+1.

n = 20
m = 20
grid = np.zeros((n,m))
grid.fill(1)

st = time.time()
free_area = largestRectangle(grid)

all_coords = []
for i in range(n):
	for j in range(m):
		all_coords.append(tuple([i,j]))
all_coords = set(all_coords)
labelled_grid = copy.copy(1.-grid)
st = time.time()

item_list = [
	[2,2],
	[10,5],
	[2,2],
	[5,2],
	[5,2],
	[12,3],
	[3,3],
	[3,2],
	[3,2],
	# [2,2]
]
areas = [-x*y for x,y in item_list]
heuristic_order = np.argsort(areas, )
for i in heuristic_order:
	item = item_list[i]
	add_item(grid,item,all_coords, labelled_grid)

d = time.time()-st
print(d)
print(labelled_grid)
print(d*math.factorial(len(item_list))/60)