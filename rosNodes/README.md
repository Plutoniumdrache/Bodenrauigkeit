# Anleitung für die Erstellung des gesamten ROS Systems
Diese Anleitung bezieht sich auf den Raspberry PI, für den Arduino siehe bite anderes README im Arduino Ordner.

# 1. Systemvorausetzungen
Vorraussetzung ist ein System mit Ubuntu 18.04 LTS mit ROS **melodic**.
Es ist vollkommen ausreichend und geht auch schneller lediglich die `ros-base` Version zu installieren.
Installationsanleitung [hier](http://wiki.ros.org/melodic/Installation/Ubuntu)

# 2. Erstellen des ROS Packages
ROS Tutorials [hier](http://wiki.ros.org/ROS/Tutorials) bis zum Punkt "3. Creating a ROS Package" ausführen.  

Den Namen `beginner_tutorials` gegen `floorpack` austauschen.

```
$ catkin_create_pkg floorpack std_msgs rospy roscpp rosserial_python

$ cd ~/catkin_ws
$ catkin_make

$ . ~/catkin_ws/devel/setup.bash
```

Zum Einbinden der rosNodes muss folgende Dateistruktur aufgebaut werden: Die Ordner `scripts` und `launch` aus dem Repository an die entsprechenden Stellen kopieren.

## Package Struktur
<!-- prettier-ignore-start -->
    .
    |–– catkin_ws
        |
        |–– build
        |
        |–– devel
        |
        |–– src
            |–– CMakeLists.txt
            |–– floorpack
                |–– CMakeLists.txt
                |–– package.xml
                |
                |–– include
                |   |–– ...
                |
                |–– src
                |   |–– ...
                |
                |–– scripts
                |   |–– cruisecontrol_node.py
                |   |–– IMUprocess_node.py
                |   |–– IMUsend_node.py
                |   |–– mpu9250_i2c.py
                |
                |–– launch
                    |– floorpack.launch
                

<!-- prettier-ignore-end -->

Die Python Skripts (NUR die _node.py Dateien) werden mit `chmod +x <filename.py>` ausführbar gemacht. 
```
$ cd ~/catkin_ws/src/floorpack/scripts
$ ls

$ chmod +x cruisecontrol_node.py IMUprocess_node.py IMUsend_node.py
$ ls
```
Die gelisteten Dateien die ausführbar gemacht wurden erscheinen jetzt in einer anderen Textfarbe.

## 2.1 setup.bash Dateien sourcen

Für einen einwandfreien Ablauf und für die Auführung der launch files müssen die setup.bash Dateien gesourcet werden.

Im Verzeichnis `/home/<your-username>/` liegt die `.bashrc` Datei. In dieser müssen die beiden folgenden Zeilen vorhanden sein:

```bash
source /opt/ros/melodic/setup.bash
source ~/catkin_ws/devel/setup.bash
```

# 3. Installation von rosserial auf dem PI

```
sudo apt-get install ros-indigo-rosserial-arduino
sudo apt-get install ros-indigo-rosserial
```
# 4. Einschalten des I2C Bus
Hierfür muss die Datei `/etc/udev/rules.d/99-com.rules` edetiert werden. 

In der die Datei folgende Zeile edetieren:
```bash
SUBSYSTEM=="ic2-dev", GROUP="i2c", MODE="0660"
```
MODE muss zu "0666" geändert werden.

Sollte die Datei nicht bestehen, muss diese erstellt werden und die Zeile hinzugefügt werden. Auf `MODE="0666"` und das "==" achten!

(Nicht empfohlen) Temporär lässt sich der Bus mittels folgendem Kommando einschalten:
```
sudo chmod a+rw /dev/i2c-*
```
# 5. Installation von Python Package smbus
Damit die IMU ausgelesen werden kann wird das [Python Package](https://pypi.org/project/smbus/) smbus benötigt.

```
pip install smbus 
```

# 6. Starten der nodes bei Systemstart konfigurieren

Es muss als erstes das Paket `robot_upstart` installiert werden.
```
$ sudo apt-get install ros-melodic-robot-upstart
```
Als nächstes wird alles konfiguriert. 
```
$ rosrun robot_upstart install floorpack/launch/floorpack.launch
```
Der Output sollte so aussehen:
```
$ rosrun robot_upstart install floorpack/launch/floorpack.launch
/lib/systemd/systemd
Preparing to install files to the following paths:
  /etc/ros/melodic/floorpack.d/.installed_files
  /etc/ros/melodic/floorpack.d/floorpack.launch
  /etc/systemd/system/multi-user.target.wants/floorpack.service
  /lib/systemd/system/floorpack.service
  /usr/sbin/floorpack-start
  /usr/sbin/floorpack-stop
Now calling: /usr/bin/sudo /opt/ros/melodic/lib/robot_upstart/mutate_files
Filesystem operation succeeded.
** To complete installation please run the following command:
 sudo systemctl daemon-reload && sudo systemctl start floorpack
```
Als nächstes die beiden Anweisungen ausführen.
```
$ sudo systemctl daemon-reload
$ sudo systemctl start floorpack
```
## 6.1 Testen
Man muss den PC nicht jedesmal neustarten. Getestet werden kann folgendermaßen:
```
$ sudo systemctl start floorpack.service
$ rosnode list 
/cruisecontrol_node
/IMUprocess_node
/IMUsend_node
/serial_node
/rosout

...
$ sudo systemctl stop floorpack.service
$ rosnode list 
ERROR: Unable to communicate with master!
```
## 6.2 Ein- und Ausschalten des automatischen Starts
Ausschalten:
```sudo systemctl disable floorpack.service```

Einschalten:
```sudo systemctl enable floorpack.service```

## 6.3 Komplettes deinstallieren der Konfiguration
```$ rosrun robot_upstart uninstall floorpack```

Weitere Infos zu `robot_upstart` [hier](https://roboticsbackend.com/make-ros-launch-start-on-boot-with-robot_upstart/).

# 7. Autostart Konfiguration
Bis hierher sollte alles funktionieren nachdem man sich auf dem Desktop eingeloggt hat. (Vorausgesetzt man nutzt einen Desktop...)
Damit das ganze System auch ohne Tastatur und Bildschirm funktionier muss der automatische Login aktiviert werden.

## 7.1 Als erstes den Desktop deaktivieren.
```
systemctl enable,disable <YOUR_DESKTOP_MANAGER>
```
In unserem Fall `lightdm`

Zum aktivieren:
```
service  <YOUR_DESKTOP_MANAGER> start,stop
```
In unserem Fall `lightdm`

## 7.2 Autologin konfigurieren
```
sudo systemctl edit getty@tty1.service
```
Das erstellt eine Datei, wenn nicht schon vorhanden. Diese Zeilen hinzufügen:
```bash
[Service]
ExecStart=
ExecStart=-/sbin/agetty --noissue --autologin myusername %I $TERM
Type=idle
```
Jetzt startet das System **ohne** grafische Benutzeroberfläche!

[Quelle Autologin](https://itectec.com/ubuntu/ubuntu-how-to-get-autologin-at-startup-working-on-ubuntu-server-16-04-1/)

# 8. Automount konfigurieren
Da es sich um ein Server Image ohne Desktop handelt werden USB-Geräte nicht automatisch ins Dateisystem eingefügt. Die Anleitung [hier](https://wiki.ubuntuusers.de/USB-Datentr%C3%A4ger_automatisch_einbinden/) durcharbeiten um dies zu ändern. (Stichwort: autofs) 

Jetzt sollte der USB-Stick mit unter dem Pfad `/automnt/usb-stick/<filename.csv>` verfügbar sein.
