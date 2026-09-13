# Sistema de Análisis Empresarial con Pandas

## Descripción
Aplicación desarrollada en Python y Pandas para cargar, explorar, analizar y generar reportes a partir de información empresarial almacenada en archivos CSV y Excel.

## Estructura
```text
proyecto-pandas/
├── data/
│   ├── clientes.csv
│   ├── productos.xlsx
│   └── ventas.csv
├── src/
│   └── analisis.py
├── reports/
│   └── reporte_final.xlsx
├── README.md
└── requirements.txt
```

## Requisitos
Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta principal del proyecto:

```bash
python src/analisis.py
```

## Funciones de Pandas investigadas
El proyecto utiliza, entre otras:

- `drop_duplicates()`: elimina registros duplicados.
- `astype()`: cambia el tipo de dato de una columna.
- `rename()`: cambia nombres de columnas.
- `merge()`: une DataFrames relacionados.
- `query()`: filtra información mediante una expresión.
- `groupby()`: agrupa datos para realizar cálculos.
- `value_counts()`: cuenta la frecuencia de los valores.
- `nunique()`: cuenta valores únicos.
- `pivot_table()`: crea tablas dinámicas.
- `concat()`: une varios DataFrames.

## Ventajas de automatizar con Python y Pandas
1. Reduce el tiempo necesario para realizar análisis repetitivos.
2. Disminuye errores humanos asociados al procesamiento manual.
3. Permite actualizar y generar reportes automáticamente.

## Posible riesgo
Si los datos de entrada contienen errores, valores incorrectos o información incompleta, los resultados del análisis y del reporte también pueden ser incorrectos. Por esta razón es importante validar y limpiar los datos antes de analizarlos.
