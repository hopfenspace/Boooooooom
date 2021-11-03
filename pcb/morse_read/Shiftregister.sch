EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 3 5
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
L 74xx:74HC595 U?
U 1 1 618CB13F
P 2050 3900
AR Path="/618CB13F" Ref="U?"  Part="1" 
AR Path="/618C9959/618CB13F" Ref="U4"  Part="1" 
F 0 "U4" H 2050 4681 50  0000 C CNN
F 1 "74HC595" H 2050 4590 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 2050 3900 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/sn74hc595.pdf" H 2050 3900 50  0001 C CNN
	1    2050 3900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618CB145
P 2050 4600
AR Path="/618CB145" Ref="#PWR?"  Part="1" 
AR Path="/618C9959/618CB145" Ref="#PWR034"  Part="1" 
F 0 "#PWR034" H 2050 4350 50  0001 C CNN
F 1 "GND" H 2055 4427 50  0000 C CNN
F 2 "" H 2050 4600 50  0001 C CNN
F 3 "" H 2050 4600 50  0001 C CNN
	1    2050 4600
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR?
U 1 1 618CB14B
P 2050 3050
AR Path="/618CB14B" Ref="#PWR?"  Part="1" 
AR Path="/618C9959/618CB14B" Ref="#PWR033"  Part="1" 
F 0 "#PWR033" H 2050 2900 50  0001 C CNN
F 1 "+3.3V" H 2065 3223 50  0000 C CNN
F 2 "" H 2050 3050 50  0001 C CNN
F 3 "" H 2050 3050 50  0001 C CNN
	1    2050 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2050 3050 2050 3300
$Comp
L power:+3.3V #PWR032
U 1 1 618D55EC
P 1650 3800
F 0 "#PWR032" H 1650 3650 50  0001 C CNN
F 1 "+3.3V" V 1665 3928 50  0000 L CNN
F 2 "" H 1650 3800 50  0001 C CNN
F 3 "" H 1650 3800 50  0001 C CNN
	1    1650 3800
	0    -1   -1   0   
$EndComp
Text HLabel 1650 3700 0    47   Input ~ 0
SRCLK
$Comp
L 74xx:74HC595 U?
U 1 1 618D9F5C
P 9450 3900
AR Path="/618D9F5C" Ref="U?"  Part="1" 
AR Path="/618C9959/618D9F5C" Ref="U8"  Part="1" 
F 0 "U8" H 9450 4681 50  0000 C CNN
F 1 "74HC595" H 9450 4590 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 9450 3900 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/sn74hc595.pdf" H 9450 3900 50  0001 C CNN
	1    9450 3900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618D9F62
P 9450 4600
AR Path="/618D9F62" Ref="#PWR?"  Part="1" 
AR Path="/618C9959/618D9F62" Ref="#PWR043"  Part="1" 
F 0 "#PWR043" H 9450 4350 50  0001 C CNN
F 1 "GND" H 9455 4427 50  0000 C CNN
F 2 "" H 9450 4600 50  0001 C CNN
F 3 "" H 9450 4600 50  0001 C CNN
	1    9450 4600
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR?
U 1 1 618D9F68
P 9450 3050
AR Path="/618D9F68" Ref="#PWR?"  Part="1" 
AR Path="/618C9959/618D9F68" Ref="#PWR042"  Part="1" 
F 0 "#PWR042" H 9450 2900 50  0001 C CNN
F 1 "+3.3V" H 9465 3223 50  0000 C CNN
F 2 "" H 9450 3050 50  0001 C CNN
F 3 "" H 9450 3050 50  0001 C CNN
	1    9450 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	9450 3050 9450 3300
$Comp
L power:+3.3V #PWR041
U 1 1 618D9F6F
P 9050 3800
F 0 "#PWR041" H 9050 3650 50  0001 C CNN
F 1 "+3.3V" V 9065 3928 50  0000 L CNN
F 2 "" H 9050 3800 50  0001 C CNN
F 3 "" H 9050 3800 50  0001 C CNN
	1    9050 3800
	0    -1   -1   0   
