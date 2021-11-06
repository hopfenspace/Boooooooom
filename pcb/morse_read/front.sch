EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 5 5
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text HLabel 2000 5975 1    47   Input ~ 0
Morse_LED
Text HLabel 5225 3425 3    47   Input ~ 0
Right_Button
Text HLabel 5300 3425 3    47   Input ~ 0
Submit_Button
Text HLabel 5375 3425 3    47   Input ~ 0
Left_Button
$Comp
L power:GND #PWR060
U 1 1 61988DC2
P 5675 2775
F 0 "#PWR060" H 5675 2525 50  0001 C CNN
F 1 "GND" H 5680 2602 50  0000 C CNN
F 2 "" H 5675 2775 50  0001 C CNN
F 3 "" H 5675 2775 50  0001 C CNN
	1    5675 2775
	0    -1   -1   0   
$EndComp
Connection ~ 5675 2775
Wire Wire Line
	5675 2775 5675 2375
$Comp
L Device:R R?
U 1 1 6198B2AA
P 5525 2775
AR Path="/6198B2AA" Ref="R?"  Part="1" 
AR Path="/618C9959/6198B2AA" Ref="R?"  Part="1" 
AR Path="/61960EF8/6198B2AA" Ref="R25"  Part="1" 
F 0 "R25" V 5600 2775 50  0000 C CNN
F 1 "10k" V 5525 2775 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5455 2775 50  0001 C CNN
F 3 "~" H 5525 2775 50  0001 C CNN
	1    5525 2775
	0    1    1    0   
$EndComp
$Comp
L Device:R R?
U 1 1 6198B4FC
P 5525 2375
AR Path="/6198B4FC" Ref="R?"  Part="1" 
AR Path="/618C9959/6198B4FC" Ref="R?"  Part="1" 
AR Path="/61960EF8/6198B4FC" Ref="R24"  Part="1" 
F 0 "R24" V 5600 2375 50  0000 C CNN
F 1 "10k" V 5525 2375 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5455 2375 50  0001 C CNN
F 3 "~" H 5525 2375 50  0001 C CNN
	1    5525 2375
	0    1    1    0   
$EndComp
Wire Wire Line
	5225 2375 5375 2375
Wire Wire Line
	5225 2375 5225 3425
Wire Wire Line
	5375 2775 5300 2775
Wire Wire Line
	5300 2775 5300 3425
Wire Wire Line
	5375 3425 5375 3175
Wire Wire Line
	5675 3175 5675 2775
$Comp
L Device:R R?
U 1 1 6198A352
P 5525 3175
AR Path="/6198A352" Ref="R?"  Part="1" 
AR Path="/618C9959/6198A352" Ref="R?"  Part="1" 
AR Path="/61960EF8/6198A352" Ref="R26"  Part="1" 
F 0 "R26" V 5600 3175 50  0000 C CNN
F 1 "10k" V 5525 3175 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5455 3175 50  0001 C CNN
F 3 "~" H 5525 3175 50  0001 C CNN
	1    5525 3175
	0    1    1    0   
