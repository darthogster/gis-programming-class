stations_layer = QgsProject.instance().mapLayersByName('stations')[0]
districts_layer = QgsProject.instance().mapLayersByName('districts')[0]

required_fields = ['colour', 'some_value']
for field in required_fields:
    if field not in stations_layer.fields().names():
        raise Exception(f"0")


buffer_layer = QgsVectorLayer("Polygon?crs=EPSG:3857", "Буферы синей ветки", "memory")
provider = buffer_layer.dataProvider()

provider.addAttributes(stations_layer.fields())
buffer_layer.updateFields()

selected_districts = []
blue_value = 'blue'

for station in stations_layer.getFeatures():
    if station['colour'] == blue_value:
        try:
            buffer_size = float(station['some_value']) * 25
            buffer_geom = station.geometry().buffer(buffer_size, 8)
            
            feat = QgsFeature()
            feat.setGeometry(buffer_geom)
            feat.setAttributes(station.attributes())
            provider.addFeature(feat)
            
            for district in districts_layer.getFeatures():
                if buffer_geom.intersects(district.geometry()):
                    selected_districts.append(district.id())
        except Exception as e:
            print(f"не работает")
            continue


if selected_districts:
    districts_layer.select(selected_districts)
    buffer_layer.updateExtents()
    QgsProject.instance().addMapLayer(buffer_layer)
    

    
    print(f"Готово")
