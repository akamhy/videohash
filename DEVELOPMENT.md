## Development

#### Code formatting
We use the [black](https://github.com/psf/black) code formatter. Always format the code with black before
submitting a pull request.

#### Testing
Before submitting a pull request, make sure the code passes all the tests and is formatted by black:

```bash
# Inside the project root (directory containing this file)
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt
mypy videohash/
pytest
black .
```
This will create a virtual environment and install project's all dependencies including the ones required for running the tests, run the tests and finally format the code with black.

#### Packaging (uploading to PyPI)

In the project root run the following command inside the virtual environment created for testing.

```bash
pip install setuptools wheel twine
python setup.py sdist bdist_wheel
twine upload dist/*
```
