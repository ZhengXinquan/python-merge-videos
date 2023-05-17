
import os
import random
import functools
from moviepy.editor import VideoFileClip,  concatenate_videoclips

'''
获取镜头信息
'''


def getClip():
    print('开始从文件夹中获取镜头信息')
    fileList = os.listdir('./videos')
    list = []
    temp = ''
    for p in fileList:
        # print(p, type(p))
        pp = os.path.join(os.getcwd(), './videos', p)
        if os.path.isdir(pp):
            l2 = os.listdir(pp)
            l2temp = []
            for p2 in l2:
                path2 = os.path.join(pp, p2)
                l2temp.append(path2)
            list.append(l2temp)
        else:
            temp = pp
    return {'list': list, 'temp': temp}


'''
 分镜头重组（镜头重复出现，5*5*5*5*5 = 3125 个视频）
'''


def get_all_list(args_list):
    print('分镜头重组（重复）')
    initIndexList = [0 for item in args_list]
    indexList = initIndexList.copy()
    maxList = [(len(item)-1) for item in args_list]

    def add():
        l = len(indexList)
        checkMax = 0
        flag = 1
        for i in range(l):
            if checkMax == 1:
                if indexList[i] > maxList[i]:
                    if (i + 1 < l):
                        indexList[i] = 0
                        indexList[i+1] += 1
                        # print(i, '进位')
                    else:
                        flag = 0
                        # print('超过，无法进位，结束1')
                        break
            else:
                if indexList[i] < maxList[i]:
                    indexList[i] += 1
                    # print(i, '+1')
                    break
                else:
                    if (i + 1 < l):
                        indexList[i] = 0
                        indexList[i+1] += 1
                        checkMax = 1
                        # print(i, '进位')
                    else:
                        flag = 0
                        # print('超过，无法进位，结束2')
                        break
        return {'flag': flag, 'list': indexList.copy()}

    def getValue(vList, iList):
        re = []
        for i in range(len(iList)):
            re.append(vList[i][iList[i]])
        return re

    arr = [getValue(args_list, initIndexList)]
    temp = add()
    while (temp['flag'] == 1):
        print('temp', temp)
        arr.append(getValue(args_list, temp['list']))
        temp = add()
    return arr

# '''
# 分镜头重组（每个镜头只出现一次，用过即删）
# '''


def get_simple_list(args_list):
    print('分镜头重组（用过即删）')
    list_len = len(args_list)
    flag = 1
    arr = []
    while list_len > 0 and flag != 0:
        flag += 1

        winner = []
        for i in range(list_len):
            # 操作第N个文件夹
            item_list = args_list[i]

            #
            item_list_len = len(item_list)

            # 有一个文件夹的镜头用完了
            if (item_list_len == 0):
                flag = 0
                break
            # 随机一个镜头    元素下标
            random_index = random.randrange(item_list_len)

            # 获取一个镜头   移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
            winner_item = args_list[i].pop(random_index)

            # 将镜头写入结果
            winner.append(winner_item)
        arr.append(winner)
    return arr


# '''
# 分镜头重组（获取指定数量的组合）
# '''
def get_some_list(args_list):
    print('分镜头重组（指定数量）')
    total = functools.reduce(
        lambda x, y: x*y, [len(item) for item in args_list])

    max_num = input("请输入要生成的视频数量：（最大值"+str(total)+"）")
    max_num = int(max_num)
    list_len = len(args_list)
    arr = []
    splitStr = 'this_is_my_split_string'
    while len(arr) < max_num:
        winner = []
        for i in range(list_len):
            # 操作第N个文件夹
            item_list = args_list[i]

            #
            item_list_len = len(item_list)

            # 随机一个镜头    元素下标
            random_index = random.randrange(item_list_len)

            # 获取一个镜头   移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
            winner_item = item_list[random_index]

            # 将镜头写入结果
            winner.append(winner_item)
        # print('winner', winner)
        s = splitStr.join(winner)
        if (arr.count(s) == 0):
            arr.append(s)
            # print('str', s)

    return [s.split(splitStr)for s in arr]


'''
输出视频
'''


def outVideo(args_list, temp):
    print('开始生成的视频，数量：', len(args_list))
    demoAudio = VideoFileClip(temp).audio
    for j in range(len(args_list)):
        clips = [VideoFileClip(path, audio=False)for path in args_list[j]]
        outPath = "./out/"+str(j+1)+".mp4"
        print(outPath, '处理中...')
        concatenate_videoclips(clips).set_audio(
            demoAudio).write_videofile(outPath)


'''
main
'''


choose = input("A：用过即删；B：重复镜头；C：指定数量。 请输入：").lower()
print(choose)

clips = getClip()

if (choose == 'a'):
    winner_list = get_simple_list(clips['list'])  # 5 个
if (choose == 'b'):
    winner_list = get_all_list(clips['list'])  # 5*5*5*5*5 = 3125 个
if (choose == 'c'):
    winner_list = get_some_list(clips['list'])

if (len(winner_list) > 0):
    outVideo(winner_list, clips['temp'])