$EndComp
Text HLabel 9050 3700 0    47   Input ~ 0
SRCLK
Text HLabel 1650 4000 0    47   Input ~ 0
RCLK
Text HLabel 9050 4000 0    47   Input ~ 0
RCLK
Text Notes 7000 700  2    47   ~ 0
7 Segment LED 1,8V 10mA\n
$Comp
L 74xx:74HC595 U?
U 1 1 618F286B
P 4750 3900
AR Path="/618F286B" Ref="U?"  Part="1" 
AR Path="/618C9959/618F286B" Ref="U5"  Part="1" 
F 0 "U5" H 4750 4681 50  0000 C CNN
F 1 "74HC595" H 4750 4590 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 4750 3900 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/sn74hc595.pdf" H 4750 3900 50  0001 C CNN
	1    4750 3900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618F2871
P 4750 4600
AR Path="/618F2871" Ref="#PWR?"  Part="1" 
AR Path="/618C9959/618F2871" Ref="#PWR037"  Part="1" 
F 0 "#PWR037" H 4750 4350 50  0001 C CNN
F 1 "GND" H 4755 4427 50  0000 C CNN
F 2 "" H 4750 4600 50  0001 C CNN
F 3 "" H 4750 4600 50  0001 C CNN
	1    4750 4600
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR?
U 1 1 618F2877
P 4750 3050
AR Path="/618F2877" Ref="#PWR?"  Part="1" 
AR Path="/618C9959/618F2877" Ref="#PWR036"  Part="1" 
F 0 "#PWR036" H 4750 2900 50  0001 C CNN
F 1 "+3.3V" H 4765 3223 50  0000 C CNN
F 2 "" H 4750 3050 50  0001 C CNN
F 3 "" H 4750 3050 50  0001 C CNN
	1    4750 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	4750 3050 4750 3300
$Comp
L power:+3.3V #PWR035
U 1 1 618F287E
P 4350 3800
F 0 "#PWR035" H 4350 3650 50  0001 C CNN
F 1 "+3.3V" V 4365 3928 50  0000 L CNN
F 2 "" H 4350 3800 50  0001 C CNN
F 3 "" H 4350 3800 50  0001 C CNN
	1    4350 3800
	0    -1   -1   0   
$EndComp
Text HLabel 4350 3700 0    47   Input ~ 0
SRCLK
Text HLabel 4350 4000 0    47   Input ~ 0
RCLK
$Comp
L 74xx:74HC595 U?
U 1 1 618F31AA
P 7150 3900
AR Path="/618F31AA" Ref="U?"  Part="1" 
AR Path="/618C9959/618F31AA" Ref="U7"  Part="1" 
F 0 "U7" H 7150 4681 50  0000 C CNN
F 1 "74HC595" H 7150 4590 50  0000 C CNN
F 2 "Package_DIP:DIP-16_W7.62mm_Socket" H 7150 3900 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/sn74hc595.pdf" H 7150 3900 50  0001 C CNN
	1    7150 3900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618F31B0
P 7150 4600
AR Path="/618F31B0" Ref="#PWR?"  Part="1" 
AR Path="/618C9959/618F31B0" Ref="#PWR040"  Part="1" 
F 0 "#PWR040" H 7150 4350 50  0001 C CNN
F 1 "GND" H 7155 4427 50  0000 C CNN
F 2 "" H 7150 4600 50  0001 C CNN
F 3 "" H 7150 4600 50  0001 C CNN
	1    7150 4600
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR?
U 1 1 618F31B6
P 7150 3050
AR Path="/618F31B6" Ref="#PWR?"  Part="1" 
AR Path="/618C9959/618F31B6" Ref="#PWR039"  Part="1" 
F 0 "#PWR039" H 7150 2900 50  0001 C CNN
F 1 "+3.3V" H 7165 3223 50  0000 C CNN
F 2 "" H 7150 3050 50  0001 C CNN
F 3 "" H 7150 3050 50  0001 C CNN
	1    7150 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	7150 3050 7150 3300
