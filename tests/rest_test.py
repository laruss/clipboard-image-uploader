import pytest
from unittest.mock import MagicMock
from rest import upload_content
from app_types import ImageContentType

@pytest.fixture
def mock_session(mocker):
    """
    Mock session creation to control its behavior in tests.
    This fixture replaces the cloudscraper.session method with a mock
    that can be configured within each test.
    """
    mock_session = MagicMock()
    mocker.patch('rest.cloudscraper.session', return_value=mock_session)
    return mock_session

@pytest.mark.parametrize("payload_type,expected_json,expected_files,expected_data", [
    ('json', True, False, False),
    ('form', False, True, False),
    ('buffer', False, False, True),
])
def test_upload_content_success(mocker, payload_type, expected_json, expected_files, expected_data):
    """
    Test upload_content with different payload types (json, form, buffer).

    This test verifies:
    - The correct method (POST or PUT) is called based on the payload type.
    - Headers, authentication, and payloads are correctly constructed.
    - The function returns True on successful upload.
    """
    # Mock cloudscraper.session to return our mock_session
    mock_session = MagicMock()
    mocker.patch('rest.cloudscraper.session', return_value=mock_session)

    # Set up a fake server response
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_session.post.return_value = mock_response
    mock_session.put.return_value = mock_response

    fake_data = b'test image data'
    url = "https://example.com/upload"
    token = "mytoken"
    credentials = ("user", "pass")

    # Select the method based on the payload type
    # Ensure that the method is called with the correct parameters
    method = 'POST' if payload_type != 'buffer' else 'PUT'
    result = upload_content(
        image_data=fake_data,
        url=url,
        token=token,
        credentials=credentials,
        payload_type=payload_type,
        upload_key='file',
        content_type=ImageContentType.WEBP,
        upload_method=method,
        timeout=10
    )

    assert result is True

    # Check that the correct method (post or put) was called
    if method == 'POST':
        mock_session.post.assert_called_once()
        called_args, called_kwargs = mock_session.post.call_args
    else:
        mock_session.put.assert_called_once()
        called_args, called_kwargs = mock_session.put.call_args

    # Check that the headers are correctly set
    headers = called_kwargs.get('headers', {})
    assert headers.get('Authorization') == f'Bearer {token}'

    # Check that auth is correctly set
    auth = called_kwargs.get('auth')
    assert auth == credentials

    # Check payload based on its type
    if expected_json:
        assert 'json' in called_kwargs
        assert 'file' in called_kwargs['json']
    elif expected_files:
        assert 'files' in called_kwargs
        assert 'file' in called_kwargs['files']
    elif expected_data:
        assert 'data' in called_kwargs
        # Ensure that data is the original byte content
        assert called_kwargs['data'] == fake_data


def test_upload_content_server_error(mock_session):
    """
    Test upload_content for handling server errors.

    This test verifies that:
    - If the server responds with an error, the function returns False.
    - The correct method (POST) is called with appropriate parameters.
    """
    # Set up a fake server response with an error
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("Server error")
    mock_session.post.return_value = mock_response

    result = upload_content(
        image_data=b'data',
        url="https://example.com/upload",
        payload_type='json',
        upload_method='POST',  # Ensure the correct method is used
    )

    # Check that the function handled the exception and returned False
    assert result is False

    # Ensure that post was called once
    mock_session.post.assert_called_once_with(
        "https://example.com/upload",
        headers={},
        auth=None,
        timeout=60,
        json={'file': 'ZGF0YQ=='},  # base64 of b'data'
    )


def test_upload_content_unknown_payload_type(mock_session):
    """
    Test upload_content for handling unknown payload types.

    This test verifies that:
    - If an unsupported payload type is provided, the function raises a ValueError.
    """
    with pytest.raises(ValueError):
        upload_content(
            image_data=b'data',
            url="https://example.com/upload",
            payload_type="unknown",
            upload_method='post'
        )
