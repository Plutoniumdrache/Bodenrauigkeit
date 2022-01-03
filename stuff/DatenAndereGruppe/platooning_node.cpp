#include <ros/ros.h>
#include <sensor_msgs/Joy.h>
#include <std_msgs/String.h>
#include <sensor_msgs/LaserScan.h>
#include <std_msgs/Int16MultiArray.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <unistd.h>

#define A   0
#define B   1
#define X   2
#define Y   3
#define pi  3.141592653

using namespace std;

//Zustands Enum
enum states{ Init, Bereit, Manuell, Ausscheren0,Ausscheren1,Ausscheren2,Ausscheren3, Automatik};

//Globale Variablen deklarieren und initialisieren
short lenkwinkel = 90;
short geschwindigkeit = 90;
int state = 0;
int button[4] = {0};
float achsen[3] = {0.0};
int ausscheren0_fertig = 0;
int ausscheren1_fertig = 0;
int ausscheren2_fertig = 0;
int ausscheren3_fertig = 0;
float winkel_array[360] = {0.0};
float abstand_array[360] = {0.0};

//Variablen Automatic Betrieb
float kleinsterAbstand = 1.5;
float Abstand_neu = 0;
float Abstand_alt = 0;
short Vdiv = 0;
short Vneu = 101;
short Valt = 101;
short kleinsterAbstandWinkel = 90;
short Winkeldiv = 0;
short minWinkel = 149;
short maxWinkel = 209;
short aktuellWinkel = 179;

//Ausscheren
bool state_1 = false;
bool state_2 = false;
bool state_3 = false;
bool state_4 = false;
bool wirsinddran = false;
float Abstand_wsd = 1.0;

//Funktionen deklarieren
void evalEvents(void);
void evalStates(void);
void joy_cb(const sensor_msgs::Joy::ConstPtr& joy);
void LIDAR_cb(const sensor_msgs::LaserScanConstPtr& msg);


void joy_cb(const sensor_msgs::Joy::ConstPtr& joy){

    button[0] = joy->buttons[0];   //In Bereit (A)
    button[1] = joy->buttons[1];   //In Manuell (B)
    button[2] = joy->buttons[2];   //In Automatik (X)
    button[3] = joy->buttons[3];   //In Ausscheren (Y)
    achsen[0] = joy->axes[0];   //Lenkung
    achsen[1] = joy->axes[5];   //geschwindigkeit vorwärts
    achsen[2] = joy->axes[2];   //geschwindigkeit rückwers

    ROS_INFO("joy_cb test!");

}

void LIDAR_cb(const sensor_msgs::LaserScanConstPtr& msg){
    for(int i = 0;i < 360;i++){
        abstand_array[i] = msg->ranges[i];
        winkel_array[i] = (msg->angle_min + msg->angle_increment*i)*180/pi;
    }

}

int main(int argc, char **argv){
  // Ros Node Aktivieren
  ros::init(argc, argv, "platooning_node");
  ros::NodeHandle nh;

  // Subscriber Joy node erstellen
  ros::Subscriber sub_joy = nh.subscribe<sensor_msgs::Joy>("joy", 10, &joy_cb);

  // Subscriber LaserSan erstellen
  ros::Subscriber sub_LIDAR = nh.subscribe<sensor_msgs::LaserScan>("scan", 1, &LIDAR_cb);

  // Publisher erstellen
  ros::Publisher pub_fahrwerte = nh.advertise<std_msgs::Int16MultiArray>("fahrwerte", 2);

  std_msgs::Int16MultiArray fahrwerte_array;
  ros::Rate r(8);

  ROS_INFO("Main");


  while(ros::ok()){
    r.sleep();
    ros::spinOnce();
    evalEvents();
    evalStates();
    fahrwerte_array.data = {lenkwinkel,geschwindigkeit};
    pub_fahrwerte.publish(fahrwerte_array);

  }
  return 0;

}


void evalEvents(){
    switch(state){
        case Init:
            if(button[A] == 1){
                state = Bereit;
            }
            break;

        case Bereit:
            if(button[B] == 1){
                state = Manuell;
            }
            if(button[Y] == 1){
                state = Ausscheren0;
            }
            if(button[X] == 1){
                state = Automatik;

            }
            break;

        case Manuell:
            if(button[A] == 1){
                state = Bereit;
            }
            break;

        case Ausscheren0:
            if(ausscheren0_fertig == 1){
                state = Ausscheren1;
            }
            if(button[A] == 1){
                state = Bereit;
            }
            break;

        case Ausscheren1:
            if(ausscheren1_fertig == 1){
                state = Ausscheren2;
            }
            if(button[A] == 1){
                state = Bereit;
            }
            break;

        case Ausscheren2:
            if(ausscheren2_fertig == 1){
                state = Ausscheren3;
            }
            if(button[A] == 1){
                state = Bereit;
            }
            break;

        case Ausscheren3:
            if(ausscheren3_fertig == 1){
                state = Automatik;
            }
            if(button[A] == 1){
                state = Bereit;
            }
            break;

        case Automatik:
            if(button[A] == 1){
                state = Bereit;
            }
            break;
    }

}

