Sphinx につぶやきを埋め込んでみる
=================================

`Python Developers Festa 2013.03 <http://connpass.com/event/1579/>`_ に参加してきました。

午前中は大体人と話していて潰れるのがいつものパターンで、発表が始まったあたりから開発し始めます。

で、今回は怖い人たちに混じって人生初サインとかしてきたりしましたがまあそれはそれで。

タイトルの通り Sphinx の拡張を初めて作ってみたのでブログでも書いてました。
作ったのは Twitter のつぶやきを埋め込みだけの簡単な拡張です。

ソースは `github <https://github.com/shomah4a/sphinx-tweet-embed>`_ にあげてあります。

やっていることは twitter のつぶやきを埋め込むメニューみたいなのにあるタグを生成しているだけなので簡単です。


使い方
------

- `github のタグのページ <https://github.com/shomah4a/sphinx-tweet-embed/tags>`_ から tgz を落としてくるなり find-links で pip やら easy_install するなりしてインストールします
- sphinx の conf.py に追加します

  .. code-block:: python

     extensions = ['sphinx_tweet_embeded']

- ビルドします

  .. code-block:: sh

     $ make html



使い方 on Sphinx
----------------

こんなふうに tweet ディレクティブを使うと

.. code-block:: rst

   .. tweet:: https://twitter.com/inoshiro/status/312857117952454657


こんな感じになります。

.. tweet:: https://twitter.com/inoshiro/status/312857117952454657


便利ですねー。

Sphinx で動くのでちんけらーでももちろんそのまま動きます。


そのうち PyPI にも追加しよう。



.. author:: default
.. categories:: none
.. tags:: Sphinx, Tinkerer, Python
.. comments::
