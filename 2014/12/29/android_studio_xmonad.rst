Android Studio を動かそうとした話
=================================

年の瀬で時間あるしなんかやろうかと思って Android Studio を入れてみることにしたんですよ。

そしたら動かなかったのでメモ。


症状
----

- Android Studio をたちあげたら、描画がおかしい(再描画されない)
- 操作を一切受け付けない
- とりあえずまともにつかえない

みたいな感じ。


環境
----

とりあえず環境

- VAIO Z 2012 モデル?
- Ubuntu 14.04 LTS x64
- xmonad 0.11 (Ubuntu 標準)


ぐぐった
--------

- Android Studio は IntelliJ IDEA Community Edition の上に構築されているらしい
- Intellij IDEA は Java っていうか JVM 上で動くらしい

ということはなんとなく知ってたので、いつものように xmonad と Java 系 GUI の相性が悪いやつだと思ってた。
でもsさすがにそれでは困るのでとりあえず調べてみた。

https://code.google.com/p/android/issues/detail?id=56538

Ubuntu + xmonad で困ってる人っぽい

| #1 lordcr...@gmail.com
| This actually appears to be an xmonad issue, found the fix here: https://code.google.com/p/xmonad/issues/detail?id=177#c56

コメント一個目でいきなり答え出てた。

https://code.google.com/p/xmonad/issues/detail?id=177#c56

| Finally a fix for this problem!
|
| @53:
| 
| Add import XMonad.Hooks.ICCCMFocus to the top of your xmonad.hs file. Then set logHook = takeTopFocus. Or if you got more things there like I do:
| 
| lookHook = do
|    ...
|    takeTopFocus
|    ...


どうやら ``logHook`` なるものを指定してあげればいいらしいので、 xmonad.hs に追加。

立ち上がった後に正常に描画されるようになりましたとさ。

今の xmonad.hs はこんな感じ。

.. gist:: https://gist.github.com/shomah4a/dd6ef868c7c04205ee82







.. author:: default
.. categories:: none
.. tags:: Android, Xmonad, Android Studio
.. comments::
