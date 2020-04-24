import re
import MeCab

mecab = MeCab.Tagger()
text = open("123", encoding='utf-8').read()
lyric_begin = text.find('"lyric"')  # 是 "lyric" 的 " 的index
lyric_begin = lyric_begin + len('"lyric":"')
# begin = text[0:lyric_begin]
temp = text[lyric_begin:]
lyric_end = temp.find('"')
lyric = temp[:lyric_end]  # not with "
lines = lyric.split("\\n")  # every lines lose \n

# u0800-u4e00 日文utf-8范围
processed_lyric = ""
for i in range(0, len(lines)):
    time_end = lines[i].find(']') + 1
    pure_l = lines[i][time_end:]

    if len(pure_l) == 0:  # 略去空行
        processed_lyric += lines[i] + '\\n'
        continue

    if i <= 6:  # 略去歌手名
        if pure_l.find('：') != -1:
            processed_lyric += lines[i] + '\\n'
            continue
        elif pure_l.find(':') != -1:
            processed_lyric += lines[i] + '\\n'
            continue

    if re.search('[\u4E00-\u9FBF]', pure_l) is None:  # 如果不存在汉字
        processed_lyric += lines[i] + '\\n'
        continue

    print(pure_l)
    # print(mecab.parse(pure_l))
    results = str(mecab.parse(pure_l)).split("\n")
    print(results[0].split(',')[-2])  # read
    print(results[0].split('\t')[0])  # word
    print("#########################")
# end for