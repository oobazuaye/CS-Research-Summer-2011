/* 
 pitches.h
 Support file for Arduino side controller for interfacing with Python
 Summer 2010
 Beryl Egerter, Sarah Johnson, Philip Aelion-Moss
 */


/*************************************************
 * Public Constants
 *************************************************/


// The -1st octave is not actually going to be used
// The piezo speaker has issues playing it
#define NOTE_C_1  8.2
#define NOTE_CS_1 8.7
#define NOTE_D_1  9.2
#define NOTE_DS_1 9.7
#define NOTE_E_1  10.3
#define NOTE_F_1  10.9
#define NOTE_FS_1 11.6
#define NOTE_G_1  12.3
#define NOTE_GS_1 13
#define NOTE_A_1  13.8
#define NOTE_AS_1 14.6
#define NOTE_B_1  15.4

#define NOTE_C0  16.4
#define NOTE_CS0 17.3
#define NOTE_D0  18.4
#define NOTE_DS0 19.4
#define NOTE_E0  20.6
#define NOTE_F0  21.8
#define NOTE_FS0 23.1
#define NOTE_G0  24.5
#define NOTE_GS0 26
#define NOTE_A0  27.5
#define NOTE_AS0 29.1
#define NOTE_B0  30.9
#define NOTE_C1  32.7
#define NOTE_CS1 34.6
#define NOTE_D1  36.7
#define NOTE_DS1 38.9
#define NOTE_E1  41.2
#define NOTE_F1  43.7
#define NOTE_FS1 46.2
#define NOTE_G1  49
#define NOTE_GS1 51.9
#define NOTE_A1  55
#define NOTE_AS1 58.3
#define NOTE_B1  61.7
#define NOTE_C2  65.4
#define NOTE_CS2 69.3
#define NOTE_D2  73.4
#define NOTE_DS2 77.8
#define NOTE_E2  82.4
#define NOTE_F2  87.3
#define NOTE_FS2 92.5
#define NOTE_G2  98
#define NOTE_GS2 104
#define NOTE_A2  110
#define NOTE_AS2 117
#define NOTE_B2  123
#define NOTE_C3  131
#define NOTE_CS3 139
#define NOTE_D3  147
#define NOTE_DS3 156
#define NOTE_E3  165
#define NOTE_F3  175
#define NOTE_FS3 185
#define NOTE_G3  196
#define NOTE_GS3 208
#define NOTE_A3  220
#define NOTE_AS3 233
#define NOTE_B3  247
#define NOTE_C4  262
#define NOTE_CS4 277
#define NOTE_D4  294
#define NOTE_DS4 311
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_FS4 370
#define NOTE_G4  392
#define NOTE_GS4 415
#define NOTE_A4  440
#define NOTE_AS4 466
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988
#define NOTE_C6  1047
#define NOTE_CS6 1109
#define NOTE_D6  1175
#define NOTE_DS6 1245
#define NOTE_E6  1319
#define NOTE_F6  1397
#define NOTE_FS6 1480
#define NOTE_G6  1568
#define NOTE_GS6 1661
#define NOTE_A6  1760
#define NOTE_AS6 1865
#define NOTE_B6  1976
#define NOTE_C7  2093
#define NOTE_CS7 2217
#define NOTE_D7  2349
#define NOTE_DS7 2489
#define NOTE_E7  2637
#define NOTE_F7  2794
#define NOTE_FS7 2960
#define NOTE_G7  3136
#define NOTE_GS7 3322
#define NOTE_A7  3520
#define NOTE_AS7 3729
#define NOTE_B7  3951
#define NOTE_C8  4186
#define NOTE_CS8 4435
#define NOTE_D8  4699
#define NOTE_DS8 4978
#define NOTE_E8  5274
#define NOTE_F8  5588
#define NOTE_FS8 5920
#define NOTE_G8  6272
#define NOTE_GS8 6645
#define NOTE_A8  7040
#define NOTE_AS8 7459
#define NOTE_B8  7902
#define NOTE_C9  8372
#define NOTE_CS9 8870
#define NOTE_D9  9397
#define NOTE_DS9 9956
#define NOTE_E9  10548
#define NOTE_F9  11175
#define NOTE_FS9 11840
#define NOTE_G9  12544
#define NOTE_GS9 13290
#define NOTE_A9  14080
#define NOTE_AS9 14917
#define NOTE_B9  15804
#define NOTE_C10  16744
#define NOTE_CS10 17740
#define NOTE_D10  18795
#define NOTE_DS10 19912
#define NOTE_E10  21096
#define NOTE_F10  22351
#define NOTE_FS10 23680
#define NOTE_G10  25088
#define NOTE_GS10 26580
#define NOTE_A10  28160
#define NOTE_AS10 29835
#define NOTE_B10  31609

