#!/bin/bash

set -e

# Copiamos los datos al directorio actual (por si los tienen en otra carpeta, ajusta la ruta si es necesario)
[ -f "./data/localidades.txt" ] && cp "./data/localidades.txt" ./localidades.txt || true
[ -f "./data/encuestas_50.txt" ] && cp "./data/encuestas_50.txt" ./encuestas_50.txt || true
[ -f "./test/caso_50/output_casobase_50.txt" ] && cp "./test/caso_50/output_casobase_50.txt" ./output_casobase_50.txt || true

# Compilar (ajusta si tu código fuente tiene otro nombre o usa múltiples archivos .c)
# NOTA: Se añade -lm al final para enlazar la librería matemática <math.h>
gcc -o censo_2026 main.c -lm

# Ejecutamos pasando los 3 argumentos requeridos por el enunciado de la tarea
./censo_2026 localidades.txt encuestas_50.txt reporte_salida.txt << 'EOF' > real_output_50.txt
2
1
51
Av_Espana_1680
2
7
2
Pedro_Pascal
48
M
U
1500000
Monkey_D_Luffy
19
M
P
2200000
3
1
Valparaiso
0
EOF

echo
echo "=== Comparando salida con lo esperado (50 Hogares) ==="
diff --color=always -u output_casobase_50.txt real_output_50.txt

DIFF_COUNT=$(diff output_casobase_50.txt real_output_50.txt | wc -l)
if [ $DIFF_COUNT -eq 0 ]; then
  echo -e "\n✅ El output coincide con lo esperado."
else
  echo -e "\n❌ Se encontraron $DIFF_COUNT diferencias."
  echo "   Revisa arriba las líneas marcadas."
fi