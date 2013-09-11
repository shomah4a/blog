=========================
 Jython を実用してみた件
=========================

仕事柄 JVM は必ず使うので、その上で動くのであれば Jython でしょうということで、隠れて Jython でツール作ったりしてました。

Jython を実用するのは初めてなので、色々とハマったりしまくったのでメモっときます。


CLASSPATH と sys.path と jar の扱い
===================================

Jython で sys.path を見てみると

.. code-block:: python

   ['', '/usr/lib/site-python', '/usr/share/jython/Lib', '__classpath__', '__pyclasspath__/', '/usr/share/jython/Lib/site-packages']

こんな感じで JVM っぽいパスが追加されていません。
起動前に CLASSPATH に設定したらそれっぽく読めるようになるけど、それでも sys.path には追加されません。

なので、 sys.path に jar を追加してみても

.. code-block:: python

   >>> import sys
   >>> sys.path.append('/usr/lib/jsonic-1.3.0.jar')
   >>> import net.arnx.jsonic
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ImportError: No module named net

こんな感じで怒られてしまいます。

Jython 起動後に jar を追加するには `sys.packageManager.addJar <http://www.jython.org/javadoc/org/python/core/packagecache/PackageManager.html#addJar(java.lang.String, boolean)>`_ を使います。

.. code-block:: python

   >>> import sys
   >>> sys.packageManager.addJar('/path/to/jsonic-1.3.0.jar', True)
   >>> import net.arnx.jsonic
   >>> net.arnx.jsonic
   <java package net.arnx.jsonic 0x2>

まあ使うってわかっている場合は素直に CLASSPATH に追加しておいたほうがいいかもしれないですね。


_codecs_jp.so がない
====================

例えばよくある unicode 文字列から sjis に変換する例

.. code-block:: python

   >>> print u'あああ'.encode('sjis')
   Traceback (most recent call last):
     File "/tmp/test.py", line 3, in <module>
       print u'あああ'.encode('sjis')
   LookupError: unknown encoding 'sjis'


これが動きません。

どうやら codecs モジュールで使われている _codecs_jp というモジュールが存在しない模様。
このモジュール、どうやら CPython では so(pyd) らしいので、 Jython では使えないんですねー。

なので nio とか使って頑張るしかないようです。

.. code-block:: python

   def wrap(s):

       if s < 0:
           return s + 0x100

       return s


   def convert_sjis(s):

       sjis = java.nio.charset.Charset.forName('Shift_JIS')
       result = [chr(wrap(e)) for e in sjis.encode(s).array()]
       return ''.join(result)


なんか他にやりようないのかな。


なんか他にも色々ありそうですけど、ひとまずここまで。


.. author:: default
.. categories:: none
.. tags:: Jython, Python
.. comments::
