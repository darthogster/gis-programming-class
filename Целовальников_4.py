from osgeo import gdal
from qgis.core import QgsProject
import os


input_path = r"C:\Users\Darthog\Downloads\3.tif"
src_ds = gdal.Open(input_path)


bands_data = []
for band_num in range(1, src_ds.RasterCount + 1):
    band = src_ds.GetRasterBand(band_num)
    band_array = band.ReadAsArray().astype(float)
    bands_data.append(band_array)


driver = gdal.GetDriverByName('GTiff')
output_path = r"C:\Users\Darthog\Downloads\result_with_gcps.tif"
dst_ds = driver.Create(output_path, 
                      src_ds.RasterXSize, 
                      src_ds.RasterYSize, 
                      src_ds.RasterCount, 
                      gdal.GDT_Float32)


for i, band_data in enumerate(bands_data, start=1):
    dst_ds.GetRasterBand(i).WriteArray(band_data)


footprint_path = r"C:\Users\Darthog\Downloads\footprint_3.shp"
footprint_layer = QgsProject.instance().mapLayersByName(os.path.basename(footprint_path)[:-4])[0]
feature = footprint_layer.getFeature(0)
geom = feature.geometry().asPolygon()[0]

coords = []
for point in geom[:4]:
    coords.append((point.x(), point.y()))

dst_ds.SetProjection(footprint_layer.crs().toWkt())

gcps = []
xsize = dst_ds.RasterXSize
ysize = dst_ds.RasterYSize


gcps.append(gdal.GCP(coords[0][0], coords[0][1], 0, 0, 0))
gcps.append(gdal.GCP(coords[1][0], coords[1][1], 0, xsize-1, 0))
gcps.append(gdal.GCP(coords[2][0], coords[2][1], 0, xsize-1, ysize-1))
gcps.append(gdal.GCP(coords[3][0], coords[3][1], 0, 0, ysize-1))


dst_ds.SetGCPs(gcps, footprint_layer.crs().toWkt())
dst_ds.FlushCache()


