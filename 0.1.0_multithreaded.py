import os
import time
from multiprocessing.dummy import Pool as ThreadPool

startTime = time.time()

# music_dir = "/home/sugar/1temp/flacs/"
music_dir = "/home/sugar/VMware_shared/Music/"
save_dir = "/home/sugar/1temp/m4a/"

NUMBER_OF_THREADS = 7

itt_count = 0
total_songs = 0

def return_directory(dir_to_scan, accept_file):
    result = []
    for subdirectory in os.listdir(dir_to_scan):
        if os.path.isdir((dir_to_scan + "/" + subdirectory)) or accept_file:
            result.append(subdirectory)
        else:
            print(dir_to_scan + "/" + subdirectory, " is not a directory")
    return result

def convert_song(input_info):
    global itt_count
    artist, album, song = input_info

    input_path = music_dir + artist + '/' + album + '/' + song
    song_name = song.split(".")
    output_path = save_dir + artist + '/' + album + '/' + song_name[0] + ".m4a"
    output_dir = save_dir + artist + '/' + album

    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except:
            print("Path already exists")
        

    itt_count = itt_count + 1
    if not os.path.exists(output_path):
        itt_start_time = time.time()
        print("Converting song {0} of {1}... Artist: {2}, Album: {3} Song: {4}".format(itt_count, total_songs, artist, album, song))
        os.system("ffmpeg -i {0} -loglevel panic -q:v 420k {1}".format("\"" + input_path + "\"", "\"" + output_path + "\""))
        itt_total_time = time.time() - itt_start_time
        print("Converted song  {0} of {1} - took {2}".format(itt_count, total_songs, time.strftime("%H:%M:%S", time.gmtime(itt_total_time))))
    else:
        print("Song {0} of {1} exists. Not converting {2}".format(itt_count, total_songs, song))

all_songs = []
for artist in return_directory(music_dir, 0):
    for album in return_directory((music_dir + artist), 0):
        for song in return_directory((music_dir + artist + "/" + album), 1):
            all_songs.append([artist, album, song])
            total_songs = total_songs + 1

pool = ThreadPool(NUMBER_OF_THREADS)

pool.map(convert_song, all_songs)

pool.close()
pool.join()

endTime = time.time()

totalTime = endTime - startTime

print("Total time to complete: " + time.strftime("%H:%M:%S", time.gmtime(totalTime)))
