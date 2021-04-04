# from win32api import GetSystemMetrics
# import comtypes

# NOTE: To run these code snippets, see FAQ "Getting Started STK COM integration using Python" at http://agiweb.force.com/faqs
# Start new instance of STK using win32com
# from win32com.client import Dispatch
# uiApplication = Dispatch('STK12.Application')
# uiApplication.Visible = True
# root = uiApplication.Personality2

# Start new instance of STK using the new API
from agi.stk12.stkdesktop import STKDesktop
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
variable = "SetAnalysisTimePeriod * \"Today\" \"+4 hours\""
root.ExecuteCommand(variable)
# root.reWind()

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

root.Rewind()



# YOU NEED TO REWIND THE FUCKIN' SCENARIO TO SEE THE SATELLITE ASDFGHJKL;'
root.Rewind()


off = input('Press enter to end')