import inspect
import json
import os
import requests
from pytube import YouTube

destination_path = input("\nInsert the destination path ")
preferences = ""
CONFIGS_FILE = 'configs.json'


def create_config_file():
    with open(CONFIGS_FILE, w) as config_file:
        config_data = {'Destination path': '', 'Video quality': '',
                       'Audio quality': '', 'When unavailable': 'Highest'}
        json.dump(config_data, config_file)


def main():
    clear_terminal()
    print("\t\tYouTube Downloader\n\n")
    menu_option = input(
        "Select and option to continue\n\n\t1) Start Downloading\n\t2) Settings\n\t3) Help\n\t4) Exit").lower()
    if menu_option in ['1', '1)', 'start downloading']:
        downloads_menu()
    elif menu_option in ['2', '2)', 'settings']:
        settings_menu()
    elif menu_option in ['3', '3)', 'help']:
        help_menu()
    elif menu_option in ['4', '4)', 'exit']:
        clear_terminal()
        input("YouTube Downloader has been closed.")
    else:
        invalid_input_exception()


def downloads_menu():
    file_format = "audio"
    playlist_url = input("\nInsert the playlist URL ")
    playlist_videos = get_playlist_videos(playlist_url)
    option = input(
        "\nSelect what you want to download\n\n\t1) Audios\n\t2) Videos\n")
    if option in ['1', '1)', 'Audios']:
        pass
    elif option in ['2', '2)', 'Videos']:
        file_format = "video"
    else:
        invalid_input_exception()
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
                available_streams = get_available_streams(
                    filtered_yt_object, file_format)
                selection = resolution_selection(available_streams)
                filtered_yt_object[selection].download(destination_path)
        elif file_format == "video":
            if preferences == "Default":
                yt_object.streams.get_highest_resolution().download(destination_path)
            else:
                filtered_yt_object = yt_object.streams.filter(type=file_format).order_by(
                    'abr').desc().all()
                available_streams = get_available_streams(
                    filtered_yt_object, file_format)
                selection = resolution_selection(available_streams)
                filtered_yt_object[selection].download(destination_path)
        print(f"{yt_object.title} has been downloaded succesfully.\n")
    except Exception as error:
        print(f"{yt_object.title} couldn't be downloaded.\n")
        print(error)


def settings_menu():
    clear_terminal()
    selected_option = input(
        f"\t\tConfiguration Menu\n\tSelect an option to continue" +
        "\n\n\t1) Set default destination path" +
        "\n\t2) Set default qualities\n").lower().replace(" ", "")
    if selected_option in ["1", "setdefaultdestinationpath"]:
        set_default_destination_path()
    elif selected_option in ["2", "setdefaultqualities"]:
        set_default_qualities()
    else:
        invalid_input_exception()


def set_default_destination_path():
    clear_terminal()
    print("\n\n\t\tTo go back leave this in blank.")
    default_destination_path = input(
        "\n\nInsert the default destination path ")
    if (os.path.exists(default_destination_path) or
            os.access(os.path.dirname(default_destination_path), os.W_OK)):
        with open(CONFIGS_FILE, w) as config_file:
            json.dump(
                {'Destination path': default_destination_path}, config_file)
    elif default_destination_path == "":
        set_preferences()
    else:
        invalid_input_exception()


def set_default_qualities():
    clear_terminal()
    video_qualities = ["1080", "720", "480", "360", "144"]
    audio_qualities = ["160", "128", "70", "50"]
    print("\n\n\t\tTo go back leave both in blank.")
    default_video_quality = input(
        "\n\Select the default video quality \n1) 1080px\n2) 720px\n3) 480px\n4) 360px\n5)144px\n")
    default_audio_quality = input(
        "\n\Select the default audio quality \n1) 160kbps\n2) 128kbps\n3) 70kbps\n4) 50kbps\n")
    if default_video_quality in ["1", "2", "3", "4", "5"]:
        default_video_quality = video_qualities[int(default_video_quality) - 1]
        with open(CONFIGS_FILE, w) as config_file:
            json.dump(
                {'Video quality': default_video_quality}, config_file)
    if default_audio_quality in ["1", "2", "3", "4", "5"]:
        default_audio_quality = audio_qualities[int(
            default_audio_quality) - 1]
        with open(CONFIGS_FILE, w) as config_file:
            json.dump(
                {'Audio quality': default_audio_quality}, config_file)
    elif default_video_quality == "" and default_audio_quality == "":
        set_preferences()
    else:
        invalid_input_exception()
    set_default_when_unavailable()


def set_default_when_unavailable():
    clear_terminal()
    print(f"\t\tIf the default quality selected isn't " +
          "available then the highest quality will be downloaded.")
    change_default = input(
        f"\n\nSet lowest quality as default if" +
        " default one is unavailable\n\n\tYes\n\tNo\n").lower()
    if change_default in ["yes", "y"]:
        with open(CONFIGS_FILE, w) as config_file:
            json.dump(
                {'When unavailable': "Lowest"}, config_file)
    elif change_default in ["no", "n"]:
        return
    else:
        invalid_input_exception()


def help_menu():
    return
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
        invalid_input_exception()
    selection = int(selection) - 1
    return selection


def invalid_input_exception():
    input("\n\nError: Invalid input.\n")
    clear_terminal()
    locals()[inspect.stack()[1][3]]()


def clear_terminal():
    return os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    if not os.path.exists(CONFIGS_FILE):
        create_config_file()
    main()
