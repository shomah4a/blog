========================
 たのしい Jython 第二回
========================

さて、まだまだ Jython を使っているわけですが、色々と問題が出てきて楽しいなーってことでまたネタにしましょう。


.. _popenpid:

Popen.pid がない!
=================

はい。

.. code-block:: python

   >>> import subprocess
   >>> p = subprocess.Popen('python')
   >>> print p.pid
   None

はい。

`ここらへんに書いてあります。 <http://python.6.x6.nabble.com/subprocess-pid-td1766477.html>`_

一応理由は簡単で、プロセスの立ち上げで使っている `java.lang.Process`_ に ``pid`` を取得するようなインタフェイスがないからですね。

なので諦めましょう。


subprocess で立ち上げたプロセスを kill したい
=============================================

:ref:`上記 <popenpid>`  で触れたように ``Popen`` オブジェクトに ``pid`` がありません。

これじゃあ ``os.kill()`` とかできないわけです。

あー困ったなー殺せないなと諦めたいところですが、そうもいかないので頑張りましょう。

``Popen`` オブジェクトは ``_process`` という属性を持っています。
本来であればアクセスするべきではない属性名ですが、気にしている場合ではありません。

こいつは `java.lang.Process`_ のインスタンスなので `destroy() <http://docs.oracle.com/javase/7/docs/api/java/lang/Process.html#destroy()>`_ というメソッドを持っています。

殺すだけならこいつを呼んでしまいましょう。


.. code-block:: python

   >>> import subprocess
   >>> p = subprocess.Popen('python')
   >>> p._process
   java.lang.UNIXProcess@3e890800
   >>> p._process.destroy()
   >>> print p.poll()
   143

ほら、殺せました。


.. _keyboardinterruptjython:

KeyboardInterrupt が受け取れない
================================

さて、以下は CPython の様子です。

.. code-block:: python

   >>> while True:
   ...     pass
   ...
   ^CTraceback (most recent call last):
     File "<stdin>", line 1, in <module>
   KeyboardInterrupt
   >>>

こんな感じに処理中に `C-c` を押下すると ``KeyboardInterrupt`` 例外が発生します。

これが Jython になると

.. code-block:: python

   >>> while True:
   ...     pass
   ...
   $

最後の ``$`` はシェルのプロンプトです。

``KeyboardInterrupt`` が発生せず、 JVM ごと落ちます。

この件は `issue <http://bugs.jython.org/issue1313>`_ が上がっているようです。

そのうち直るんじゃないかなー。

Windows で C-c が効かない
=========================

:ref:`上記 <keyboardinterruptjython>` と似たような話ですが、これは深刻です。

そもそも Windows で Jython を使うと `C-c` を押下してもなんにも反応してくれません。

これも `issue <http://bugs.jython.org/issue1957>`_ が上がっています。

回避するには Jython 起動時の ``java`` コマンドのオプションに ``-Dpython.console=org.python.util.InteractiveConsole`` を追加してあげるといいようです。


atexit したい
=============

Python だと終了時処理を行うためのモジュールとして `atexit <http://docs.python.jp/2/library/atexit.html>`_ というものがあるのですが、これを使うと :ref:`KeyboardInterrupt <keyboardinterruptjython>` の件と同じ理由なのか `C-c` で落ちた時に動いてくれません。

こんなときは Python に閉じこもっていないで Java の方面から攻めましょう。

`Runtime.addShutdownHook <http://docs.oracle.com/javase/7/docs/api/java/lang/Runtime.html#addShutdownHook(java.lang.Thread)>`_ を使います。


こんな感じです。

.. code-block:: python

   from java import lang

   class ExitHandler(lang.Thread):

       def run(self):
           # なんか処理
           ...

   lang.Runtime.getRuntime().addShutdownHook(ExitHandler())


これで終了時に処理してくれます。


まとめ
======

Jython 楽しい! ✌('ω'✌ )三✌('ω')✌三( ✌'ω')✌




.. _java.lang.Process: http://docs.oracle.com/javase/7/docs/api/java/lang/Process.html


.. author:: default
.. categories:: none
.. tags:: Jython, Python
.. comments::
