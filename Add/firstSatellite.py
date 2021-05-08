# Libraries that might be useful
import math

# from win32api import GetSystemMetrics
# import comtypes

# NOTE: To run these code snippets, see FAQ "Getting Started STK COM integration using Python" at http://agiweb.force.com/faqs
# Start new instance of STK using win32com
# from win32com.client import Dispatch
# uiApplication = Dispatch('STK12.Application')
# uiApplication.Visible = True
# root = uiApplication.Personality2

# Start new instance of STK using the new API
from agi.stk12.stkdesktop import STKDesktop # Update this line
stk = STKDesktop.StartApplication(visible=True)
root = stk.Root

# Start new instance of STK using comtypes
# from comtypes.client import CreateObject
# uiApplication = CreateObject('STK12.Application')
# uiApplication.Visible = True
# root = uiApplication.Personality2

# Note: When 'root=uiApplication.Personality2' is executed, the comtypes library automatically creates a gen folder that contains STKUtil and STK Objects. 
# After running this at least once on your computer, the following two lines should be moved before the 'uiApplication=CreateObject("STK12.Application")'
# line for improved performance.  

# from comtypes.gen import STKUtil
# from comtypes.gen import STKObjects

root.NewScenario("Example_Scenario")
variable = "SetAnalysisTimePeriod * \"Today\" \"+24 hours\""
root.ExecuteCommand(variable)
# root.reWind()


# Satellite Code

# IAgStkObjectRoot root: STK Object Model Root
satellite = root.CurrentScenario.Children.New(18, 'MySatellite')  # eSatellite


# IAgSatellite satellite: Satellite object
keplerian = satellite.Propagator.InitialState.Representation.ConvertTo(1)  # eOrbitStateClassical, Use the Classical Element interface
keplerian.SizeShapeType = 0  # eSizeShapeAltitude, Changes from Ecc/Inc to Perigee/Apogee Altitude
keplerian.LocationType = 5  # eLocationTrueAnomaly, Makes sure True Anomaly is being used
keplerian.Orientation.AscNodeType = 0  # eAscNodeLAN, Use LAN instead of RAAN for data entry

# Assign the perigee and apogee altitude values:
keplerian.SizeShape.PerigeeAltitude = 500      # km
keplerian.SizeShape.ApogeeAltitude = 600       # km

# Assign the other desired orbital parameters:
keplerian.Orientation.Inclination = 90         # deg
keplerian.Orientation.ArgOfPerigee = 12        # deg
keplerian.Orientation.AscNode.Value = 24       # deg
keplerian.Location.Value = 180                 # deg

# Apply the changes made to the satellite's state and propagate:
satellite.Propagator.InitialState.Representation.Assign(keplerian)
satellite.Propagator.Propagate()

# Code for adding 45 satellites with 2 deg difference in inclinication angle (0-90)
# for i in range(46):
    # name = "Satellite" + str(i)
    # satellite2 = root.CurrentScenario.Children.New(18, name)  # eSatellite
    
    # All the constant stuff
    # keplerian = satellite2.Propagator.InitialState.Representation.ConvertTo(1)
    # keplerian.SizeShapeType = 0  # eSizeShapeAltitude, Changes from Ecc/Inc to Perigee/Apogee Altitude
    # keplerian.LocationType = 5  # eLocationTrueAnomaly, Makes sure True Anomaly is being used
    # keplerian.Orientation.AscNodeType = 0  # eAscNodeLAN, Use LAN instead of RAAN for data entry

    # keplerian.SizeShape.PerigeeAltitude = 500      # km
    # keplerian.SizeShape.ApogeeAltitude = 600       # km
    # keplerian.Orientation.Inclination = 2*i        # deg > the one thing thats changing
    # keplerian.Orientation.ArgOfPerigee = 12        # deg
    # keplerian.Orientation.AscNode.Value = 24       # deg
    # keplerian.Location.Value = 180                 # deg

    # satellite2.Propagator.InitialState.Representation.Assign(keplerian)
    # satellite2.Propagator.Propagate()
    # print(name + ": done")


# SOLIS Code

# Because fuck those guys I don't have 45k$ for you >:0
# IAgSatellite satellite: Satellite object
basic = satellite.Attitude.Basic
basic.SetProfileType(16)  # eProfileSpinning
basic.Profile.Body.AssignXYZ(0, 0, 1)
basic.Profile.Inertial.AssignXYZ(0, 1, 0)
basic.Profile.Rate = 6   # rev/sec


# Facility Code

# Rutgers Ground Station Coordinates
Lat = 40.5215   # Latitude (deg)
Lon = -74.4618   # Longitude (deg)
Alt = -0.00104515   # Altitude (km)

facility = root.CurrentScenario.Children.New(8, 'RUGS')  # eFacility
# IAgFacility facility: Facility Object
facility.Position.AssignGeodetic(Lat, Lon, Alt)  # Latitude, Longitude, Altitude

# Set altitude to height of terrain
facility.UseTerrain = True

# Set altitude to a distance above the ground
facility.HeightAboveGround = 0.01   # km (height above the building)


# Sensor Code
sensor = facility.Children.New(20, 'MySensor')

# IAgSensor sensor: Sensor object
# Change pattern and set
sensor.CommonTasks.SetPatternSimpleConic(90, 1)

# Runs smoother if you do this?
root.BeginUpdate()

# Adding a range constraint 
range1 = sensor.AccessConstraints.AddConstraint(34) # Range is 34, more can be found by using the code above
range1.EnableMin = True
range1.EnableMax = True
range1.Min = 0
range1.Max = 1000

# Adding an angle of elevation constraint
# angle_s = sensor.AccessConstraints.AddConstraint(14)
# angle_s.EnableMin = True
# angle_s.EnableMax = True
# angle_s.Min = 0
# angle_s.Max = 90

# Runs smoother if you do this!
root.EndUpdate()


# Access Code

# Compute Access
access = satellite.GetAccessToObject(sensor)
access.ComputeAccess()

# Getting information from access
intervalCollection = access.ComputedAccessIntervalTimes
computedIntervals = intervalCollection.ToArray(0,-1)
access.SpecifyAccessIntervals(computedIntervals)

# Displaying that information
print(computedIntervals)
print()
print(len(computedIntervals))


# YOU NEED TO REWIND THE FUCKIN' SCENARIO TO SEE THE SATELLITEs ASDFGHJKL;'
root.Rewind()

# Killing STK
off = input('Press enter to kill STK')
