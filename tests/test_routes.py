from datetime import datetime
from pathlib import Path
from main import app

def test_upload():
    app.config.update({
        "TESTING": True,
    })
    resources = Path(__file__).parent / "statics"
    client = app.test_client()
    test_date_str = str(datetime.today())
    response = client.post("/upload", data={
        "name": "Test " + test_date_str,
        "certname": "Test Cert " + test_date_str,
        "file": (resources / "AWS Certified Cloud Practitioner Certificate.pdf").open("rb"),
    })
    assert response.status_code == 201