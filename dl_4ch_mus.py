import sys
import chan
import youtube_dl

c = chan.Chan()

def dl_from_link(lnk):
    split = lnk.split('#')[0].split('/')
    if len(split) < 6: return False
    board = split[3]
    post_id = split[5]
    posts = c.get_thread(board, post_id)
    if posts.status_code != 200: return False
    postsj = posts.json()['posts']
    thread_name = postsj[0]['semantic_url']
    com = postsj[0]['com'].split('<br>')[0] if 'com' in postsj[0] else ''
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
    links = c.get_yt_links(postsj)
    print('downloading ' + str(len(links)) + ' songs from ' + sdir)
    ydl.download(links)
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2: print('enter a link to a 4chan thread')
    elif not dl_from_link(sys.argv[1]): print('invalid url')
