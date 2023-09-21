# Generate STL-Files for CTCR-Tubes programmatically
This scripts use FreeCAD and provide a macro to generate tubes with pre-curvature as FreeCad project.

## usage
To generate a tube you simple create the tube object with your intended specifications and call the generate function. It will open a new document containing your specified tube.
Example:
` python
tube = TubeGen(inner_radius=5,outer_radius=7,line_length=110,arc_angle=60,arc_length=60,document_name='my_tube')
tube.generate()
`
The parameters describe:
- inner_radius: inner radius of the cross section
- outer_radius: inner radius of the cross section
- line_length: length of the straight part of the tube
- arc_length: length of the curved part of the tube
- arc_angle: curvature angle of the curved part