// The -1st octave is not actually going to be used
int OCTAVE_1[] = { NOTE_C_1, NOTE_CS_1, NOTE_D_1, 
NOTE_DS_1, NOTE_E_1, NOTE_F_1, NOTE_FS_1, NOTE_G_1, 
NOTE_GS_1, NOTE_A_1, NOTE_AS_1, NOTE_B_1 };

int OCTAVE0[] = { NOTE_C0, NOTE_CS0, NOTE_D0, 
NOTE_DS0, NOTE_E0, NOTE_F0, NOTE_FS0, NOTE_G0, 
NOTE_GS0, NOTE_A0, NOTE_AS0, NOTE_B0 };

int OCTAVE1[] = { NOTE_C1, NOTE_CS1, NOTE_D1, 
NOTE_DS1, NOTE_E1, NOTE_F1, NOTE_FS1, NOTE_G1, 
NOTE_GS1, NOTE_A1, NOTE_AS1, NOTE_B1 };

int OCTAVE2[] = { NOTE_C2, NOTE_CS2, NOTE_D2, 
NOTE_DS2, NOTE_E2, NOTE_F2, NOTE_FS2, NOTE_G2, 
NOTE_GS2, NOTE_A2, NOTE_AS2, NOTE_B2 };

int OCTAVE3[] = { NOTE_C3, NOTE_CS3, NOTE_D3, 
NOTE_DS3, NOTE_E3, NOTE_F3, NOTE_FS3, NOTE_G3, 
NOTE_GS3, NOTE_A3, NOTE_AS3, NOTE_B3 };

int OCTAVE4[] = { NOTE_C4, NOTE_CS4, NOTE_D4, 
NOTE_DS4, NOTE_E4, NOTE_F4, NOTE_FS4, NOTE_G4, 
NOTE_GS4, NOTE_A4, NOTE_AS4, NOTE_B4 };

int OCTAVE5[] = { NOTE_C5, NOTE_CS5, NOTE_D5, 
NOTE_DS5, NOTE_E5, NOTE_F5, NOTE_FS5, NOTE_G5, 
NOTE_GS5, NOTE_A5, NOTE_AS5, NOTE_B5 };

int OCTAVE6[] = { NOTE_C6, NOTE_CS6, NOTE_D6, 
NOTE_DS6, NOTE_E6, NOTE_F6, NOTE_FS6, NOTE_G6, 
NOTE_GS6, NOTE_A6, NOTE_AS6, NOTE_B6 };

int OCTAVE7[] = { NOTE_C7, NOTE_CS7, NOTE_D7, 
NOTE_DS7, NOTE_E7, NOTE_F7, NOTE_FS7, NOTE_G7, 
NOTE_GS7, NOTE_A7, NOTE_AS7, NOTE_B7 };

int OCTAVE8[] = { NOTE_C8, NOTE_CS8, NOTE_D8, 
NOTE_DS8, NOTE_E8, NOTE_F8, NOTE_FS8, NOTE_G8, 
NOTE_GS8, NOTE_A8, NOTE_AS8, NOTE_B8 };

int OCTAVE9[] = { NOTE_C9, NOTE_CS9, NOTE_D9, 
NOTE_DS9, NOTE_E9, NOTE_F9, NOTE_FS9, NOTE_G9, 
NOTE_GS9, NOTE_A9, NOTE_AS9, NOTE_B9 };

int OCTAVE10[] = { NOTE_C10, NOTE_CS10, NOTE_D10, 
NOTE_DS10, NOTE_E10, NOTE_F10, NOTE_FS10, NOTE_G10, 
NOTE_GS10, NOTE_A10, NOTE_AS10, NOTE_B10 };

int NUMOCTAVES = 11;
int NUMNOTES = 12;

int OCTAVES[11][12];

