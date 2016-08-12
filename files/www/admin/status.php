<?php
/*Resourced by header.php
GeoIP status updates end-to-end encrypted */

    $f1 = fopen("/www/admin/config/ssid", "r");
    $ssid=fgets($f1);                                                                                                                              
    fclose($f1);
    $fn='/www/admin/config/networkstate';
    if (file_exists($fn)) {
        $f2 = fopen("/www/admin/config/networkstate", "r");
        $g=fgets($f2);                                                                                                                              
        if ($g) {
            if (preg_match('/online/', $g) == 1) {
                $url = 'https://plugunplug.net/geoip/yourip.php';
                $ch = curl_init();
                $timeout = 5;
                curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
                curl_setopt($ch, CURLOPT_HEADER, 0); 
                curl_setopt($ch,CURLOPT_URL, $url);
                curl_setopt($ch,CURLOPT_CONNECTTIMEOUT,$timeout);
                curl_setopt($ch,CURLOPT_CAINFO,'/etc/stunnel/server.crt');
                echo $ssid."<b> Status</b> ONLINE "; 
                $vpnstatus = fopen("/www/admin/config/vpnstatus", "r");
                $h=fgets($vpnstatus);
                if (preg_match('/up/', $h) == 1) {
                    echo "<b>Tunneled via</b> ";
                } 
                else {
                    echo "<b>Routed via</b> ";
                }
                fclose($vpnstatus);
                curl_exec($ch);
                //echo "unplug SSID: ".$ssid."Status: ONLINE. Tunneled through:".curl_exec($ch);
                curl_close($ch);
            }
            else if (preg_match('/offline/', $g) == 1) {
                echo $ssid."<b>Status</b> OFFLINE";
            }
        }
        fclose($f2);
    }
?>
