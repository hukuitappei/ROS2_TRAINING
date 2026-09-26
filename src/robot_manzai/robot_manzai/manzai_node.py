"""Publish a scripted two-robot manzai performance."""

import json
from pathlib import Path
from typing import Any

import rclpy
import yaml
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node
from std_msgs.msg import String


class ManzaiNode(Node):
    """Read a YAML script and publish each performance cue in order."""

    def __init__(self) -> None:
        super().__init__('manzai_node')

        self.declare_parameter('script_file', '')
        self.declare_parameter('repeat', False)
        self.declare_parameter('start_delay_sec', 0.5)

        script_file = str(self.get_parameter('script_file').value)
        if not script_file:
            share_dir = get_package_share_directory('robot_manzai')
            script_file = str(Path(share_dir) / 'config' / 'sample_manzai.yaml')

        self._repeat = bool(self.get_parameter('repeat').value)
        start_delay = float(self.get_parameter('start_delay_sec').value)
        self._lines = self._load_script(Path(script_file))
        self._line_index = 0
        self._timer = None

        self._line_publisher = self.create_publisher(
            String, 'manzai/line', 10
        )
        self._speech_publisher = self.create_publisher(
            String, 'manzai/speech_text', 10
        )
        self._motion_publisher = self.create_publisher(
            String, 'manzai/motion_cue', 10
        )

        self.get_logger().info(
            f'Loaded {len(self._lines)} lines from {script_file}'
        )
        self._schedule_next(start_delay)

    def _load_script(self, path: Path) -> list[dict[str, Any]]:
        if not path.is_file():
            raise RuntimeError(f'Manzai script not found: {path}')

        with path.open(encoding='utf-8') as stream:
            document = yaml.safe_load(stream) or {}

        lines = document.get('lines')
        if not isinstance(lines, list) or not lines:
            raise RuntimeError('The script must contain a non-empty lines list.')

        normalized = []
        for index, line in enumerate(lines):
            if not isinstance(line, dict):
                raise RuntimeError(f'Line {index} must be a mapping.')
            if not line.get('role') or not line.get('text'):
                raise RuntimeError(
                    f'Line {index} requires both role and text.'
                )

            pause_sec = float(line.get('pause_sec', 1.5))
            if pause_sec < 0.05:
                raise RuntimeError(
                    f'Line {index} pause_sec must be at least 0.05.'
                )

            normalized.append({
                'role': str(line['role']),
                'text': str(line['text']),
                'emotion': str(line.get('emotion', 'neutral')),
                'motion': str(line.get('motion', 'neutral')),
                'pause_sec': pause_sec,
            })

        return normalized

    def _schedule_next(self, delay_sec: float) -> None:
        self._timer = self.create_timer(
            max(delay_sec, 0.05), self._publish_next
        )

    def _publish_next(self) -> None:
        timer = self._timer
        if timer is not None:
            timer.cancel()
            self.destroy_timer(timer)
            self._timer = None

        line = self._lines[self._line_index]
        payload = {
            'index': self._line_index,
            'total': len(self._lines),
            'role': line['role'],
            'text': line['text'],
            'emotion': line['emotion'],
            'motion': line['motion'],
        }

        self._line_publisher.publish(
            String(data=json.dumps(payload, ensure_ascii=False))
        )
        self._speech_publisher.publish(String(data=line['text']))
        self._motion_publisher.publish(String(data=line['motion']))
        self.get_logger().info(
            f"[{line['role']}] {line['text']} ({line['motion']})"
        )

        self._line_index += 1
        if self._line_index >= len(self._lines):
            if self._repeat:
                self._line_index = 0
            else:
                self.get_logger().info('Manzai performance finished.')
                return

        self._schedule_next(line['pause_sec'])


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ManzaiNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
