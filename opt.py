import numpy as np 
import copy
import time
# Pinched from GFG but couldn't use their full one because for some reason it didn't work for rectangles
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

def add_item(grid, l, w, all_coords):
	# Lots of optimisations can be done here in terms of checking against existing placements
	# For now let's just ensure we don't start at any points occupied by existing items. That
	# won't fully prevent collisions but will be a good start

	occupied = set(zip(*np.where(grid == 0.)))
	available = sorted(occupied ^ all_coords)
	test_grid = copy.copy(grid)
	overall_max_free_area = 0
	placement = []
	for coord in available:
		x,y = coord
		test_grid[x:x+l,y:y+w] = 0
		max_free_area = largestRectangle(test_grid) + largestRectangle(1.-test_grid)
		if max_free_area > overall_max_free_area:
			overall_max_free_area = max_free_area
			placement = coord
	x,y = placement
	grid[x:x+l,y:y+w] = 0

n = 20
m = 20
grid = np.zeros((n,m))
grid.fill(1)
# print(1.-grid)
st = time.time()
free_area = largestRectangle(grid)
# print(time.time()-st)
# print(free_area)
all_coords = []
for i in range(n):
	for j in range(m):
		all_coords.append(tuple([i,j]))
# print(all_coords)
add_item(grid, 2, 2, set(all_coords))
add_item(grid, 10, 10, set(all_coords))
add_item(grid, 2, 2, set(all_coords))
add_item(grid, 5, 2, set(all_coords))
add_item(grid, 5, 2, set(all_coords))
add_item(grid, 12, 3, set(all_coords))
add_item(grid, 10, 10, set(all_coords))

print(grid)