$Comp
L power:+3.3V #PWR038
U 1 1 618F31BD
P 6750 3800
F 0 "#PWR038" H 6750 3650 50  0001 C CNN
F 1 "+3.3V" V 6765 3928 50  0000 L CNN
F 2 "" H 6750 3800 50  0001 C CNN
F 3 "" H 6750 3800 50  0001 C CNN
	1    6750 3800
	0    -1   -1   0   
$EndComp
Text HLabel 6750 3700 0    47   Input ~ 0
SRCLK
Text HLabel 6750 4000 0    47   Input ~ 0
RCLK
Wire Wire Line
	7550 4400 8500 4400
Wire Wire Line
	8500 4400 8500 3500
Wire Wire Line
	8500 3500 9050 3500
Wire Wire Line
	6750 3500 6000 3500
Wire Wire Line
	6000 3500 6000 4400
Wire Wire Line
	6000 4400 5150 4400
Wire Wire Line
	4350 3500 3500 3500
Wire Wire Line
	3500 3500 3500 4400
Wire Wire Line
	3500 4400 2450 4400
Text HLabel 1650 3500 0    47   Input ~ 0
SER
Text Label 2450 3500 0    47   ~ 0
QA
Text Label 2450 3600 0    47   ~ 0
QB
Text Label 2450 3700 0    47   ~ 0
QC
Text Label 2450 3800 0    47   ~ 0
QD
Text Label 2450 3900 0    47   ~ 0
QE
Text Label 2450 4000 0    47   ~ 0
QF
Text Label 2450 4100 0    47   ~ 0
QG
Text Label 2450 4200 0    47   ~ 0
QH
Wire Wire Line
	2450 4100 2550 4100
Wire Wire Line
	2450 4200 2550 4200
Wire Wire Line
	2450 4000 2550 4000
Wire Wire Line
	2450 3900 2550 3900
Wire Wire Line
	2450 3500 2550 3500
Wire Wire Line
	2450 3600 2550 3600
Wire Wire Line
	2450 3700 2550 3700
Wire Wire Line
	2550 3800 2450 3800
Text Label 5150 3500 0    47   ~ 0
QA
Text Label 5150 3600 0    47   ~ 0
QB
Text Label 5150 3700 0    47   ~ 0
QC
Text Label 5150 3800 0    47   ~ 0
QD
Text Label 5150 3900 0    47   ~ 0
QE
Text Label 5150 4000 0    47   ~ 0
QF
Text Label 5150 4100 0    47   ~ 0
QG
Text Label 5150 4200 0    47   ~ 0
QH
Wire Wire Line
	5150 4100 5250 4100
Wire Wire Line
	5150 4200 5250 4200
Wire Wire Line
	5150 4000 5250 4000
Wire Wire Line
	5150 3900 5250 3900
Wire Wire Line
	5150 3500 5250 3500
Wire Wire Line
	5150 3600 5250 3600
Wire Wire Line
	5150 3700 5250 3700
Wire Wire Line
	5250 3800 5150 3800
Text Label 7550 3500 0    47   ~ 0
QA
Text Label 7550 3600 0    47   ~ 0
QB
Text Label 7550 3700 0    47   ~ 0
QC
Text Label 7550 3800 0    47   ~ 0
QD
Text Label 7550 3900 0    47   ~ 0
QE
Text Label 7550 4000 0    47   ~ 0
QF
Text Label 7550 4100 0    47   ~ 0
QG
Text Label 7550 4200 0    47   ~ 0
QH
Wire Wire Line
	7550 4100 7650 4100
Wire Wire Line
	7550 4200 7650 4200
Wire Wire Line
	7550 4000 7650 4000
Wire Wire Line
	7550 3900 7650 3900
Wire Wire Line
	7550 3500 7650 3500
Wire Wire Line
	7550 3600 7650 3600
