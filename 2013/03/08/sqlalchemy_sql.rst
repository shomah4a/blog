SQL 表現言語のあれこれ
======================

`@hirokiky <https://twitter.com/hirokiky>`_ が SQLAlchemy の `SQL 表現言語 <http://omake.accense.com/static/doc-ja/sqlalchemy/sqlexpression.html>`_ (っていうらしいことを初めて知った)を使って `なんかやっていて <http://blog.hirokiky.org/2013/03/07/aggregation_with_sqlalchemy_sqlexpression.html>`_ 、ちょっと書いてみたくなったので書きます。

SQL 表現言語はオブジェクトの演算子オーバロードを駆使して SQL を生成するためのライブラリです。
なので ORM よりは若干レイヤが低い感じ。

いつも `sqlalchemy.ext.declarative` でテーブル定義を書いて、 SQL 表現言語でクエリ作って投げるくらいしか使わないから色々やっているんだけど、あれやるときどうやるのーみたいなのが結構あるのでメモったほうがいいかなーと思いつつ書きます。


`Java の型からメソッドを検索するもの <https://github.com/shomah4a/sakuya>`_ (Java の `Hoogle <http://www.haskell.org/hoogle/>`_ とか `Hayoo! <http://holumbus.fh-wedel.de/hayoo/hayoo.html>`_ みたいなの, 以下 sakuya) を作った時のテーブルを使いまわし。


テーブル定義
------------

sakuya で使ったテーブル定義は以下のようなもの。
型情報、メソッド情報、メソッドの引数情報を持つだけのテーブル定義なのでこの3つだけ。


.. code-block:: python

   # tables.py

   import sqlalchemy as al
   from sqlalchemy import sql
   from sqlalchemy.sql import functions
   from sqlalchemy.ext import declarative as decl


   Base = decl.declarative_base()


   class Type(Base):
       u'''
       型の名前と名前空間を保持

       :param int id: primary key
       :param str name: クラス名
       :param str fqname: パッケージ名まで含めた名前
       '''

       __tablename__ = 'types'
       __table_args__ = (
           al.UniqueConstraint('fqname', name='uc_fqname'),)

       id = al.Column(al.Integer, primary_key=True, autoincrement=True)
       name = al.Column(al.Unicode(255), nullable=False)
       fqname = al.Column(al.Unicode(1024), nullable=False)



   class Method(Base):
       u'''
       メソッド情報

       :param int id: primary key
       ;param int signature:
       :param str name: メソッド名
       :param str fqname: パッケージ名・クラス名まで含めた名前
       '''

       __tablename__ = 'methods'

       id = al.Column(al.Integer, primary_key=True, autoincrement=True)
       signature = al.Column(al.Unicode(512), nullable=False)
       name = al.Column(al.Unicode(255), nullable=False)
       fqname = al.Column(al.Unicode(1024), nullable=False)
       class_ = al.Column(al.Integer, al.ForeignKey('types.id'), nullable=False)
       return_type = al.Column(al.Integer, al.ForeignKey('types.id'), nullable=False)
       argcount = al.Column(al.Integer)
       modifiers = al.Column(al.Integer, nullable=False)



   class MethodArg(Base):
       u'''
       メソッドの引数

       :param int method_id: 対象メソッド (PK, FK)
       :param int order: メソッドの番号 (PK)
       :param int type: 型名 (FK)
       '''

       __tablename__ = 'methodargs'

       method_id = al.Column(al.Integer, al.ForeignKey('methods.id'), primary_key=True)
       order = al.Column(al.Integer, primary_key=True)
       type = al.Column(al.Integer, al.ForeignKey('types.id'), nullable=False)


セッション
----------

セッションは大体 `sqlalchemy.orm.sessionmaker` で作ったセッションを使って作ることが多いので、以下のような感じで `Session` クラスとか作って対応してます。
これ標準でやってくれそうだけど調べてない。

