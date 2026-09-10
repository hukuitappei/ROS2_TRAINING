# Docker移行の検討記録

## 前提の注意

**この記録は特定の検証用PC上での確認結果であり、実際にROS2を動かす対象環境(実機・本番検証機)とは異なる可能性がある。**
数値(メモリ量・GPU有無など)や結論は参考情報として扱い、実環境で改めて確認すること。

## 検証時点のPC環境(参考値)

検証日: 2026-09-08時点。

| 項目 | このPCでの確認結果 |
|---|---|
| Docker Desktop(Windows側) | 導入済み。docker-desktop WSLディストリビューション稼働中 |
| Docker Engine(WSL2内) | 導入済み。docker.service稼働中 |
| 現在のDocker接続先 | docker info上はDocker Desktop |
| WSL2 `systemd` | 有効(`/etc/wsl.conf`に`systemd=true`設定済み) |
| WSL2ディスク空き容量 | 約928GB |
| 物理メモリ総量 | 約61.6GiB |
| WSL2へのメモリ割当 | 30GiB、Swap 8GiB (.wslconfigなし) |
| CPU | 24論理コア |
| GPU | NVIDIA専用GPUなし。`/usr/lib/wsl/lib`にD3D12ドライバ(WSLg用)を確認 |
| X11/WSLgソケット | `/tmp/.X11-unix/X0`、`/mnt/wslg`とも存在を確認 |

## 判断の経緯

1. **WSL2のネイティブROS 2環境を主開発環境にする**
   - 理由: 24論理コア、30GiBメモリ、約928GBの空き容量があり、GUIや実機連携を直接検証できるため。
   - ROS 2 Jazzy Desktopとros-dev-toolsは2026-09-08に導入済み。

2. **Dockerは再現・隔離用途の補助経路にする**
   - 理由: GUIやUSBパススルーではDocker固有の設定が増える一方、依存関係を隔離できる利点は残るため。
   - Docker DesktopとUbuntu内Docker Engineの一本化は、Dockerを本格利用する時点で判断する。

3. **ネットワーク設定は `network_mode: host` + `ROS_LOCALHOST_ONLY=1` を初期値にする**
   - 理由: WSL2のNAT越しDDS discoveryが不安定になりうるという既知の懸念(README精査時の議論)を踏まえ、
     まずは単一ホスト内で閉じた検証から始め、複数ノード/複数マシン構成が必要になった時点で
     環境変数やネットワークモードを見直す。

## 実環境で確認すべきこと(未検証・要フォローアップ)

- 長時間ビルドやGazebo実行時のCPU・メモリ使用量
- 対象PCでのGPU有無・種別(NVIDIA/Intel/AMD)とWSLgのGPUアクセラレーション動作可否
- `docker compose run --rm ros2 rviz2` が実際にGUI表示できるか
- 実機(センサー・アクチュエータ)接続が必要になった場合、USB直結はコンテナ化してもWSL2の制約
  ([`usbipd-win`](https://github.com/dorssel/usbipd-win)によるパススルー要否)は変わらない点に注意
