# Pre-Alert

Pre-Alert is an advanced early warning system designed to notify users **before** traditional sirens are triggered during rocket attacks in Israel. By analyzing real-time movements of planes, the app detects abnormal, simultaneous deviations from their flight paths - changes that typically occur due to regulations enacted at the onset of an attack.

As of now, the system runs as a Python script, but I'm looking forward to rewriting it in either Rust, C or C++ in the near future!

## Concept

When a rocket attack is imminent, aviation authorities enforce strict regulations causing planes in the affected region to change course, land, or hold patterns. These coordinated maneuvers often precede public warning sirens and alerts, especially when we're dealing with a long-range threat such as a ballistic missile.

Pre-Alert leverages this critical window by:

- **Monitoring Plane Positions:** Tracking and extracting detailed information from various aircraft signals.
- **Generating a Heatmap:** Continuously updating a 3D heatmap of plane movements and deviations over the region.
- **Detecting Anomalies:** Identifying clusters of planes that abruptly leave their routes in synchronization, suggesting regulatory action.
- **Early Notification:** Providing alerts when multiple planes become isolated or deviate in patterns indicative of imminent attack protocols, potentially ahead of official warnings and sirens.

Here's 1 hour of traffic, in a 60x timelapse:

![radar-timelapse](https://github.com/user-attachments/assets/13da5ff2-b598-4685-8fd3-1fb5f8dcb3e6)

## Working Proof
While leaving the detection system running on the background in my room, I suddenly started hearing **BEEP**, **BEEP**, **BEEP**, **BEEP**... I rushed to my room to see if it actually detected an oncoming attack, and, well, 2 minutes later, I got a notification on my phone from Home Front Command notifying about an oncoming ballistic missile.

### Here are the logs of the actual event - worth having a look!:

Format is as follows, where pr = path rating, i.e. how "on-path" the plane is (0-100), according to the heatmap: 
```
<plane 1 pr> <plane 2 pr> <plane 3 pr>(...) <isolated planes>/<total planes> A:<average pr>
```

<details>
  <summary><b>[IMG]</b> Before the attack, everything seemed fine:</summary>
  <img width="179" height="150" alt="image" src="https://github.com/user-attachments/assets/2d7f30df-fd0a-4f7f-8def-75461d7f00fa" />
</details>

<details>
  <summary><b>[IMG]</b> Right when the attack began, the system quickly detected the planes beginning their evacuation patterns. Numbers going down are simply planes doing <i>something</i> they don't normally do:</summary>
  <img width="126" height="372" alt="image" src="https://github.com/user-attachments/assets/450df071-65e3-4df7-9cf2-bb7256938275" />
</details>

<details>
  <summary><b>[IMG]</b> The numbers kept going down, while another plane joined in, evacuating too:</summary>
  <img width="152" height="415" alt="image" src="https://github.com/user-attachments/assets/2f99d1d5-41ef-4c9b-8f21-74869ab7c253" />
</details>

<details>
  <summary><b>[IMG]</b> And RIGHT HERE, is when the <b>BEEP</b>s began:</summary>
  <img width="205" height="330" alt="image" src="https://github.com/user-attachments/assets/f2593cad-87ae-4797-ab74-3557ca172955" />
</details>

<details>
  <summary><b>[IMG]</b> And it kept going...</summary>
  <img width="141" height="847" alt="image" src="https://github.com/user-attachments/assets/75cf0b74-99a8-4a30-bf43-ca663250254a" />
</details>

## Simple Mobile App Vision

Pre-Alert's goal is to offer a **very simple mobile app**:

- You install the app and enable notifications.
- When an attack is detected, you'll receive a notification on your phone.
- The data processing and detection runs in the cloud, keeping the app lightweight and fully automatic for end users.

## Status

Pre-Alert is **actively working and near completion**. It already performs the following:

- Fetches and decodes real-time flight data from multiple aircraft types and signal formats.
- Filters and processes aircraft, extracting position, altitude, flight status, and other relevant metrics.
- Builds and updates a heatmap (`heatmap.json`) of aircraft movements at regular intervals.
- Analyzes current aircraft positions (`current.json`) and compares them to historical patterns.
- Detects and highlights isolated planes, indicating possible regulatory maneuvers.
- Visualizes data and triggers notifications (including audible alerts) if anomalies are detected.

## Roadmap

- [x] Integrate real-time flight data sources and decode multiple aircraft formats.
- [x] Build and update a persistent heatmap of aircraft movements.
- [x] Detect and notify about isolated planes and abnormal movement clusters.
- [x] Visualize aircraft positions and heatmap deviations.
- [x] Implement audible alerts for detected anomalies.
- [ ] Create a simple mobile app with push notification support.
- [ ] Deploy detection backend to a cloud environment.
- [ ] Add support for configurable alert rules and thresholds.

## How To Run

In order to run the backend detection system you must have a program running to populate `current.json` with live aircraft positions. This can be done using official APIs (e.g. "FlightRadar24" or "ADSBx"). Once you do, simply run the python script by running `python main.py`.

## Contributing

All feedback, ideas, and contributions are welcome! Please open an issue or pull request if you'd like to help! ❤️

---

⚠️ **Disclaimer:** Pre-Alert is <u>experimental</u> and should **NOT** be relied upon as the sole source of information for personal safety. Always follow official guidance and warning systems, i.e. Home Front Command (Pikud HaOref).
