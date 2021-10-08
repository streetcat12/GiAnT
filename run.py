import eel
import asyncio
from datetime import datetime, timedelta
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras import metrics
import tensorflow as tf
import pickle
import numpy as np
import time
from konlpy.tag import Okt
import json
import os
from keras.models import load_model
import keyboard as kb
from termcolor import cprint, colored
from pynput import keyboard
from pynput.keyboard import Key, Controller
import re, string
from tkinter import *
import os
import alert
import os
from shutil import copyfile
import matplotlib.pyplot as plt
import matplotlib
from twilio.rest import Client
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

account_sid = 'ACe0900c6e0ad3cdd5f1e9ee1ea4d3cbae'
auth_token = '24de2e1fc3583155b7fc69fa1684f899'
client = Client(account_sid, auth_token)

eel.init('web')

keyboard_disabling_count = 0
sadnessCount = 0

from pynput import keyboard
from pynput.keyboard import Key, Controller
import re, string
import msvcrt
import keyboard as kb

from hangul_utils import join_jamos


#mistakeChange = ['Y','U','I','H','J','K','L','B','N','M']

############################
import csv
sadness_word_list = list()
with open('sadness_word.csv', newline='') as f:
    reader = csv.reader(f)
    for word in list(reader):
        sadness_word_list.append(word[0])

perDays = {}
if os.path.isfile('accounts/perDays.pk'):
    with open('accounts/perDays.pk', 'rb') as f:
        perDays = pickle.load(f)
else:
    with open('accounts/perDays.pk', 'wb') as f:
        pickle.dump({},f)

def csv_to_list(file_):
    array = list()
    f = open(file_, 'r', encoding='utf-8')
    sentences = csv.reader(f)
    for row in sentences:
        array.append(row[1])
    f.close
    return array

def txt_to_list(file_):
    with open(file_, 'r') as f:
        list_file = f.readlines()
        list_file = [line.rstrip('\n') for line in list_file]

    return list(set(list_file))

sadness_sentences = csv_to_list('./dataset/sadness_fix.csv')
print(sadness_sentences)


def isSadness(user_sentence, sadness_sentences=sadness_sentences):
    okt = Okt()
    vect = TfidfVectorizer()

    for sen in sadness_sentences:
        x_data = np.array([sen, user_sentence])

        for i, document in enumerate(x_data):
            nouns = okt.morphs(document)
            x_data[i] = ' '.join(nouns)
        try:
            x_datas = vect.fit_transform(x_data)
            cosine_similarity_matrix = (x_datas * x_datas.T)
            result = (cosine_similarity_matrix.toarray())
            # 유사도 필터링
            if result[0][1] >= 0.35:
                print(x_data, result[0][1])
                return True
        except:return False

    return False

anger_dict = txt_to_list('./dataset/anger_words.txt')
#print(anger_dict)


def isAnger(sentence,anger_dict=anger_dict):
    okt = Okt()
    sentence_list = sentence.split()
    print(sentence_list)
    for words in sentence_list:
        for anger_word in anger_dict:
            if anger_word in words:
                return True
    else:
        return False

#############################
## 리포트 기능 관련 ##

import pandas as pd

def gen_report(file_name):
    a = pd.read_csv(file_name, encoding='CP949')
    a.to_html("log/negative_log_report.html")
    html_file = a.to_html()  # html code
    print(html_file)

def append_neg_row(file_name, list_of_elem):
    headers = ['Sentence', 'Date']
    with open(file_name, 'a+', newline='\n') as write_obj:
        file_is_empty = (os.stat(file_name).st_size == 0)
        csv_writer = csv.writer(write_obj)
        if file_is_empty==True:
            csv_writer.writerow(headers)
        date = datetime.today().strftime('%Y-%m-%d')
        csv_writer.writerow([list_of_elem[0],date])

