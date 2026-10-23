## TO BE IMPLEMENTED

cube(size, center) // Generates a solid 3D cube or rectangular cuboid
sphere(r|d) // Generates a solid 3D sphere
cylinder(h, r|r1|r2, d|d1|d2, center) // Generates a 3D cylinder or cone
translate([x, y, z]) // Moves child elements along the specified axes
rotate([a, b, c]) // Rotates child elements around the X, Y, and Z axes
scale([x, y, z]) // Scales child elements horizontally, vertically, or in depth
resize([x, y, z], auto) // Forces child elements to fit into exact specified dimensions
mirror([x, y, z]) // Mirrors child elements across a plane perpendicular to the vector
union() // Merges all child shapes into a single unified object
difference() // Subtracts all subsequent child shapes from the first child shape
intersection() // Keeps only the overlapping volume shared by all child shapes
hull() // Creates a convex hull wrapping around all child shapes
minkowski() // Computes the Minkowski sum of child shapes to round off edges
let(var) // Assigns local variables inside a localized geometric block


# POSTPONED:

## 2d shapes-related:

circle(r|d) // Generates a 2D circle with a given radius or diameter
square(size, center) // Generates a 2D square or rectangle
polygon(points, paths) // Creates a custom 2D shape from a list of coordinates
text(text, size, font, halign, valign, spacing, direction, language, script) // Renders text into a 2D geometric shape
offset(r|delta, chamfer) // Expands or shrinks the outlines of 2D shapes
linear_extrude(height, twist, scale, convexity, slices) // Pulls a 2D shape straight up into 3D space
rotate_extrude(angle, convexity) // Revolves a 2D shape around the Y-axis to create a 3D object
projection(cut) // Flattens a 3D object into a 2D graphic layout

## Too complex: 

polyhedron(points, faces, convexity) // Creates a custom 3D shape from points and faces
multmatrix(m) // Multiplies geometry by a custom 4x4 transformation matrix
import(file, convexity) // Imports external 2D or 3D files (STL, DXF, SVG, 3MF)
surface(file, center, convexity, invert) // Reads heightmaps from files to generate 3D terrain

# requires grammar improvement

if(condition) // Conditionally renders geometric branches 
for(i) // Loops over a range or array to duplicate child shapes
intersection_for(i) // Loops through variables and keeps only the geometric intersection

## Unclear how to implement:

color([r, g, b, a]) // Changes the display color and opacity of the geometry in preview
echo(...) // Prints text or variable data to the console window
render(convexity) // Forces full mesh calculation and caching instead of quick preview
assert(condition, message) // Halts evaluation if a designated condition is false

Not a real module

children(idx) // References inner geometric elements passed into a user-defined module
