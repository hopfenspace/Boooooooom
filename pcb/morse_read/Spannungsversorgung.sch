EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 5
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
L Regulator_Linear:LM7805_TO220 U?
U 1 1 618BF391
P 4350 3550
AR Path="/618BF391" Ref="U?"  Part="1" 
AR Path="/618B7139/618BF391" Ref="U2"  Part="1" 
F 0 "U2" H 4350 3792 50  0000 C CNN
F 1 "LM7805_TO220" H 4350 3701 50  0000 C CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 4350 3775 50  0001 C CIN
F 3 "https://www.onsemi.cn/PowerSolutions/document/MC7800-D.PDF" H 4350 3500 50  0001 C CNN
	1    4350 3550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618BF3AA
P 4350 3850
AR Path="/618BF3AA" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF3AA" Ref="#PWR023"  Part="1" 
F 0 "#PWR023" H 4350 3600 50  0001 C CNN
F 1 "GND" H 4355 3677 50  0000 C CNN
F 2 "" H 4350 3850 50  0001 C CNN
F 3 "" H 4350 3850 50  0001 C CNN
	1    4350 3850
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 618BF3B0
P 4750 3700
AR Path="/618BF3B0" Ref="C?"  Part="1" 
AR Path="/618B7139/618BF3B0" Ref="C3"  Part="1" 
F 0 "C3" H 4865 3746 50  0000 L CNN
F 1 "68uF" H 4865 3655 50  0000 L CNN
F 2 "Capacitor_THT:C_Radial_D6.3mm_H7.0mm_P2.50mm" H 4788 3550 50  0001 C CNN
F 3 "~" H 4750 3700 50  0001 C CNN
	1    4750 3700
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618BF3B6
P 4750 3850
AR Path="/618BF3B6" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF3B6" Ref="#PWR026"  Part="1" 
F 0 "#PWR026" H 4750 3600 50  0001 C CNN
F 1 "GND" H 4755 3677 50  0000 C CNN
F 2 "" H 4750 3850 50  0001 C CNN
F 3 "" H 4750 3850 50  0001 C CNN
	1    4750 3850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618BF3BC
P 3850 3850
AR Path="/618BF3BC" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF3BC" Ref="#PWR020"  Part="1" 
F 0 "#PWR020" H 3850 3600 50  0001 C CNN
F 1 "GND" H 3855 3677 50  0000 C CNN
F 2 "" H 3850 3850 50  0001 C CNN
F 3 "" H 3850 3850 50  0001 C CNN
	1    3850 3850
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR?
U 1 1 618BF3C2
P 3800 3550
AR Path="/618BF3C2" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF3C2" Ref="#PWR019"  Part="1" 
F 0 "#PWR019" H 3800 3400 50  0001 C CNN
F 1 "+12V" V 3815 3678 50  0000 L CNN
F 2 "" H 3800 3550 50  0001 C CNN
F 3 "" H 3800 3550 50  0001 C CNN
	1    3800 3550
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4650 3550 4750 3550
Connection ~ 4750 3550
Wire Wire Line
	4750 3550 4850 3550
$Comp
L power:+5V #PWR?
U 1 1 618BF3CB
P 4850 3550
AR Path="/618BF3CB" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF3CB" Ref="#PWR027"  Part="1" 
F 0 "#PWR027" H 4850 3400 50  0001 C CNN
F 1 "+5V" V 4865 3678 50  0000 L CNN
F 2 "" H 4850 3550 50  0001 C CNN
F 3 "" H 4850 3550 50  0001 C CNN
	1    4850 3550
	0    1    1    0   
$EndComp
Wire Wire Line
	3800 3550 3850 3550
$Comp
L Device:C C?
U 1 1 618BF3D2
P 3850 3700
AR Path="/618BF3D2" Ref="C?"  Part="1" 
AR Path="/618B7139/618BF3D2" Ref="C2"  Part="1" 
F 0 "C2" H 3965 3746 50  0000 L CNN
F 1 "22uF" H 3965 3655 50  0000 L CNN
F 2 "Capacitor_THT:C_Radial_D6.3mm_H7.0mm_P2.50mm" H 3888 3550 50  0001 C CNN
F 3 "~" H 3850 3700 50  0001 C CNN
	1    3850 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3850 3550 4050 3550
