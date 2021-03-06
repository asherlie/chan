import requests
import json
import os
import urllib

class Chan:
        base = "http://a.4cdn.org/"
        pic_base = "http://i.4cdn.org/"
        boards = set()
        boards = (['a', 'c', 'w', 'm', 'cgl', 'cm', 'f', 'n', 'jp', 'v', 'vg', 'vp', 'vr', 'co', 'g', 'tv', 'k', 'o', 'an', 'tg', 'sp', 'asp','sci', 'his', 'int', 'out', 'toy', 'i', 'po', 'p', 'ck', 'ic', 'wg', 'lit', 'mu', 'fa', '3', 'gd', 'diy', 'wsg', 'qst', 'biz', 'trv', 'fit', 'x', 'adv', 'lgbt', 'mlp', 'news', 'wsr', 'vip', 'b', 'r9k', 'pol', 'soc', 's4s', 's', 'hc', 'hm', 'h', 'e', 'u', 'd', 'y', 't', 'hr', 'gif', 'aco', 'r'])
        def get_front(self, board, page_num):
                response = requests.get(self.base + board + "/" + str(page_num) + ".json")
                return response

        def get_thread(self, board, thread):
                return requests.get(self.base + board + "/thread/" + str(thread) + ".json")

        def search_thread(self, th, terms):
            ret = []
            tmp_val = 0
            tmp_str = ''
            tmp_str_e = ''
            for term in terms:
                for i in th:
                    if 'com' in i:
                        tmp_str_e = i['com']
                        rng = 0
                        while True:
                            tmp_str = tmp_str_e[rng:]
                            fv = tmp_str.find(term)
                            if fv == -1: break
                            rng += fv
                            tmp_str = tmp_str_e[rng:]
                            fv = tmp_str.find(' ')
                            if fv != -1:
                                tmp_str = tmp_str[0:fv]
                            ret.append(tmp_str)
                            rng += 1
            return list(set(ret))
    
        def fix_links(self, links):
            ret = []
            tv = 0
            tvv = 0
            ts = ''
            for i in links:
                tv = i.find('<')
                tvv = i.find('>')
                if(tv == -1 or tvv == -1):
                    ret.append(i)
                    continue
                ts = i[0:tv] + i[tvv+1:]
                ret.append(ts)
            return ret

        # takes in get_thread().json()['posts']
        def get_yt_links(self, posts):
                res = self.search_thread(posts, ['youtube.com', 'youtu.be'])
                r = []
                for i in res:
                    r.append(i.split('<br>')[0])
                return self.fix_links(r)
        
        #returns num of new images downloaded
        def save_pics(self, board, thread, directory):
                new_p = 0
        #pics are saved at http(s)://i.4cdn.org/board/['tim'].['ext']

        #urllib.request.urlretrieve(url, dir)
#               if not os.path.exists(directory):
#                       print("archiving new thread")
                if not os.path.exists(directory + "/" + board):
                        os.makedirs(directory + "/" + board)
                if not os.path.exists(directory + "/" + board + "/" + str(thread)):
                        print('archiving new thread!')
                        os.makedirs(directory + "/" + board + "/" + str(thread))
                thread_dl = self.get_thread(board, thread)
                if 'semantic_url' in thread_dl.json()['posts'][0]:
                        print("downloading thread: '" + thread_dl.json()['posts'][0]['semantic_url'] + "' from /" + board + "/")
                else:
                        if 'com' in thread_dl.json()['posts'][0]:
                                print("downloading thread: '" + thread_dl.json()['posts'][0]['com'] + "' from /" + board + '/')

                with open(directory + "/" + board + "/" + str(thread) + "/title.txt", "w") as f:
                        if 'com' in thread_dl.json()['posts'][0]:
                                f.write(thread_dl.json()['posts'][0]['com']) 
                        else:
                                f.write('no title')
                for post in thread_dl.json()['posts']:
                        if 'fsize' in post: #if theres a pic attached
                                if not os.path.exists(directory + "/" + board + "/" + str(thread) + "/" + str(post['tim']) + post['ext']):
                                        new_p = new_p + 1
                                        urllib.request.urlretrieve(self.pic_base + board + "/" +  str(post['tim']) + post['ext'], directory + "/" + board + "/" + str(thread) + "/" + str(post['tim']) + post['ext'])
                print(str(new_p) + " new pics downloaded")
                return new_p
                                
        def print_all_in_board(self, board):
                i = 1 #indexing starts at 1 for some reason
                while i <= 10: #didn't do for to start at 1 -- CHANGE THIS ASAP!! THERE ARE NOT ALWAYS 10 PAGES. I MAKE IT WHILE ERROR IS STILL 200!!!!
#                       g = self.get_front(board, i).json()['threads'] #this always works
                        g = self.get_front(board, i)
                        if g.status_code == 200:
                                g = g.json()['threads']
                                for thread in g:
                                        if 'com' in thread['posts'][0]:
                                                print(thread['posts'][0]['com'] + ". " + str(thread['posts'][0]['replies']) + " replies. " + "ID: " + str(thread['posts'][0]['no']))
                                i = i + 1
                        else: break #this is a hacky workaround that should be fixed asap
                

        def print_everything(self):
                for board in self.boards:
                        print("~~ /" + str(board) +  "/ ~~")
                        self.print_all_in_board(board)
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
