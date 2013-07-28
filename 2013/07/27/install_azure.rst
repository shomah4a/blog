================================================
 Windows Azure 上で Hello, World するまでのメモ
================================================

`Python Developers Festa 2013.07 <http://connpass.com/event/2217/>`_ で Azure 使って Python でなんかやるぞーと思って SDK 入れてみようとしたメモ。

環境は Ubuntu 12.10 x64

Azure SDK をビルドするまで
==========================

- ここから SDK をダウンロードする

  http://www.windowsazure.com/ja-jp/downloads/?sdk=python

- 展開して configure する
- configure の中身は Python

  - 全体的にインデントが2スペースで残念な気持ち

- 38行目あたりで errors = true とか書いてあって未定義だと言われて残念な気持ち
- nodejs と npm を apt-get install で入れる
- 入れたら node のコマンドが違って node_version() の返り値がおかしくて落ちる
- 8行目の

  .. code-block:: python

     proc = subprocess.Popen(['node', '-v'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

  を

  .. code-block:: python

     proc = subprocess.Popen(['nodejs', '-v'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

  に書き換え

- configure 通った
- make install したら node のライブラリを入れないといけないらしくて sudo する必要あるぽい
- 会場で git:// が使えなくて https:// に書き換えた
- ubuntu 12.10 で入れた node.js と npm だと古くてダメっぽいので `自力ビルド <http://nodejs.org/download/>`_
- nodejs ってのは ubuntu の apt-get で入れた時の node コマンドだという事が判明
- ~/.npm が root の権限で作られていて死ぬから消す
- 普通にビルドしたら通った
- bin/azure してみた
- streamline がない
- npm install streamline
- commander がない
- npm install commander
- winston が(ry
- eyes が(ry
- easy-table が(ry
- azure (ry
- underscore (ry
- xml2js (ry
- node-uuid (ry
- tunnel (ry
- async (ry
- kuduscript (ry
- github (ry

で、やっと動いた。
んだけどこれセットアップできてるのかしら。
っていうか npm install だけでいけたのではないか。

で、これの結果実行できるようになった azure コマンドは azure のインスタンス立ち上げたりする管理用コマンドみたい。

まあそうですよね。

Windows で入れたら Visual Studio みたいなのもくっついてきたけど Linux でそんなもんあるわけないわな。


Python で Hello, World してみるまで
===================================

Web サイトで Python 使う場合はこれ見たほうが手っ取り早い(わかる人は)
http://www.windowsazure.com/en-us/develop/python/tutorials/web-sites-configuration/

django は `これ <http://www.windowsazure.com/en-us/develop/python/tutorials/web-sites-with-django/>`_ らしいんだけど、 django 使う気も特になかったから問題ない。

で、 WSGI で Hello, World するだけのアプリケーションを作って適当にデプロイして設定したら動いた。
よかったねー。

で、動くまで色々試したんだけど、まあエラー出まくるわけです。

その際のログは ftp で見られるらしいんだけど、トレースバックログとかどこに出るのよ?


あと、普通にインスタンスたちあげてセットアップして動かしたほうが融通効いて楽なのではと思いましたまる。



.. author:: default
.. categories:: Azure Python
.. tags:: none
.. comments::
