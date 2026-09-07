# Docker移行の検討記録

## 前提の注意

**この記録は特定の検証用PC上での確認結果であり、実際にROS2を動かす対象環境(実機・本番検証機)とは異なる可能性がある。**
数値(メモリ量・GPU有無など)や結論は参考情報として扱い、実環境で改めて確認すること。

## 検証時点のPC環境(参考値)

検証日: 2026-09-07時点。

| 項目 | このPCでの確認結果 |
|---|---|
| Docker Desktop(Windows側) | 未インストール |
| Docker Engine(WSL2内) | 未インストール |
| WSL2 `systemd` | 有効(`/etc/wsl.conf`に`systemd=true`設定済み) |
| WSL2ディスク空き容量 | 約955GB |
| 物理メモリ総量 | 約16GB |
| WSL2へのメモリ割当 | 約7.6GB(`.wslconfig`未設定によるデフォルト値) |
| CPU | 12論理コア |
| GPU | NVIDIA専用GPUなし。`/usr/lib/wsl/lib`にD3D12ドライバ(WSLg用)を確認 |
| X11/WSLgソケット | `/tmp/.X11-unix/X0`、`/mnt/wslg`とも存在を確認 |

## 判断の経緯

1. **Docker Desktop for Windows は採用しない**
   - 理由: 大企業利用時のライセンス条件が発生しうること、WSL2の上にさらに管理レイヤーが乗り
     「WSL2+Ubuntuで完結させる」という本リポジトリの既存方針(README本体)と矛盾するため。
   - 代わりに、`systemd=true`が既に有効なWSL2 Ubuntu内へDocker Engine(CE)を直接インストールする方式を採用。

2. **全面Docker化はせず、ネイティブ手順と併用する**
   - 理由: GUI(X11/WSLg)対応やボリューム設定などDocker固有の複雑さが学習初期には過大。
     また検証PCのメモリ割当(約7.6GB)はGazebo等重いシミュレーションでは不足する可能性があり、
     全員がDocker前提にすると詰まるリスクがある。
   - README本体のネイティブ手順は維持し、`docker/`配下に選択肢として追加する構成にした。

3. **ネットワーク設定は `network_mode: host` + `ROS_LOCALHOST_ONLY=1` を初期値にする**
   - 理由: WSL2のNAT越しDDS discoveryが不安定になりうるという既知の懸念(README精査時の議論)を踏まえ、
     まずは単一ホスト内で閉じた検証から始め、複数ノード/複数マシン構成が必要になった時点で
     環境変数やネットワークモードを見直す。

## 実環境で確認すべきこと(未検証・要フォローアップ)

- 対象PCでの物理メモリ量とWSL2への割当量(`.wslconfig`の要否)
- 対象PCでのGPU有無・種別(NVIDIA/Intel/AMD)とWSLgのGPUアクセラレーション動作可否
- `docker compose run --rm ros2 rviz2` が実際にGUI表示できるか
- 実機(センサー・アクチュエータ)接続が必要になった場合、USB直結はコンテナ化してもWSL2の制約
  ([`usbipd-win`](https://github.com/dorssel/usbipd-win)によるパススルー要否)は変わらない点に注意
