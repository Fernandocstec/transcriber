from setuptools import setup, find_packages

setup(
    name="transcriber",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "python-multipart==0.0.6",
        "sqlalchemy==2.0.23",
        "psycopg2-binary==2.9.9",
        "pydantic==2.5.2",
        "python-dotenv==1.0.0",
        "openai-whisper==20231117",
        "moviepy==1.0.3",
        "pydub==0.25.1",
        "python-jose==3.3.0",
        "passlib==1.7.4",
        "bcrypt==4.0.1",
        "pyannote.audio==3.1.1",
    ],
) 