$EndComp
$Comp
L Transistor_FET:AO3400A Q1
U 1 1 61996C60
P 2500 5975
F 0 "Q1" H 2705 6021 50  0000 L CNN
F 1 "AO3400A" H 2705 5930 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 2700 5900 50  0001 L CIN
F 3 "http://www.aosmd.com/pdfs/datasheet/AO3400A.pdf" H 2500 5975 50  0001 L CNN
	1    2500 5975
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 6199E2B5
P 2150 5975
AR Path="/6199E2B5" Ref="R?"  Part="1" 
AR Path="/618C9959/6199E2B5" Ref="R?"  Part="1" 
AR Path="/61960EF8/6199E2B5" Ref="R19"  Part="1" 
F 0 "R19" V 2225 5975 50  0000 C CNN
F 1 "330" V 2150 5975 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 2080 5975 50  0001 C CNN
F 3 "~" H 2150 5975 50  0001 C CNN
	1    2150 5975
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR052
U 1 1 619B5A0C
P 2600 6175
F 0 "#PWR052" H 2600 5925 50  0001 C CNN
F 1 "GND" H 2605 6002 50  0000 C CNN
F 2 "" H 2600 6175 50  0001 C CNN
F 3 "" H 2600 6175 50  0001 C CNN
	1    2600 6175
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR051
U 1 1 619B69FB
P 2600 5175
F 0 "#PWR051" H 2600 5025 50  0001 C CNN
F 1 "+5V" H 2615 5348 50  0000 C CNN
F 2 "" H 2600 5175 50  0001 C CNN
F 3 "" H 2600 5175 50  0001 C CNN
	1    2600 5175
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 619BBD44
P 2600 5325
AR Path="/619BBD44" Ref="R?"  Part="1" 
AR Path="/618C9959/619BBD44" Ref="R?"  Part="1" 
AR Path="/61960EF8/619BBD44" Ref="R20"  Part="1" 
F 0 "R20" V 2675 5325 50  0000 C CNN
F 1 "150" V 2600 5325 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 2530 5325 50  0001 C CNN
F 3 "~" H 2600 5325 50  0001 C CNN
	1    2600 5325
	-1   0    0    1   
$EndComp
Text Notes 2425 4925 0    47   ~ 0
gelbe LED
$Comp
L Device:R R?
U 1 1 619BEEEE
P 4100 5350
AR Path="/619BEEEE" Ref="R?"  Part="1" 
AR Path="/618C9959/619BEEEE" Ref="R?"  Part="1" 
AR Path="/61960EF8/619BEEEE" Ref="R22"  Part="1" 
F 0 "R22" V 4175 5350 50  0000 C CNN
F 1 "150" V 4100 5350 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 4030 5350 50  0001 C CNN
F 3 "~" H 4100 5350 50  0001 C CNN
	1    4100 5350
	-1   0    0    1   
$EndComp
Text Notes 4025 4925 0    47   ~ 0
Rote LED\n
$Comp
L Device:R R?
U 1 1 619BCA80
P 5625 5350
AR Path="/619BCA80" Ref="R?"  Part="1" 
AR Path="/618C9959/619BCA80" Ref="R?"  Part="1" 
AR Path="/61960EF8/619BCA80" Ref="R27"  Part="1" 
F 0 "R27" V 5700 5350 50  0000 C CNN
F 1 "91" V 5625 5350 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5555 5350 50  0001 C CNN
F 3 "~" H 5625 5350 50  0001 C CNN
	1    5625 5350
	-1   0    0    1   
$EndComp
Text Notes 5475 5100 0    47   ~ 0
grüne LED\n\n\n
$Comp
L power:+5V #PWR058
U 1 1 619B74E3
P 5625 5200
F 0 "#PWR058" H 5625 5050 50  0001 C CNN
F 1 "+5V" H 5640 5373 50  0000 C CNN
F 2 "" H 5625 5200 50  0001 C CNN
F 3 "" H 5625 5200 50  0001 C CNN
	1    5625 5200
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR053
U 1 1 619B71AA
P 4100 5200
F 0 "#PWR053" H 4100 5050 50  0001 C CNN
F 1 "+5V" H 4115 5373 50  0000 C CNN
F 2 "" H 4100 5200 50  0001 C CNN
F 3 "" H 4100 5200 50  0001 C CNN
	1    4100 5200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR059
U 1 1 619B621F
P 5625 6200
F 0 "#PWR059" H 5625 5950 50  0001 C CNN
F 1 "GND" H 5630 6027 50  0000 C CNN
F 2 "" H 5625 6200 50  0001 C CNN
F 3 "" H 5625 6200 50  0001 C CNN
	1    5625 6200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR054
U 1 1 619B5E28
P 4100 6200
F 0 "#PWR054" H 4100 5950 50  0001 C CNN
F 1 "GND" H 4105 6027 50  0000 C CNN
F 2 "" H 4100 6200 50  0001 C CNN
F 3 "" H 4100 6200 50  0001 C CNN
	1    4100 6200
	1    0    0    -1  
