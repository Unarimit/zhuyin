import re
import MeCab
import NakaDictionary
from Debug import DEBUG


class PlayMode:
    """enum class"""
    HIRA_ZHUYIN = 1
    NAKA_ZHUYIN = 2
    TO_ROMAJI = 3
    HIRA_ZHUYIN_SP = 4


class Processor:
    def __init__(self, mode: int = PlayMode.HIRA_ZHUYIN):
        self.mecab = MeCab.Tagger()  # -Oyomi -Owakati
        self.Mode = mode

    def process(self,  file_name: str = '123') -> str:
        try:
            text = open(file_name, encoding='utf-8').read()
        except UnicodeDecodeError:
            return ""
        if text[0] != '{':
            return ""

        lyric_begin = text.find('"lyric"')  # 是 "lyric" 的 " 的index
        lyric_begin = lyric_begin + len('"lyric":"')
        # begin = text[0:lyric_begin]
        temp = text[lyric_begin:]
        lyric_end = temp.find('"},')  # 小心转义字符
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

            if DEBUG:
                print(pure_l)
            # 初步处理 \u3000
            pure_l = re.sub('\u3000', ' ', pure_l)
            segment_line = pure_l.split(' ')  # 有没有使用空格分开不同的句子
            processed_text = ""
            for segment in segment_line:
                if self.Mode == PlayMode.HIRA_ZHUYIN:
                    processed_text += self._process_hira(segment) + ' '
                elif self.Mode == PlayMode.NAKA_ZHUYIN:
                    processed_text += self._process_naka(segment) + ' '
                elif self.Mode == PlayMode.TO_ROMAJI:
                    processed_text += self._process_romaji(segment) + ' '
                elif self.Mode == PlayMode.HIRA_ZHUYIN_SP:
                    processed_text += self._process_hira_sp(segment) + ' '
            processed_lyric += lines[i][:time_end] + processed_text[:-1] + '\\n'
        # end for
        if DEBUG:
            print(processed_lyric)
        result = text[:lyric_begin] + processed_lyric + temp[lyric_end:]
        ''' clear klyric'''
        '''
        klyric_begin = result.find('"klyric":{')
        if klyric_begin != -1:
            klyric_begin += len('"klyric":{')
            if result[klyric_begin:].find('null') == -1 or result[klyric_begin:].find('null') > 35:
                klyric_end = result[klyric_begin:].find('}')
                clear_str = '"version":0,"lyric":null'
                result = result[:klyric_begin] + clear_str + result[klyric_begin:][klyric_end:]
                # version = 8 chu wen ti
                version_begin = result.find('"lrc":{"version":') + len('"lrc":{"version":')
                # print(result[version_begin]) first number
                if 47 < ord(result[version_begin+1]) < 58:
                    result = result[:version_begin] + '10' + result[version_begin + 2:]
                else:
                    result = result[:version_begin] + '10' + result[version_begin + 1:]
        '''

        if DEBUG:
            print(result)
        return result

    def _process_hira(self, pure_line: str) -> str:
        processed_line = ''
        try:
            result = str(self.mecab.parse(pure_line)).split("\n")
            for single in result:
                word = single.split('\t')[0]  # word
                if len(single.split(',')) < 3 or single.split(',')[-2] == '*':  # 如果没那么多数据项说明不可读
                    if word != 'EOS':
                        processed_line += word
                    continue

                read = single.split(',')[-2]  # read
                hiragana = ""
                if word == read:
                    processed_line += word
                    continue

                for kata in read:  # 将得到的片假名注音(最后带有换行符)换成平假名
                    if kata in NakaDictionary.kata_to_hira:
                        hiragana += NakaDictionary.kata_to_hira.get(kata)
                    else:
                        hiragana += kata

                if word == hiragana:  # 如果注音和原句相同
                    processed_line += word
                else:
                    processed_line += word + '(' + hiragana + ')'

            if DEBUG:
                print(processed_line)
                print("######################")
        except RuntimeError as e:
            if DEBUG:
                print("RuntimeError:" + str(e))
            print('可能因为没有安装MeCab，出现了异常')

        return processed_line

    def _process_naka(self, pure_line: str) -> str:
        processed_line = ''
        try:
            result = str(self.mecab.parse(pure_line)).split("\n")
            for single in result:
                word = single.split('\t')[0]  # word
                if len(single.split(',')) < 3 or single.split(',')[-2] == '*':  # 如果没那么多数据项说明不可读
                    if word != 'EOS':
                        processed_line += word
                    continue

                read = single.split(',')[-2]  # read
                hiragana = ""
                if word == read:
                    processed_line += word
                    continue

                for kata in read:  # 将得到的片假名注音(最后带有换行符)换成平假名
                    if kata in NakaDictionary.kata_to_hira:
                        hiragana += NakaDictionary.kata_to_hira.get(kata)
                    else:
                        hiragana += kata

                if word == hiragana:  # 如果注音和原句相同
                    processed_line += word
                else:
                    processed_line += word + '(' + read + ')'
            if DEBUG:
                print(processed_line)
                print("######################")
        except RuntimeError as e:
            if DEBUG:
                print("RuntimeError:" + str(e))
            print('可能因为没有安装MeCab，出现了异常')

        return processed_line

    def _process_romaji(self, pure_line: str):
        processed_line = ''
        try:
            result = str(self.mecab.parse(pure_line)).split("\n")
            for single in result:
                word = single.split('\t')[0]  # word
                if len(single.split(',')) < 3 or single.split(',')[-2] == '*':  # 如果没那么多数据项说明不可读
                    if word != 'EOS':
                        processed_line += word
                    continue

                read = single.split(',')[-2]  # read
                hiragana = ""
                for kata in read:  # 将得到的片假名注音(最后带有换行符)换成平假名
                    if kata in NakaDictionary.kata_to_romaji:
                        hiragana += NakaDictionary.kata_to_romaji.get(kata)
                    else:
                        hiragana += kata

                processed_line += hiragana + " "
            if DEBUG:
                print(processed_line)
                print("######################")
        except RuntimeError as e:
            if DEBUG:
                print("RuntimeError:" + str(e))
            print('可能因为没有安装MeCab，出现了异常')

        return processed_line

    def _process_hira_sp(self, pure_line: str) -> str:
        processed_line = ''
        try:
            result = str(self.mecab.parse(pure_line)).split("\n")
            for single in result:
                word = single.split('\t')[0]  # word
                if len(single.split(',')) < 3 or single.split(',')[-2] == '*':  # 如果没那么多数据项说明不可读
                    if word != 'EOS':
                        processed_line += word
                    continue

                read = single.split(',')[-2]  # read
                hiragana = ""
                if word == read:
                    processed_line += word
                    continue

                for kata in read:  # 将得到的片假名注音(最后带有换行符)换成平假名
                    if kata in NakaDictionary.kata_to_hira:
                        hiragana += NakaDictionary.kata_to_hira.get(kata)
                    else:
                        hiragana += kata

                if word == hiragana:  # 如果注音和原句相同
                    processed_line += word
                else:
                    processed_line += '{' + word + '}' + '(' + hiragana + ')'
            if DEBUG:
                print(processed_line)
                print("######################")
        except RuntimeError as e:
            if DEBUG:
                print("RuntimeError:" + str(e))
            print('可能因为没有安装MeCab，出现了异常')

        return processed_line
