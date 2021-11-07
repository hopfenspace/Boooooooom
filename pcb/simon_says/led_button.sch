EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 2
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L power:+3.3V #PWR?
U 1 1 618D1C8A
P 3050 1000
F 0 "#PWR?" H 3050 850 50  0001 C CNN
F 1 "+3.3V" H 3065 1173 50  0000 C CNN
F 2 "" H 3050 1000 50  0001 C CNN
F 3 "" H 3050 1000 50  0001 C CNN
	1    3050 1000
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR?
U 1 1 618D2A15
P 1250 1000
F 0 "#PWR?" H 1250 850 50  0001 C CNN
F 1 "+12V" H 1265 1173 50  0000 C CNN
F 2 "" H 1250 1000 50  0001 C CNN
F 3 "" H 1250 1000 50  0001 C CNN
	1    1250 1000
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Female J?
U 1 1 618D15B3
P 2300 800
F 0 "J?" V 2146 948 50  0000 L CNN
F 1 "Conn_01x04_Female" V 2237 948 50  0000 L CNN
F 2 "" H 2300 800 50  0001 C CNN
F 3 "~" H 2300 800 50  0001 C CNN
	1    2300 800 
	0    -1   -1   0   
$EndComp
Text Notes 2200 800  0    50   ~ 0
LED_RED
$Comp
L Transistor_FET:AO3400A Q?
U 1 1 618E6C80
P 1950 1450
F 0 "Q?" H 2155 1496 50  0000 L CNN
F 1 "AO3400A" H 2155 1405 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 2150 1375 50  0001 L CIN
F 3 "http://www.aosmd.com/pdfs/datasheet/AO3400A.pdf" H 1950 1450 50  0001 L CNN
	1    1950 1450
	1    0    0    -1  
$EndComp
Wire Wire Line
	1700 1450 1750 1450
$Comp
L Device:R R?
U 1 1 618FA917
P 1550 1450
F 0 "R?" V 1343 1450 50  0000 C CNN
F 1 "330" V 1434 1450 50  0000 C CNN
F 2 "" V 1480 1450 50  0001 C CNN
F 3 "~" H 1550 1450 50  0001 C CNN
	1    1550 1450
	0    1    1    0   
$EndComp
Wire Wire Line
	2500 1000 3050 1000
$Comp
L power:GND #PWR?
U 1 1 619C344C
P 2050 1800
F 0 "#PWR?" H 2050 1550 50  0001 C CNN
F 1 "GND" H 2055 1627 50  0000 C CNN
F 2 "" H 2050 1800 50  0001 C CNN
F 3 "" H 2050 1800 50  0001 C CNN
	1    2050 1800
	1    0    0    -1  
$EndComp
Wire Wire Line
	2050 1800 2050 1650
Wire Wire Line
	1250 1000 2200 1000
Wire Wire Line
	2050 1250 2050 1150
Wire Wire Line
	2300 1150 2300 1000
Wire Wire Line
	2050 1150 2300 1150
$Comp
L Device:R R?
U 1 1 6194F8D4
P 3300 1550
F 0 "R?" H 3370 1596 50  0000 L CNN
F 1 "18000" H 3370 1505 50  0000 L CNN
F 2 "" V 3230 1550 50  0001 C CNN
F 3 "~" H 3300 1550 50  0001 C CNN
	1    3300 1550
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 61936D90
P 2550 1300
F 0 "R?" V 2343 1300 50  0000 C CNN
F 1 "200" V 2434 1300 50  0000 C CNN
F 2 "" V 2480 1300 50  0001 C CNN
F 3 "~" H 2550 1300 50  0001 C CNN
	1    2550 1300
	0    1    1    0   
$EndComp
Wire Wire Line
	2400 1000 2400 1300
Wire Wire Line
	3300 1300 3300 1400
Wire Wire Line
	3300 1700 3300 1800
Wire Wire Line
	3300 1800 3050 1800
Wire Wire Line
	2800 1800 2800 1700
$Comp
L Device:C C?
U 1 1 61951252
P 2800 1550
F 0 "C?" H 2915 1596 50  0000 L CNN
F 1 "190nF" H 2915 1505 50  0000 L CNN
F 2 "" H 2838 1400 50  0001 C CNN
F 3 "~" H 2800 1550 50  0001 C CNN
	1    2800 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	2700 1300 2800 1300
