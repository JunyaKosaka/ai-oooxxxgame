#! python3
# -*- coding: utf-8 -*-
# 三目並べ
# 遊んでいる人をユーザー、プレイヤーは別

import random, time

board10 = [None, '1', '2', '3', '4', '5', '6', '7', '8', '9']
XX = {'O': 10, 'X': -10, ' ': 0}

def draw_board(board):
    # ボードを表示する。"board"は10個の文字列のリスト。Index0は無視。
    for i in range(7, 0, -3):
        print('   |   |')
        print(' ' + ' | '.join(board[i:i+3]))
        print('   |   |')
        if i > 1:
            print('-----------')

def input_user_letter():
    # ユーザーに OかXを選んでもらう。[ユーザーの駒, コンピュータの駒] のリストを返す。
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('O=先手、X=後手、どちらにしますか？（O or X)')
        letter = input().upper()
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def play_again():
    #プレイヤーがもう一度遊ぶと答えたらTrue、そうでなければFalseを返す。
    print('もう一度遊ぶ？（yes or no)')
    return input().lower().startswith('y')

def make_move(board, letter, move):
    board[move] = letter

def count_all_lines(bo):
    # bo  はボード。全てのラインの点数のリストを返す
    score_all_lines = [XX[bo[7]] + XX[bo[8]] + XX[bo[9]],
    XX[bo[4]] + XX[bo[5]] + XX[bo[6]],
    XX[bo[1]] + XX[bo[2]] + XX[bo[3]],
    XX[bo[7]] + XX[bo[4]] + XX[bo[1]],
    XX[bo[8]] + XX[bo[5]] + XX[bo[2]],
    XX[bo[9]] + XX[bo[6]] + XX[bo[3]],
    XX[bo[7]] + XX[bo[5]] + XX[bo[3]],
    XX[bo[9]] + XX[bo[5]] + XX[bo[1]]]
    return score_all_lines

def is_winner(bo, le):
    # どちらかのプレイヤーが勝ちなら True を返す。boはボードの略。
    if le == 'O':
        return count_all_lines(bo).count(30) >= 1
    else:
        return count_all_lines(bo).count(-30) >= 1

def reach_status(bo, le):
    # リーチがいくつかかっているかの数を返す。
    # boはボード、leはプレイヤーの駒、re_numはreach_number（いくつリーチしているか）の略
    if le == 'O':
        return count_all_lines(bo).count(20)
    else :
        return count_all_lines(bo).count(-20)

def get_board_copy(board):
    # ボードのコピーを作る
    return board[:]

def is_space_free(board, move):
    # ボードが空いていればTrueを返す
    return board[move] == ' '

def reverse_le(letter):
    if letter == 'O':
        return 'X'
    else:
        return 'O'

def avoid_reach(board, letter):
    # リーチをletterで回避したboardを返す
    for i in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, i):
            letter2 = reverse_le(letter)
            make_move(copy, letter2, i)
            if is_winner(copy, letter2):
                make_move(board, letter, i)
                return board

def get_user_move(board):
    # プレイヤーに次の手を入力してもらう。
    while True:
        print('1=左下 〜 9=右上のどこに打つ？(1-9)')
        move = input()
        if move in board10:
            imove = int(move)
            if is_space_free(board, imove):
                return imove
            else:
                print('マスの番号')
                draw_board(board10)

def choose_random_move_from_list(board, moves_list):
    # 渡されたリストから有効な次の手をランダムに選んで返す。
    # 打つ場所がなければNoneを返す
    possible_moves = []
    for i in moves_list:
        if is_space_free(board, i):
            possible_moves.append(i)
    
    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    else:
        return None

def check_2nd_ryonerai(board, letter):
    # リーチがかかっている状態で相手がリーチを防ぐ。letterはリーチをかけた方。その後両狙いがあるかどうか。行けるならTrueを返す
    opponents_letter = reverse_le(letter)
    copy2 = get_board_copy(board)
    avoid_reach(copy2, opponents_letter)
    if  reach_status(copy2, opponents_letter) == 2:
        print('チェック１')
        return False
    elif reach_status(copy2, opponents_letter) == 1:
        print('チェック２')
        # 相手が逆王手してきてそれに両狙いで返せるか
        for j in range(1,10):
            copy3 = get_board_copy(copy2)
            avoid_reach(copy3, letter)
            if reach_status(copy3, letter) == 2:
                print('逆王手に両狙いの返し技！！')
                return True
            return False
    print('チェック３') # リーチ→相手が逆王手なし→両狙いの３ての読み
    check = there_is_ryonerai(copy2, letter)
    return check 

