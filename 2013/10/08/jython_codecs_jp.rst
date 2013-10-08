Jython 用 _codecs_jp を作ってみた
=================================

:doc:`/2013/07/30/jython` で触れた通り、 Jython には ``_codecs_jp`` というモジュールがないために

.. code-block:: python

   >>> u'あいうえお'.encode('cp932')
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   LookupError: unknown encoding 'cp932'

なんてコードすら動かなかったりします。

これでは結構困ってしまうので、 `java.nio.charset <http://docs.oracle.com/javase/7/docs/api/java/nio/charset/package-summary.html>`__ を使って適当に ``_codecs_jp`` モジュールを作りました。

ソースは `github <https://github.com/shomah4a/jython_codecs_jp>`__ に上がっています。

適当に ``git clone`` してパスを通して使ってください。

jython の場合は ``PYTHONPATH`` ではなく ``JYTHONPATH`` を使うみたいなので間違わないようにしてください。




.. author:: default
.. categories:: none
.. tags:: Python, Jython
.. comments::
