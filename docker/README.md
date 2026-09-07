# Docker運用手順(検証用・オプション)

`README.md`本体のネイティブ手順(WSL2 + Ubuntu 24.04に直接ROS2 Jazzyをインストール)と併用する、
コンテナ経由の検証手段。どちらか一方に統一する必要はなく、用途に応じて選択する。

判断根拠は [`docs/docker_migration.md`](../docs/docker_migration.md) を参照。

## 前提

- WSL2 Ubuntu上で作業する(Docker Desktopは使わない)。
- WSL2側でDocker Engineをインストール済みであること。
  ```bash
  # WSL2 Ubuntu内で実行
  sudo apt update
  sudo apt install -y ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt update
  sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
  sudo usermod -aG docker $USER
  # 上記usermod後は一度WSLを再起動(`wsl --shutdown`をWindows側で実行)
  ```
- `/etc/wsl.conf` に `systemd=true` が設定済みであること(このリポジトリ検証時点では設定済みを確認)。

## ビルド・起動

```bash
cd ~/ROS2_TRAINING/docker   # WSL側にcloneしたパス
docker compose build
docker compose run --rm ros2
```

コンテナ内でREADME本体と同じ動作確認ができる。

```bash
ros2 run demo_nodes_cpp talker
# 別ターミナル(同コンテナに入る場合は `docker compose exec ros2 bash`)
ros2 run demo_nodes_py listener
```

## GUI(RViz2等)を使う場合

`docker-compose.yml`は`/tmp/.X11-unix`と`/mnt/wslg`をマウントし、`DISPLAY`等の環境変数を引き継ぐ設定にしてある。
WSLg(Windows 11標準)が有効な環境であれば、追加設定なしで以下が動く想定。

```bash
docker compose run --rm ros2 rviz2
```

動かない場合はGPUドライバやWSLgのバージョンに依存するため、まずネイティブ(README本体の手順)側で
`rviz2`が起動するか切り分けること。

## メモリが足りない場合

WSL2はデフォルトで物理メモリの一部しか使わない設定になっていることが多い(`.wslconfig`未設定時)。
Gazebo等重いシミュレーションで不足する場合は、Windows側の `%USERPROFILE%\.wslconfig` に以下を追記し、
`wsl --shutdown` 後に再起動する。

```ini
[wsl2]
memory=12GB
```

## 復旧・作り直し

コンテナが壊れた場合はイメージを作り直すだけで良い。

```bash
docker compose down
docker compose build --no-cache
```

`src/`はホスト側のリポジトリをマウントしているだけなので、コンテナを壊してもソースコードは失われない。
