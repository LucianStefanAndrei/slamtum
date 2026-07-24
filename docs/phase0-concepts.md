# Phase 0 — Concepts you must understand before writing code

Work through these in order. Each item says **why it matters for THIS project**, and links
to the exact ROS2 Humble docs page. Tick them off as you go — Phase 1 assumes all of them.

## 1. Nodes and topics (the pub/sub backbone)
- [ ] What a node is, and why our pipeline is 5 separate nodes instead of one program
  (isolation, restartability, per-node profiling — which matters in Phase 7).
- [ ] Topics as typed, many-to-many pub/sub channels. Our whole node graph is topics.
- Docs: [Understanding nodes](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html) ·
  [Understanding topics](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)

## 2. Messages — especially the three we live on
- [ ] `sensor_msgs/msg/Image` — how encoding (`rgb8` vs `16UC1` for TUM depth) and `step` work.
- [ ] `sensor_msgs/msg/CameraInfo` — the intrinsics matrix `K`. **This is what makes Phase 5's
  2D→3D projection possible.** If `K` is wrong, SLAM and fusion silently produce garbage.
- [ ] `sensor_msgs/msg/Imu` — orientation/velocity/acceleration + covariance.
- [ ] Every message has a `header` with `stamp` and `frame_id`. Internalize this now:
  **`frame_id` ties data to the TF tree, `stamp` ties it to time.**
- Docs: [Image](https://docs.ros2.org/latest/api/sensor_msgs/msg/Image.html) ·
  [CameraInfo](https://docs.ros2.org/latest/api/sensor_msgs/msg/CameraInfo.html) ·
  [Imu](https://docs.ros2.org/latest/api/sensor_msgs/msg/Imu.html)

## 3. QoS — the #1 "why is my subscriber silent?" trap
- [ ] Reliability (`reliable` vs `best_effort`), history/depth, durability.
- [ ] Why sensor streams use `SensorDataQoS` (best-effort, shallow queue): a late camera
  frame is worthless — drop it, don't retransmit it.
- [ ] The incompatibility rule: a `reliable` subscriber will NOT connect to a
  `best_effort` publisher. This will bite you in Phase 2 when wiring SLAM; know it now.
- Docs: [About QoS settings](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html)

## 4. TF2 and coordinate frames — the conceptual core of the whole project
- [ ] REP-105 frame conventions: `map` → `odom` → `base_link` (who publishes each edge, and
  why `map→odom` is a *correction*, not a pose).
- [ ] REP-103: axis conventions (x forward, y left, z up; but **optical frames** are
  z forward, x right, y down — TUM data lives in an optical frame!).
- [ ] Static vs dynamic transforms; how a node asks "where was the camera at time t?"
  That single question is Phase 5's fusion, so this must be solid.
- Docs: [Tf2 tutorials](https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Tf2-Main.html) ·
  [REP-103](https://www.ros.org/reps/rep-0103.html) · [REP-105](https://www.ros.org/reps/rep-0105.html)

## 5. Time, timestamps, and synchronization
- [ ] `builtin_interfaces/Time`, node clocks, and `use_sim_time` (we replay a dataset —
  we must publish *dataset* time, not wall time, or TF lookups fail).
- [ ] Why RGB + depth must be paired by timestamp (TUM records them asynchronously);
  `message_filters.ApproximateTimeSynchronizer` is the tool — you'll implement this in Phase 1.
- Docs: [Clock and Time](https://design.ros2.org/articles/clock_and_time.html) ·
  [message_filters](https://github.com/ros2/message_filters)

## 6. rosbag2
- [ ] Record/play, `--clock`, rate control. In Phase 1 you build a custom publisher FIRST
  (to learn timestamps/QoS/CameraInfo the hard way), then record it into a bag.
- Docs: [Recording and playing back data](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html)

## 7. Launch files
- [ ] Python launch files: starting several nodes with parameters and remappings in one command.
- Docs: [Launch tutorials](https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-Main.html)

## 8. Colcon workspace and package anatomy (what we built today)
- [ ] Workspace = `src/` (code, committed) + `build/`, `install/`, `log/` (generated, gitignored).
- [ ] Underlay vs overlay sourcing: `/opt/ros/humble/setup.bash` first, then `install/setup.bash`.
- [ ] The four files of an `ament_python` package — open ours and read them:
  - `package.xml` — manifest: name, dependencies, and `<build_type>ament_python</build_type>`
  - `setup.py` — how Python code gets installed; `console_scripts` is where node executables
    will be registered (`ros2 run <pkg> <node>` looks there)
  - `setup.cfg` — tells colcon to install scripts to `lib/<pkg>` so `ros2 run` can find them
  - `resource/<pkg>` — empty marker file registering the package in the ament index
- Docs: [Creating a workspace](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html) ·
  [Creating a package](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html)

---

## Humble vs Jazzy — decided: Humble
Jazzy targets Ubuntu 24.04; this Jetson runs JetPack on Ubuntu 22.04, where **Humble is the
supported LTS** (EOL May 2027 — fine for a portfolio project). No contest on this hardware.

## Phase 0 exit criteria
1. ROS2 Humble desktop installed (see README/chat for the install command — needs sudo).
2. `colcon build` succeeds from the workspace root.
3. `ros2 pkg list | grep slamtum` shows all five packages after sourcing `install/setup.bash`.