# 로그 날짜 기반으로 count_graph.jpg 라는 파일 생성
def create_graph(file_name,begin=7,end=0):
    now = datetime.now()
    begin_ = str(now - timedelta(days=begin))[:10]
    end_ = str(now + timedelta(days=end))[:10]
    try:
        matplotlib.rc('axes', edgecolor='w')

        plt.figure(figsize=[9, 3])
        df = pd.read_csv("./"+file_name, encoding='CP949')
        df = df[(df.Date >= begin_) & (df.Date <= end_)]
        cnt = df.groupby('Date').size().rename('Count')
        df = df.drop(['Sentence'], axis=1)
        df = df.drop_duplicates(subset='Date').merge(cnt, left_on='Date', right_index=True)
        ax = df.groupby('Date').agg(['sum']).plot.bar(legend='',width=0.2, color="white") # bar 디자인
        ax.spines['left'].set_color('white')
        ax.tick_params(colors='white', which='both')

        for day in range(6, -1, -1):
            current_ = int(end_[5:7] + end_[8:10])
            del_day = str(current_ - day)
            if len(del_day) == 3:
                del_day = '0' + del_day[0:1] + '-' + del_day[1:3]
            else:
                del_day = del_day[0:2] + '-' + del_day[2:4]
            file = './web/img/' + end_[0:5] + del_day + '_log_graph.png'
            if os.path.isfile(file):
                os.remove(file)
        plt.savefig(file, transparent=True)

    except ValueError:
        for day in range(6, -1, -1):
            current_ = int(end_[5:7] + end_[8:10])
            del_day = str(current_ - day)
            if len(del_day) == 3:
                del_day = '0' + del_day[0:1] + '-' + del_day[1:3]
            else:
                del_day = del_day[0:2] + '-' + del_day[2:4]
            file = './web/img/' + end_[0:5] + del_day + '_log_graph.png'
            if os.path.isfile(file):
                os.remove(file)
        # 복사할 이미지
        copyfile('./web/graph.png', file)
        pass

def manage_graph(file_name):
    for file in os.scandir('./web/img'):
        if file.name.endswith(".png"):
            os.unlink(file.path)

    create_graph(file_name,begin=7,end=0)
    create_graph(file_name, begin=14, end=-7)
    create_graph(file_name, begin=21, end=-14)
    create_graph(file_name, begin=28, end=-21)
    arr = os.listdir('./web/img')
    arr.sort(reverse=True)

    for i in range(4):
        file = './web/img/'+str(i)+'.png'
        if os.path.isfile(file):
            os.remove(file)
        copyfile('./web/img/'+arr[i], file)

manage_graph('neg_sentence_log.csv')
######################################

def engkor(text):
    # 자음-초성/종성
    cons = {'r': 'ㄱ', 'R': 'ㄲ', 's': 'ㄴ', 'e': 'ㄷ', 'E': 'ㄸ', 'f': 'ㄹ', 'a': 'ㅁ', 'q': 'ㅂ', 'Q': 'ㅃ', 't': 'ㅅ',
            'T': 'ㅆ', 'd': 'ㅇ', 'w': 'ㅈ', 'W': 'ㅉ', 'c': 'ㅊ', 'z': 'ㅋ', 'x': 'ㅌ', 'v': 'ㅍ', 'g': 'ㅎ'}
    # 모음-중성
    vowels = {'k': 'ㅏ', 'o': 'ㅐ', 'i': 'ㅑ', 'O': 'ㅒ', 'j': 'ㅓ', 'p': 'ㅔ', 'u': 'ㅕ', 'P': 'ㅖ', 'h': 'ㅗ', 'hk': 'ㅘ',
              'ho': 'ㅙ', 'hl': 'ㅚ', 'y': 'ㅛ', 'n': 'ㅜ', 'nj': 'ㅝ', 'np': 'ㅞ', 'nl': 'ㅟ', 'b': 'ㅠ', 'm': 'ㅡ', 'ml': 'ㅢ',
              'l': 'ㅣ'}
    # 자음-종성
    cons_double = {'rt': 'ㄳ', 'sw': 'ㄵ', 'sg': 'ㄶ', 'fr': 'ㄺ', 'fa': 'ㄻ', 'fq': 'ㄼ', 'ft': 'ㄽ', 'fx': 'ㄾ', 'fv': 'ㄿ',
                   'fg': 'ㅀ', 'qt': 'ㅄ'}

    result = ''  # 영 > 한 변환 결과

    # 1. 해당 글자가 자음인지 모음인지 확인
    vc = ''
    for t in text:
        if t in cons:
            vc += 'c'
        elif t in vowels:
            vc += 'v'
        else:
            vc += '!'

    # cvv → fVV / cv → fv / cc → dd
    vc = vc.replace('cvv', 'fVV').replace('cv', 'fv').replace('cc', 'dd')

    # 2. 자음 / 모음 / 두글자 자음 에서 검색
    i = 0
    while i < len(text):
        v = vc[i]
        t = text[i]
        j = 1
        # 한글일 경우
        try:
            if v == 'f' or v == 'c':  # 초성(f) & 자음(c) = 자음
                result += cons[t]

            elif v == 'V':  # 더블 모음
                result += vowels[text[i:i + 2]]
                j += 1

            elif v == 'v':  # 모음
                result += vowels[t]

            elif v == 'd':  # 더블 자음
                result += cons_double[text[i:i + 2]]
                j += 1
            else:
                result += t

        # 한글이 아닐 경우
        except:
            if v in cons:
                result += cons[t]
            elif v in vowels:
                result += vowels[t]
            else:
                result += t

        i += j

    return join_jamos(result)

