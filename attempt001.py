# from win32api import GetSystemMetrics
# import comtypes

# NOTE: To run these code snippets, see FAQ "Getting Started STK COM integration using Python" at http://agiweb.force.com/faqs
# Start new instance of STK using win32com
# from win32com.client import Dispatch
# uiApplication = Dispatch('STK12.Application')
# uiApplication.Visible = True

# Start new instance of STK using the new API
from agi.stk12.stkdesktop import STKDesktop
stk = STKDesktop.StartApplication(visible=True)

# Get the IAgStkObjectRoot interface
root = stk.Root 

# Start new instance of STK using comtypes
# from comtypes.client import CreateObject
# uiApplication = CreateObject('STK12.Application')
# uiApplication.Visible = True

# Get our IAgStkObjectRoot interface
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
keplerian.SizeShape.PerigeeAltitude = 1000      # km
keplerian.SizeShape.ApogeeAltitude = 1000       # km

# Assign the other desired orbital parameters:
keplerian.Orientation.Inclination = 90         # deg
keplerian.Orientation.ArgOfPerigee = 12        # deg
keplerian.Orientation.AscNode.Value = 24       # deg
keplerian.Location.Value = 180                 # deg

# Apply the changes made to the satellite's state and propagate:
satellite.Propagator.InitialState.Representation.Assign(keplerian)
satellite.Propagator.Propagate()


off = input('Shut off: ')
while off != "off":
    off = input('Shut off: ')
    if off == "off":
        root.CloseScenario()
        uiApplication.Quit()
 