def there_is_ryonerai(board, letter):
    # 両狙いの手があるならTrueを返す
    for i in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, i):
            make_move(copy, letter, i)
            if reach_status(copy, letter) == 2:
                return True
    return False

def get_computer_move(board, computer_letter):
    user_letter = reverse_le(computer_letter)
    # 三目並べのAIのアルゴリズム
    # まず、次の手で勝てるかどうかを調べる。
    for i in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, i):
            make_move(copy, computer_letter, i)
            if is_winner(copy, computer_letter):
                return i
    # ユーザーがリーチしているなら、それを防ぐ
    for i in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, i):
            make_move(copy, user_letter, i)
            if is_winner(copy, user_letter):
                print('必然手')
                return i
    
    # 両狙いが出来るならそこに打つ。
    for i in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, i):
            make_move(copy, computer_letter, i)
            if reach_status(copy, computer_letter) == 2:
                print('両狙い！')
                return i
    
    # リーチをかけて3手先に両狙いが出来るならそこに打つ。
    for i in range(1, 10):
        copy = get_board_copy(board)
        if is_space_free(copy, i):
            make_move(copy, computer_letter, i)
            if reach_status(copy, computer_letter) == 1:
                if check_2nd_ryonerai(copy, computer_letter):
                    print('好手')
                    return i
    print('ランダムで打とうかな')
    # 角か真ん中が空いていれば、ランダムでそこに打つ。
    #但し次の手で相手に両狙いがあるなら他の手を探す。10回の試行回数
    for _ in range(1, 10): 
        move = choose_random_move_from_list(board, [1, 3, 5, 7, 9])
        if move != None:
            copy = get_board_copy(board)
            make_move(copy, computer_letter, move)
            if reach_status(copy, computer_letter) == 0 and there_is_ryonerai(copy, user_letter):
                print('両狙いを看破')
                continue
            elif reach_status(copy, computer_letter) == 1 and there_is_ryonerai(copy, user_letter):
                for j in range(1, 10):                   
                    copy2 = get_board_copy(copy)
                    avoid_reach(copy2, user_letter)
                    if reach_status(copy2, user_letter) ==2 :
                        print('リーチをかけたら両狙いで返されるね')
                        continue
                    else :
                        print('リーチをかければ両狙いを防げるね')
                        return move
            else :
                return move                    
                
    print('やっぱりランダムしかない')
    # 真ん中が空いていれば、そこに打つ。
    if is_space_free(board, 5):
        return 5

    # 上下左右に打つ。
    return choose_random_move_from_list(board, [2, 4, 6, 8])

def is_board_full(board):
    # ボードが埋まったらTrueを返す。
    for i in range(1, 10):
        if is_space_free(board, i):
            return False
    return True


print('三目並べにようこそ！')
draw_board(board10)
time.sleep(1)
print('手番の時は1から9で入力してね')

while True:
    # ボードをリセットする。
    the_board = [' '] * 10

    user_letter, computer_letter = input_user_letter()
    
    if user_letter == 'O':
        turn = 'プレーヤー'
    else:
        turn = 'コンピュータ'
    print(turn + 'が先手。')
    
    start_choice = ['お手柔やかに^^', 'お手並み拝見！', 'Good Luck!']
    print(random.choice(start_choice))
    
    while True:
       time.sleep(1)
       if is_winner(the_board, user_letter):
            draw_board(the_board)
            print('おめでとう！　あなたの勝ち！')
            break

       if is_winner(the_board, computer_letter):
            draw_board(the_board)
            print('コンピュータの勝ち！')
            break
           
       if is_board_full(the_board):
            draw_board(the_board)
            print('引き分けだね！')
            break    

       if turn == 'プレーヤー':
            # プレーヤーの番
            draw_board(the_board)
            move = get_user_move(the_board)
            make_move(the_board, user_letter, move)
            turn = 'コンピュータ'

       else:
            # コンピュータの番
            move = get_computer_move(the_board, computer_letter)
            make_move(the_board, computer_letter, move)
            turn = 'プレーヤー'

    if not play_again():
        break