Wire Wire Line
	2800 1400 2800 1300
Connection ~ 2800 1300
Wire Wire Line
	2800 1300 3300 1300
$Comp
L power:GND #PWR?
U 1 1 61A2553D
P 3050 1800
F 0 "#PWR?" H 3050 1550 50  0001 C CNN
F 1 "GND" H 3055 1627 50  0000 C CNN
F 2 "" H 3050 1800 50  0001 C CNN
F 3 "" H 3050 1800 50  0001 C CNN
	1    3050 1800
	1    0    0    -1  
$EndComp
Connection ~ 3050 1800
Wire Wire Line
	3050 1800 2800 1800
Wire Wire Line
	3300 1300 3500 1300
Connection ~ 3300 1300
Text HLabel 1300 1450 0    50   Input ~ 0
R_OUT
Text HLabel 3500 1300 2    50   Output ~ 0
R_IN
Wire Wire Line
	1300 1450 1400 1450
$Comp
L power:+3.3V #PWR?
U 1 1 61A8CC74
P 6050 1000
F 0 "#PWR?" H 6050 850 50  0001 C CNN
F 1 "+3.3V" H 6065 1173 50  0000 C CNN
F 2 "" H 6050 1000 50  0001 C CNN
F 3 "" H 6050 1000 50  0001 C CNN
	1    6050 1000
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR?
U 1 1 61A8CC7A
P 4250 1000
F 0 "#PWR?" H 4250 850 50  0001 C CNN
F 1 "+12V" H 4265 1173 50  0000 C CNN
F 2 "" H 4250 1000 50  0001 C CNN
F 3 "" H 4250 1000 50  0001 C CNN
	1    4250 1000
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Female J?
U 1 1 61A8CC80
P 5300 800
F 0 "J?" V 5146 948 50  0000 L CNN
F 1 "Conn_01x04_Female" V 5237 948 50  0000 L CNN
F 2 "" H 5300 800 50  0001 C CNN
F 3 "~" H 5300 800 50  0001 C CNN
	1    5300 800 
	0    -1   -1   0   
$EndComp
Text Notes 5150 800  0    50   ~ 0
LED_YELLOW
$Comp
L Transistor_FET:AO3400A Q?
U 1 1 61A8CC87
P 4950 1450
F 0 "Q?" H 5155 1496 50  0000 L CNN
F 1 "AO3400A" H 5155 1405 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 5150 1375 50  0001 L CIN
F 3 "http://www.aosmd.com/pdfs/datasheet/AO3400A.pdf" H 4950 1450 50  0001 L CNN
	1    4950 1450
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 1450 4750 1450
$Comp
L Device:R R?
U 1 1 61A8CC8E
P 4550 1450
F 0 "R?" V 4343 1450 50  0000 C CNN
F 1 "330" V 4434 1450 50  0000 C CNN
F 2 "" V 4480 1450 50  0001 C CNN
F 3 "~" H 4550 1450 50  0001 C CNN
	1    4550 1450
	0    1    1    0   
$EndComp
Wire Wire Line
	5500 1000 6050 1000
$Comp
L power:GND #PWR?
U 1 1 61A8CC95
P 5050 1800
F 0 "#PWR?" H 5050 1550 50  0001 C CNN
F 1 "GND" H 5055 1627 50  0000 C CNN
F 2 "" H 5050 1800 50  0001 C CNN
F 3 "" H 5050 1800 50  0001 C CNN
	1    5050 1800
	1    0    0    -1  
$EndComp
Wire Wire Line
	5050 1800 5050 1650
Wire Wire Line
	4250 1000 5200 1000
Wire Wire Line
	5050 1250 5050 1150
Wire Wire Line
	5300 1150 5300 1000
Wire Wire Line
	5050 1150 5300 1150