Wire Wire Line
	7550 3700 7650 3700
Wire Wire Line
	7650 3800 7550 3800
Text Label 9850 3500 0    47   ~ 0
QA
Text Label 9850 3600 0    47   ~ 0
QB
Text Label 9850 3700 0    47   ~ 0
QC
Text Label 9850 3800 0    47   ~ 0
QD
Text Label 9850 3900 0    47   ~ 0
QE
Text Label 9850 4000 0    47   ~ 0
QF
Text Label 9850 4100 0    47   ~ 0
QG
Text Label 9850 4200 0    47   ~ 0
QH
Wire Wire Line
	9850 4100 9950 4100
Wire Wire Line
	9850 4200 9950 4200
Wire Wire Line
	9850 4000 9950 4000
Wire Wire Line
	9850 3900 9950 3900
Wire Wire Line
	9850 3500 9950 3500
Wire Wire Line
	9850 3600 9950 3600
Wire Wire Line
	9850 3700 9950 3700
Wire Wire Line
	9950 3800 9850 3800
Text Label 5025 925  0    47   ~ 0
QA
Text Label 5025 1075 0    47   ~ 0
QB
Text Label 5025 1225 0    47   ~ 0
QC
Text Label 5025 1375 0    47   ~ 0
QD
Text Label 5025 1525 0    47   ~ 0
QE
Text Label 5025 1675 0    47   ~ 0
QF
Text Label 5025 1825 0    47   ~ 0
QG
Text Label 5025 1975 0    47   ~ 0
QH
Wire Wire Line
	5025 1825 5125 1825
Wire Wire Line
	5025 1975 5125 1975
Wire Wire Line
	5025 1675 5125 1675
Wire Wire Line
	5025 1525 5125 1525
Wire Wire Line
	5025 925  5125 925 
Wire Wire Line
	5025 1075 5125 1075
Wire Wire Line
	5025 1225 5125 1225
Wire Wire Line
	5125 1375 5025 1375
$Comp
L Device:R R?
U 1 1 6196742E
P 5275 925
AR Path="/6196742E" Ref="R?"  Part="1" 
AR Path="/618C9959/6196742E" Ref="R11"  Part="1" 
F 0 "R11" V 5350 925 50  0000 C CNN
F 1 "150" V 5275 925 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5205 925 50  0001 C CNN
F 3 "~" H 5275 925 50  0001 C CNN
	1    5275 925 
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 61972B77
P 5275 1075
AR Path="/61972B77" Ref="R?"  Part="1" 
AR Path="/618C9959/61972B77" Ref="R12"  Part="1" 
F 0 "R12" V 5350 1075 50  0000 C CNN
F 1 "150" V 5275 1075 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5205 1075 50  0001 C CNN
F 3 "~" H 5275 1075 50  0001 C CNN
	1    5275 1075
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 61972F12
P 5275 1225
AR Path="/61972F12" Ref="R?"  Part="1" 
AR Path="/618C9959/61972F12" Ref="R13"  Part="1" 
F 0 "R13" V 5350 1225 50  0000 C CNN
F 1 "150" V 5275 1225 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5205 1225 50  0001 C CNN
F 3 "~" H 5275 1225 50  0001 C CNN
	1    5275 1225
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 61973597
P 5275 1375
AR Path="/61973597" Ref="R?"  Part="1" 
AR Path="/618C9959/61973597" Ref="R14"  Part="1" 
F 0 "R14" V 5350 1375 50  0000 C CNN
F 1 "150" V 5275 1375 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5205 1375 50  0001 C CNN
F 3 "~" H 5275 1375 50  0001 C CNN
	1    5275 1375
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 619738CA
P 5275 1525
AR Path="/619738CA" Ref="R?"  Part="1" 
AR Path="/618C9959/619738CA" Ref="R15"  Part="1" 
F 0 "R15" V 5350 1525 50  0000 C CNN
F 1 "150" V 5275 1525 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5205 1525 50  0001 C CNN
F 3 "~" H 5275 1525 50  0001 C CNN
	1    5275 1525
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 61973C26
P 5275 1675
AR Path="/61973C26" Ref="R?"  Part="1" 
AR Path="/618C9959/61973C26" Ref="R16"  Part="1" 
F 0 "R16" V 5350 1675 50  0000 C CNN
F 1 "150" V 5275 1675 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5205 1675 50  0001 C CNN
F 3 "~" H 5275 1675 50  0001 C CNN
	1    5275 1675
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 619771F7
P 5275 1825
AR Path="/619771F7" Ref="R?"  Part="1" 
AR Path="/618C9959/619771F7" Ref="R17"  Part="1" 
F 0 "R17" V 5350 1825 50  0000 C CNN
F 1 "150" V 5275 1825 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5205 1825 50  0001 C CNN
F 3 "~" H 5275 1825 50  0001 C CNN
	1    5275 1825
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 61977662
P 5275 1975
AR Path="/61977662" Ref="R?"  Part="1" 
AR Path="/618C9959/61977662" Ref="R18"  Part="1" 
F 0 "R18" V 5350 1975 50  0000 C CNN
F 1 "150" V 5275 1975 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5205 1975 50  0001 C CNN
F 3 "~" H 5275 1975 50  0001 C CNN
	1    5275 1975
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5425 1975 5600 1975
Wire Wire Line
	5600 1975 5600 1800
