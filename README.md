Repository for the Hardware build of the concentric_tube_continuum_robot


For generating tubes using the freecad macro script do the following steps:
1- Close the start page tab befor executing the script. This is important or you will get errors!!

2 - Open ClassTubeGen.FCMacro in FreeCad

3 - To change the design parameters "length, curvature .. "

edit this line 

tube = TubeGen(inner_radius=<radius in mm>,outer_radius=<radius in mm>,line_length=<straight line in mm>,arc_angle=<arc_angle in degree>,arc_length=<length in mm>,document_name='<model name>')

example : 	tube = TubeGen(inner_radius=5,outer_radius=7,line_length=110,arc_angle=60,arc_length=60,document_name='my_tube')
		tube.generate()
	

4 - you can excute the script as many as you want only if the document_name='<model name>' has a unique name for each model ex. 'model1' then next run 'model2' etc..

