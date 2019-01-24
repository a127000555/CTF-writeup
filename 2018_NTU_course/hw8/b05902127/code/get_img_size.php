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

    function __destruct() {
    	echo "call destrution!\n";
        if( $this->mode === "delete" )
            $this->delFile();
        if( $this->mode === "upload" ){
        	echo "wow? just put!\n";
            file_put_contents($this->name, $this->content);
        }
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
    }

}

$size = getimagesize($argv[1]);
echo "Your file size: " . $size[3] . "\n";
?>