$Comp
L Device:R R?
U 1 1 61A8CCA0
P 6300 1550
F 0 "R?" H 6370 1596 50  0000 L CNN
F 1 "18000" H 6370 1505 50  0000 L CNN
F 2 "" V 6230 1550 50  0001 C CNN
F 3 "~" H 6300 1550 50  0001 C CNN
	1    6300 1550
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 61A8CCA6
P 5550 1300
F 0 "R?" V 5343 1300 50  0000 C CNN
F 1 "200" V 5434 1300 50  0000 C CNN
F 2 "" V 5480 1300 50  0001 C CNN
F 3 "~" H 5550 1300 50  0001 C CNN
	1    5550 1300
	0    1    1    0   
$EndComp
Wire Wire Line
	5400 1000 5400 1300
Wire Wire Line
	6300 1300 6300 1400
Wire Wire Line
	6300 1700 6300 1800
Wire Wire Line
	6300 1800 6050 1800
Wire Wire Line
	5800 1800 5800 1700
$Comp
L Device:C C?
U 1 1 61A8CCB1
P 5800 1550
F 0 "C?" H 5915 1596 50  0000 L CNN
F 1 "190nF" H 5915 1505 50  0000 L CNN
F 2 "" H 5838 1400 50  0001 C CNN
F 3 "~" H 5800 1550 50  0001 C CNN
	1    5800 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	5700 1300 5800 1300
Wire Wire Line
	5800 1400 5800 1300
Connection ~ 5800 1300
Wire Wire Line
	5800 1300 6300 1300
$Comp
L power:GND #PWR?
U 1 1 61A8CCBB
P 6050 1800
F 0 "#PWR?" H 6050 1550 50  0001 C CNN
F 1 "GND" H 6055 1627 50  0000 C CNN
F 2 "" H 6050 1800 50  0001 C CNN
F 3 "" H 6050 1800 50  0001 C CNN
	1    6050 1800
	1    0    0    -1  
$EndComp
Connection ~ 6050 1800
Wire Wire Line
	6050 1800 5800 1800
Wire Wire Line
	6300 1300 6500 1300
Connection ~ 6300 1300
Text HLabel 4300 1450 0    50   Input ~ 0
Y_OUT
Text HLabel 6500 1300 2    50   Output ~ 0
Y_IN
Wire Wire Line
	4300 1450 4400 1450
$Comp
L power:+3.3V #PWR?
U 1 1 61AC3258
P 3050 2550
F 0 "#PWR?" H 3050 2400 50  0001 C CNN
F 1 "+3.3V" H 3065 2723 50  0000 C CNN
F 2 "" H 3050 2550 50  0001 C CNN
F 3 "" H 3050 2550 50  0001 C CNN
	1    3050 2550
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR?
U 1 1 61AC325E
P 1250 2550
F 0 "#PWR?" H 1250 2400 50  0001 C CNN
F 1 "+12V" H 1265 2723 50  0000 C CNN
F 2 "" H 1250 2550 50  0001 C CNN
F 3 "" H 1250 2550 50  0001 C CNN
	1    1250 2550
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Female J?
U 1 1 61AC3264
P 2300 2350
F 0 "J?" V 2146 2498 50  0000 L CNN
F 1 "Conn_01x04_Female" V 2237 2498 50  0000 L CNN
F 2 "" H 2300 2350 50  0001 C CNN
F 3 "~" H 2300 2350 50  0001 C CNN
	1    2300 2350
	0    -1   -1   0   
$EndComp
Text Notes 2200 2350 0    50   ~ 0
LED_BLUE
$Comp
L Transistor_FET:AO3400A Q?
U 1 1 61AC326B
P 1950 3000
F 0 "Q?" H 2155 3046 50  0000 L CNN
F 1 "AO3400A" H 2155 2955 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 2150 2925 50  0001 L CIN
F 3 "http://www.aosmd.com/pdfs/datasheet/AO3400A.pdf" H 1950 3000 50  0001 L CNN
	1    1950 3000
	1    0    0    -1  
$EndComp
Wire Wire Line
	1700 3000 1750 3000
$Comp
L Device:R R?
U 1 1 61AC3272
P 1550 3000
F 0 "R?" V 1343 3000 50  0000 C CNN
F 1 "330" V 1434 3000 50  0000 C CNN
F 2 "" V 1480 3000 50  0001 C CNN
F 3 "~" H 1550 3000 50  0001 C CNN
	1    1550 3000
	0    1    1    0   
