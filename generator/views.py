from django.shortcuts import render
from .logica_personaje import Personaje # Importamos nuestro "cerebro"

# Vista para la página de inicio (aún no la hemos creado, pero la dejamos lista)
def home(request):
    # Más adelante, esta será nuestra página de bienvenida.
    # Por ahora, la enlazaremos a la creación del personaje.
    return render(request, 'generator/home.html')

# Vista para la página de selección de raza
def elegir_raza(request):
    # 1. Creamos una instancia de nuestra lógica para poder usar sus datos.
    personaje_logic = Personaje()

    # 2. Obtenemos el diccionario de razas con sus descripciones.
    razas = personaje_logic.DESCRIPCIONES_RAZAS

    # 3. Preparamos los datos para enviarlos a la página HTML.
    #    La clave 'razas_items' estará disponible en el HTML.
    context = {
        'razas_items': razas.items()
    }

    # 4. Renderizamos la página HTML y le pasamos los datos.
    return render(request, 'generator/elegir_raza.html', context)