from OCC.Core.Geom import Geom_CartesianPoint,Geom_Plane
from OCC.Core.gp import gp_Ax3,gp,gp_Pnt2d
from OCC.Core.TopoDS import  TopoDS_Edge
from OCC.Core.TColStd import TColStd_HSequenceOfTransient
from OCC.Core.ElCLib import elclib
from OCC.Core.Geom2dAPI import *
from OCC.Core.Standard import Standard_Transient
from OCC.Core.Quantity import Quantity_NOC_CYAN1
from OCC.Core.Geom2d import Geom2d_CartesianPoint
from OCC.Core.AIS import AIS_InteractiveContext,AIS_InteractiveObject,AIS_Point
from data.sketch.sketch_type import *
MINIMUMSNAP = 25
MINANGLE = 3.14 / 64


class Sketch_Snap(object):
    def __init__(self):
        self.myContext = AIS_InteractiveContext()
        self.data = TColStd_HSequenceOfTransient()
        self.curHilightedObj = AIS_InteractiveObject()
        self.ProjectOnCurve = Geom2dAPI_ProjectPointOnCurve()

        self.curCoordinateSystem = gp_Ax3(gp.XOY())
        self.FirstEdge = TopoDS_Edge()
        self.SecondEdge = TopoDS_Edge()

        self.curPnt2d = gp.Origin2d()
        self.objectPnt2d = gp.Origin2d()
        self.bestPnt2d = gp.Origin2d()
        self.findbestPnt2d = False

        self.firstDisplay = True
        self.myGeom_Point = Geom_CartesianPoint(gp.Origin())
        self.myAIS_Point = AIS_Point(self.myGeom_Point)
        self.myAIS_Point.SetColor(Quantity_NOC_CYAN1)

        self.minimumSnapDistance = MINIMUMSNAP
        self.minDistance = 0
        self.curDistance = 0
        self.curGeom2d_Point = Geom2d_CartesianPoint(self.curPnt2d)
        self.myPlane = Geom_Plane(self.curCoordinateSystem)

    def SetContext(self, theContext: AIS_InteractiveContext):
        self.myContext = theContext

    def SetData(self, theData: TColStd_HSequenceOfTransient):
        self.data = theData

    def SetAx3(self, theAx3: gp_Ax3):
        self.curCoordinateSystem = theAx3

    def SetMinDistance(self, aPrecise):
        self.minDistance = aPrecise

    def MouseInputEvent(self, tempPnt2d: gp_Pnt2d):
        self.curPnt2d = tempPnt2d
        self.SelectEvent()
        self.EraseSnap()
        return self.bestPnt2d

    def MouseMoveEvent(self, tempPnt2d: gp_Pnt2d):
        self.curPnt2d = tempPnt2d
        self.SelectEvent()
        if self.findbestPnt2d:
            self.myGeom_Point.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.bestPnt2d))
            self.myAIS_Point.SetComponent(self.myGeom_Point)
            if self.firstDisplay:
                self.myContext.Display(self.myAIS_Point, 0, -1)
                self.DrawRelation()
                self.firstDisplay = False
            else:
                self.myContext.Redisplay(self.myAIS_Point)
                self.DrawRelation()
        else:
            self.myContext.Remove(self.myAIS_Point)
            self.EraseRelation()
            self.firstDisplay = True
        return self.bestPnt2d

    def EraseSnap(self):
        self.firstDisplay = False
        self.myContext.Remove(self.myAIS_Point)
        self.EraseRelation()

    def AnalyserEvent(self, tempPnt2d: gp_Pnt2d):
        self.curPnt2d = tempPnt2d
        self.SelectEvent()
        newPnt2d = self.bestPnt2d
        dist = self.minDistance
        type = self.GetSnapType()
        return self.findbestPnt2d,newPnt2d,dist,type

    def DrawRelation(self):
        self.myContext.SetSelected(self.curHilightedObj)

    def EraseRelation(self):
        self.myContext.ClearSelected()

    def countProject(self):
        if self.ProjectOnCurve.NbPoints() > 0:
            objectPnt2d = self.ProjectOnCurve.NearestPoint()
            return self.count()
        else:
            return False

    def count(self):
        curDistance = self.objectPnt2d.Distance(self.curPnt2d)
        if self.minDistance > curDistance:
            self.minDistance = curDistance
            return True
        else:
            return False

    def setFirstPnt(self, p: gp_Pnt2d,ttype:TangentType=None):
        pass

    def GetSnapType(self) -> Sketcher_SnapType:
        return 0
