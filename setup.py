"""YouTubeDownloader - setup.py"""
import setuptools

LONG_DESC = open('README.md').read()

setuptools.setup(
    name="YouTubeDownloader",
    version="1.0",
    author="Jodagito",
    description="A simple to use youtube playlists/videos/audios downloader",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    url="https://github.com/Jodagito/YoutubeDownloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": [
        "YouTubeDownloader=YouTubeDownloader:main"]},
    python_requires=">=3.6",
    install_requires=[
        'pytube3>=9.5.13'
    ]
)
