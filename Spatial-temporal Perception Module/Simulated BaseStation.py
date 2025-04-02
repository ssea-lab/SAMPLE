import numpy as np
import pandas as pd
np.random.seed(40)

def main():
    df = pd.read_csv('Spatial-temporal Perception Module/data/geolife/geolife.csv')
    points = df[['latitude', 'longitude']].values
    num_points = len(points)
    station_indices = np.random.choice(num_points, size=600, replace=False)
    stations = points[station_indices]
    radii = np.random.uniform(low=50, high=200, size=600)
    base_df = pd.DataFrame({
        'latitude': stations[:, 0],
        'longitude': stations[:, 1],
        'radius': radii
    })

    base_df.to_csv('base.csv', index=False)

if __name__ == "__main__":
    main()