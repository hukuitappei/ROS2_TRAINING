# Gazeboシミュレーション

## 目的

ROS 2から送った速度指令をGazeboの物理シミュレーションへ反映し、
オドメトリと2D LiDARをROS 2トピックとして取得する。

## 構成

- シミュレーター: Gazebo Harmonic
- ROS連携: `ros_gz_sim`、`ros_gz_bridge`
- ロボット: 二輪差動駆動 + キャスター
- センサー: 360サンプル、最大8 mのGPU LiDAR
- ワールド: 平面、照明、LiDAR確認用障害物

## 起動

```bash
cd ~/ROS2_TEST
source setup.bash
ros2 launch ros2_training_sim simulation.launch.py
```

GUIなしで実行する場合:

```bash
ros2 launch ros2_training_sim simulation.launch.py headless:=true
```

## 操作

別ターミナルで次を実行する。

```bash
source ~/ROS2_TEST/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

1回だけ速度指令を送る例:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist +  "{linear: {x: 0.4}, angular: {z: 0.2}}"
```

停止指令:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist +  "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

## 確認

```bash
ros2 topic echo /odom
ros2 topic echo /scan
ros2 run tf2_ros tf2_echo odom base_link
ros2 run tf2_ros tf2_echo base_link training_robot/lidar_link/lidar
```

2026-09-10の実機確認では、`/cmd_vel`に直進0.4 m/s・旋回0.2 rad/sを送り、
`/odom`で同じ速度と位置変化を確認した。`/scan`では360方向の距離データを確認した。

## WSLgで描画できない場合

まずヘッドレスモードで物理演算とROS bridgeを切り分ける。

```bash
ros2 launch ros2_training_sim simulation.launch.py headless:=true
```

この環境では`btsi1`を`video`と`render`グループへ追加済み。
GUIに問題が残る場合は、WSLを再起動してから再確認する。

```powershell
wsl --shutdown
```

2026-09-10時点ではGazebo GUIが8秒間継続起動することを確認したが、
OpenGL rendererはRTX 3080ではなく`llvmpipe`（CPU描画）だった。
現在の小規模ワールド、物理演算、LiDARは動作する。
カメラ追加や大規模ワールドへ進む前に、WSL／WSLg更新後のGPUアクセラレーションを再確認する。
