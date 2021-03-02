# HxStompMidiFootPedal

## Introduction
The [Line 6 HX Stomp](https://line6.com/hx-stomp/) is a compact yet powerful amp and effects modeler.  In addition to it's modeling features it is also a powerful and felxible midi dveice.  The HX Stomp has the ability to offer expanded parameter control using midi input.  There are a number of popular commercial midi foot controllers on the market that are frequently used along side the HX Stomp.  This project's aim is to offer a low cost open source alternative to such devices using easily obtainable parts.

## Parts List
1. [Project Enclosure](https://www.radioshack.com/products/radioshack-project-enclosure-6x4x2?_pos=5&_sid=c6f24d49a&_ss=r)
2. [6" Male/Male jumper wires.](https://www.adafruit.com/product/1957)
3. [Arduino Uno R3](https://store.arduino.cc/usa/arduino-uno-rev3) or similar. 
4. [Midi Breakout Board](http://ubld.it/products/midi-breakout-board-ez/)
5. [Momentary SPST Stomp Switches](https://www.amazon.com/gp/product/B076V2QYSJ/ref=ppx_yo_dt_b_asin_title_o02_s01?ie=UTF8&psc=1)
6. Diagonal cutters
7. Wire stripper
8. Soldering iron
9. Hookup wire

## Overview
The arduino circuit is about as simple as it gets.  One leg of each switch is connected to a digital input of the arduino, the other legs are connected to the arduino ground.  Since there is a limited number of ground connections on the arduino it is neccessary to daisy chain the pins on the swtiches using hookup wire and connceting them to a single ground input on the arduino.  The arduino's digital input pins will be configured to use the [internal pullup resistors.](https://www.arduino.cc/en/Tutorial/Foundations/DigitalPins#properties-of-pins-configured-as-input_pullup).  The initial prototype uses only the midi out of the breakout board.  Note:  if the midi in portion is used the serial connection over USB will not work correctly.

## Code
