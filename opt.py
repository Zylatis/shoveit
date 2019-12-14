import math 
import numpy as np 
import copy
import time
import random
import matplotlib.pyplot as plt
from numba import jit, prange
# http://hjemmesider.diku.dk/~pisinger/codes.html
# https://onlinelibrary.wiley.com/doi/abs/10.1111/itor.12094
# http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0101-74382015000100001

# Pinched from GFG but couldn't use their full one because for some reason it didn't work for rectangles
@jit(nopython=True)
def largestRectangleArea( heights):
      stack = [-1]
      maxArea = 0

      for i in prange(len(heights)):
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

@jit(nopython=True)
def calc_perimiter(grid):
	box_l, box_w = grid.shape
	p = 0
	for i in range(box_l):
		for j in range(box_w):
			if grid[i,j] == 0:
				if i>0:
					if grid[i-1,j] == 1:
						p+=1
				if i<box_l-1:
					if grid[i+1,j] == 1:
						p+=1
				if j>0:
					if grid[i,j-1] == 1:
						p+=1
				if j<box_w-1:
					if grid[i,j+1] == 1:
						p+=1
	return p

# @jit
def add_item(grid, item_size, all_coords, labelled_grid):
	# Lots of optimisations can be done here in terms of checking against existing placements,
	# is okay for now 
	l,w = item_size
	box_l, box_w = grid.shape
	occupied = list(zip(*np.where(grid == 0.)))

	available = sorted(set(occupied) ^ set(all_coords))

	# available = (1.-grid).reshape(int(box_l*box_w/2), 2)
	# print(available)
	# exit(0)

	# available = [ c for c in all_coords if c not in occupied]
	# available = []
	# for c in all_coords:
	# 	if c not in occupied:
	# 		available.append(c)

	test_grid = grid.copy()
	overall_max_free_area = 0
	overall_perimiter = pow(10,10)
	placement = np.array([-1,-1])

	for coord in available:
		
		x,y = coord

		# try original orientation
		if (test_grid[x:x+l,y:y+w].all() == 1.) and (x+l < box_l) and (y+w < box_w):
			test_grid[x:x+l,y:y+w] = 0
			max_free_area = largestRectangle(test_grid) + 1./calc_perimiter(test_grid)
			test_grid[x:x+l,y:y+w] = 1
			if (max_free_area > overall_max_free_area):
				overall_max_free_area = max_free_area
				placement = coord

		# try rotated object
		# if (test_grid[x:x+w,y:y+l].all() == 1.) and (x+w < box_l) and (y+l < box_w):
		# 	test_grid[x:x+w,y:y+l] = 0
		# 	max_free_area = largestRectangle(test_grid) + 1./calc_perimiter(test_grid)
		# 	test_grid[x:x+w,y:y+l] = 1
		# 	if (max_free_area > overall_max_free_area):
		# 		overall_max_free_area = max_free_area
		# 		placement = coord
		# 		w,l = l, w

	if (placement == np.array([-1,-1])).all():
		print("Failed to place item")
		print(item_size)
	else:
		x,y = placement
		grid[x:x+l,y:y+w] = 0
		labelled_grid[x:x+l,y:y+w] = np.max(labelled_grid)+1.

def gen_item_list(n, x_range, y_range):
	items = []
	for i in range(n):
		x = random.randrange(x_range[0],x_range[1])
		y = random.randrange(y_range[0],y_range[1])
		items.append([x,y])

	return items

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

random.seed(0)
item_list = gen_item_list(30,[1,5],[1,5])

areas = [-x*y for x,y in item_list]
heuristic_order = np.argsort(areas)
c = 0
for i in heuristic_order:
	item = item_list[i]
	add_item(grid,item,all_coords, labelled_grid)
	plt.imshow(labelled_grid, cmap='hot', interpolation='nearest')
	plt.savefig(f'imgs/{c}.png')
	c+=1

d = time.time()-st
print(d)
