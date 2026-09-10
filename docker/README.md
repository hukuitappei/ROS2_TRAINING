# Docker運用手順(検証用・オプション)

`README.md`本体のネイティブ手順を主開発環境とし、依存関係の隔離や再現確認が必要な場合に使う補助経路。

判断根拠は [`docs/docker_migration.md`](../docs/docker_migration.md) を参照。

## 前提

- WSL2 Ubuntu上で作業する。
- 現在のPCではDocker DesktopとUbuntu内Docker Engineの両方を検出している。
- 接続先は docker context ls と docker info で確認する。2026-09-08時点の接続先はDocker Desktop。
- Ubuntu内Docker Engineを再構築する場合の参考手順:
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
cd ~/ROS2_TEST/docker
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

現在は .wslconfig なしでWSL2から30 GiBを利用できる。実測で不足が確認された場合だけWindows側の
%USERPROFILE%\.wslconfig を調整し、wsl --shutdown 後に再起動する。

```ini
[wsl2]
memory=32GB
```

## 復旧・作り直し

コンテナが壊れた場合はイメージを作り直すだけで良い。

```bash
docker compose down
docker compose build --no-cache
```

`src/`はホスト側のリポジトリをマウントしているだけなので、コンテナを壊してもソースコードは失われない。