.. code-block:: python

   # session.py

   class Session():

       def __init__(self):

           self.session = session()


       def __enter__(self):

           return self.session


       def __exit__(self, *exception):

           if exception[0] is not None:
               self.session.rollback()

           self.session.close()


insert
------

`insert` は大体 `declaretive` の機能そのまんまでやることが多いかも。

例えば `Type` を追加するときはこんな感じ。

.. code-block:: python

   # セッション作って
   with session.Session() as sess:

       # トランザクション張って
       with sess.begin():

           # 作って
           typ = tables.Type(name='List', fqname='java.util.List')

           # 追加
           sess.add(typ)


まあ見たまんまですね。


selsct
------

例えばさっき作った `List` を検索するならこんな感じ。

.. code-block:: python

   tbl = tables.Type.__table__

   # 等価な SQL
   # selsct name, fqname from types where name = 'List';
   query = sql.select([tbl.c.name, tbl.c.fqname], tbl.c.name == 'List', tbl)

   with sesion.Session() as sess:
       result_proxy = sess.execute(query).fetchone()


まあなんとなくわかりますね。


join
----

続いて `Method` と `Type` を `join` して `'List'` が返り値の型であるメソッドを取得してみます。


.. code-block:: python

   method = tables.Method.__table__
   rtype = tables.Type.__table__

   joined = method.join(rtype, method.c.return_type == rtype.c.id)

   u'''
     等価な SQL
     select methods.name, types.name
     from methods
       join types on methods.return_type = types.id
     where types.name = 'List'
   '''

   query = sql.select([method.c.name, rtype.c.name], rtype.c.name == 'List', joined)

   with sesion.Session() as sess:
       result_proxy = sess.execute(query).fetchall()


もうちょっと複雑なこと
----------------------

なんかいい例がなかったので、メソッドの引数と返り値を全部列挙して文字列にしてみましょう。

この時「返り値の型が `'List'` 」かつ「引数が3つ」という条件で検索します。

`methods`, `types`, `methodargs` テーブルを `join` する必要があります。
また、 `types` は引数と返り値で二回出てくるので、別名を付けないといけません。

あと、 `group by` の結果の順序は保証されないのでもうちょっと考えないといけないですね。

.. code-block:: python

   # 別名をつける
   method = tables.Method.__table__
   marg = tables.MehodArg.__table__
   rtype = tables.Type.__table__.alias('return_type')
   atype = tables.Type.__table__.alias('arg_type')

   u'''
     こんなことやってる
     from methods
       join methodargs on methods.id = methodargs.method_id
       join types atype on methodargs.type = atype.id
       join types rtype on methods.return_type = rtype.id
   '''
   joined = method.join(marg, method.c.id == marg.c.method_id)
   joined = joined.join(atype, marg.c.type == atype.c.id)
   joined = joined.join(rtype, method.c.return_type == rtype.c.id)

   # sqlite 用に group by の後のカラムをカンマで連結する
   # group_concat(atype.name, ',')
   concat = sql.func.group_concat(atype.c.name, ',')

   query = sql.select([rtype.c.name, method.c.name, concat],
                      sql.and_(rtype.c.name == 'List',
                               method.c.argcount == 3),
                      joined).group_by(method.c.id)

   u'''
     最終的に作られるクエリは以下のようなもの

     select rtype.name, methods.name, group_concat(atype.name, ',')
     from methods
       join methodargs on methods.id = methodargs.method_id
       join types atype on methodargs.type = atype.id
       join types rtype on methods.return_type = rtype.id
     where
       rtype.name = 'List' and
       methods.argcount = 3
     group by methods.id
   '''

   with session.Session() as sess:
       # 多分こんなのがたくさん返ってくる(一例)
       # ['List', 'someMethod', 'Integer,String,String']
       result_proxy = sess.execute(query).fetchall()


色々やるときは SQL 生で書くよりはずっと楽なのでいいですよね。




.. author:: default
.. categories:: none
.. tags:: Python, SQLAlchemy
.. comments::
