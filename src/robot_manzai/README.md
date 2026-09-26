# robot_manzai

2台のロボットによる漫才を、YAML台本から順番に進行するROS 2 Jazzy向けサンプルパッケージ。

## ビルド

```bash
cd ~/ROS2_TEST
source setup.bash
rosdep install --from-paths src --ignore-src -r -y --skip-keys ament_python
colcon build --symlink-install --packages-select robot_manzai
source install/setup.bash
```

## 実行

```bash
ros2 launch robot_manzai manzai.launch.py
```

繰り返し再生する場合:

```bash
ros2 launch robot_manzai manzai.launch.py repeat:=true
```

別の台本を使う場合:

```bash
ros2 launch robot_manzai manzai.launch.py \
  script_file:=/absolute/path/to/manzai.yaml
```

## トピック

| トピック | 型 | 用途 |
|---|---|---|
| `manzai/line` | `std_msgs/msg/String` | 台詞番号、役割、感情、動作を含むJSON |
| `manzai/speech_text` | `std_msgs/msg/String` | 音声合成へ渡す本文 |
| `manzai/motion_cue` | `std_msgs/msg/String` | ロボット制御へ渡す動作名 |

動作確認:

```bash
ros2 topic echo /manzai/line
ros2 topic echo /manzai/speech_text
ros2 topic echo /manzai/motion_cue
```

## 台本形式

```yaml
title: サンプル
lines:
  - role: boke
    text: 台詞
    emotion: proud
    motion: nod
    pause_sec: 1.5
```

`pause_sec` は、その台詞を配信してから次の台詞までの秒数。音声合成・実機動作は、このパッケージの各トピックを購読するノードとして追加する。

全体設計と段階的な実装方針は [docs/robot_manzai.md](../../docs/robot_manzai.md) を参照。
