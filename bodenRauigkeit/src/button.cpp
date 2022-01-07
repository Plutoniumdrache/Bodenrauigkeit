#include "button.h"

button::button()
{

}

/* Refer to the pin which is connected to the pushbutton */
void button::initializeButton(int pinNumber)
{
    this->pinNumber = pinNumber;
    pinMode(pinNumber, INPUT_PULLUP); //define as INPUT_PULLUP
    // INPUT_PULLUP: No external pullup or pulldown resistor needed
}

button::~button()
{
}
/* if the button is pressed the method returns true,
otherwise false */
bool button::isButtonPressed()
{
    bool read = digitalRead(pinNumber); // reading the state of the button

    // If the button has changed, due to noise or pressing: 
    if (read != lastButtonState)
    {
        lastDebounceTime = millis(); // reset the debouncing timer
    }

    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:
    if((millis() - lastDebounceTime) > debounceDelay)
    {
        // if the buttonState has changed:
        if (read != buttonState)
        {
            buttonState = read; // Assign the read buttonstate 
            
            // Return true if the buttonstate is HIGH:
            if(HIGH == buttonState)
            {
                return true;
            }
        }
    }
    // remember the buttonstate for the next time checking
    lastButtonState = read;
    
    // Return false if the button was not pressed:
    return false;
}