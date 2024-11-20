variables_unidades_de_medida = {
    "temperature": ["K", "C", "F"],
    "2m_temperature": ["K", "C", "F"],
    "u_component_of_wind": ["m/s", "km/h", "mph", "kts"],
    "v_component_of_wind": ["m/s", "km/h", "mph", "kts"],
    "10m_u_component_of_wind": ["m/s", "km/h", "mph"],
    "10m_v_component_of_wind": ["m/s", "km/h", "mph"],
    "mean_sea_level_pressure": ["Pa", "hPa"],
    "specific_humidity": ["kg|kg", "g|kg"],
    "surface_pressure": ["Pa", "hPa"],
    "toa_incident_solar_radiation": ["J/m^2", "W/m^2"],
    "total_cloud_cover": ["(0-1)"],
    "vertical_velocity": ["Pa/s", "Pa/h"],
    "total_precipitation": ["mm"],
}

mapeo_correcto = {
    "m|s": "m/s",
    "km|h": "km/h",
    "kg|kg": "kg/kg",
    "g|kg": "g/kg",
    "Pa|s": "Pa/s",
    "Pa|h": "Pa/h",
    "J|m^2": "J/m^2",
    "W|m^2": "W/m^2",
}