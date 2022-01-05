# Inverter Toestand

Skryf toestand van inverter uit na die teksskerm.  Word gebruik in VNC om vinnig die status te kry en vir ontfouting.

Gebruik die status drukker deur die volgende opdrag in bash te tik:

./statusAxpert





## Verwerk die gemete leer


Om 'n lyn in die leer te verwyder met 'n sekere vorm van teks en die uitset na standaard uitset uit te skryf:

sed '/pattern to match/d' ./infile

Dus om die leer Axpert2021-12-31.log skoon te maak vir die meting en uit te skryf na out.log:

sed '/(2/d' ./Axpert2021-12-31.log > out.log