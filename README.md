<h1>Installation</h1>
Client (Windows)
<br>
<code>setup_windows.bat</code>
<br><br>
Server (Raspbian)
<br>
<code>source setup_raspbian.sh</code>

<h1>Command</h1>
Client (Windows)
<br>
<code>cd Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi-master\Code\Client\</code>
<br>
<code>python Main.py</code>
<br><br>
Server (Raspbian)
<br>
<code>cd Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi-master/Code/Camera/</code>
<br>
<code>sudo python main.py</code>
<br><br>
Camera - Capture (Raspbian)
<br>
<code>cd Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi-master/Code/Camera/</code>
<br>
<code>sudo python capture.py</code>
<br><br>
Camera - Calibration (Raspbian)
<br>
<code>cd Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi-master/Code/Camera/images/</code>
<br>
<code>sudo mv captured/* calibration/</code>
<br>
<code>cd ..</code>
<br>
<code>sudo python capture.py</code>