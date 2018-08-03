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
                        # while tmp_val != -1:
                        while True:
                            tmp_str = tmp_str_e
                            tmp_val = tmp_str.find(term)
                            if tmp_val == -1: break
                            tmp_str = tmp_str[tmp_val:]
                            tmp_val = tmp_str.find(' ')
                            if tmp_val != -1:
                                tmp_str = tmp_str[0:tmp_val]
                            print(tmp_str)
                            ret.append(tmp_str)
                            tmp_str_e = tmp_str_e[tmp_val:]
            return ret

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
