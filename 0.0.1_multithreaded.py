import os
import time
from multiprocessing.dummy import Pool as ThreadPool

startTime = time.time()

music_dir = "/home/sugar/1temp/flacs/"
# music_dir = "/home/sugar/VMware_shared/Music/"
save_dir = "/home/sugar/1temp/m4a/"

def return_directory(dir_to_scan, accept_file):
    result = []
    for subdirectory in os.listdir(dir_to_scan):
        if os.path.isdir or accept_file:
            result.append(subdirectory)
        else:
            print(subdirectory, " is not a directory")
    return result

def convert_song(input_info):
    artist = input_info[0]
    album = input_info[1]
    song = input_info[2]

    input_path = "\"" + music_dir + artist + '/' + album + '/' + song + "\""
    song_name = song.split(".")
    output_path = "\"" + save_dir + artist + '/' + album + '/' + song_name[0] + ".m4a" + "\""
    output_dir = save_dir + artist + '/' + album

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    os.system("ffmpeg -i {0} -q:v 420k {1} ".format(input_path, output_path))

all_songs = []
for artist in return_directory(music_dir, 0):
    for album in return_directory((music_dir + artist), 0):
        for song in return_directory((music_dir + artist + "/" + album), 1):
            # print("Artist: ", artist, " Album: ", album, " Song: ", song)
            all_songs.append([artist, album, song])

pool = ThreadPool(7)

pool.map(convert_song, all_songs)

pool.close()
pool.join()

endTime = time.time()

totalTime = endTime - startTime

print("Total time to complete: " + time.strftime("%H:%M:%S", time.gmtime(totalTime)))
