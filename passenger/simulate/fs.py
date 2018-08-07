def read_csv(filename):
    points = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            parts = line.split('|')
            lon, lat, name = float(parts[2]), float(parts[3]), parts[4]
            points.append((lat, lon, name))
    return points
