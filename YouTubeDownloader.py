import inspect
import json
import os
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError, PytubeError


CONFIGURATIONS = {'destination_path': '', 'video_quality': '',
                  'audio_quality': '', 'when_unavailable': ''}
CONFIGS_FILE = 'configs.json'


def create_config_file():
    with open(CONFIGS_FILE, 'w') as config_file:
        config_data = {'destination_path': '', 'video_quality': '',
                       'audio_quality': '', 'when_unavailable': 'Highest'}
        json.dump(config_data, config_file)


def load_config_file():
    with open(CONFIGS_FILE) as config_file:
        config_data = json.load(config_file)
        CONFIGURATIONS['destination_path'] = config_data['destination_path']
        CONFIGURATIONS['video_quality'] = config_data['video_quality']
        CONFIGURATIONS['audio_quality'] = config_data['audio_quality']
        CONFIGURATIONS['when_unavailable'] = config_data['when_unavailable']


if not os.path.exists(CONFIGS_FILE):
    create_config_file()
load_config_file()


def main():
    clear_terminal()
    print("\tYouTube Downloader\n\n")
    menu_option = input(
        "Select and option to continue\n\n\t1) Start Downloading\n\t2) Settings\n\t3) Help\n\t4) Exit\n").lower()
    if menu_option in ['1', '1)', 'start downloading']:
        return downloads_menu()
    elif menu_option in ['2', '2)', 'settings']:
        return settings_menu()
    elif menu_option in ['3', '3)', 'help']:
        return help_menu()
    elif menu_option in ['4', '4)', 'exit']:
        return exit()
    else:
        return handle_invalid_input()


def downloads_menu():
    clear_terminal()
    print("\tDownloads Menu\n\n")
    download_source_url = ""
    try:
        download_source_url = input("Input the download source url ")
        if not download_source_url:
            return handle_invalid_input()
    except KeyboardInterrupt:
        return main()
    if not validate_youtube_url(download_source_url):
        return main()
    pytube_object = YouTube(download_source_url)
    playlist_videos = look_for_playlist(pytube_object)
    format_selection = input(
        "\n\nSelect a download option\n\t1) Audio only\n\t2) Video and audio\n")
    if format_selection in ['1', '1)']:
        for element in playlist_videos:
            download_audio(element)
        else:
            download_audio(pytube_object)
    elif format_selection in ['2', '2)']:
        for element in playlist_videos:
            download_video(element)
        else:
            download_video(pytube_object)
    else:
        return handle_invalid_input()
    input("\nPress enter to continue...")
    return main()


def look_for_playlist(pytube_object):
    if validate_playlist(pytube_object.watch_url):
        pytube_object = Playlist(pytube_object.watch_url)
        return pytube_object.videos
    return []


def validate_youtube_url(url):
    try:
        YouTube(url)
        return
    except RegexMatchError as e:
        input(
            f"Error: An invalid URL has been inserted.\n{e}\n\nPress enter to continue...")
        return False


def validate_playlist(url):
    try:
        Playlist(url)
        return True
    except KeyError:
        return False


def download_audio(pytube_object):
    print(f"\nDownloading {pytube_object.title}")
    try:
        if not CONFIGURATIONS['audio_quality']:
            unavailable_audio(pytube_object)
        else:
            default_quality = CONFIGURATIONS['audio_quality'] + 'kbps'
            filtered_pytube_object = pytube_object.streams.filter(
                type='audio', abr=default_quality).order_by('abr').desc().all()[0]
            if not filtered_pytube_object:
                print(
                    f"\n\nDefault quality isn't available. {CONFIGURATIONS['when_unavailable']} quality will be downloaded.")
                return unavailable_audio(pytube_object)
            filtered_pytube_object.download(destination_path)
            print(f"\n{pytube_object.title} downloaded succesfully.")
    except (IOError, OSError, PytubeError) as e:
        print(f"{pytube_object.title} couldn't be downloaded.\n{e}\n")
        return


def unavailable_audio(pytube_object):
    if CONFIGURATIONS['when_unavailable'] == "Highest":
        pytube_object.streams.filter(type='audio').order_by(
            'abr').desc().all()[0].download(destination_path)
    else:
        pytube_object.streams.filter(type='audio').order_by(
            'abr').all()[0].download(destination_path)
    print(f"\n{pytube_object.title} downloaded succesfully.")


def download_video(pytube_object):
    print(f"\nDownloading {pytube_object.title}")
    try:
        if not CONFIGURATIONS['video_quality']:
            unavailable_video(pytube_object)
        else:
            default_quality = CONFIGURATIONS['video_quality'] + 'p'
            filtered_pytube_object = pytube_object.streams.filter(
                type='video', res=default_quality).order_by('resolution').desc().all()[0]
            if not filtered_pytube_object:
                print(
                    f"\n\nDefault quality isn't available. {CONFIGURATIONS['when_unavailable']} quality will be downloaded.")
                return unavailable_video(pytube_object)
            filtered_pytube_object.download(destination_path)
            print(f"\n{pytube_object.title} downloaded succesfully.")
    except (IOError, OSError, PytubeError) as e:
        print(f"{pytube_object.title} couldn't be downloaded.\n{e}\n")
        return


