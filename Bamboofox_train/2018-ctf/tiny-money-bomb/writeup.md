bitcoin 地址算法流程：http://8btc.com/article-1929-1.html



#### Stage 1 : Fill up to 50 chars

* 題目給的是"bitcoin address"，而我們要轉成"valid address"，這句話聽起來非常奇怪，其實指的是valid address還有多一個check。
* 因此我們只要把bitcoin address**先補0後**，逆解base58，最後在利用上面網址所說的：sha256兩次抓前4個bytes丟尾端在重新base58，就可以解第一個階段了。

#### Stage 2 : Address Warping

* 題目把一個"valid address"的char用空白取代掉，此時我們只要爆搜base58裡面58個characters，再利用bitcoin valid address機制檢查就可以了。