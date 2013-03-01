Tinkerer にはてなスターでもつけてみる
=====================================

:doc:`この前 </2013/02/26/setup_tinkerer>` はちんけらーのセットアップとカスタマイズをしましたが、今日も引き続きカスタマイズします。

はてなブックマークだけでは飽きたらず、はてなスターをつけてみます。
まあ、スターとかいいじゃないですか。もらったらちょっと嬉しかったりしますよね。

なのでつけます。

あ、ドキュメントは `ここらへん <http://developer.hatena.ne.jp/ja/documents/star/misc/hatenastarjs>`_ にあるので、これ見たら一通りできるっぽいですよ。


自分のブログを登録
------------------

まず、はてなにログインして http://s.hatena.ne.jp/${userid}/blogs に行き、作ったブログを登録します。

で、なんかトークンを埋め込むための JavaScript がが表示されるので、 Tinkerer のテンプレートに埋め込みます。

埋め込むのは layout.html です。

layout.html には extrahead というブロックが定義されていて、これをオーバライドすることでヘッダ領域に自由にタグを埋め込めます。

.. code-block:: html

   {% extends "minimal/layout.html" %}


   {% block extrahead %}
       <script type="text/javascript" src="http://s.hatena.ne.jp/js/HatenaStar.js"></script>
       <script type="text/javascript">
         Hatena.Star.Token = 'それぞれのトークン';
       </script>
   {% endblock %}


これでトークンの登録ができたようです。


スターを出す
------------

で、トークンを置いたらスターを実際に表示する部分を作ります。

現在 page.html は以下のようになっています。

`div.buttons` の下に twitter ボタンやらはてブボタンやらをズラッと並べる感じです。

ここで、スターを出すための要素は buttons の最後に並べて左揃えにしてあります。
ふぁぼ爆っぽく無駄に連打したいじゃないですか。スターだし。

で、ここで問題があります。
というか前と全く同じなのですが、ブログトップでのエントリ一覧で、リンク先のページの絶対 URL が取れないという問題です。

なのでここは仕方なくはてブの時と全く同じように JavaScript で URL を生成し、非表示の `a` タグの `href` に突っ込むという方法をとりました。

できあがった `page.html` は以下のような感じです。

.. code-block:: html

   {#
       tinkerbase/page.html
       ~~~~~~~~~~~~~~~~~~~~

       Master layout for Tinkerer pages.

       :copyright: Copyright 2011-2012 by Vlad Riscutia and contributors (see
       CONTRIBUTORS file)
       :license: FreeBSD, see LICENSE file
   #}

   {% extends "layout.html" %}

   {% block body %}
       {{ tinkerer_relbar() }}
       <div class="section_head">
       <div class="timestamp_layout">
         {{ timestamp(metadata.formatted_date) }}
       </div>
       {% block buttons %}
       <div class="buttons">
         <a href="https://twitter.com/share" class="twitter-share-button">Tweet</a>
         <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
         <a href="http://b.hatena.ne.jp/entry/http://google.com/" class="hatena-bookmark-button" data-hatena-bookmark-title="{{ title }} - {{ project }}" data-hatena-bookmark-layout="simple-balloon" title="このエントリーをはてなブックマークに追加"><img src="http://b.st-hatena.com/images/entry-button/button-only.gif" alt="このエントリーをはてなブックマークに追加" width="20" height="20" style="border: none;" /></a>
         <span class="hatenastar"> </span>

         {# パーマリンクのための URL 生成してつけるためのタグ #}
         <a style="display:none" class="parmalink_for_star">a</a>
       </div>

       <script type="text/javascript"><!--
         $('a[class="hatena-bookmark-button"]').toArray().map(
             function (e)
             {
                 e.setAttribute('href', 'http://b.hatena.ne.jp/entry/' + window.location.host + window.location.pathname);
             });
       --></script>
       <script type="text/javascript" src="http://b.st-hatena.com/js/bookmark_button.js" charset="utf-8" async="async"></script>
       <script type="text/javascript"><!--
         $('a[class="parmalink_for_star"]').toArray().map(
             function (e)
             {
                 e.setAttribute('href', window.location.origin + window.location.pathname);
             });
       --></script>
       {% endblock %}
       </div>
       {{ link }}
       {{ body }}
       {{ post_meta(metadata) }}
       {{ comments }}
   {% endblock %}


で、このあとに先ほど埋め込んだスクリプトにはてなスターを出す設定をします。

詳しいことはドキュメントを見てもらうとして、以下のように `Hatena.Star.SiteConfig.entryNodes` の中で場所とスターをつける先の URL を指定するらしいです。

.. code-block:: html

   {% extends "minimal/layout.html" %}


   {% block extrahead %}
       <script type="text/javascript" src="http://s.hatena.ne.jp/js/HatenaStar.js"></script>
       <script type="text/javascript">
         Hatena.Star.Token = 'おまいのトークン';

         Hatena.Star.SiteConfig = {
           entryNodes: {
             'div.body': {
               uri: 'div.section_head div.buttons a.parmalink_for_star',
               title: 'div.section h1',
               container: 'div.section_head div.buttons span.hatenastar'
             };
           }
         };

       </script>
   {% endblock %}


ビルド
------

で、後はビルドしてアップロードすればスターつけ放題ってわけですね。

すばらしい。


.. author:: default
.. categories:: none
.. tags:: tinkerer, sphinx, hatena
.. comments::
