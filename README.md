# ROS2_TRAINING

ROS2の勉強・検証用リポジトリ。

## 主開発環境

このリポジトリは、次のWindows 11 + WSL2環境を主開発環境として使用する。
値は2026-09-10に実測したもので、空き容量や使用量は変動する。

| 項目 | 状態 |
|---|---|
| WSL2 | 導入済み(要 `wsl` で起動) |
| ディストリビューション | Ubuntu 24.04.3 LTS (noble) |
| 対応するROS2ディストロ | **Jazzy Jalisco**(LTS, サポート〜2029年) |
| Windows物理メモリ | 約61.6 GiB |
| WSL2割当メモリ / Swap | 30 GiB / 8 GiB |
| CPU | 24論理コア |
| WSL2ディスク | 約1,007 GB、Gazebo導入後の空き約922 GB |
| ROS2 | Jazzy Desktop導入済み |
| シミュレーター | Gazebo Harmonic連携（ros_gz 1.0.22）導入済み |
| 開発ツール | ros-dev-tools / colcon導入済み |
| GUI | WSLg有効。Gazebo GUI起動確認済み。OpenGLは現在llvmpipe |
| Docker | Docker DesktopとUbuntu内Docker Engineを検出。現在の接続先はDocker Desktop。詳細は[`docker/README.md`](./docker/README.md)参照 |

ROS2はネイティブWindows版も存在するが、パッケージ対応状況やビルド環境構築(Visual Studio Build Tools等)が複雑なため、
**WSL2 + Ubuntu 24.04 + ROS2 Jazzy** を検証環境として採用する。

## セットアップ手順(再構築時)

1. WSLを起動して Ubuntu に入る
   ```powershell
   wsl -d Ubuntu
   ```
2. ROS 2公式のUbuntu向けDebパッケージ手順に従い、Jazzy Desktopと開発ツールをインストールする
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y software-properties-common curl ca-certificates
   sudo add-apt-repository universe

   sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
     -o /usr/share/keyrings/ros-archive-keyring.gpg

   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
     | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

   sudo apt update
   sudo apt install -y ros-jazzy-desktop ros-dev-tools ros-jazzy-ros-gz ros-jazzy-xacro
   sudo rosdep init
   rosdep update
   ```
3. リポジトリ直下でROS 2環境を読み込む
   ```bash
   cd ~/ROS2_TEST
   source setup.bash
   ```
   毎回の読み込みを省略する場合だけ、source ~/ROS2_TEST/setup.bash を ~/.bashrc に追加する。
4. talker/listenerで動作確認
   ```bash
   ros2 run demo_nodes_cpp talker
   # 別ターミナルで
   ros2 run demo_nodes_py listener
   ```

## リポジトリ構成

```
ROS2_TRAINING/
├── src/
│   ├── ros2_training_cpp/    # C++ Publisher、設定、launch、テスト
│   ├── ros2_training_py/     # Python Subscriber、設定、launch、テスト
│   └── ros2_training_sim/    # Gazeboワールド、車輪型ロボット、LiDAR、bridge
├── docs/                      # 学習メモ・検証記録
├── docker/                    # 再現確認用のDocker環境
├── setup.bash                 # ROS 2 underlay/overlayの読み込み
└── README.md
```

`build/`、`install/`、`log/`はcolconが生成するGit管理外のディレクトリ。

## colcon workspaceのビルド

```bash
cd ~/ROS2_TEST
source setup.bash
rosdep install --from-paths src --ignore-src -r -y --skip-keys ament_python
colcon build --symlink-install
source install/setup.bash
```

`ament_python`はPythonパッケージのビルド種別で、ROS 2 Jazzy環境には導入済みのため、
`rosdep`のシステム依存解決対象から除外する。

## トレーニングノードの実行

C++ PublisherとPython Subscriberを同時に起動する。

```bash
cd ~/ROS2_TEST
source setup.bash
ros2 launch ros2_training_cpp training.launch.py
```

`training/chatter`トピックへ、C++ノードがメッセージを配信し、Pythonノードが受信して表示する。

テストは次のコマンドで実行する。

```bash
colcon test
colcon test-result --verbose
```

## Gazeboシミュレーション

Gazebo GUIを含めて起動する。

```bash
cd ~/ROS2_TEST
source setup.bash
ros2 launch ros2_training_sim simulation.launch.py
```

GUIを使わない場合は`headless:=true`を指定する。

```bash
ros2 launch ros2_training_sim simulation.launch.py headless:=true
```

別ターミナルからキーボードで走行操作できる。

```bash
source ~/ROS2_TEST/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

主なトピックは`/cmd_vel`（速度指令）、`/odom`（自己位置）、`/scan`（LiDAR）、
`/tf`、`/clock`。詳しい確認方法は
[`docs/simulation.md`](./docs/simulation.md)を参照。

## Dockerでの検証(オプション)

通常の開発は、CPU・メモリ・ディスクに余裕がある上記ネイティブ環境で行う。
Dockerは依存関係の隔離や再現確認が必要な場合の補助経路として使用する。

- 手順: [`docker/README.md`](./docker/README.md)
- 採用理由・検証時の環境情報: [`docs/docker_migration.md`](./docs/docker_migration.md)
