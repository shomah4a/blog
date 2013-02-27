Tinkerer を使ってブログを作るまでのメモ
=======================================

っていうか特にやることないですが。

まあメモ程度にダラダラと。

Tinkerer って何よ
-----------------

ちんけらーとは Sphinx の上に乗っかって作られたブログ生成システムです。

こいつを使うと Sphinx のドキュメントの書きやすさをそのままにブログっぽいものが作れます。

例えばこのブログみたいな。


ブログを作る
------------

pip でも easy_install でも buildout でもなんでもいいので `Tinkerer <https://pypi.python.org/pypi/Tinkerer/>`_ をインストールしましょう。

んでもって tinker ってコマンドに `-s` をつけて実行するとブログのテンプレートがどかっと作られます。

.. code-block:: sh

   $ tinker -s
   Your new blog is almost ready!
   You just need to edit a couple of lines in conf.py
   $ tree

   .
   ├── _static
   ├── conf.py
   ├── drafts
   ├── index.html
   └── master.rst

   2 directories, 3 files

こんなの。

まあ sphinx のプロジェクトですから見慣れてますよね。

conf.pyをいじる
---------------

conf.py を見るといじれと書いてあるのでいじりましょう。

.. code-block:: python

   # **************************************************************
   # TODO: Edit the lines below
   # **************************************************************

   # Change this to the name of your blog
   project = 'My blog'

   # Change this to the tagline of your blog
   tagline = 'Add intelligent tagline here'

   # Change this to your name
   author = 'Winston Smith'

   # Change this to your copyright string
   copyright = '1984, ' + author

   # Change this to your blog root URL (required for RSS feed)
   website = 'http://127.0.0.1/blog/html/'


とりあえずビルドしてみる
------------------------

ブログを作ったディレクトリで `tinker -b` するとブログがビルドされます。

同じディレクトリに `index.html` があるので、こいつをブラウザで開くとブログっぽいものが表示されます。

簡単ですね。


エントリ追加
------------

`tinker -p ページ名` でページを追加します。

.. code-block:: sh

   $ tinker -p test
   New post created as '/tmp/aaaa/2013/02/26/test.rst'

なんか rst ファイルが作られたので、これを編集して `tinker -b` するとブログにエントリが追加されるってわけです。

すげーわかりやすいですね。


カスタマイズ
------------

せっかくなのでカスタマイズもしてしまいます。

とりあえずお手軽なのがテーマですね。

conf.py にある

.. code-block:: python

   html_theme = "modern5"

ってところを書き換えます。

デフォルトではこんなテーマがあるようです。

- modern
- boilerplate
- minimal
- responsive
- tinkerbase
- modern5

見た目の好みだけなのでとりあえず minimal を選びました。

シンプルでいいですね。


テンプレートをいじる
--------------------

以下のようなことをやりたかったのでテンプレートをいじりました。

- プロフィール追加
- tweet ボタン追加
- はてブボタン追加


カスタムテーマ
~~~~~~~~~~~~~~

`themes/custom_minimal` とかディレクトリを掘ってやり、 `conf.py` でパスを通します。

んでテーマ名を今作った custom_minimal に変更します。

.. code-block:: python

   ...

   # Pick another Tinkerer theme or use your own
   html_theme = "custom_minimal"

   ...

   # Add other theme paths here
   html_theme_path = [tinkerer.paths.themes, 'themes']

   ...



このディレクトリに `theme.conf` を置いておくとテーマが作られるので

.. code-block:: ini

   [theme]
   inherit = minimal

こんな内容で作りましょう。

同じディレクトリに author.html を置いて、適当な内容を記述しておきます。

まあ HTML を書くだけですが、 `tinker/themes/tinkerbase/recent.html <https://bitbucket.org/vladris/tinkerer/src/default/tinkerer/themes/tinkerbase/recent.html?at=default>`_ なんかからコピーしてきて書き換えるとそれっぽくなるんじゃないかな。

そんで `conf.py` の `html_sidebars` に値を追加して出来上がり。

.. code-block:: python

   # Add templates to be rendered in sidebar here
   html_sidebars = {
       "**": ["author.html", "recent.html", "searchbox.html"]
   }


ボタンとか追加
~~~~~~~~~~~~~~

んーここらへんは説明がめんどくさい。

`Twitter Buttons <https://twitter.com/about/resources/buttons>`_ とか `はてブボタン <http://b.hatena.ne.jp/guide/bbutton>`_ とかからソースをコピーしてきて適当に設置しましたが、 URL がどうとかまあ面倒なこともあるし、 Tinkerer だと aggregation.html から conf.py の website の値が見られないので JavaScript で色々頑張ったりとか。

あと Zope Page Template 以外はほとんど触ったことがなかったので Jinja2 をフィーリングでなんとなく使ったりとか。

JavaScript が有効じゃないとまともに見られないサイトは糞だと思っていますが、ここはまあページの本質じゃないし仕方ないかなあ。

ウダウダ言うよりソース見たほうがはやいと思うので `ソース <https://bitbucket.org/shomah4a/blog/src/master/themes/custom_minimal>`_ 見てください。


まとめ
------

Tinkerer というか Sphinx 最高ですね。

Sphinx の拡張使いまくってブログ書けるのマジ便利。


.. author:: default
.. categories:: none
.. tags:: sphinx, tinkerer
.. comments::
