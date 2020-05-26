import cartopy.crs as ccrs
import matplotlib.pyplot as plt

ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()

# AR
ar_lat, ar_lon = -34.613150, -58.377230

# US
# 67.17.94.249
us1_lat, us1_lon = 32.783060, -96.806670

# 4.69.142.209
us2_lat, us2_lon = 40.714270, -74.005970

# 195.122.181.62
us3_lat, us3_lon = 32.783060, -96.806670

# DE
# 188.1.144.58, 188.1.235.118, 130.149.126.78
de_lat, de_lon = 52.524370, 13.410530

plt.plot([ar_lon, us1_lon], [ar_lat, us1_lat], color='blue', linestyle='solid', marker='o', transform=ccrs.PlateCarree())
plt.text(ar_lon - 3, ar_lat - 12, '181.96.120.69\n181.96.120.63\n190.216.88.3', horizontalalignment='right',transform=ccrs.Geodetic())

plt.plot([us1_lon, us2_lon], [us1_lat, us2_lat], color='red', linestyle='dashed', marker='o', transform=ccrs.PlateCarree())
plt.text(us1_lon - 3, us1_lat - 12, '67.17.94.249\n195.122.181.62', horizontalalignment='right',transform=ccrs.Geodetic())

plt.plot([us2_lon, us3_lon], [us2_lat, us3_lat], color='green', linestyle='dotted', marker='o', transform=ccrs.Geodetic())
plt.text(us2_lon + 10, us2_lat + 3, '4.69.142.209', horizontalalignment='right',transform=ccrs.Geodetic())

plt.plot([us3_lon, de_lon], [us3_lat, de_lat], color='black', linestyle='dashdot', marker='o', transform=ccrs.PlateCarree())
plt.text(de_lon + 10, de_lat + 3, '188.1.144.58\n188.1.235.118\n130.149.126.78', horizontalalignment='right',transform=ccrs.Geodetic())

plt.show()