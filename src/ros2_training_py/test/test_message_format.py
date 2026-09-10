from ros2_training_py.message_format import format_received_message


def test_format_received_message():
    assert format_received_message("Hello World: 7") == "Received: 'Hello World: 7'"
