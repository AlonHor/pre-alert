# Pre-Alert

Pre-Alert is an advanced early warning system designed to notify users **before** traditional sirens are triggered during rocket attacks in Israel. By analyzing real-time movements of planes, the app detects abnormal, simultaneous deviations from their flight paths - changes that typically occur due to regulations enacted at the onset of an attack.

## Concept

When a rocket attack is imminent, aviation authorities enforce strict regulations causing planes in the affected region to change course, land, or hold patterns. These coordinated maneuvers often precede public warning sirens and alerts, especially when we're dealing with a long-range threat such as a ballistic missile.

Pre-Alert leverages this critical window by:

- **Monitoring Plane Positions:** Tracking and extracting detailed information from various aircraft signals.
- **Generating a Heatmap:** Continuously updating a 3D heatmap of plane movements and deviations over the region.
- **Detecting Anomalies:** Identifying clusters of planes that abruptly leave their routes in synchronization, suggesting regulatory action.
- **Early Notification:** Providing alerts when multiple planes become isolated or deviate in patterns indicative of imminent attack protocols, potentially ahead of official warnings and sirens.

Here's 1 hour of traffic, in a 60x timelapse:
![radar-timelapse](https://github.com/user-attachments/assets/13da5ff2-b598-4685-8fd3-1fb5f8dcb3e6)

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

## Contributing

All feedback, ideas, and contributions are welcome! Please open an issue or pull request if you'd like to help! :)

---

**Disclaimer:** Pre-Alert is experimental and should not be relied upon as the sole source of information for personal safety. Always follow official guidance and warning systems.
