import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"


def cargar_datos():
    """Carga y valida los archivos de clientes, productos y ventas."""
    clientes = pd.read_csv(DATA_DIR / "clientes.csv")
    productos = pd.read_excel(DATA_DIR / "productos.xlsx")
    ventas = pd.read_csv(DATA_DIR / "ventas.csv", parse_dates=["fecha"])

    if clientes.empty or productos.empty or ventas.empty:
        raise ValueError("Uno o más archivos fueron cargados sin información.")

    print("Archivos cargados correctamente.")
    return clientes, productos, ventas


def explorar_datos(nombre, df):
    """Muestra información básica de un DataFrame."""
    print(f"\n{'=' * 20} {nombre.upper()} {'=' * 20}")
    print("Cantidad de registros:", len(df))
    print("Número de columnas:", df.shape[1])
    print("Nombres de columnas:", list(df.columns))
    print("\nTipos de datos:")
    print(df.dtypes)
    print("\nPrimeros 5 registros:")
    print(df.head())
    print("\nÚltimos 5 registros:")
    print(df.tail())
    print("\nValores nulos por columna:")
    print(df.isnull().sum())


def preparar_datos(clientes, productos, ventas):
    """
    Aplica funciones de Pandas investigadas:
    drop_duplicates, astype, rename, merge, query,
    groupby, value_counts, nunique y pivot_table.
    """
    clientes = clientes.drop_duplicates()
    productos = productos.drop_duplicates()
    ventas = ventas.drop_duplicates()

    clientes["id_cliente"] = clientes["id_cliente"].astype(int)
    productos["id_producto"] = productos["id_producto"].astype(int)
    ventas["id_cliente"] = ventas["id_cliente"].astype(int)
    ventas["id_producto"] = ventas["id_producto"].astype(int)

    clientes = clientes.rename(columns={"nombre": "nombre_cliente"})

    ventas_completas = ventas.merge(
        clientes[["id_cliente", "nombre_cliente", "ciudad"]],
        on="id_cliente",
        how="left"
    ).merge(
        productos[["id_producto", "producto", "categoria"]],
        on="id_producto",
        how="left"
    )

    return clientes, productos, ventas, ventas_completas


def analizar_ventas(ventas):
    resumen = pd.DataFrame({
        "Indicador": [
            "Total de ventas",
            "Promedio de venta",
            "Venta máxima",
            "Venta mínima",
            "Número de transacciones"
        ],
        "Valor": [
            ventas["total_venta"].sum(),
            ventas["total_venta"].mean(),
            ventas["total_venta"].max(),
            ventas["total_venta"].min(),
            ventas["id_venta"].count()
        ]
    })

    ventas_superiores_promedio = ventas.query("total_venta > total_venta.mean()")
    print("\nVentas superiores al promedio:", len(ventas_superiores_promedio))

    return resumen


def analizar_clientes(clientes, ventas_completas):
    compras_por_cliente = ventas_completas.groupby(
        ["id_cliente", "nombre_cliente"], as_index=False
    ).agg(
        numero_compras=("id_venta", "count"),
        dinero_gastado=("total_venta", "sum"),
        promedio_compra=("total_venta", "mean")
    )

    cliente_mas_compras = compras_por_cliente.loc[
        compras_por_cliente["numero_compras"].idxmax()
    ]

    cliente_mas_gasto = compras_por_cliente.loc[
        compras_por_cliente["dinero_gastado"].idxmax()
    ]

    ciudad_mas_clientes = clientes["ciudad"].value_counts().idxmax()

    resumen_clientes = pd.DataFrame({
        "Indicador": [
            "Cliente con mayor número de compras",
            "Cliente que más dinero ha gastado",
            "Ciudad con mayor número de clientes"
        ],
        "Resultado": [
            cliente_mas_compras["nombre_cliente"],
            cliente_mas_gasto["nombre_cliente"],
            ciudad_mas_clientes
        ]
    })

    print("\nCantidad de ciudades diferentes:", clientes["ciudad"].nunique())

    return compras_por_cliente, resumen_clientes


def analizar_productos(ventas_completas):
    resumen_productos = ventas_completas.groupby(
        ["id_producto", "producto"], as_index=False
    ).agg(
        unidades_vendidas=("cantidad", "sum"),
        ingreso_total=("total_venta", "sum")
    )

    producto_mas_vendido = resumen_productos.loc[
        resumen_productos["unidades_vendidas"].idxmax()
    ]

    producto_menos_vendido = resumen_productos.loc[
        resumen_productos["unidades_vendidas"].idxmin()
    ]

    producto_mayor_ingreso = resumen_productos.loc[
        resumen_productos["ingreso_total"].idxmax()
    ]

    producto_menor_ingreso = resumen_productos.loc[
        resumen_productos["ingreso_total"].idxmin()
    ]

    indicadores = pd.DataFrame({
        "Indicador": [
            "Producto más vendido",
            "Producto menos vendido",
            "Producto con mayor ingreso",
            "Producto con menor ingreso"
        ],
        "Resultado": [
            producto_mas_vendido["producto"],
            producto_menos_vendido["producto"],
            producto_mayor_ingreso["producto"],
            producto_menor_ingreso["producto"]
        ]
    })

    return resumen_productos, indicadores


def crear_pivot(ventas_completas):
    """Crea una tabla dinámica de ingresos por ciudad y categoría."""
    return ventas_completas.pivot_table(
        index="ciudad",
        columns="categoria",
        values="total_venta",
        aggfunc="sum",
        fill_value=0
    )


def generar_reporte(resumen_ventas, resumen_clientes, indicadores_productos,
                    ventas_completas, compras_por_cliente, resumen_productos):
    REPORTS_DIR.mkdir(exist_ok=True)

    resumen_general = pd.concat(
        [
            resumen_ventas.rename(columns={"Valor": "Resultado"}),
            resumen_clientes,
            indicadores_productos
        ],
        ignore_index=True
    )

    ruta_reporte = REPORTS_DIR / "reporte_final.xlsx"

    with pd.ExcelWriter(ruta_reporte, engine="openpyxl") as writer:
        resumen_general.to_excel(writer, sheet_name="Resumen", index=False)
        ventas_completas.to_excel(writer, sheet_name="Ventas", index=False)
        compras_por_cliente.to_excel(writer, sheet_name="Clientes", index=False)
        resumen_productos.to_excel(writer, sheet_name="Productos", index=False)

    print(f"\nReporte generado correctamente en: {ruta_reporte}")


def main():
    clientes, productos, ventas = cargar_datos()

    explorar_datos("Clientes", clientes)
    explorar_datos("Productos", productos)
    explorar_datos("Ventas", ventas)

    clientes, productos, ventas, ventas_completas = preparar_datos(
        clientes, productos, ventas
    )

    resumen_ventas = analizar_ventas(ventas)
    compras_por_cliente, resumen_clientes = analizar_clientes(
        clientes, ventas_completas
    )
    resumen_productos, indicadores_productos = analizar_productos(
        ventas_completas
    )

    tabla_pivot = crear_pivot(ventas_completas)
    print("\nIngresos por ciudad y categoría:")
    print(tabla_pivot)

    generar_reporte(
        resumen_ventas,
        resumen_clientes,
        indicadores_productos,
        ventas_completas,
        compras_por_cliente,
        resumen_productos
    )


if __name__ == "__main__":
    main()
