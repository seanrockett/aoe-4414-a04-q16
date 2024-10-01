# script_name.py
#
# Usage: python3 ecef_to_sez o_x_km o_y_km o_z_km x_km y_km z_km
#  Text explaining script usage
# Parameters:
#  arg1: description of argument 1
#  arg2: description of argument 2
#  ...
# Output:
#  A description of the script output
#
# Written by Sean Rockett
# Other contributors: Brad Denby, the part of the code where the llh of the sez origin is calculated comes from his ecef_to_llh.py script.
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
# e.g., import math # math module
import sys # argv
import math

# "constants"
R_E_KM = 6378.137
E_E = 0.081819221456

# helper functions

# denominator calculation
def calc_denom(ecc,lat_rad):
    return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad))**2)

# initialize script arguments
o_x_km = 'nan' # x origin of sez frame in ecef coordinates
o_y_km = 'nan' # y origin of sez frame in ecef coordinates
o_z_km = 'nan' # z origin of sez frame in ecef coordinates
x_km = 'nan' # ecef x location of object
y_km = 'nan' # ecef y location of object
z_km = 'nan' # ecef z location of object

# parse script arguments
if len(sys.argv)==7:
    o_x_km = float(sys.argv[1])
    o_y_km = float(sys.argv[2])
    o_z_km = float(sys.argv[3])
    x_km = float(sys.argv[4])
    y_km = float(sys.argv[5])
    z_km = float(sys.argv[6])
else:
    print(\
    'Usage: '\
    'python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'\
    )
    exit()

# write script below this line

# determine ecef vector from sez origin to object
local_x = x_km-o_x_km
local_y = y_km-o_y_km
local_z = z_km-o_z_km

# determine llh of sez origin
lon_rad = math.atan2(o_y_km,o_x_km)
lon_deg = lon_rad*180.0/math.pi

lat_rad = math.asin(o_z_km/math.sqrt(o_x_km**2+o_y_km**2+o_z_km**2))
r_lon_km = math.sqrt(o_x_km**2+o_y_km**2)
prev_lat_rad = float('nan')

c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(E_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((o_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1
  
hae_km = r_lon_km/math.cos(lat_rad)-c_E

# determine sez location of object
sin_lat = math.sin(lat_rad)
sin_lon = math.sin(lon_rad)
cos_lat = math.cos(lat_rad)
cos_lon = math.cos(lon_rad)

v1_x = cos_lon*local_x + sin_lon*local_y
v1_y = -sin_lon*local_x + cos_lon*local_y
v1_z = local_z

s_km = sin_lat*v1_x - cos_lat*v1_z
e_km = v1_y
z_km = cos_lat*v1_x + sin_lat*v1_z

# print results
print(s_km)
print(e_km)
print(z_km)