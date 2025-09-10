import json
import matplotlib.pyplot as plt
import winsound
import numpy as np
import threading
import numpy.typing as npt

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
ORANGE = "\033[33m"
GRAY = "\033[90m"

plt.ion()
fig = plt.figure()
try:
    fig.canvas.manager.set_window_title('Pre-Alert Radar') # type: ignore
except Exception:
    pass
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel("lon")
ax.set_ylabel("lat")
ax.set_zlabel("alt") # type: ignore
ax.set_xlim(34.181249, 35.52949)
ax.set_ylim(31.874889, 32.502673)
ax.set_zlim(0, 8000) # type: ignore
ax.view_init(elev=90, azim=-90) # type: ignore
plt.tight_layout()
plt.bar

heatmap_scatter = None
current_planes_scatter = None
close_points_scatter = None
isolated_planes_scatter = None

heatmap: npt.NDArray[np.float64] = np.array([])
current_planes: npt.NDArray[np.float64] = np.array([])
close_points = []
isolated_planes = []
close_points_sum = 0

int_hm_refresh = 10

def is_isolated(point: npt.NDArray[np.float64], reference_points_np: npt.NDArray[np.float64]):
    global close_points_sum
    lat1, lon1, alt1 = point

    lat2 = reference_points_np[:, 0]
    lon2 = reference_points_np[:, 1]
    alt2 = reference_points_np[:, 2]

    dlat = (lat1 - lat2) * 111_000
    dlon = (lon1 - lon2) * 111_000 * np.cos(np.radians((lat1 + lat2) / 2))
    dalt = (alt1 - alt2) * 0.3048 * 12

    distances = np.sqrt(dlat**2 + dlon**2 + dalt**2)

    close_mask = distances <= 2000
    close_count = min(np.count_nonzero(close_mask), 100)

    close_points.extend(reference_points_np[close_mask].tolist())

    isolated = close_count < 10
    close_points_sum += close_count
    print(f"{RED if isolated else GREEN}{close_count} {RESET}", end="")
    return isolated

while True:
    if int_hm_refresh < 9:
        int_hm_refresh += 1
    else:
        with open("heatmap.json") as f:
            try:
                heatmap = np.array(json.load(f))
            except: continue

        int_hm_refresh = 0

    if heatmap_scatter:
        try:
            heatmap_scatter.remove()
        except: pass

    with open("current.json") as f:
        try:
            current_planes = np.array(json.load(f))
        except: continue

    if current_planes_scatter:
        try:
            current_planes_scatter.remove()
        except: pass

    if close_points_scatter:
        try:
            close_points_scatter.remove()
        except: pass

    if isolated_planes_scatter:
        try:
            isolated_planes_scatter.remove()
        except: pass

    close_points = []
    isolated_planes = []
    close_points_sum = 0

    isolated_count = 0
    for plane in current_planes:
        if is_isolated(plane, heatmap):
            current_plane_mask = ~(current_planes == plane).all(axis=1)
            current_planes = current_planes[current_plane_mask]
            isolated_planes.append(plane)
            isolated_count += 1

    plane_count = len(current_planes) + isolated_count

    print(f"{ORANGE if isolated_count == 1 else RED if isolated_count > 0 else GREEN}{isolated_count}{RESET}{GRAY}/{plane_count}{RESET} A: ", end="")

    ax_title = ""
    close_points_avg = -1
    if plane_count > 0:
        close_points_avg = int(close_points_sum / plane_count)
        print(f"{GREEN if close_points_avg >= 25 else RED}{close_points_avg}{RESET} ", end="")
        ax_title = f"{close_points_avg}/100"
    else:
        print(f"{GREEN}0{RESET} ", end="")
        ax_title = "N/A"

    if close_points_avg != -1 and close_points_avg < 25 and isolated_count > 1:
        threading.Thread(target=lambda: winsound.Beep(1200, 2000), daemon=True).start()
        print(f"{RED}ATTK{RESET}")
        ax_title = "ATTK"
    else: print()

    ax.set_title(ax_title)

    heatmap_lats = heatmap[:, 0]
    heatmap_lons = heatmap[:, 1]
    heatmap_alts = heatmap[:, 2]

    if len(current_planes) > 0:
        current_planes_lats = current_planes[:, 0]
        current_planes_lons = current_planes[:, 1]
        current_planes_alts = current_planes[:, 2]
    else:
        current_planes_lats = []
        current_planes_lons = []
        current_planes_alts = []

    close_points_lats =  [p[0] for p in close_points]
    close_points_lons = [p[1] for p in close_points]
    close_points_alts = [p[2] for p in close_points]

    isolated_planes_lats = [p[0] for p in isolated_planes]
    isolated_planes_lons = [p[1] for p in isolated_planes]
    isolated_planes_alts = [p[2] for p in isolated_planes]

    heatmap_scatter = ax.scatter(heatmap_lons, heatmap_lats, heatmap_alts, c='b', marker='o', label='Heatmap', edgecolors='none', s=10, alpha=0.05) # type: ignore
    current_planes_scatter = ax.scatter(current_planes_lons, current_planes_lats, current_planes_alts, c='g', marker='o', label='Current Planes', edgecolors='k', linewidths=1.0, s=80, alpha=1) # type: ignore
    isolated_planes_scatter = ax.scatter(isolated_planes_lons, isolated_planes_lats, isolated_planes_alts, c='r', marker='o', label='Isolated Planes', edgecolors='k', linewidths=1.0, s=80, alpha=1) # type: ignore
    close_points_scatter = ax.scatter(close_points_lons, close_points_lats, close_points_alts, c='purple', marker='o', label='Close Points', edgecolors='none', linewidths=1.0, s=30, alpha=0.05) # type: ignore

    plt.draw()
    plt.pause(1)
