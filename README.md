# 把网易云音乐的日文歌词加上注音吧\!

可以把网易云音乐的日文歌词加上注音(效果见[Test.md](https://github.com/Unarimit/Japanese-Music-ZhuYin-Tool/blob/master/Test.md))，也可以全部转换成罗马音(效果见[TestRomaji.md](https://github.com/Unarimit/Japanese-Music-ZhuYin-Tool/blob/master/TestRomaji.md))，两者结果大部分准确。

网易云版本2.7.1, Windows10, 2020/4/24 功能正常

## 怎么做

### 方法一，对缓存中的歌词文件进行替换(注音)

问题：有些歌曲替换(注音)之后，格式正确，网易云仍会请求覆盖掉替换的结果（大概10首歌里面一首是这样

- 下载并安装 [mecab-0.996.exe](https://drive.google.com/drive/folders/0B4y35FiV1wh7fjQ5SkJETEJEYzlqcUY4WUlpZmR4dDlJMWI5ZUlXN2xZN2s2b0pqT3hMbTQ)
    >访问不了google? 去百度一下别的下载方法！
    >
    >最好选择UTF-8的字典(在安装选字典编码的时候)
- 下载release中的[zhuyin.exe](https://github.com/Unarimit/Japanese-Music-ZhuYin-Tool/releases/download/ver1.1/zhuyin.exe)
- 关闭网易云音乐
    > 一些歌词会被载入到内存中，退出以释放
- 打开zhuyin.exe，找到歌词的**缓存**目录进行替换
    > 一般在C:\Users\\[你的用户名]\AppData\Local\Netease\CloudMusic\Temp
    >
    > 注:AppData是一个隐藏文件夹
- 重新打开网易云
    > 如果以离线方式打开，可以解决开头所说的问题

### 方法二，对下载后的歌词文件进行替换(注音)

- 下载并安装 [mecab-0.996.exe](https://drive.google.com/drive/folders/0B4y35FiV1wh7fjQ5SkJETEJEYzlqcUY4WUlpZmR4dDlJMWI5ZUlXN2xZN2s2b0pqT3hMbTQ)
    >访问不了google? 去百度一下别的下载方法！
    >
    >最好选择UTF-8的字典(在安装选字典编码的时候)
- 下载release中的[zhuyin.exe](https://github.com/Unarimit/Japanese-Music-ZhuYin-Tool/releases/download/ver1.1/zhuyin.exe)
- 将要改的歌先用网易云下下来
- 让你的网易云连不上网，并清空缓存
    > 可以在设置里面的工具选单，将Http代理指向不存在的代理端口，例如 服务器:127.0.0.1 端口:80
    > 也可以直接断网
- 打开zhuyin.exe，找到歌词的目录进行替换
    > 一般在C:\Users\\[你的用户名]\AppData\Local\Netease\CloudMusic\webdata\lyric，那些一大堆数字的就是歌词文件了
    >
    > 注:AppData是一个隐藏文件夹
- 重新打开网易云(此时网易云不能访问网络)
    > 如果之后联网让网易云拿到缓存的话，再清空一下缓存即可。

## 一些原因

- mecab是一个分词软件，我用到了，我不会把他嵌入进软件里，所以要安装。

## 问题

会把带有量词的读音弄错（例如：二人 futari 会被分成二(に) 人(にん)) ni nin）毕竟分词器本身并不是用来标注读音的，是日语的错。
> 可以通过加字典来解决，但

Romaji 助词は 错误的-> ha
> 可以通过对词性的判断解决，但

## 未来

有空把"显示转换结果，可以对其修改完再保存"的功能做了
