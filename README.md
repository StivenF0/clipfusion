# ClipFusion
### Video demo: <https://youtu.be/8iAWLOGAdKg>
### Description:

It's an app that users can log in and join videos together storing information about the videos that was processed on the website.

## Setup and Configuration

### 1. Python is required.
1. If Python is not installed. It can be downloaded on the website <https://python.org>.

### 2. Pipenv python package is required.
1. To install pipenv. Run:
    ```shell
    pip install pipenv
    ```
### 3. Enter the virtual environment with pipenv and download dependencies.
In the project folder, run:
```shell
pipenv shell

pipenv sync
```

### 4. Download ffmpeg binary and configure
1. Download ffmpeg on the official website <https://ffmpeg.org/download.html>
2. Put the binary of `ffmpeg` on the `video/` directory.
3. Go to the file `app.py` and change:
    ```python
    ### app.py ###

    # Change the variable FFMPEG_LOCAL to the name of downloaded binary
    FFMPEG_LOCAL = "ffmpeg.exe" # ffmpeg name on video folder
    FFMPEG_BINARY = path.join(app.config.get("UPLOAD_FOLDER"), FFMPEG_LOCAL)
    
    # ...
    ```

### 5. The web app is ready to use!