$EndComp
Wire Wire Line
	2500 2550 3050 2550
$Comp
L power:GND #PWR?
U 1 1 61AC3279
P 2050 3350
F 0 "#PWR?" H 2050 3100 50  0001 C CNN
F 1 "GND" H 2055 3177 50  0000 C CNN
F 2 "" H 2050 3350 50  0001 C CNN
F 3 "" H 2050 3350 50  0001 C CNN
	1    2050 3350
	1    0    0    -1  
$EndComp
Wire Wire Line
	2050 3350 2050 3200
Wire Wire Line
	1250 2550 2200 2550
Wire Wire Line
	2050 2800 2050 2700
Wire Wire Line
	2300 2700 2300 2550
Wire Wire Line
	2050 2700 2300 2700
$Comp
L Device:R R?
U 1 1 61AC3284
P 3300 3100
F 0 "R?" H 3370 3146 50  0000 L CNN
F 1 "18000" H 3370 3055 50  0000 L CNN
F 2 "" V 3230 3100 50  0001 C CNN
F 3 "~" H 3300 3100 50  0001 C CNN
	1    3300 3100
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 61AC328A
P 2550 2850
F 0 "R?" V 2343 2850 50  0000 C CNN
F 1 "200" V 2434 2850 50  0000 C CNN
F 2 "" V 2480 2850 50  0001 C CNN
F 3 "~" H 2550 2850 50  0001 C CNN
	1    2550 2850
	0    1    1    0   
$EndComp
Wire Wire Line
	2400 2550 2400 2850
Wire Wire Line
	3300 2850 3300 2950
Wire Wire Line
	3300 3250 3300 3350
Wire Wire Line
	3300 3350 3050 3350
Wire Wire Line
	2800 3350 2800 3250
$Comp
L Device:C C?
U 1 1 61AC3295
P 2800 3100
F 0 "C?" H 2915 3146 50  0000 L CNN
F 1 "190nF" H 2915 3055 50  0000 L CNN
F 2 "" H 2838 2950 50  0001 C CNN
F 3 "~" H 2800 3100 50  0001 C CNN
	1    2800 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	2700 2850 2800 2850
Wire Wire Line
	2800 2950 2800 2850
Connection ~ 2800 2850
Wire Wire Line
	2800 2850 3300 2850
$Comp
L power:GND #PWR?
U 1 1 61AC329F
P 3050 3350
F 0 "#PWR?" H 3050 3100 50  0001 C CNN
F 1 "GND" H 3055 3177 50  0000 C CNN
F 2 "" H 3050 3350 50  0001 C CNN
F 3 "" H 3050 3350 50  0001 C CNN
	1    3050 3350
	1    0    0    -1  
$EndComp
Connection ~ 3050 3350
Wire Wire Line
	3050 3350 2800 3350
Wire Wire Line
	3300 2850 3500 2850
Connection ~ 3300 2850
Text HLabel 1300 3000 0    50   Input ~ 0
B_OUT
Text HLabel 3500 2850 2    50   Output ~ 0
B_IN
Wire Wire Line
	1300 3000 1400 3000
$Comp
L power:+3.3V #PWR?
U 1 1 61AD1F33
P 6050 2550
F 0 "#PWR?" H 6050 2400 50  0001 C CNN
F 1 "+3.3V" H 6065 2723 50  0000 C CNN
F 2 "" H 6050 2550 50  0001 C CNN
F 3 "" H 6050 2550 50  0001 C CNN
	1    6050 2550
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR?
U 1 1 61AD1F39
P 4250 2550
F 0 "#PWR?" H 4250 2400 50  0001 C CNN
F 1 "+12V" H 4265 2723 50  0000 C CNN
F 2 "" H 4250 2550 50  0001 C CNN
F 3 "" H 4250 2550 50  0001 C CNN
	1    4250 2550
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Female J?
U 1 1 61AD1F3F
P 5300 2350
F 0 "J?" V 5146 2498 50  0000 L CNN
F 1 "Conn_01x04_Female" V 5237 2498 50  0000 L CNN
F 2 "" H 5300 2350 50  0001 C CNN
F 3 "~" H 5300 2350 50  0001 C CNN
	1    5300 2350
	0    -1   -1   0   
