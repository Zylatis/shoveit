import math 
import numpy as np 
import copy
import time
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

def calc_perimiter(grid):
	box_l, box_w = grid.shape
	p = 0
	for i in range(box_l):
		for j in range(box_w):
			bools = []
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

		if (test_grid[x:x+l,y:y+w].all() == 1.) and (x+l < box_l) and (y+w < box_w):

			test_grid[x:x+l,y:y+w] = 0
			max_free_area = largestRectangle(test_grid) + 1./calc_perimiter(test_grid)# + largestRectangle(1.-test_grid)
			# perim = calc_perimiter(test_grid)
			test_grid[x:x+l,y:y+w] = 1
			# print(perim)
			if (max_free_area > overall_max_free_area) :#and (perim <= overall_perimiter):
			# if perim <= overall_perimiter:
				overall_max_free_area = max_free_area
				# overall_perimiter = perim
				placement = coord

	if (placement == np.array([-1,-1])).all():
		print("Failed to place item")
		print(item_size)
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
	[1,1],
	[7,5],
	[7,5],
	# [15,5],
	[2,1],
	[5,5],
	[1,4],
	[1,1],
	[1,1]

	]
areas = [-x*y for x,y in item_list]
# heuristic_order = range(len(areas))
heuristic_order = np.argsort(areas)
for i in heuristic_order:
	item = item_list[i]
	add_item(grid,item,all_coords, labelled_grid)

d = time.time()-st
print(d)
# print(labelled_grid)
print(d*math.factorial(len(item_list))/60)
plt.imshow(labelled_grid, cmap='hot', interpolation='nearest')
plt.savefig('test.png')

# print(calc_perimiter(labelled_grid))
# grid = np.zeros((n,m))
# print(grid)
# print(calc_perimiter(grid))
# grid[0:2,7:9]=0
# print(calc_perimiter(grid))
# print(grid)

# grid[0:2,7:9]=1
# grid[2:4,0:2]=0
# print(calc_perimiter(grid))
# print(grid)