Wire Wire Line
	5425 1825 5575 1825
Wire Wire Line
	5575 1825 5575 1700
Wire Wire Line
	5575 1700 5600 1700
Wire Wire Line
	5425 1675 5550 1675
Wire Wire Line
	5550 1675 5550 1600
Wire Wire Line
	5550 1600 5600 1600
Wire Wire Line
	5425 1525 5525 1525
Wire Wire Line
	5525 1525 5525 1500
Wire Wire Line
	5525 1500 5600 1500
Wire Wire Line
	5425 1375 5525 1375
Wire Wire Line
	5525 1375 5525 1400
Wire Wire Line
	5525 1400 5600 1400
Wire Wire Line
	5425 1225 5550 1225
Wire Wire Line
	5550 1225 5550 1300
Wire Wire Line
	5550 1300 5600 1300
Wire Wire Line
	5425 1075 5575 1075
Wire Wire Line
	5575 1075 5575 1200
Wire Wire Line
	5575 1200 5600 1200
Wire Wire Line
	5425 925  5600 925 
Wire Wire Line
	5600 925  5600 1100
$Comp
L Connector:Conn_01x04_Female J?
U 1 1 6182D354
P 5800 1200
AR Path="/6182D354" Ref="J?"  Part="1" 
AR Path="/618C9959/6182D354" Ref="J9"  Part="1" 
F 0 "J9" H 5828 1176 50  0000 L CNN
F 1 "Conn_01x04_Female" H 5828 1085 50  0000 L CNN
F 2 "Connector_Molex:Molex_KK-254_AE-6410-04A_1x04_P2.54mm_Vertical" H 5800 1200 50  0001 C CNN
F 3 "~" H 5800 1200 50  0001 C CNN
	1    5800 1200
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Female J?
U 1 1 61830A9D
P 5800 1600
AR Path="/61830A9D" Ref="J?"  Part="1" 
AR Path="/618C9959/61830A9D" Ref="J10"  Part="1" 
F 0 "J10" H 5828 1576 50  0000 L CNN
F 1 "Conn_01x04_Female" H 5828 1485 50  0000 L CNN
F 2 "Connector_Molex:Molex_KK-254_AE-6410-04A_1x04_P2.54mm_Vertical" H 5800 1600 50  0001 C CNN
F 3 "~" H 5800 1600 50  0001 C CNN
	1    5800 1600
	1    0    0    -1  
$EndComp
Text Notes 5950 1500 0    50   ~ 0
verbinder für front panel\n
$EndSCHEMATC
