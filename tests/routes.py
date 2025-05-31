"""Very simple test for the routes of the web app."""

from app import my_web_app

app = my_web_app()


def test_homepage() -> None:
    """Test homepage."""
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200  # noqa: S101, PLR2004
    assert b"Welcome" in response.data  # noqa: S101


def test_ocr() -> None:
    """Test OCR page."""
    client = app.test_client()
    response = client.get("/ocr")
    assert response.status_code == 200  # noqa: S101, PLR2004
    assert b"Upload a photo to see OCR results." in response.data  # noqa: S101


def test_face() -> None:
    """Test Face page."""
    client = app.test_client()
    response = client.get("/face")
    assert response.status_code == 200  
    assert b"Upload a photo to see face recognition results." in response.data  # noqa: S101