character = ''
sentence = list()

def on_press(key):
    global character

    try:
        character += key.char

    except:
        if key == Key.space:
            character += ' '
        else:
            character += ''

def get_sentence_kor(sentence):
    kor_list = list()
    for text in sentence:
        kor_list.append(engkor(text))
    return kor_list

def on_release(key):
    global character
    global sentence
    regex = re.compile('[^a-zA-Z ]')

    #print('{0} released'.format(key))
    if key == keyboard.Key.enter:
        character = regex.sub('', character)
        #print(character)
        character_list = character.split()
        sentence = character_list
        character = ''
        # Stop listener
        #return False
        predict_pos_neg(' '.join(get_sentence_kor(sentence)))

def keyboardListen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as Listener:
        Listener.join()


def tokenize(doc):
    # norm은 정규화, stem은 근어로 표시하기를 나타냄
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]

okt = Okt()

sentenceLogM = {}
try:
    with open('accounts/sentence.pk','rb') as f:
        sentenceLogM = dict(pickle.load((f)))
except:
    with open('accounts/sentence.pk','wb') as f:
        pickle.dump(sentenceLogM,f)

with open('data/sw.pkl', 'rb') as f:
    selected_words = pickle.load(f)[1]

def term_frequency(doc):
    return [doc.count(word) for word in selected_words]
model = tf.keras.models.load_model('data/saved_model/modelM')
cprint('모델 불러오기 완료','green')

now = datetime.now()

def predict_pos_neg(review):
    global sadnessCount
    if len(review) <= 1:
        return None
    token = tokenize(review)
    tf = term_frequency(token)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(model.predict(data))
    new_neg_sentence = list()
    ban = False
    for i in bannedWords:
        if i in review:
            ban=True
            score = 0
            break
    if (score > 0.5):
        print(colored('{}\n{:.2f} 긍정적인 감정'.format(review, score * 100), 'green'))
    else:
        global keyboard_disabling_count
        #### 리포트 기능 관련 ####
        #append_neg_row('neg_sentence_log.csv', [review])
        #manage_graph('neg_sentence_log.csv')
        #################################################################################
        # 입력문장, 어간 추출, 감정단어사전 비교, 가중치X
        negative_sentence = okt.morphs(review, stem=True)

        if ban:
            angryOnly = True
        else:
            angryOnly = isAnger(review, anger_dict=anger_dict)  ## 수정1 -> anger일 경우 True 반환

        print(angryOnly)
        if angryOnly:
            for anger_word in negative_sentence:
                sentenceLogM[currentUser].append(now.strftime("%b %d, %H:%M ") + review)
                with open('accounts/sentence.pk', 'wb') as f:
                    pickle.dump(sentenceLogM, f)
                eel.giveList('<li>' + ('</li>\n<li>'.join(sentenceLogM[currentUser])) + "</li>")
                if now.strftime('%Y-%m-%d') in perDays.keys():
                    perDays[now.strftime('%Y-%m-%d')][now.hour] += 1
                else:
                    perDays[now.strftime('%Y-%m-%d')] = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
                                                         10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0,
                                                         19: 0, 20: 0, 21: 0, 22: 0, 23: 0}
                    perDays[now.strftime('%Y-%m-%d')][now.hour] += 1
                print(colored('{}\n{:.2f} 부정적인 감정'.format(review, (1 - score) * 100), 'red'))
                run(keyboard_disabling_count * 20, 8)
                keyboard_disabling_count += 1
                run(keyboard_disabling_count * 20, 10)
                print(str(keyboard_disabling_count) + '/5')
                break
            if keyboard_disabling_count >= 5:
                ####리포트###
                gen_report('neg_sentence_log.csv')
                ############
                for i in range(150):
                    kb.block_key(i)
                cprint('20초 키보드 입력 정지', 'red')
                print(CheckVar.get())
                if CheckVar.get() == 0:
                    alert.balloon_tip('키보드 입력 정지됨', '20초 후 키보드가 활성화됩니다.')
                keyboard_disabling_count = 0
                time.sleep(16)
                time.sleep(1)
                print(3)
                time.sleep(1)
                print(2)
                time.sleep(1)
                print(1)
                time.sleep(1)
                print('사용가능')
                for i in range(150):
                    kb.unblock_key(i)
        # 슬픔일 경우
        else:
            sadness = isSadness(review)
            if sadness == True:
                sadnessCount += 1
                if sadnessCount >= 3:
                    if number != '':
                        print('SMS is sent to {}'.format(number))
                        sadnessCount = 0
                        message = client.messages.create(to="+82{}".format(number), from_="+18329812324",body="Mindful Keyboard 사용자님이 지금 우울해요. 같이 대화를 좀 해주시겠어요?")