Connection ~ 3850 3550
$Comp
L Regulator_Linear:AMS1117-3.3 U?
U 1 1 618BF3DA
P 6750 3550
AR Path="/618BF3DA" Ref="U?"  Part="1" 
AR Path="/618B7139/618BF3DA" Ref="U3"  Part="1" 
F 0 "U3" H 6750 3792 50  0000 C CNN
F 1 "AMS1117-3.3" H 6750 3701 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-223-3_TabPin2" H 6750 3750 50  0001 C CNN
F 3 "http://www.advanced-monolithic.com/pdf/ds1117.pdf" H 6850 3300 50  0001 C CNN
	1    6750 3550
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR?
U 1 1 618BF3E0
P 6450 3550
AR Path="/618BF3E0" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF3E0" Ref="#PWR028"  Part="1" 
F 0 "#PWR028" H 6450 3400 50  0001 C CNN
F 1 "+5V" V 6465 3678 50  0000 L CNN
F 2 "" H 6450 3550 50  0001 C CNN
F 3 "" H 6450 3550 50  0001 C CNN
	1    6450 3550
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618BF3E6
P 6750 3850
AR Path="/618BF3E6" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF3E6" Ref="#PWR029"  Part="1" 
F 0 "#PWR029" H 6750 3600 50  0001 C CNN
F 1 "GND" H 6755 3677 50  0000 C CNN
F 2 "" H 6750 3850 50  0001 C CNN
F 3 "" H 6750 3850 50  0001 C CNN
	1    6750 3850
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 618BF3EC
P 7050 3700
AR Path="/618BF3EC" Ref="C?"  Part="1" 
AR Path="/618B7139/618BF3EC" Ref="C4"  Part="1" 
F 0 "C4" H 7165 3746 50  0000 L CNN
F 1 "22uF" H 7165 3655 50  0000 L CNN
F 2 "Capacitor_THT:C_Radial_D6.3mm_H7.0mm_P2.50mm" H 7088 3550 50  0001 C CNN
F 3 "~" H 7050 3700 50  0001 C CNN
	1    7050 3700
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618BF3F2
P 7050 3850
AR Path="/618BF3F2" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF3F2" Ref="#PWR031"  Part="1" 
F 0 "#PWR031" H 7050 3600 50  0001 C CNN
F 1 "GND" H 7055 3677 50  0000 C CNN
F 2 "" H 7050 3850 50  0001 C CNN
F 3 "" H 7050 3850 50  0001 C CNN
	1    7050 3850
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR?
U 1 1 618BF3F8
P 7050 3550
AR Path="/618BF3F8" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF3F8" Ref="#PWR030"  Part="1" 
F 0 "#PWR030" H 7050 3400 50  0001 C CNN
F 1 "+3.3V" V 7065 3678 50  0000 L CNN
F 2 "" H 7050 3550 50  0001 C CNN
F 3 "" H 7050 3550 50  0001 C CNN
	1    7050 3550
	0    1    1    0   
$EndComp
Connection ~ 7050 3550
$Comp
L Device:LED D?
U 1 1 618BF3FF
P 3600 5200
AR Path="/618BF3FF" Ref="D?"  Part="1" 
AR Path="/618B7139/618BF3FF" Ref="D2"  Part="1" 
F 0 "D2" V 3639 5082 50  0000 R CNN
F 1 "LED" V 3548 5082 50  0000 R CNN
F 2 "LED_THT:LED_D3.0mm" H 3600 5200 50  0001 C CNN
F 3 "~" H 3600 5200 50  0001 C CNN
	1    3600 5200
	0    -1   -1   0   
$EndComp
$Comp
L Device:LED D?
U 1 1 618BF405
P 4050 5200
AR Path="/618BF405" Ref="D?"  Part="1" 
AR Path="/618B7139/618BF405" Ref="D3"  Part="1" 
F 0 "D3" V 4089 5082 50  0000 R CNN
F 1 "LED" V 3998 5082 50  0000 R CNN
F 2 "LED_THT:LED_D3.0mm" H 4050 5200 50  0001 C CNN
F 3 "~" H 4050 5200 50  0001 C CNN
	1    4050 5200
	0    -1   -1   0   
