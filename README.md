# Optimizador de rutas con grafos

Aplicación Streamlit para construir o editar un grafo ponderado y encontrar el camino de distancia mínima entre dos nodos con el algoritmo de Dijkstra.

## Funciones

- Incluye un mapa de ejemplo con ubicaciones y distancias.
- Permite editar, agregar y eliminar tramos desde una tabla.
- Busca una ruta mínima entre el origen y el destino seleccionados.
- Muestra la distancia total y resalta la ruta en el grafo.
- Admite tramos bidireccionales con pesos no negativos.

## Estructura

```text
.
├── backend.py       # Grafo y algoritmo de Dijkstra
├── frontend.py      # Interfaz Streamlit y visualización
├── requirements.txt
└── README.md
```

## Instalación y ejecución

Desde esta carpeta, crea un entorno e instala las dependencias:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En macOS o Linux, activa el entorno con `source .venv/bin/activate`.

Ejecuta la aplicación desde la raíz del proyecto:

```bash
python -m streamlit run frontend.py
```

## Uso

1. Edita las columnas de origen, destino y distancia. Puedes agregar filas al final.
2. Elige el origen y destino debajo de la tabla.
3. Consulta la distancia mínima y la ruta resaltada en la gráfica.

Cada conexión se considera de doble sentido. Los pesos deben ser no negativos. Si el grafo no conecta el origen con el destino, la aplicación lo indicará.
