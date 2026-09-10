from pathlib import Path
import xml.etree.ElementTree as ET


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def test_sdf_files_are_valid_xml():
    ET.parse(PACKAGE_ROOT / "worlds" / "training_world.sdf")
    ET.parse(PACKAGE_ROOT / "models" / "training_robot" / "model.sdf")
    ET.parse(PACKAGE_ROOT / "models" / "training_robot" / "model.config")


def test_robot_has_drive_and_lidar():
    root = ET.parse(
        PACKAGE_ROOT / "models" / "training_robot" / "model.sdf"
    ).getroot()
    model = root.find("model")
    assert model is not None
    assert model.attrib["name"] == "training_robot"
    assert model.find(".//plugin[@name='gz::sim::systems::DiffDrive']") is not None
    assert model.find(".//sensor[@type='gpu_lidar']") is not None


def test_bridge_covers_control_and_sensor_topics():
    bridge = (PACKAGE_ROOT / "config" / "bridge.yaml").read_text()
    for topic in ("/cmd_vel", "/odom", "/scan", "/tf", "/clock"):
        assert f"ros_topic_name: {topic}" in bridge