$EndComp
$Comp
L Transistor_FET:AO3400A Q3
U 1 1 619A4505
P 5525 6000
F 0 "Q3" H 5730 6046 50  0000 L CNN
F 1 "AO3400A" H 5730 5955 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 5725 5925 50  0001 L CIN
F 3 "http://www.aosmd.com/pdfs/datasheet/AO3400A.pdf" H 5525 6000 50  0001 L CNN
	1    5525 6000
	1    0    0    -1  
$EndComp
$Comp
L Transistor_FET:AO3400A Q2
U 1 1 619A1D5F
P 4000 6000
F 0 "Q2" H 4205 6046 50  0000 L CNN
F 1 "AO3400A" H 4205 5955 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 4200 5925 50  0001 L CIN
F 3 "http://www.aosmd.com/pdfs/datasheet/AO3400A.pdf" H 4000 6000 50  0001 L CNN
	1    4000 6000
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 6199EE44
P 5175 6000
AR Path="/6199EE44" Ref="R?"  Part="1" 
AR Path="/618C9959/6199EE44" Ref="R?"  Part="1" 
AR Path="/61960EF8/6199EE44" Ref="R23"  Part="1" 
F 0 "R23" V 5250 6000 50  0000 C CNN
F 1 "330" V 5175 6000 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5105 6000 50  0001 C CNN
F 3 "~" H 5175 6000 50  0001 C CNN
	1    5175 6000
	0    1    1    0   
$EndComp
$Comp
L Device:R R?
U 1 1 6199E9FC
P 3650 6000
AR Path="/6199E9FC" Ref="R?"  Part="1" 
AR Path="/618C9959/6199E9FC" Ref="R?"  Part="1" 
AR Path="/61960EF8/6199E9FC" Ref="R21"  Part="1" 
F 0 "R21" V 3725 6000 50  0000 C CNN
F 1 "330" V 3650 6000 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 3580 6000 50  0001 C CNN
F 3 "~" H 3650 6000 50  0001 C CNN
	1    3650 6000
	0    1    1    0   
$EndComp
Text HLabel 5025 6000 1    47   Input ~ 0
Solved_LED
Text HLabel 3500 6000 1    47   Input ~ 0
Strike_LED
$Comp
L Connector:Conn_01x02_Female J?
U 1 1 619D630A
P 4300 5700
AR Path="/619D630A" Ref="J?"  Part="1" 
AR Path="/61960EF8/619D630A" Ref="J4"  Part="1" 
F 0 "J4" H 4328 5676 50  0000 L CNN
F 1 "Conn_01x02_Female" H 4328 5585 50  0000 L CNN
F 2 "Connector_Molex:Molex_KK-254_AE-6410-02A_1x02_P2.54mm_Vertical" H 4300 5700 50  0001 C CNN
F 3 "~" H 4300 5700 50  0001 C CNN
	1    4300 5700
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 5700 4100 5500
$Comp
L Connector:Conn_01x02_Female J?
U 1 1 619D72D6
P 2800 5675
AR Path="/619D72D6" Ref="J?"  Part="1" 
AR Path="/61960EF8/619D72D6" Ref="J3"  Part="1" 
F 0 "J3" H 2828 5651 50  0000 L CNN
F 1 "Conn_01x02_Female" H 2828 5560 50  0000 L CNN
F 2 "Connector_Molex:Molex_KK-254_AE-6410-02A_1x02_P2.54mm_Vertical" H 2800 5675 50  0001 C CNN
F 3 "~" H 2800 5675 50  0001 C CNN
	1    2800 5675
	1    0    0    -1  
$EndComp
Wire Wire Line
	2600 5675 2600 5475
