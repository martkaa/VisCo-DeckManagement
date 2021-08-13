import numpy as np
import math as m


a = np.array([[1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1],
            [1,1,1,1,1]])

length, width = 2, 3
rows, cols = 7, 5
hazards,risk = False, True
takes_hazards, takes_risk = True, True
j = 2
coor = 0

print(a)
#print(coordinates)

print(coor)
print(type(coor))

coord = ','.join([str(c/2) for c in coor])
print(coord)
    


import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

H = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12],
              [13, 14, 15, 16]])  # added some commas and array creation code

plt.title('LDA001')
plt.pcolormesh(a, edgecolors='w')
ax = plt.gca()
ax.set_aspect('equal')
plt.colorbar(orientation='vertical')

ax.invert_yaxis()
#plt.show()

fig, ax = plt.subplots()
data = np.random.randn(6, 6)
y = ["Prod. {}".format(i) for i in range(10, 70, 10)]
x = ["Cycle {}".format(i) for i in range(1, 7)]

qrates = list("ABCDEFG")
norm = matplotlib.colors.BoundaryNorm(np.linspace(-3.5, 3.5, 8), 7)
fmt = matplotlib.ticker.FuncFormatter(lambda x, pos: qrates[::-1][norm(x)])

#im, _ = heatmap(data, y, x, ax,
 #               cmap=plt.get_cmap("PiYG", 7), norm=norm,
  #              cbar_kw=dict(ticks=np.arange(-3, 4), format=fmt),
   #             cbarlabel="Quality Rating")
#annotate_heatmap(im, valfmt=fmt, size=9, fontweight="bold", threshold=-1,
 #                textcolors=("red", "black"))

# Let's design a dummy land use field



# Let's also design our color mapping: 1s should be plotted in blue, 2s in red, etc...
col_dict={-1:"blue",
        1: "yellow",
          2:"red",
          3:"orange",
          4:"green"}

# We create a colormar from our list of colors
cm = ListedColormap([col_dict[x] for x in col_dict.keys()])

# Let's also define the description of each category : 1 (blue) is Sea; 2 (red) is burnt, etc... Order should be respected here ! Or using another dict maybe could help.
labels = np.array(["space/unavailable","available", "ABC001","ABC002","ABC003"])
len_lab = len(labels)

# prepare normalizer
## Prepare bins for the normalizer
norm_bins = np.sort([*col_dict.keys()]) + 0.5
norm_bins = np.insert(norm_bins, 0, np.min(norm_bins) - 1.0)
#print(norm_bins)

## Make normalizer and formatter
norm = matplotlib.colors.BoundaryNorm(norm_bins, len_lab, clip=True)
fmt = matplotlib.ticker.FuncFormatter(lambda x, pos: labels[norm(x)])

# Plot our figure
fig,ax = plt.subplots()
im = ax.imshow(a, cmap=cm, norm=norm)

diff = norm_bins[1:] - norm_bins[:-1]
tickz = norm_bins[:-1] + diff / 2
cb = fig.colorbar(im, format=fmt, ticks=tickz)
fig.savefig("example_landuse.png")
#plt.show()


 

sort_list = [["area and smallest"],
                ['area and biggest'],
                ['area and risk and hazards'],
                ['weight and smallest'],
                ['weight and biggest'],
                ['weight and risk and hazards'],
                ['location andsmallest'],
                ['location and biggest'],
                ['location and risk and hazards'],
                ['risk and hazards and smallest'],
                ['risk and hazards and biggest'],
                ['risk and hazards and risk and hazards']]

cargo_sort = ['Unsorted', 'Area', 'Weight', 'Location', 'Risk and Hazards']
LDA_sort = ['Unsorted', 'Smallest', 'Biggest', 'Risk and Hazards']

print(sort_list)

n = 0
for i in range(len(sort_list)):
    print(sort_list[i])

# write to file functions

    