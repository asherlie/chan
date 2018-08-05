import sys
import chan
import youtube_dl

c = chan.Chan()

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        #'preferredcodec': 'mp3',
        # 'preferredquality': '192',
    }],
}

ydl = youtube_dl.YoutubeDL(ydl_opts)

if __name__ == '__main__':
    split = sys.argv[1].split('#')[0].split('/')
    if len(split) < 6:
            raise Exception('malformed url')
    board = split[3]
    post_id = split[5]
    ydl.download(c.get_yt_links(board, post_id))