$EndComp
$Comp
L Device:LED D?
U 1 1 618BF40B
P 4400 5200
AR Path="/618BF40B" Ref="D?"  Part="1" 
AR Path="/618B7139/618BF40B" Ref="D4"  Part="1" 
F 0 "D4" V 4439 5082 50  0000 R CNN
F 1 "LED" V 4348 5082 50  0000 R CNN
F 2 "LED_THT:LED_D3.0mm" H 4400 5200 50  0001 C CNN
F 3 "~" H 4400 5200 50  0001 C CNN
	1    4400 5200
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 618BF411
P 3600 4900
AR Path="/618BF411" Ref="R?"  Part="1" 
AR Path="/618B7139/618BF411" Ref="R8"  Part="1" 
F 0 "R8" H 3670 4946 50  0000 L CNN
F 1 "510" H 3670 4855 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 3530 4900 50  0001 C CNN
F 3 "~" H 3600 4900 50  0001 C CNN
	1    3600 4900
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 618BF417
P 4050 4900
AR Path="/618BF417" Ref="R?"  Part="1" 
AR Path="/618B7139/618BF417" Ref="R9"  Part="1" 
F 0 "R9" H 4120 4946 50  0000 L CNN
F 1 "180" H 4120 4855 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 3980 4900 50  0001 C CNN
F 3 "~" H 4050 4900 50  0001 C CNN
	1    4050 4900
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 618BF41D
P 4400 4900
AR Path="/618BF41D" Ref="R?"  Part="1" 
AR Path="/618B7139/618BF41D" Ref="R10"  Part="1" 
F 0 "R10" H 4470 4946 50  0000 L CNN
F 1 "56" H 4470 4855 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 4330 4900 50  0001 C CNN
F 3 "~" H 4400 4900 50  0001 C CNN
	1    4400 4900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618BF423
P 3600 5350
AR Path="/618BF423" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF423" Ref="#PWR018"  Part="1" 
F 0 "#PWR018" H 3600 5100 50  0001 C CNN
F 1 "GND" H 3605 5177 50  0000 C CNN
F 2 "" H 3600 5350 50  0001 C CNN
F 3 "" H 3600 5350 50  0001 C CNN
	1    3600 5350
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618BF429
P 4050 5350
AR Path="/618BF429" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF429" Ref="#PWR022"  Part="1" 
F 0 "#PWR022" H 4050 5100 50  0001 C CNN
F 1 "GND" H 4055 5177 50  0000 C CNN
F 2 "" H 4050 5350 50  0001 C CNN
F 3 "" H 4050 5350 50  0001 C CNN
	1    4050 5350
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 618BF42F
P 4400 5350
AR Path="/618BF42F" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF42F" Ref="#PWR025"  Part="1" 
F 0 "#PWR025" H 4400 5100 50  0001 C CNN
F 1 "GND" H 4405 5177 50  0000 C CNN
F 2 "" H 4400 5350 50  0001 C CNN
F 3 "" H 4400 5350 50  0001 C CNN
	1    4400 5350
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR?
U 1 1 618BF435
P 3600 4750
AR Path="/618BF435" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF435" Ref="#PWR017"  Part="1" 
F 0 "#PWR017" H 3600 4600 50  0001 C CNN
F 1 "+12V" H 3615 4923 50  0000 C CNN
F 2 "" H 3600 4750 50  0001 C CNN
F 3 "" H 3600 4750 50  0001 C CNN
	1    3600 4750
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR?
U 1 1 618BF43B
P 4050 4750
AR Path="/618BF43B" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF43B" Ref="#PWR021"  Part="1" 
F 0 "#PWR021" H 4050 4600 50  0001 C CNN
F 1 "+5V" H 4065 4923 50  0000 C CNN
F 2 "" H 4050 4750 50  0001 C CNN
F 3 "" H 4050 4750 50  0001 C CNN
	1    4050 4750
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR?
U 1 1 618BF441
P 4400 4750
AR Path="/618BF441" Ref="#PWR?"  Part="1" 
AR Path="/618B7139/618BF441" Ref="#PWR024"  Part="1" 
F 0 "#PWR024" H 4400 4600 50  0001 C CNN
F 1 "+3.3V" H 4415 4923 50  0000 C CNN
F 2 "" H 4400 4750 50  0001 C CNN
F 3 "" H 4400 4750 50  0001 C CNN
	1    4400 4750
	1    0    0    -1  
$EndComp
Text Notes 4550 4450 2    50   ~ 0
Status Spannungsversorgung
Text Notes 4500 3250 2    50   ~ 0
12V->5V\n
Text Notes 6900 3250 2    50   ~ 0
5V->3.3V\n
Text Notes 3875 4525 0    47   ~ 0
gelbe LEDs\n
$EndSCHEMATC