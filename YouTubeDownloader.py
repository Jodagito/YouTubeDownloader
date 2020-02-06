from pytube import YouTube
import requests
import os

destination_path = input("Insert the destination path ")


def main():
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
        incorrectSelectionException()


def download_playlists():
    playlist = input("Insert the playlist url ")
    playlist_web = requests.get(playlist).content
    website_data = str(playlist_web).split(' ')
    item = 'href="/watch?'
    playlist_songs = [link.replace('href="', 'https://youtube.com')
                      for link in website_data if item in link]
    option = input("\nSelect what you want to download\n\n\t1) Audios\n\t2) Videos\n")
    for file_url in playlist_songs:
        file_url = file_url.split(';')[0]
        if option in ['1', '1)', 'Audios']:
            download_file(file_url)
        elif option in ['2', '2)', 'Videos']:
            download_file(file_url, "video")
        else:
            incorrectSelectionException()
    print("The playlist has been downloaded succesfully.\n")


def download_file(file_url=None, file_format="song"):
    if not file_url:
        file_url = input(f"Insert the {file_format} url ")
    try:
        print(f"Downloading {YouTube(file_url).title}")
        if file_format == "song":
            YouTube(file_url).streams.get_audio_only().download(destination_path)
        elif file_format == "video":
            YouTube(file_url).streams.get_highest_resolution().download(destination_path)
        print(f"{YouTube(file_url).title} has been downloaded succesfully.\n")
    except Exception as e:
        print(f"{YouTube(file_url).title} couldn't be downloaded.\n")


def incorrectSelectionException():
    input("\n\n\tError: Incorrect selection.")
    return main()


def clear_terminal():
    return os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
