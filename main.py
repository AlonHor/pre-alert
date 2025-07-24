import json
import matplotlib.pyplot as plt
import winsound
import numpy as np

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Load and plot static blue points once
with open("paths.json") as f:
    all_paths = json.load(f)

lats = [p[0] for p in all_paths]
longs = [p[1] for p in all_paths]
alts = [p[2] for p in all_paths]

ax.scatter(longs, lats, alts, c='b', marker='o', label='Static Points', s=50, alpha=0.1) # type: ignore
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Altitude (m)')  # type: ignore
plt.draw()

update_scatter = None

def is_isolated(point, reference_points):
    lat1, lon1, alt1 = point
    min_distance = 100000
    isolated = True # DEL
    for lat2, lon2, alt2 in reference_points:
        dlat = (lat1 - lat2) * 111000
        dlon = (lon1 - lon2) * 111000 * np.cos(np.radians((lat1 + lat2) / 2))
        dalt = alt1 - alt2
        distance = np.sqrt(dlat**2 + dlon**2 + dalt**2)
        if distance < min_distance:
            min_distance = distance
        if distance <= 2500:
            isolated = False
            # return False
    print(min_distance)
    return isolated # return True

while True:
    try:
        with open("update.json") as f:
            updates = json.load(f)

        # Remove previous red points if they exist
        if update_scatter:
            update_scatter.remove()

        # Check isolation and beep
        for point in updates:
            if is_isolated(point, all_paths):
                winsound.Beep(1000, 200)

        # Plot new red points
        update_lats = [p[0] for p in updates]
        update_longs = [p[1] for p in updates]
        update_alts = [p[2] for p in updates]

        update_scatter = ax.scatter(update_longs, update_lats, update_alts, c='r', marker='o', label='Updated Points', edgecolors='k', linewidths=1.0, s=80, alpha=1) # type: ignore
        plt.draw()

    except Exception as e:
        print("Error:", e)

    plt.pause(10)
