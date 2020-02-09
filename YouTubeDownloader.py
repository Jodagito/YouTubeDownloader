import inspect
import json
import os
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError


CONFIGURATIONS = {'destination_path': '', 'video_quality': '',
                  'audio_quality': '', 'when_unavailable': ''}
CONFIGS_FILE = 'configs.json'
if not CONFIGURATIONS['destination_path']:
    destination_path = input("\nInsert the destination path ")
destination_path = CONFIGURATIONS['destination_path']


def create_config_file():
    with open(CONFIGS_FILE, 'w') as config_file:
        config_data = {'Destination path': '', 'Video quality': '',
                       'Audio quality': '', 'When unavailable': 'Highest'}
        json.dump(config_data, config_file)


def load_config_file():
    with open(CONFIGS_FILE) as config_file:
        config_data = json.loads(config_file)
        CONFIGURATIONS['destination_path'] = config_data['Destination path']
        CONFIGURATIONS['video_quality'] = config_data['Video quality']
        CONFIGURATIONS['audio_quality'] = config_data['Audio quality']
        CONFIGURATIONS['when_unavailable'] = config_data['When unavailable']


def main():
    clear_terminal()
    print("\t\tYouTube Downloader\n\n")
    menu_option = input(
        "Select and option to continue\n\n\t1) Start Downloading\n\t2) Settings\n\t3) Help\n\t4) Exit\n").lower()
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
        handle_incorrect_selection()


def downloads_menu():
    clear_terminal()
    print("\t\tDownloads Menu\n\n")
    download_source_url = input("Input the download source url ")
    validate_youtube_url(download_source_url)
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
        handle_incorrect_selection()


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
        input("""Error: An invalid URL has been inserted.\n{e}\n
              \nPress enter to continue...""")
        main()


def validate_playlist(url):
    try:
        Playlist(download_source_url)
        return True
    except KeyError:
        return False


def download_audio(pytube_object):
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
    except (IOError, OSError, PytubeError) as e:
        print(f"{pytube_object.title} couldn't be downloaded.\n{e}\n")


def unavailable_audio(pytube_object):
    if CONFIGURATIONS['when_unavailable'] == "Highest":
        pytube_object.streams.filter(type='audio').order_by(
            'abr').desc().all()[0].download(destination_path)
    else:
        pytube_object.streams.filter(type='audio').order_by(
            'abr').all()[0].download(destination_path)


def download_video(pytube_object):
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
    except (IOError, OSError, PytubeError) as e:
        print(f"{pytube_object.title} couldn't be downloaded.\n{e}\n")


def unavailable_video(pytube_object):
    if CONFIGURATIONS['when_unavailable'] == "Highest":
        pytube_object.streams.filter(type='audio').order_by(
            'abr').desc().all()[0].download(destination_path)
    else:
        pytube_object.streams.filter(type='audio').order_by(
            'abr').all()[0].download(destination_path)


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
        handle_incorrect_selection()


def set_default_destination_path():
    clear_terminal()
    print("\n\n\t\tTo go back leave this in blank.")
    default_destination_path = input(
        "\n\nInsert the default destination path ")
    if (os.path.exists(default_destination_path) or
            os.access(os.path.dirname(default_destination_path), os.W_OK)):
        with open(CONFIGS_FILE, 'w') as config_file:
            json.dump(
                {'Destination path': default_destination_path}, config_file)
    elif default_destination_path == "":
        settings_menu()
    else:
        handle_incorrect_selection()


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
        with open(CONFIGS_FILE, 'w') as config_file:
            json.dump(
                {'Video quality': default_video_quality}, config_file)
    if default_audio_quality in ["1", "2", "3", "4", "5"]:
        default_audio_quality = audio_qualities[int(
            default_audio_quality) - 1]
        with open(CONFIGS_FILE, 'w') as config_file:
            json.dump(
                {'Audio quality': default_audio_quality}, config_file)
    elif default_video_quality == "" and default_audio_quality == "":
        settings_menu()
    else:
        handle_incorrect_selection()
    set_default_when_unavailable()


def set_default_when_unavailable():
    clear_terminal()
    print(f"\t\tIf the default quality selected isn't " +
          "available then the highest quality will be downloaded.")
    change_default = input(
        f"\n\nSet lowest quality as default if" +
        " default one is unavailable\n\n\tYes\n\tNo\n").lower()
    if change_default in ["yes", "y"]:
        with open(CONFIGS_FILE, 'w') as config_file:
            json.dump(
                {'When unavailable': "Lowest"}, config_file)
    elif change_default in ["no", "n"]:
        return
    else:
        handle_incorrect_selection()


def help_menu():
    return


def handle_incorrect_selection():
    input("\n\nError: Incorrect selection.\nPress enter to continue...")
    clear_terminal()
    locals()[inspect.stack()[1][3]]()


def clear_terminal():
    return os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    if not os.path.exists(CONFIGS_FILE):
        create_config_file()
    load_config_file()
    main()