def run(rate,sp):
	eel.move(rate,sp)

## ID: admin / PW: asd

bannedWords = []
for i in open('bannedWord.txt','r', encoding='UTF-8').readlines():
    bannedWords.append(i.replace('\n',''))

def register():
    global register_screen
    register_screen = Toplevel(login_window)
    register_screen.title("등록하기")
    register_screen.geometry("500x250")

    register_screen.geometry("500x200")
    register_screen.resizable(width='False', height='False')
    register_screen.configure(bg='#1F1C33')

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="아래 정보를 기입해주세요.", bg="#1F1C33",fg='white').pack()
    Label(register_screen, text="", bg="#1F1C33").pack()
    username_lable = Label(register_screen, text="아이디 * ",bg="#1F1C33",fg='white')
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username,bg='#1F1C33',highlightcolor='white',highlightthickness=1, fg='white')
    username_entry.pack()
    password_lable = Label(register_screen, text="비밀번호 * ",bg="#1F1C33",fg='white')
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*',bg='#1F1C33',highlightcolor='white',highlightthickness=1, fg='white')
    password_entry.pack()
    Label(register_screen, text="", bg="#1F1C33").pack()
    Button(register_screen, text="가입", width=10, height=1, command=register_user,bg='#1F1C33',highlightcolor='white',highlightthickness=4, fg='white').pack()

def setting():
    global settings
    try:
        with open('setting.pk','rb') as f:
            global settings
            settings = pickle.load(f)
    except:
        with open('setting.pk','wb') as f:
            pickle.dump({1:0,2:''},f)
            settings = {1:0,2:''}
    global setting_screen
    setting_screen = Toplevel(login_window)
    setting_screen.title("Setting")
    setting_screen.geometry("500x300")
    setting_screen.resizable(width='False', height='False')
    setting_screen.configure(bg='#1F1C33')
    Label(setting_screen, text="", bg='#1F1C33').pack()
    global CheckVar
    CheckVar=IntVar()
    Label(setting_screen, text="키보드 정지 알림 끄기", fg='white', bg='#1F1C33').pack()
    c1 = Checkbutton(setting_screen, variable=CheckVar, bg='#1F1C33')
    c1.pack()
    Label(setting_screen, text="", bg='#1F1C33').pack()
    Label(setting_screen, text="우울 감지 알림 전화번호", fg='white', bg='#1F1C33').pack()
    global call_entry
    call_entry = Entry(setting_screen, bg='#1F1C33', highlightcolor='white',
                                 highlightthickness=1, fg='white')

    if settings[1] == 1:
        c1.toggle()
    c1.update()
    call_entry.insert(0,settings[2])
    number = call_entry.get()
    print(CheckVar.get())

    call_entry.pack()
    Label(setting_screen, text="", bg='#1F1C33').pack()
    Label(setting_screen, text="사용자 설정 분노단어 목록(재시작 필요)", fg='white', bg='#1F1C33').pack()
    Button(setting_screen, text="열기", width=6, height=1, command=openBan, bg='#1F1C33', highlightcolor='white',
           highlightthickness=4, fg='white').pack()
    Label(setting_screen, text="", bg='#1F1C33').pack()
    Label(setting_screen, text="", bg='#1F1C33').pack()
    Button(setting_screen, text="설정 저장", width=30, height=1, command=setting_save, bg='#1F1C33', highlightcolor='white',
           highlightthickness=4, fg='white').pack()

