<h2>ITER CODAC
55.C4 divertor Thomson scattering (DTS) diagnostic</h2>
Ioffe institute, Russia
<h3>Slow controller examples.</h3>


Hardware
========
**Siemens Simatic 1200:**
-6ES7214-1HG40-0XB0 - SIMATIC S7-1200 1214C DC/DC/RLY
-6ES7223-1BL32-0XB0 - 16DI/16DO
-6ES7241-1CH30-1XB0 - CB-1241 RS485
-6EP1332-1SH71 - PM1207 24V/2.5A
-6ED1052-1MD08-0BA1 - LOGO! 12/24RCE

**Trinamic** TMCM-3110 V1.1  StepMotors driver 3ch RS485 edition

**Moxa** N-Port 5130

**STM32** 32F746G-DISCO 

Software
========
- TiaPortal v17, Step7 (for porting), Logo SoftComfort (for testing)
- Windows 11, VS Code
- CODAC-6.3 RHEL-7.4 SDD-6.3.1 CSS-4.7.8
- TMCL-IDE 3.5.0
- Moxa N-Port
- STM32 CubeMX IDE, TouchGFX


Projects
=========

plc-Trinamic485
-----------
Trinamic step motor controller via RS485
CB1241 board in P2P mode
Trinamic board motor=0, address=1, 9600 8N1
Profinet: 172.16.18.220/24

- IO and Commands processing [MainPLC1]
	- CODAC.CMD1-4 -> Q8.0-3
	- CODAC.CMD1   -> Start Motor
	- I1.1 -> Start Motor continuously
	- I1.4 -> Stop Motor continuously
	- send Evt.StatusBits[1,2] at 0.5Hz
	- Q9.6 = 1 Hz (Orange Led)
	- Q8.6 = ADC1x1 Hz (Green Led)	
	- I0.1 -> Q0.1 (HwBtn: Motor Left-Right)

- Variables and ADC processing [MainPLC2]
	- Var16out = Var16in * 2
	- LedG delay depend on ADC1
	- Motor delay = 1.5s + (10s-Var16in)
	- Motor speed = ADC1 + Var16in
	- Motor Left/Right = I0.1 button
	- Q0.0 = Var16in.%X0
	- I0.1 -> I0.1, Motor Rotate Left/Right
	- Q1.0 = ADC1.%X1
	- Q1.1 = ADC1.%X0 

- RS485 processing [MainPLC3]
	- config port as Point-2-Point at startup
	- send VER heartbeat every 2s
	- send ROR/ROL at CMD1 or I1.1
	- send MST at CMD1 delayed

**CODAC interchange variables**
D1-J3-F0:Var16out [DB101.ai16, Config, Fast->Slow]
D1-J3-F0:Var16in  [DB100.ao16, State, Slow->Fast]
D1-J3-F0:Cmd1     [DB102.CMD1, Commands, Fast->Slow]
D1-J3-F0:Evt1/2   [DB105.StatusBits, Events, Slow->Fast]



codac_spss_test.py
------------------
CODAC asyn7 protocol sniffer and reverse engineering
- Receive States packet (2000 port)
- Send Config packets   (2001 port)
- Receive Event packets (2002 port)
- Simple server side socket test


plc-1BG40-3.0_V17
---------
ITER Cubicle monitoring firmware adoption for TIA portal v17 and DC/DC/RLY CPU + 16DI/DO module.


plc-Logo
--------
Simatic Logo! PLC helper to test s7-1200

laser-modbus
------------
STM32 based RS485 device simulator with GUI
