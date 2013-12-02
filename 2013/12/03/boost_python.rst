=============================================================
 Python Advent Calendar 2013 三日目: Python3 と Boost.Python
=============================================================

`Python Advent Calendar 2013 <http://www.adventar.org/calendars/166>`__ の三日目です。
なんかネタもなかったので `Boost.Python <http://www.boost.org/doc/libs/1_55_0/libs/python/doc/index.html>`__ で遊んでました。

で、 `Python2.x <http://python.org/download/releases/2.7.6/>`__ はもはや Legacy Python と呼ばれているようなので、ここは Modern な処理系である `Python3.3 <http://python.org/download/releases/3.3.3/>`__ を使います。

環境
====

遊んでた環境は以下の通り。
Python がちょっと前にビルドしたやつなんでちょっと古いけど気にしてはいけません。


.. list-table::

   * - OS
     - Ubuntu 12.10 x64
   * - Python
     - 3.3.2
   * - gcc
     - 4.7.2

Boost をビルドする
==================

Boost をビルドしましょう。

したことなかった気がする。

- `ダウンロードページから <http://www.boost.org/users/history/version_1_55_0.html>`__ tarball ゲット
- ``$HOME/user-config.jam`` に使いたい Python のパスを通してあげる。

  .. code-block:: text

     using python : 3.3 : /usr/local/python3.3 : /home/shoma/files/Python-3.3.2/Include : /usr/local/python3.3/lib ;


- boost のソースを展開してきたパスに移動して

  .. code-block:: sh

     $ ./bootstrap.sh
     $ ./b2

とやったらビルド終了らしい。
なにこれ簡単。


モジュールでも作ってみる
========================

Boost がビルドできたのでなんか作りましょう。

とりあえず、 ``hello`` というモジュールに ``output`` という関数と ``SomeObject`` というクラスを定義して、 Python から使えるようにする例です。


.. code-block:: cpp

   #include <string>
   #include <iostream>
   #include <boost/python.hpp>


   #define self (*this) // !important


   const std::string output(const std::string str)
   {
       std::cout << str << std::endl;

       return str;
   }



   class SomeObject
   {
       int value;

   public:
       SomeObject(const int x) : value(x) {}
       SomeObject(const SomeObject& r) : value(r.value) {}

       const int get_value() const
       {
           return self.value;
       }

       void set_value(const int x)
       {
           self.value = x;
       }
   };


   BOOST_PYTHON_MODULE(hello)
   {
       namespace python = boost::python;

       python::def("output", output);

       python::class_<SomeObject>("SomeObject", python::init<const int>())
           .def("get_value", &SomeObject::get_value)
           .def("set_value", &SomeObject::set_value);
   }


で、これをビルドします。

.. code-block:: sh

   $ g++ test.cpp -o hello.so -shared -fPIC `/usr/local/python3.3/bin/python3.3-config --libs --cflags` \
        -L/usr/local/python3.3/lib -lpython3.3m \
        -I/home/shoma/files/Python-3.3.2 \
        -I/home/shoma/downloads/boost_1_55_0 \
        -L/home/shoma/downloads/boost_1_55_0/stage/lib \
        -lboost_python \
        --std=c++11


すると hello.so なんてファイルができるので、この場で Python を立ち上げます。

.. code-block:: sh

   $ LD_LIBRARY_PATH=/usr/local/python3.3/lib:/home/shoma/downloads/boost_1_55_0/stage/lib /usr/local/python3.3/bin/python3



そしておもむろに作ったモジュールを読み込んでみましょう。


.. code-block:: python

   >>> import hello
   >>> hello
   <module 'hello' from './hello.so'>
   >>> hello.output("Hello, Boost.Python")
   Hello, Boost.Python
   'Hello, Boost.Python'
   >>> obj = hello.SomeObject(100)
   >>> obj
   <hello.SomeObject object at 0x7febeebbf838>
   >>> obj.get_value()
   100
   >>> obj.set_value(10)
   >>> obj.get_value()
   10


ほら動きました。


まとめ
======

- Boost.Python は Python3 でも使えるよ!
- Boost.Python かわいい
- C++ かわいい

つくったものは `github <https://github.com/shomah4a/python-advent-calendar-2013>`__ に置いてます。


.. author:: default
.. categories:: none
.. tags:: Advent Calendar, Python, C++, Advent Calendar 2013
.. comments::
