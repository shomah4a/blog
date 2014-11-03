====================================
 Emacs の環境設定をモダンにしてみた
====================================

malabar-mode 使うのにまた挑戦しよう! と思って .emacs.d 以下を見てみたら、過去の秘伝のソースが大量にあるわけです。
そのままでは大変カスタマイズがめんどくさそうだったので、最近の Emacs で使えるらしいパッケージマネージメントみたいなのを導入してみました。

経緯はこんな感じ。

.. tweet:: https://twitter.com/shomah4a/status/528048032848175104

.. tweet:: https://twitter.com/shomah4a/status/528061278963511296

.. tweet:: https://twitter.com/shomah4a/status/528061362082021376


パッケージマネージャ使ってみる
==============================

まずは環境をバッサリやっちゃう。
と言っても .emacs.d を mv するだけだけど。

これやらないとパッケージマネージャがまともに動かなかった。何やった過去の俺。

で、パッケージマネージャの使い方は簡単。

``M-x package-install`` してパッケージ名を選んでインストールするだけ。めっちゃ簡単!
インストールされたパッケージは ``~/.emacs.d/elpa`` にいる。

パッケージ候補が補完できない場合は ``M-x package-refresh-contents`` でパッケージカタログを取ってくるといいみたい。
なのだけど、標準だと malabar-mode とかないので、以下のサイトをみて emacswiki とかその他サイトをパッケージソースに追加した。

`ELPA <http://www.emacswiki.org/emacs/ELPA>`__

.. code-block:: cl

   (add-to-list 'package-archives '("marmalade" . "https://marmalade-repo.org/packages/"))
   (add-to-list 'package-archives '("melpa" . "http://melpa.milkbox.net/packages/"))
   (add-to-list 'package-archives '("org" . "http://orgmode.org/elpa/")) ; Org-mode's repository

追加したら ``M-x package-refresh-contents`` でパッケージ再取得を忘れずに。


インストールしたもの
--------------------

- init-loader
- migemo
- malabar-mode
- auto-complete
- theme-chenger
- js2-mode
- browse-kill-ring
- gtags
- calfw

設定とかは個別に書かないとダメらしい。

で、

.. tweet:: https://twitter.com/kiris/status/528073351021858816

と言われたので入れてみた。
これは大変便利なものですね。


init-loader
===========

init-loader は

.. code-block:: cl

   (require 'init-loader)
   (init-loader-load (substitute-in-file-name "$HOME/.emacs.d/init-loader")

こんなふうにして ``(init-loader-load "path")`` とするとそこにある *.el を読み込んでくれる。
さらに

- 00-hoge.el
- 10.fuga.el

みたいな init.d っぽい名前をつけるとその順番で読んでくれる。

でも init.el にそのまま書くとダメなようで、 package.el の初期化の後に回す必要があるらしい。

なので ``after-init-hook`` を使ってこんな感じにする。

.. code-block:: cl

   (add-to-list 'after-init-hook (lambda ()
                                    (require 'init-loader)
                                    (init-loader-load (substitute-in-file-name "$HOME/.emacs.d/init-loader"))
                                    ))


パッケージ以外
==============

パッケージにないやつで入れたい物もある。

- `windows.el <http://www.gentei.org/~yuuji/software/>`__
- `howm <http://howm.sourceforge.jp/index.html>`__

こういうのは ``$HOME/.emacs.d/site-lisp`` とかディレクトリ掘っといて、

.. code-block:: cl
                
   ;; ロードパス追加
   (setq site-lisp-root (substitute-in-file-name "$HOME/.emacs.d/site-lisp"))

   (mapcar (lambda (p)
              (if (not (or (eq "." p) (eq ".." p)))
                (add-to-list 'load-path (concat site-lisp-root "/" p))
              )) (directory-files site-lisp-root))

みたいな感じにして適当にパスに入れておく。


設定持ってくる
==============

ここまでやったら最初に mv しておいた秘伝のソースから init-loader のディレクトリにコピペしまくる。

とりあえず

- 00 emacs の標準機能系カスタマイズ
- 10 emacs の標準で入っている el のカスタマイズ
- 20 パッケージで入れたやつのうち、言語系以外
- 50 言語ごとにファイル作ってカスタマイズ (50-python.el とか 50-rst.el とか)

みたいな感じにしてる。

ここまでやってモダンになりましたっと。


まとめ
======

.. tweet:: https://twitter.com/shomah4a/status/528105383512920064


.emacs.d は適当に `github <https://github.com/shomah4a/.emacs.d>`__ にあげときました。

次は emacs24 でも入れてみるかなあ。

あ、ちなみに肝心の malabar-mode はまともにうごいてません。




.. author:: default
.. categories:: none
.. tags:: Emacs
.. comments::
