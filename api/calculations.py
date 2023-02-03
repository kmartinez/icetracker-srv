import numpy as np
from haversine import haversine_vector, Unit

# Quickly calculates the velocity for many tuples of lat, long, timestamp
# Unit: Meters/Year
def velocity_a_s_vector(lat_longs_before, lat_longs_after, times_before, times_after):
    # Calculate the distance in M between both sets of coordinates using haversine formula
    distances_m = haversine_vector(lat_longs_before, lat_longs_after, unit=Unit.METERS)
    # Calculate the differences between times in timedelta objects
    time_differences = np.subtract(times_after, times_before)
    get_time_delta_in_years = np.vectorize(lambda t_delta: t_delta.total_seconds() / 31536000)

    # Convert between timedelta objects and years
    time_differences_years = get_time_delta_in_years(time_differences)

    # Calculate velocity using distance/time
    reciprocal_time_differences_years = np.reciprocal(time_differences_years)
    velocities_m_a = np.multiply(distances_m, reciprocal_time_differences_years)

    return velocities_m_a

# Quickly calculates the displacement for many tuples of lat, long
# Unit: Meters
def displacement_m_vector(lat_longs_before, lat_longs_after):
    # Calculate the distance in M between both sets of coordinates using haversine formula
    return haversine_vector(lat_longs_before, lat_longs_after, unit=Unit.METERS)