from pathlib import Path

import yaml


def test_sample_script_has_alternating_roles():
    script_path = (
        Path(__file__).parents[1] / 'config' / 'sample_manzai.yaml'
    )
    with script_path.open(encoding='utf-8') as stream:
        lines = yaml.safe_load(stream)['lines']

    assert len(lines) >= 2
    assert all(line['role'] in {'boke', 'tsukkomi'} for line in lines)
    assert all(line['text'].strip() for line in lines)
    assert all(
        left['role'] != right['role']
        for left, right in zip(lines, lines[1:])
    )
