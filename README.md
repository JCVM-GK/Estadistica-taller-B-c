# Estadistica-taller-B-c

Manual de Operación: Stat-Sim Pro
1. Filosofía del Sistema
   
Este software está diseñado para transformar conceptos abstractos de probabilidad en datos tangibles. Su objetivo es permitir al usuario experimentar con la frecuencia de resultados para entender patrones a largo plazo.

2. Guía de Módulos 


| Modulo | Funcion Estadistica | Aplicación Teórica |
| :--- | :---: | ---: |
| Simulaciones | Genera experimentos aleatorios repetitivos. | Validación de la Regla de Laplace mediante la frecuencia. |
| Calculadora de Sucesos | Gestiona conjuntos y subconjuntos del Espacio Muestral (S). | Análisis de compatibilidad, complementariedad y probabilidad clásica. |
| Generador de Muestreo | Extrae una parte representativa de una población. | Ejecución de Muestreo Probabilístico Sistemático. |
3. Protocolos de Operación (El "Cómo" usarlo)
A. Identificación del Universo (Espacio Muestral)
Antes de calcular, el usuario debe definir si su experimento es Finito (dados, monedas) o Infinito (teórico).
Regla de Oro: Si el espacio muestral contiene palabras (ej. "Cara"), los filtros matemáticos como "Pares" no funcionarán, ya que la naturaleza del dato es categórica, no numérica.


 B. Análisis de Relaciones Lógicas
Para determinar si dos eventos pueden ocurrir simultáneamente, el software utiliza la intersección:
Sucesos Compatibles: Si el programa muestra elementos en la intersección, pueden ocurrir a la vez.
Sucesos Incompatibles: Si el resultado es set(), son mutuamente excluyentes.

C. Extracción de Muestras Representativas
Para evitar el Muestreo No Probabilístico (por conveniencia o sin norma) , el software utiliza el Factor de Elevación ($FE$).
El usuario ingresa la Población ($N$) y el tamaño deseado ($n$).
El software calcula el intervalo $k$.
Se selecciona un Arranque Aleatorio para garantizar que todos tengan una probabilidad conocida de ser elegidos.

4. Limitaciones Técnicas y Advertencias
Integridad de la Muestra: El software impedirá extraer una muestra ($n$) mayor a la población total ($N$), respetando la lógica de que la muestra es solo una parte del todo.
Naturaleza de los Datos: Los cálculos de Media Muestral ($\bar{X}$) y filtros numéricos requieren que los elementos del espacio muestral sean números reales para ser procesados matemáticamente.
