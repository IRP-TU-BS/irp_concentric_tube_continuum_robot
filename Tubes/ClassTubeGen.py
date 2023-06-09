import FreeCAD as App
import Part
from math import pi


'''
This Class is for generating 3d models of tubes for irp_concentric_tube_continuum_robot 
'''

class TubeGen():

    def __init__(self,inner_radius,outer_radius,line_length, arc_angle,arc_length,document_name):
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.line_length = line_length
        self.arc_angle = arc_angle
        self.arc_length = arc_length
        self.document_name = document_name
    

    def generate(self):

        doc = App.newDocument(self.document_name)
        doc.addObject('PartDesign::Body','Body')
    #create a sketch for 2D design
        App.getDocument(self.document_name).getObject('Body').newObject('Sketcher::SketchObject','Sketch')
        App.getDocument(self.document_name).getObject('Sketch').Support = (App.getDocument(self.document_name).getObject('XZ_Plane'),[''])
        App.getDocument(self.document_name).getObject('Sketch').MapMode = 'FlatFace'
    # tube inner and outer circles
        inner_circle = Part.Circle() 
        inner_circle.Radius = self.inner_radius
        outer_circle = Part.Circle() 
        outer_circle.Radius = self.outer_radius
    # add the circles to the created sketch
        App.getDocument(self.document_name).getObject('Sketch').addGeometry( inner_circle)
        App.getDocument(self.document_name).getObject('Sketch').addGeometry(outer_circle)


        path=TubeGen.tube_path(self)

    # extrude along the created path 
        TubeGen.extrude_along_path(self)
        App.activeDocument().recompute()
        Gui.activeDocument().activeView().viewAxometric()
        Gui.SendMsgToActiveView("ViewFit")
        return   inner_circle,outer_circle


    # function to create path (straight+curve)


    def tube_path(self):
        App.getDocument(self.document_name).getObject('Body').newObject('Sketcher::SketchObject','Sketch2')
    # create a sketch for drawing the path
        App.getDocument(self.document_name).getObject('Sketch2').Support = (App.getDocument(self.document_name).getObject('XY_Plane'),[''])
        App.getDocument(self.document_name).getObject('Sketch2').MapMode = 'FlatFace'
    # straight part
        line=Part.LineSegment()
        line.StartPoint=App.Vector(0,0,0)
        line.EndPoint=App.Vector(0,self.line_length,0)


    # arcs angles are in Radians so we need to convert from degrees
        radians = self.arc_angle * pi/180
    # length of an arc is its angle * its radius
        arc_radius = self.arc_length/radians
    # create a circle of the arc radius
        curvature= Part.Circle(App.Vector(-25.872555,31.913834,0),App.Vector(0,0,1),arc_radius)
    # cut an arc from that circle
        arc=Part.ArcOfCircle(curvature,0.00,radians)
    # add the created geometry to the sketcht2
        App.getDocument(self.document_name).getObject('Sketch2').addGeometry(line)
        App.getDocument(self.document_name).getObject('Sketch2').addGeometry(arc)

    # create to construction lines to help constrain the angle of the curve
        App.getDocument(self.document_name).getObject('Sketch2').addGeometry(Part.LineSegment(App.Vector(-23.872555,31.913834,0),App.Vector(-25.872555,31.913834,0)),False)
        App.getDocument(self.document_name).getObject('Sketch2').addGeometry(Part.LineSegment(App.Vector(-25.872555,33.913834,0),App.Vector(-25.872555,31.913834,0)),False)

    # add constrains to the ceated geometry
        App.getDocument(self.document_name).getObject('Sketch2').addConstraint(Sketcher.Constraint('Coincident', 2, 2, 1, 3))
        App.getDocument(self.document_name).getObject('Sketch2').addConstraint(Sketcher.Constraint('Coincident', 3, 2, 1, 3)) 
        App.getDocument(self.document_name).getObject('Sketch2').addConstraint(Sketcher.Constraint('Coincident', 2, 1, 0, 2)) 
        App.getDocument(self.document_name).getObject('Sketch2').addConstraint(Sketcher.Constraint('Coincident', 3, 1, 1, 2)) 
        App.getDocument(self.document_name).getObject('Sketch2').addConstraint(Sketcher.Constraint('Vertical',0)) 
    # length of the straight part
        App.getDocument(self.document_name).getObject('Sketch2').addConstraint(Sketcher.Constraint('DistanceY',0,1,0,2,self.line_length)) 
        App.getDocument(self.document_name).getObject('Sketch2').addConstraint(Sketcher.Constraint('Coincident', 0, 1, -1, 1)) 
        App.getDocument(self.document_name).getObject('Sketch2').addConstraint(Sketcher.Constraint('Tangent',1,1,0,2)) 

        App.getDocument(self.document_name).getObject('Sketch2').toggleConstruction(2) 
        App.getDocument(self.document_name).getObject('Sketch2').toggleConstruction(3) 
    # angle and radius of the curved part
        App.getDocument(self.document_name).getObject('Sketch2').addConstraint(Sketcher.Constraint('Angle',2,2,3,2,radians)) 
        App.getDocument(self.document_name).getObject('Sketch2').addConstraint(Sketcher.Constraint('Radius',1,arc_radius)) 
    # recompute
        App.activeDocument().recompute()

        return line,arc


    # funvtion to extrude the two circles along the path we created
    def extrude_along_path(self):

        App.getDocument(self.document_name).getObject('Body').newObject('PartDesign::AdditivePipe','AdditivePipe')
        App.getDocument(self.document_name).getObject('AdditivePipe').Profile = App.getDocument(self.document_name).getObject('Sketch')
        App.getDocument(self.document_name).getObject('AdditivePipe').Spine = (FreeCAD.getDocument(self.document_name).getObject('Sketch2'),['Edge1','Edge2'])
        App.getDocument(self.document_name).recompute()
        Gui.getDocument(self.document_name).getObject('AdditivePipe').Visibility = True
        return 0



	

if __name__ == "__main__":
	tube = TubeGen(inner_radius=5,outer_radius=7,line_length=110,arc_angle=60,arc_length=60,document_name='my_tube')
	tube.generate()