def unavailable_video(pytube_object):
    if CONFIGURATIONS['when_unavailable'] == "Highest":
        pytube_object.streams.filter(type='audio').order_by(
            'abr').desc().all()[0].download(destination_path)
    else:
        pytube_object.streams.filter(type='audio').order_by(
            'abr').all()[0].download(destination_path)
    print(f"\n{pytube_object.title} downloaded succesfully.")


def settings_menu():
    clear_terminal()
    selected_option = input(
        f"\t\tConfiguration Menu\n\tSelect an option to continue" +
        "\n\n\t1) List actual settings" +
        "\n\t2) Set destination path\n\t3) Set qualities\n\t4) Go back\n").lower().replace(" ", "")
    if selected_option in ["1", "listactualsettings"]:
        return list_settings()
    elif selected_option in ["2", "setdestinationpath"]:
        set_destination_path()
    elif selected_option in ["3", "setqualities"]:
        set_qualities()
    elif selected_option in ["4", "goback"]:
        return main()
    else:
        return handle_invalid_input()


def set_destination_path():
    clear_terminal()
    print("\n\n\t\tTo go back leave this in blank.")
    default_destination_path = input(
        "\n\nInsert the default destination path ")
    if (os.path.exists(default_destination_path) or
            os.access(os.path.dirname(default_destination_path), os.W_OK)):
        with open(CONFIGS_FILE, 'r+') as config_file:
            config_data = json.load(config_file)
            config_data['destination_path'] = default_destination_path
            config_file.seek(0)
            config_file.write(json.dumps(config_data))
            config_file.truncate()
    elif default_destination_path == "":
        return settings_menu()
    else:
        return handle_invalid_input()
    return settings_menu()


def set_qualities():
    clear_terminal()
    video_qualities = ["1080", "720", "480", "360", "144"]
    audio_qualities = ["160", "128", "70", "50"]
    print("\n\n\t\tTo go back leave both in blank.")
    default_video_quality = input(
        "\n\tSelect the default video quality \n1) 1080px\n2) 720px\n3) 480px\n4) 360px\n5) 144px\n")
    default_audio_quality = input(
        "\n\tSelect the default audio quality \n1) 160kbps\n2) 128kbps\n3) 70kbps\n4) 50kbps\n")
    if default_video_quality in ["1", "2", "3", "4", "5"]:
        default_video_quality = video_qualities[int(default_video_quality) - 1]
        with open(CONFIGS_FILE, 'r+') as config_file:
            config_data = json.load(config_file)
            config_data['video_quality'] = default_video_quality
            config_file.seek(0)
            config_file.write(json.dumps(config_data))
            config_file.truncate()
    if default_audio_quality in ["1", "2", "3", "4", "5"]:
        default_audio_quality = audio_qualities[int(
            default_audio_quality) - 1]
        with open(CONFIGS_FILE, 'r+') as config_file:
            config_data = json.load(config_file)
            config_data['audio_quality'] = default_audio_quality
            config_file.seek(0)
            config_file.write(json.dumps(config_data))
            config_file.truncate()
    elif default_video_quality == "" and default_audio_quality == "":
        return settings_menu()
    else:
        return handle_invalid_input()
    set_default_when_unavailable()
    return settings_menu()


def set_default_when_unavailable():
    clear_terminal()
    print(f"\t\tIf the default quality selected isn't " +
          "available then the highest quality will be downloaded.")
    change_default = input(
        f"\n\nSet lowest quality as default if" +
        " default one is unavailable\n\n\tYes\n\tNo\n").lower()
    if change_default in ["yes", "y"]:
        with open(CONFIGS_FILE, 'r+') as config_file:
            config_data = json.load(config_file)
            config_data['when_unavailable'] = 'Lowest'
            config_file.seek(0)
            config_file.write(json.dumps(config_data))
            config_file.truncate()
    elif change_default in ["no", "n"]:
        return
    else:
        return handle_invalid_input()


def list_settings():
    clear_terminal()
    with open(CONFIGS_FILE, 'r+') as config_file:
        config_data = json.load(config_file)
        for setting, value in config_data.items():
            print(f"{setting.capitalize().replace('_', ' ')} = {value}")
    input("\n\nPress enter to continue...")
    return settings_menu()


def help_menu():
    clear_terminal()
    input("Sorry, this menu is being developed\nPress enter to continue...")
    return main()


def exit():
    clear_terminal()
    input("YouTube Downloader has been closed.")


def handle_invalid_input():
    input("\n\nError: Invalid input.\nPress enter to continue...")
    clear_terminal()
    return globals()[inspect.stack()[1][3]]()


def clear_terminal():
    return os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    try:
        if not CONFIGURATIONS['destination_path']:
            destination_path = input("\nInsert the destination_path ")
        destination_path = CONFIGURATIONS['destination_path']
        main()
    except KeyboardInterrupt:
        exit()