$Comp
L Connector:Conn_01x02_Female J?
U 1 1 619D7BE1
P 5825 5700
AR Path="/619D7BE1" Ref="J?"  Part="1" 
AR Path="/61960EF8/619D7BE1" Ref="J8"  Part="1" 
F 0 "J8" H 5853 5676 50  0000 L CNN
F 1 "Conn_01x02_Female" H 5853 5585 50  0000 L CNN
F 2 "Connector_Molex:Molex_KK-254_AE-6410-02A_1x02_P2.54mm_Vertical" H 5825 5700 50  0001 C CNN
F 3 "~" H 5825 5700 50  0001 C CNN
	1    5825 5700
	1    0    0    -1  
$EndComp
Wire Wire Line
	5625 5700 5625 5500
$Comp
L Connector:Conn_01x02_Female J?
U 1 1 619D9045
P 4875 2975
AR Path="/619D9045" Ref="J?"  Part="1" 
AR Path="/61960EF8/619D9045" Ref="J7"  Part="1" 
F 0 "J7" V 4900 2875 50  0000 L CNN
F 1 "Conn_01x02_Female" V 4600 2650 50  0000 L CNN
F 2 "Connector_Molex:Molex_KK-254_AE-6410-02A_1x02_P2.54mm_Vertical" H 4875 2975 50  0001 C CNN
F 3 "~" H 4875 2975 50  0001 C CNN
	1    4875 2975
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x02_Female J?
U 1 1 619D9678
P 4875 2575
AR Path="/619D9678" Ref="J?"  Part="1" 
AR Path="/61960EF8/619D9678" Ref="J6"  Part="1" 
F 0 "J6" V 4900 2500 50  0000 L CNN
F 1 "Conn_01x02_Female" V 4600 2275 50  0000 L CNN
F 2 "Connector_Molex:Molex_KK-254_AE-6410-02A_1x02_P2.54mm_Vertical" H 4875 2575 50  0001 C CNN
F 3 "~" H 4875 2575 50  0001 C CNN
	1    4875 2575
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x02_Female J?
U 1 1 619D9D55
P 4875 2175
AR Path="/619D9D55" Ref="J?"  Part="1" 
AR Path="/61960EF8/619D9D55" Ref="J5"  Part="1" 
F 0 "J5" H 4903 2151 50  0000 L CNN
F 1 "Conn_01x02_Female" V 4600 1875 50  0000 L CNN
F 2 "Connector_Molex:Molex_KK-254_AE-6410-02A_1x02_P2.54mm_Vertical" H 4875 2175 50  0001 C CNN
F 3 "~" H 4875 2175 50  0001 C CNN
	1    4875 2175
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5375 3175 4975 3175
Connection ~ 5375 3175
Wire Wire Line
	5300 2775 4975 2775
Connection ~ 5300 2775
Wire Wire Line
	5225 2375 4975 2375
Connection ~ 5225 2375
$Comp
L power:+3.3V #PWR055
U 1 1 619DB54B
P 4525 2375
F 0 "#PWR055" H 4525 2225 50  0001 C CNN
F 1 "+3.3V" V 4540 2503 50  0000 L CNN
F 2 "" H 4525 2375 50  0001 C CNN
F 3 "" H 4525 2375 50  0001 C CNN
	1    4525 2375
	0    -1   -1   0   
$EndComp
$Comp
L power:+3.3V #PWR056
U 1 1 619DB9D9
P 4525 2775
F 0 "#PWR056" H 4525 2625 50  0001 C CNN
F 1 "+3.3V" V 4540 2903 50  0000 L CNN
F 2 "" H 4525 2775 50  0001 C CNN
F 3 "" H 4525 2775 50  0001 C CNN
	1    4525 2775
	0    -1   -1   0   
$EndComp
$Comp
L power:+3.3V #PWR057
U 1 1 619DBE80
P 4550 3175
F 0 "#PWR057" H 4550 3025 50  0001 C CNN
F 1 "+3.3V" V 4565 3303 50  0000 L CNN
F 2 "" H 4550 3175 50  0001 C CNN
F 3 "" H 4550 3175 50  0001 C CNN
	1    4550 3175
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4550 3175 4875 3175
Wire Wire Line
	4875 2775 4525 2775
Wire Wire Line
	4525 2375 4875 2375
$EndSCHEMATC