"""Module that contains the routes of the webapp."""

from flask import Blueprint, current_app, render_template, request, url_for
from werkzeug.utils import secure_filename

from modules.face import RetinaNetWrapper
from modules.ocr import EasyOCRWrapper

main = Blueprint("main", __name__)
ocr_wrapper = EasyOCRWrapper()
face_wrapper = RetinaNetWrapper()


@main.route("/")
def home() -> str:
    """Route to the home page."""
    return render_template("index.html")


@main.route("/ocr", methods=["GET", "POST"])
def ocr() -> str:
    """Route to the OCR page. Which runs OCR on an image on demand."""
    image_url = None
    if request.method == "POST":
        image = request.files.get("image")
        if image:
            filename = secure_filename(image.filename)
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            results_folder = current_app.config["RESULTS_FOLDER"]

            image_path = upload_folder / filename
            image.save(image_path)

            _ = ocr_wrapper.visualize(image_path, save_path=results_folder / filename)
            image_url = url_for("static", filename=f"{results_folder.stem}/{filename.rsplit('.', 1)[0]}.jpg")

    return render_template("ocr.html", image_url=image_url)


@main.route("/face", methods=["GET", "POST"])
def face() -> str:
    """Route to the face recognition page. Which runs face recognition on an image on demand."""
    image_url = None
    if request.method == "POST":
        image = request.files.get("image")
        if image:
            filename = secure_filename(image.filename)
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            results_folder = current_app.config["RESULTS_FOLDER"]

            image_path = upload_folder / filename
            image.save(image_path)

            _ = face_wrapper.visualize(image_path, save_path=results_folder / filename)
            image_url = url_for("static", filename=f"{results_folder.stem}/{filename.rsplit('.', 1)[0]}.jpg")

    return render_template("face.html", image_url=image_url)
