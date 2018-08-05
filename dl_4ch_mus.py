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
    com = posts[0]['com'].split('<br>')[0]
    sdir = com if len(com) > len(thread_name) else thread_name
    sdir = sdir.replace('/', '_')
    ydl_opts = {
        # TODO: use longest of the two - first line of first comment or semantic url
        'outtmpl': sdir+'/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            # 'preferredquality': '192',
        }],
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    links = c.get_yt_links(posts)
    print('downloading ' + str(len(links)) + ' songs from ' + sdir)
    ydl.download(links)