def openBan():
    os.system('notepad.exe '
              'bannedWord.txt')

def setting_save():
    global number
    number = call_entry.get()
    print(number)
    if len(number) == 11 or number == '':
        print('settingSaved')
        print(CheckVar.get())
        print(number)
        with open('setting.pk','wb') as f:
            pickle.dump({1:CheckVar.get(),2:number},f)
        setting_screen.destroy()
    else:
        tempNotice = Label(setting_screen, text="전화번호가 잘못됬습니다. (- 기호 제외)", fg="red", font=("calibri", 8), bg='#1F1C33')
        tempNotice.pack()
        tempNotice.after(2000, tempNotice.destroy)


def login():
    global login_screen
    login_screen = Toplevel(login_window)
    login_screen.title("Login")
    login_screen.geometry("500x200")
    login_screen.resizable(width='False',height='False')
    login_screen.configure(bg='#1F1C33')
    Label(login_screen, text="", bg='#1F1C33').pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="아이디 ",fg='white' ,bg='#1F1C33').pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify,bg='#1F1C33',highlightcolor='white',highlightthickness=1, fg='white')
    username_login_entry.pack()
    Label(login_screen, text="",bg='#1F1C33').pack()
    Label(login_screen, text="비밀번호 ",fg = 'white', bg='#1F1C33').pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*',bg='#1F1C33',highlightcolor='white',highlightthickness=1, fg='white')
    password_login_entry.pack()
    Label(login_screen, text="",bg='#1F1C33').pack()
    Button(login_screen, text="로그인", width=10, height=1, command=login_verify,bg='#1F1C33',highlightcolor='white',highlightthickness=4, fg='white').pack()

def register_user():
    username_info = username.get()
    password_info = password.get()

    file = open('accounts/'+username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    sentenceLogM[username_info] = []
    with open('accounts/sentence.pk', 'wb') as f:
        pickle.dump(sentenceLogM, f)


    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="가입완료", fg="green", font=("calibri", 11),bg='#1F1C33').pack()

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir('accounts/')
    if username1 in list_of_files:
        file1 = open('accounts/'+username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess(username1)
        else:
            tempNotice = Label(login_screen, text="비밀번호가 틀렸습니다.", fg="red", font=("calibri", 8), bg='#1F1C33')
            tempNotice.pack()
            tempNotice.after(2000, tempNotice.destroy)
    else:
        tempNotice = Label(login_screen, text="유저를 찾을 수 없습니다.", fg="red", font=("calibri", 8), bg='#1F1C33')
        tempNotice.pack()
        tempNotice.after(2000, tempNotice.destroy)

# 로그인 성공 시 -> 이부분 모델 실행쪽으로 넘어가게 설정
def login_sucess(x):
    login_window.destroy()
    global currentUser
    currentUser = x
    eel.start('main.html', block=False)
    eel.sleep(2.0)
    keyboardListen()

def main_account_screen():
    global login_window
    login_window = Tk()

    login_window.geometry("520x330") #등록하기 기능 O
    login_window.resizable(width='False', height='False')
    #login_window.geometry("500x260") #등록하기 기능 X
    login_window.configure(bg='#1F1C33')
    login_window.title("Mindful Keyboard")
    key_img = PhotoImage(file='keyboard.png')
    Label(image=key_img, width="400", height="170",bg='white').pack()

    global settings
    global CheckVar
    try:
        with open('setting.pk','rb') as f:
            settings = pickle.load(f)
        CheckVar = IntVar()
        c1 = Checkbutton(setting_screen, variable=CheckVar, bg='#1F1C33')
        c1.pack()
        if settings[1] == 1:
            c1.toggle()
        c1.destroy()
    except:
        with open('setting.pk','wb') as f:
            pickle.dump({1:0,2:''},f)
            settings = {1:0,2:''}

    global number
    number = settings[2]
    Button(text="로그인", height="2", width="30", command=login, bg='#1F1C33',highlightcolor='white',highlightthickness=4, fg='white').pack()
    Button(text="등록하기", height="2", width="30", command=register,bg='#1F1C33',highlightcolor='white',highlightthickness=4, fg='white').pack()
    Button(text="설정", height="1", width="30", command=setting,bg='#1F1C33',highlightcolor='white',highlightthickness=4, fg='white').pack()
    login_window.mainloop()

if __name__ == '__main__':
    main_account_screen()