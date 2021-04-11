Lat = 40.5215
Lon = -74.4618
Alt = -0.00104515

facility = root.CurrentScenario.Children.New(8, 'MyFacility')  # eFacility
# IAgFacility facility: Facility Object
facility.Position.AssignGeodetic(Lat, Lon, Alt)  # Latitude, Longitude, Altitude

# Set altitude to height of terrain
facility.UseTerrain = True

# Set altitude to a distance above the ground
facility.HeightAboveGround = 0.01   # km
