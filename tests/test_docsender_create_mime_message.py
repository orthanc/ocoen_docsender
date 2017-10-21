from email import message_from_bytes
from ocoen.docsender import _create_mime_message
import pytest


example_message = {
    'subject': 'test subject',
    'text': 'test message',
}
example_attachment = {}


def test_create_mime_message_sets_content_type():
    result = _create_mime_message('test@example.com', 'to@example.com', 'subject', example_message, example_attachment)
    email = message_from_bytes(result)
    assert 'multipart/mixed' == email.get_content_type()


def test_create_mime_message_sets_from():
    result = _create_mime_message('test@example.com', 'to@example.com', 'subject', example_message, example_attachment)
    email = message_from_bytes(result)
    assert 'test@example.com' == email['From']


def test_create_mime_message_sets_to():
    result = _create_mime_message('test@example.com', 'to@example.com', 'subject', example_message, example_attachment)
    email = message_from_bytes(result)
    assert 'to@example.com' == email['To']


def test_create_mime_message_sets_subject():
    result = _create_mime_message('test@example.com', 'to@example.com', 'test subject',
                                  example_message, example_attachment)
    email = message_from_bytes(result)
    assert 'test subject' == email['Subject']


def test_create_mime_message_errors_with_none_message():
    with pytest.raises(ValueError):
        _create_mime_message('test@example.com', 'to@example.com', 'subject', None, example_attachment)


def test_create_mime_message_errors_without_message_body(mocker):
    mocker.patch.dict(example_message)
    _remove_message_bodies(example_message)
    with pytest.raises(ValueError):
        _create_mime_message('test@example.com', 'to@example.com', 'subject', example_message, example_attachment)


def test_create_mime_message_sets_text_body(mocker):
    mocker.patch.dict(example_message)
    _remove_message_bodies(example_message)
    example_message['text'] = 'text message'
    result = _create_mime_message('test@example.com', 'to@example.com', 'subject', example_message, example_attachment)
    email = message_from_bytes(result)
    text_part = email.get_payload()[0]
    assert 'text/plain' == text_part.get_content_type()
    assert 'text message' == text_part.get_payload()


def test_create_mime_message_sets_html_body(mocker):
    mocker.patch.dict(example_message)
    _remove_message_bodies(example_message)
    example_message['html'] = 'html message'
    result = _create_mime_message('test@example.com', 'to@example.com', 'subject', example_message, example_attachment)
    email = message_from_bytes(result)
    html_part = email.get_payload()[0]
    assert 'text/html' == html_part.get_content_type()
    assert 'html message' == html_part.get_payload()


def test_create_mime_message_sets_alternatives_body(mocker):
    mocker.patch.dict(example_message)
    _remove_message_bodies(example_message)
    example_message['text'] = 'text message'
    example_message['html'] = 'html message'
    result = _create_mime_message('test@example.com', 'to@example.com', 'subject', example_message, example_attachment)
    email = message_from_bytes(result)
    alternative_part = email.get_payload()[0]
    assert 'multipart/alternative' == alternative_part.get_content_type()

    text_part = alternative_part.get_payload()[0]
    assert 'text/plain' == text_part.get_content_type()
    assert 'text message' == text_part.get_payload()

    html_part = alternative_part.get_payload()[1]
    assert 'text/html' == html_part.get_content_type()
    assert 'html message' == html_part.get_payload()


def _remove_message_bodies(msg):
    msg.pop('text', None)
    msg.pop('html', None)