void evalStates(){
    switch(state){
        case Init:
            ROS_INFO("Init");
            break;

        case Bereit:
            ROS_INFO("Bereit");
            geschwindigkeit = 90;
            Vneu = 90;
            lenkwinkel = 90;
            state_1 = false;
            state_2 = false;
            state_3 = false;
            state_4 = false;
            wirsinddran = false;
            Abstand_wsd = 1.0;
            ausscheren0_fertig = 0;
            ausscheren1_fertig = 0;
            ausscheren2_fertig = 0;
            break;

        case Manuell:
            ROS_INFO("Manuell");
            lenkwinkel = short(-29 * achsen[0] + 95);
            geschwindigkeit = short((-22.5 * achsen[1] + 112.5));
            if((achsen[1] == 1.0) && (achsen[2] <= 1.0)){
                geschwindigkeit = short(22.5 * achsen[2] + 67.5);
            }

            ROS_INFO("geschwindigkeit: %d",geschwindigkeit);
            break;

        case Ausscheren0:
            ROS_INFO("Ausscheren0");

            Abstand_wsd = 1.0;

            for(int j=0; j<21; j++){
                if(abstand_array[j] < Abstand_wsd){
                    Abstand_wsd = abstand_array[j];
                }
            }

            for(int j=340; j<360; j++){
                if(abstand_array[j] < Abstand_wsd){
                    Abstand_wsd = abstand_array[j];
                }
            }

            if(Abstand_wsd > 0.8)
                wirsinddran = true;


            if(wirsinddran){
                for(int j=291; j<315; j++ ){
                    if((abstand_array[j] > 0.2) && (abstand_array[j] < 0.5))
                        state_1 = true;
                }
                for(int j=269; j<291; j++ ){
                    if((abstand_array[j] > 0.2) && (abstand_array[j] < 0.5) && (state_1))
                        state_2 = true;
                }
                for(int j=246; j<269; j++ ){
                    if((abstand_array[j] > 0.2) && (abstand_array[j] < 0.5) && (state_2))
                        state_3 = true;
                }
                for(int j=224; j<246; j++ ){
                    if((abstand_array[j] > 0.2) && (abstand_array[j] < 0.5) && (state_3))
                        state_4 = true;
                }
            }
            if(state_4){ //jetzt können wir losfahren
                ROS_INFO("Los fahren !!");
                 lenkwinkel = 66;
                geschwindigkeit = 105;
                ausscheren0_fertig = 1;

            }
            ROS_INFO("Wir sind dran: %d",wirsinddran);
            ROS_INFO("Bereich 1: %d",state_1);
            ROS_INFO("Bereich 2: %d",state_2);
            ROS_INFO("Bereich 3: %d",state_3);
            ROS_INFO("Bereich 4: %d",state_4);
            break;

        case Ausscheren1:
            usleep(900000);
            lenkwinkel = 90;
            geschwindigkeit = 106;
            ausscheren1_fertig = 1;
            break;

        case Ausscheren2:
            usleep(600000);
            lenkwinkel = 124;
            geschwindigkeit = 105;
            ausscheren2_fertig = 1;
            break;

        case Ausscheren3:
            ROS_INFO("START Links fahren");
            usleep(900000);
            ROS_INFO("STOPP Links fahren");
            ausscheren3_fertig = 1;
            Valt = 105;
            break;

        case Automatik:
            ROS_INFO("Automatik");

            kleinsterAbstand = 2;

            for(int i = minWinkel; i < maxWinkel; i++){         // Absuchen in einem Kegel von 60° nach vorne
                if((abstand_array[i] <= 2) && (abstand_array[i] < kleinsterAbstand)){
                    kleinsterAbstand = abstand_array[i];
                    kleinsterAbstandWinkel = i- 89;
                    aktuellWinkel = i;

                }
            }

            minWinkel = aktuellWinkel -15;
            maxWinkel = aktuellWinkel +15;

            if(kleinsterAbstand >= 2){
                minWinkel = 149;
                maxWinkel = 209;
            }


                //Abstand_neu aus dem LIDAR in cm umnrechnen
            Abstand_neu = round(kleinsterAbstand*100);
            if ((Abstand_neu - Abstand_alt >= 0) && (Vneu <135) && (Abstand_neu > 40)){
                /*if (Abstand_neu > 40)
                    Vdiv = short(0.28125 * Abstand_neu -11.25);
                else
                    Vdiv = short(-0.28125 * Abstand_neu +11.25);//Fallend (bremsen)
                    */
                    if(Abstand_neu > 65)
                        Vdiv = 1;

                    else
                        Vdiv = 1;
            } //Steigend (beschleunigen)
            if ((Abstand_neu - Abstand_alt < 0) && (Vneu > 101)){
                /*if (Abstand_neu > 40)
                    Vdiv = short(-0.28125 * Abstand_neu +11.25);
                else
                    Vdiv = short(0.28125 * Abstand_neu -11.25);//Fallend (bremsen)
                    */
                    if(Abstand_neu - Abstand_alt < -8)
                        Vdiv = -10;

                    if(Abstand_neu < 40)
                        Vdiv = -10;

                    else
                        Vdiv = -1;
            }
            if ((Abstand_neu - Abstand_alt == 0) && (Abstand_neu < 45))
                Vdiv = 0;

            Vneu = short(Valt + Vdiv);
            Valt = Vneu;
            Vdiv = 0;
            Abstand_alt = Abstand_neu;

            if ((Abstand_neu < 25) || (Vneu  < 101))
                Vneu = 101;
            // Vneu publishen
            geschwindigkeit = Vneu;

            //Lenkung

            lenkwinkel = kleinsterAbstandWinkel*(-1)+180;
            if(lenkwinkel > 114)
                lenkwinkel = 114;
            if(lenkwinkel < 66)
                lenkwinkel = 66;

            ROS_INFO("geschwindigkeit: %d",Vneu);
            ROS_INFO("lenkwinkel: %d",lenkwinkel);
            ROS_INFO("minWinkel: %d",minWinkel);
            ROS_INFO("maxWinkel: %d",maxWinkel);

            ROS_INFO("Aktueller Abstand: %f",Abstand_neu);
            break;
    }
}
