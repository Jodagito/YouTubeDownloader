import inspect
import os
import requests
from pytube import YouTube

destination_path = input("\nInsert the destination path ")
preferences = ""


def main():
    preferences = set_preferences()
    clear_terminal()
    download_option = input("""What are you going to download?
                            \n\t1) Song\n\t2) Video\n\t3) Playlist\n""")
    if download_option in ['1', '1)', 'Song']:
        download_file()
    elif download_option in ['2', '2)', 'Video']:
        download_file(file_format="video")
    elif download_option in ['3', '3)', 'Playlist']:
        download_playlists()
    else:
        invalidInputException()


def download_playlists():
    file_format = "audio"
    playlist_url = input("\nInsert the playlist URL ")
    playlist_videos = get_playlist_videos(playlist_url)
    option = input("\nSelect what you want to download\n\n\t1) Audios\n\t2) Videos\n")
    if option in ['1', '1)', 'Audios']:
        pass
    elif option in ['2', '2)', 'Videos']:
        file_format = "video"
    else:
        invalidInputException()
    for file_url in playlist_videos:
        download_file(file_url, file_format)
    print("The playlist has been downloaded succesfully.\n")


def get_playlist_videos(url):
    playlist_web = requests.get(url).content
    website_data = str(playlist_web).split(' ')
    item = 'href="/watch?'
    playlist_videos = [link.replace('href="', 'https://youtube.com').split(';')[0]
                      for link in website_data if item in link]
    return playlist_videos


def download_file(file_url=None, file_format="audio"):
    if not file_url:
        file_url = input(f"\nInsert the URL ")
    yt_object = YouTube(file_url)
    try:
        print(f"Downloading {YouTube(file_url).title}")
        if file_format == "audio":
            if preferences == "Default":
                yt_object.streams.get_audio_only().download(destination_path)
            else:
                filtered_yt_object = yt_object.streams.filter(type=file_format).order_by(
                            'resolution').desc().all()
                available_streams = get_available_streams(filtered_yt_object, file_format)
                selection = resolution_selection(available_streams)
                filtered_yt_object[selection].download(destination_path)
        elif file_format == "video":
            if preferences == "Default":
                yt_object.streams.get_highest_resolution().download(destination_path)
            else:
                filtered_yt_object = yt_object.streams.filter(type=file_format).order_by(
                            'resolution').desc().all()
                available_streams = get_available_streams(filtered_yt_object, file_format)
                selection = resolution_selection(available_streams)
                filtered_yt_object[selection].download(destination_path)
        print(f"{yt_object.title} has been downloaded succesfully.\n")
    except Exception as error:
        print(f"{yt_object.title} couldn't be downloaded.\n")
        print(error)
    

def set_preferences():
    print(f"\nBy default YouTube Downloader will always download the best quality option")
    preference = input("Would you like to manually select the quality option?\n\n\tYes\n\tNo\n")
    if preference in ["Yes", "yes", "y", "Y"]:
        return "Manual"
    elif preference in ["No", "no", "n", "N"]:
        return "Default"
    else:
        invalidInputException()


def get_available_streams(yt_object, file_format):
    available_streams = ["File size: " + str(stream.filesize) +
                         " | File resolution: " +
                         stream.resolution +
                         " | File extension: " +
                         stream.mime_type for stream in
                         yt_object]
    return available_streams


def resolution_selection(available_streams):
    position = 1
    for stream in available_streams:
        print(f"{position} {stream}")
        position += 1
    selection = input("\n\nWhich resolution would you like for your file? ")
    if selection == "" or int(selection) not in range(len(available_streams)):
        invalidInputException()
    selection = int(selection) - 1
    return selection


def invalidInputException():
    input("\n\nError: Invalid input.\n")
    clear_terminal()
    inspect.stack()[1][3]()


def clear_terminal():
    return os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
