# ROS2_TRAINING

ROS2の勉強・検証用リポジトリ。

## Windowsでの実行環境について

このマシン(Windows 11)での動作確認結果:

| 項目 | 状態 |
|---|---|
| WSL2 | 導入済み(要 `wsl` で起動) |
| ディストリビューション | Ubuntu 24.04.2 LTS (noble) |
| 対応するROS2ディストロ | **Jazzy Jalisco**(LTS, サポート〜2029年) |
| ROS2インストール状況 | 未インストール |
| Docker | 未インストール |

ROS2はネイティブWindows版も存在するが、パッケージ対応状況やビルド環境構築(Visual Studio Build Tools等)が複雑なため、
**WSL2 + Ubuntu 24.04 + ROS2 Jazzy** を検証環境として採用する。

## セットアップ手順(WSL2 + ROS2 Jazzy)

1. WSLを起動して Ubuntu に入る
   ```powershell
   wsl -d Ubuntu
   ```
2. ROS2 Jazzy をインストール(公式手順に従う)
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y software-properties-common curl
   sudo add-apt-repository universe

   sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
     -o /usr/share/keyrings/ros-archive-keyring.gpg

   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
     | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

   sudo apt update
   sudo apt install -y ros-jazzy-desktop ros-dev-tools
   ```
3. 環境変数を設定(`~/.bashrc` に追記)
   ```bash
   echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
   source ~/.bashrc
   ```
4. 動作確認
   ```bash
   ros2 run demo_nodes_cpp talker
   # 別ターミナルで
   ros2 run demo_nodes_py listener
   ```

## リポジトリ構成

```
ROS2_TRAINING/
├── src/        # colcon workspaceのROS2パッケージを配置
├── docs/       # 学習メモ・検証記録
└── README.md
```

## colcon workspaceのビルド

```bash
cd ~/ROS2_TRAINING   # WSL側にcloneしたパス
colcon build
source install/setup.bash
```
