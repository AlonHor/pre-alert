import json
import matplotlib.pyplot as plt
import winsound
import numpy as np
import threading

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"

plt.ion()
fig = plt.figure()
try:
    fig.canvas.manager.set_window_title('Pre-Alert Radar') # type: ignore
except Exception:
    pass
ax = fig.add_subplot(111, projection='3d')

heatmap_scatter = None
current_planes_scatter = None
close_points_scatter = None
isolated_planes_scatter = None

heatmap = []
current_planes = []
close_points = []
isolated_planes = []

def is_isolated(point, reference_points):
    lat1, lon1, alt1 = point
    min_distance = 100000
    close_points_count = 0
    for lat2, lon2, alt2 in reference_points:
        dlat = (lat1 - lat2) * 111000
        dlon = (lon1 - lon2) * 111000 * np.cos(np.radians((lat1 + lat2) / 2))
        dalt = (alt1 - alt2) * 4
        distance = np.sqrt(dlat**2 + dlon**2 + dalt**2)
        if distance < min_distance:
            min_distance = distance
        if distance <= 2000: #2500
            close_points.append([lat2, lon2, alt2])
            close_points_count += 1

    isolated = close_points_count < 10
    print(f"{RED if isolated else GREEN}{close_points_count} {RESET}", end="")
    return isolated

while True:
    try:
        with open("heatmap.json") as f:
            heatmap = json.load(f)

        if heatmap_scatter:
            heatmap_scatter.remove()

        lats = [p[0] for p in heatmap]
        longs = [p[1] for p in heatmap]
        alts = [p[2] for p in heatmap]

        ax.set_xlabel("long")
        ax.set_ylabel("lat")
        heatmap_scatter = ax.scatter(longs, lats, alts, c='b', marker='o', label='Heatmap', alpha=0.05)

        with open("current.json") as f:
            current_planes = json.load(f)

        if current_planes_scatter:
            current_planes_scatter.remove()

        if close_points_scatter:
            close_points_scatter.remove()

        if isolated_planes_scatter:
            isolated_planes_scatter.remove()

        close_points = []
        isolated_planes = []

        print("amount of points in 2km rad per plane: ", end="")

        isolated_count = 0
        for plane in current_planes:
            if is_isolated(plane, heatmap):
                current_planes.remove(plane)
                isolated_planes.append(plane)
                isolated_count += 1

        if isolated_count > 2:
            threading.Thread(target=lambda: winsound.Beep(1200, 2000), daemon=True).start()

        print(f"\nisolated: {RED if isolated_count > 0 else GREEN}{isolated_count}{RESET}\n")

        current_planes_lats = [p[0] for p in current_planes]
        current_planes_longs = [p[1] for p in current_planes]
        current_planes_alts = [p[2] for p in current_planes]

        close_points_lats = [p[0] for p in close_points]
        close_points_longs = [p[1] for p in close_points]
        close_points_alts = [p[2] for p in close_points]

        isolated_planes_lats = [p[0] for p in isolated_planes]
        isolated_planes_longs = [p[1] for p in isolated_planes]
        isolated_planes_alts = [p[2] for p in isolated_planes]

        current_planes_scatter = ax.scatter(current_planes_longs, current_planes_lats, current_planes_alts, c='g', marker='o', label='Updated Points', edgecolors='k', linewidths=1.0, s=80, alpha=1) # type: ignore
        isolated_planes_scatter = ax.scatter(isolated_planes_longs, isolated_planes_lats, isolated_planes_alts, c='r', marker='o', label='Isolated Planes', edgecolors='k', linewidths=1.0, s=80, alpha=1) # type: ignore
        close_points_scatter = ax.scatter(close_points_longs, close_points_lats, close_points_alts, c='y', marker='o', label='Close Points', edgecolors='k', linewidths=1.0, s=30, alpha=0.5) # type: ignore
        plt.draw()

    except Exception as e:
        print("Error:", e)

    plt.pause(1)
