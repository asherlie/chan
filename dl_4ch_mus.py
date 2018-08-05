import sys
import chan
import youtube_dl

c = chan.Chan()

if __name__ == '__main__':
    split = sys.argv[1].split('#')[0].split('/')
    if len(split) < 6:
            raise Exception('malformed url')
    board = split[3]
    post_id = split[5]
    posts = c.get_thread(board, post_id).json()['posts']
    thread_name = posts[0]['semantic_url']
    ydl_opts = {
        # TODO: use longest of the two - first line of first comment or semantic url
        'outtmpl': thread_name+'/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            # 'preferredquality': '192',
        }],
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    links = c.get_yt_links(posts)
    print('downloading ' + str(len(links)) + ' songs from ' + thread_name)
    ydl.download(links)
