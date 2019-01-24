* 看到php -> wrapper
* 雖然沒有source code，但是可以透過?page = ...來知道他可能是利用include來做事。
* 只要?page = index.php ，就會include index.php，但是php會被apache解析，因此利用php://filter/convert.base64-encode/resource=index來繞過，得到index.php的source code。
* flag就在source code裡面。
