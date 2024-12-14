import pytest
from PIL import Image
import io
from utils import to_webp

@pytest.fixture
def sample_image_bytes():
    """
    Create a sample image in memory and return its bytes.
    """
    img = Image.new("RGB", (100, 100), color="blue")
    output = io.BytesIO()
    img.save(output, format="JPEG")
    return output.getvalue()

def test_to_webp_with_image_bytes(sample_image_bytes):
    """
    Tests image conversion from bytes to WEBP format.
    """
    result = to_webp(image_bytes=sample_image_bytes, max_size_in_kb=500)
    assert isinstance(result, bytes)
    assert len(result) <= 500 * 1024

def test_to_webp_with_image_path(tmp_path, sample_image_bytes):
    """
    Test image conversion using a file path.
    """
    image_path = tmp_path / "test_image.jpg"
    with open(image_path, "wb") as f:
        f.write(sample_image_bytes)

    result = to_webp(image_path=str(image_path), max_size_in_kb=500)
    assert isinstance(result, bytes)
    assert len(result) <= 500 * 1024

def test_to_webp_exceeding_max_size(sample_image_bytes):
    """
    Tests image quality reduction if it exceeds the maximum size.
    """
    large_size_kb = 1  # Set a very small size to force quality reduction
    result = to_webp(image_bytes=sample_image_bytes, max_size_in_kb=large_size_kb)
    assert isinstance(result, bytes)
    assert len(result) <= large_size_kb * 1024

def test_to_webp_invalid_input():
    """
    Tests handling of invalid input.
    """
    with pytest.raises(ValueError):
        to_webp()

    with pytest.raises(FileNotFoundError):
        to_webp(image_path="non_existent_file.jpg")

    with pytest.raises(OSError):
        to_webp(image_bytes=b"not_an_image")