$EndComp
Text Notes 5150 2350 0    50   ~ 0
LED_GREEN
$Comp
L Transistor_FET:AO3400A Q?
U 1 1 61AD1F46
P 4950 3000
F 0 "Q?" H 5155 3046 50  0000 L CNN
F 1 "AO3400A" H 5155 2955 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 5150 2925 50  0001 L CIN
F 3 "http://www.aosmd.com/pdfs/datasheet/AO3400A.pdf" H 4950 3000 50  0001 L CNN
	1    4950 3000
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 3000 4750 3000
$Comp
L Device:R R?
U 1 1 61AD1F4D
P 4550 3000
F 0 "R?" V 4343 3000 50  0000 C CNN
F 1 "330" V 4434 3000 50  0000 C CNN
F 2 "" V 4480 3000 50  0001 C CNN
F 3 "~" H 4550 3000 50  0001 C CNN
	1    4550 3000
	0    1    1    0   
$EndComp
Wire Wire Line
	5500 2550 6050 2550
$Comp
L power:GND #PWR?
U 1 1 61AD1F54
P 5050 3350
F 0 "#PWR?" H 5050 3100 50  0001 C CNN
F 1 "GND" H 5055 3177 50  0000 C CNN
F 2 "" H 5050 3350 50  0001 C CNN
F 3 "" H 5050 3350 50  0001 C CNN
	1    5050 3350
	1    0    0    -1  
$EndComp
Wire Wire Line
	5050 3350 5050 3200
Wire Wire Line
	4250 2550 5200 2550
Wire Wire Line
	5050 2800 5050 2700
Wire Wire Line
	5300 2700 5300 2550
Wire Wire Line
	5050 2700 5300 2700
$Comp
L Device:R R?
U 1 1 61AD1F5F
P 6300 3100
F 0 "R?" H 6370 3146 50  0000 L CNN
F 1 "18000" H 6370 3055 50  0000 L CNN
F 2 "" V 6230 3100 50  0001 C CNN
F 3 "~" H 6300 3100 50  0001 C CNN
	1    6300 3100
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 61AD1F65
P 5550 2850
F 0 "R?" V 5343 2850 50  0000 C CNN
F 1 "200" V 5434 2850 50  0000 C CNN
F 2 "" V 5480 2850 50  0001 C CNN
F 3 "~" H 5550 2850 50  0001 C CNN
	1    5550 2850
	0    1    1    0   
$EndComp
Wire Wire Line
	5400 2550 5400 2850
Wire Wire Line
	6300 2850 6300 2950
Wire Wire Line
	6300 3250 6300 3350
Wire Wire Line
	6300 3350 6050 3350
Wire Wire Line
	5800 3350 5800 3250
$Comp
L Device:C C?
U 1 1 61AD1F70
P 5800 3100
F 0 "C?" H 5915 3146 50  0000 L CNN
F 1 "190nF" H 5915 3055 50  0000 L CNN
F 2 "" H 5838 2950 50  0001 C CNN
F 3 "~" H 5800 3100 50  0001 C CNN
	1    5800 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	5700 2850 5800 2850
Wire Wire Line
	5800 2950 5800 2850
Connection ~ 5800 2850
Wire Wire Line
	5800 2850 6300 2850
$Comp
L power:GND #PWR?
U 1 1 61AD1F7A
P 6050 3350
F 0 "#PWR?" H 6050 3100 50  0001 C CNN
F 1 "GND" H 6055 3177 50  0000 C CNN
F 2 "" H 6050 3350 50  0001 C CNN
F 3 "" H 6050 3350 50  0001 C CNN
	1    6050 3350
	1    0    0    -1  
$EndComp
Connection ~ 6050 3350
Wire Wire Line
	6050 3350 5800 3350
Wire Wire Line
	6300 2850 6500 2850
Connection ~ 6300 2850
Text HLabel 4300 3000 0    50   Input ~ 0
G_OUT
Text HLabel 6500 2850 2    50   Output ~ 0
G_IN
Wire Wire Line
	4300 3000 4400 3000
$EndSCHEMATC
