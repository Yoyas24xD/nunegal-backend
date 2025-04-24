# Prueba Técnica - Backend

Este proyecto es una prueba técnica para implementar una API REST que proporcione los detalles de productos similares a un producto dado. El objetivo es exponer un nuevo endpoint que combine dos APIs existentes: una que devuelve los IDs de productos similares y otra que proporciona los detalles de un producto por su ID.

## Descripción

El proyecto consiste en desarrollar una aplicación backend que cumpla con el contrato definido en el archivo [`similarProducts.yaml`](./similarProducts.yaml). La aplicación debe:

1. Exponer un endpoint en el puerto `5000` que devuelva los detalles de los productos similares a un producto dado.
2. Integrarse con las APIs existentes documentadas en [`existingApis.yaml`](./existingApis.yaml).
3. Manejar errores y tiempos de espera de manera resiliente.


## Requisitos

- **Python 3.13** (ver archivo [`.python-version`](./server/.python-version))

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd nunegal-backend/server
   ```
2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```
3. Activa el entorno virtual:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS y Linux:
     ```bash
     source venv/bin/activate
     ```
4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. Crea un archivo `.env` en la raíz del proyecto y define las variables de entorno necesarias.
```bash
API_URL=http://localhost:3001
```

## Ejecución
Para ejecutar la aplicación, utiliza el siguiente comando:

```bash
fastapi dev srt/main.py --port 5000
```

Para ejecutarlo en modo producción, utiliza:
```bash
fastapi run srt/main.py --port 5000
```

## Testing
Para ejecutar los tests primero debes tener instalado `pytest`. Puedes ejecutar los tests con el siguiente comando:

```bash
pip install pytest
```

Luego, ejecuta los tests con:

```bash
cd src
pytest
```


## Documentación de la API
La documentación de la API está disponible en [http://localhost:5000/docs](http://localhost:5000/docs) una vez que la aplicación esté en ejecución en modo desarrollo.

## Consideraciones
- **Asincronismo**: Por defecto, FastAPI utiliza asincronismo para manejar las peticiones. Esto permite que la aplicación maneje múltiples peticiones simultáneamente sin bloquear el hilo principal. Se ha aprovechado esta característica para realizar las peticiones a las APIs externas de manera asincrónica, lo que mejora el rendimiento y la capacidad de respuesta de la aplicación.
- **Manejo de errores**: A la hora de realizar peticiones a la API externa se ha implementado un manejo de errores que ignorara los productos que generen errores o sobrepasen el limite de tiempo establecido. Esto permite que la aplicación siga funcionando incluso si una de las APIs externas no responde o genera un error. Se ha implementado un timeout de 10 segundos para las peticiones a las APIs externas, lo que significa que si una API no responde en ese tiempo, se ignorará y se continuará con la siguiente.
- **Comprobación de tipos**: Se ha utilizado `pydantic` para la validación de los datos de entrada y salida. Esto permite que la aplicación valide automáticamente los datos y genere documentación OpenAPI de manera sencilla. Además, se han definido modelos de datos para las respuestas de las APIs externas, lo que facilita la comprensión y el mantenimiento del código.



## Aspectos a mejorar
- **Testing**: Debido a la falta de tiempo, se ha implementado una suite basica de tests que han sido generados automaticamente. Por lo que se puede trabajar en mejorar este aspecto.
- **Logging**: Se ha implementado un sistema de logging básico, pero se puede mejorar como por ejemplo guardando los logs en un archivo ya que ahora solo estan configurados para mostrarse en consola.
- **Cache**: Se puede implementar un sistema de cache para almacenar los resultados de las peticiones a las APIs externas y así mejorar el rendimiento de la aplicación. Pero no lo he implementado por falta de tiempo.
