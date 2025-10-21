import random
import json
import os
import math
import re

# ==================== LÓGICA DE PERSONAJE ====================
class Personaje:
    DESCRIPCIONES_RAZAS = {
        "Humano": "Versátil y equilibrado, destaca por su adaptabilidad.",
        "Elfo": "Ágil, inteligente, visión infrarroja y resistencia mágica.",
        "Enano": "Robusto, gran fortaleza y resistencia a venenos.",
        "Semiorco": "Muy fuerte, pero menos carismático. Difícil de dejar inconsciente.",
        "Semielfo": "Híbrido adaptable, mezcla talentos élficos y humanos.",
        "Mediano": "Pequeño, muy ágil y perceptivo, difícil de atrapar."
    }
    
    DESCRIPCIONES_SENDAS = {
        "Senda de los Guerreros": "Especialistas en combate físico y uso de armaduras.",
        "Senda de los Bribones": "Expertos en habilidades furtivas y engaño.",
        "Senda de los Diplomáticos": "Dominan las artes sociales y la manipulación.",
        "Senda de los Magos": "Poderosos usuarios de la magia y el saber arcano."
    }
    
    DESCRIPCIONES_PROFESIONES = {
        "Bárbaro": "Guerrero salvaje, fuerza bruta y resistencia.", 
        "Paladín": "Guerrero sagrado, defensor de la justicia.", 
        "Luchador": "Combatiente experto en armas y armaduras.", 
        "Ranger": "Explorador y rastreador experto en naturaleza.",
        "Asesino": "Maestro del sigilo y eliminación rápida.", 
        "Timador": "Especialista en engaños y disfraces.", 
        "Explorador": "Conocedor de la naturaleza y el rastreo.", 
        "Ladrón": "Hábil en robos, trampas y sigilo.",
        "Mentalista": "Manipula la mente y las emociones.", 
        "Agente": "Espía profesional, experto en infiltración.", 
        "Bardo": "Artista y narrador, usa la música como arma.", 
        "Noble": "Líder social, con recursos y privilegios.",
        "Nigromante": "Controla la muerte y las energías oscuras.", 
        "Sacerdote": "Canaliza poder divino para proteger y curar.", 
        "Ilusionista": "Crea ilusiones y confunde a sus enemigos.", 
        "Hechicero": "Maestro de la alquimia y la transmutación."
    }
    
    DESCRIPCIONES_TALENTOS = {
        "Afín a": "El personaje puede desarrollar la habilidad indicada como si estuviese en el grupo de sus habilidades afines.",
        "Afortunado": "Con un 40% de posibilidades, nuestro personaje salva la vida en el último momento de un modo epicamente increíble.",
        "Aguante": "Las hemorragias del personaje nunca superan 1PV por asalto.",
        "Alerta": "El personaje tiene un +20% cada vez que tire percepción para ver o escuchar a otra criatura. Incluso si está dormido.",
        "Ambidiestro": "Permita utilizar cualquier mano para combatir. En el casi de cambiar el arma de mano no perdería ningún dado de ataque.",
        "Arma exótica": "Permite utilizar un arma especificada no convencional. Katanas o armas fantasticas de otras razas.",
        "Atacar y desvanecerse": "Permite hacer una tiradad de esconderse (enfrentada contra su rival) justo despues de sus dados de ataque. Sólo una vez por combate.",
        "Aterrar": "Cualquiera que luche contra este personaje, tendrá que superar una tirada de valentía al ponerse en contacto con el, o tendrá un -3 al TAC durante todo lo que dure este combate.",
        "Ayuda del dios": "El personaje puede gastar esta ayuda una vez por sesión. Puede hacerlo en una ayuda de aventura, o en que una tirada de dado sea cual sea, tenga éxito normal.",
        "Cabalgar": "Luchar desde el caballo da +15PV y +15EXT al ataque. Se puede atacar al caballo; 20 PV y no defiende.",
        "Correr y disparar": "El personaje corre, y además puede disparar como si sólo hubiera andado. Perderá 1 dado de ataque, pero no 2 ni aunque no haya recargado.",
        "Crear pócimas": "Con una tirada de ciencia, y los materiales necesarios; el personaje puede crear pócimas. Por ejemplo de curar +1d6.",
        "Crítico atroz": "Si el personaje está escondido y consigue acercarse a su víctima, y obtiene uno o varios éxitos no bloqueados; puede sacrificar todos los éxitos por 1 solo ataque que haga 3 tiradas de daño del arma. Solo una vez por combate.",
        "Crítico audaz": "Las caras que hacen crítico son 19 y 20; no solo 20.",
        "Desenfundar": "El personaje saca un nuevo arma sin sacrificar sus dados de ataque.",
        "Disparo a la garganta": "Si el personaje está escondido y consigue disparar a su víctima, y obtiene uno o varios éxitos no bloqueados/esquivados; puede sacrificar todos los éxitos por 1 solo ataque que haga 3 tiradas de daño del arma. Solo una vez por combate.",
        "Disparo incapacitante": "Si el personaje consigue un éxito sobre la víctima, esta pierde la capacidad de moverse mientras dure el combate. Solo una vez por combate.",
        "Disparo preciso": "El personaje ignora las restricciones por cobertura cuando dispara.",
        "Dominio armadura": "El personaje puede utilizar las armaduras del nivel que especifique.",
        "Dominio armas": "El personaje puede utilizar el tipo de arma (o estilo de combate, como 2 armas de mano) que especifique.",
        "Dominio 2 armas de mano": "El personaje puede equiparse con dos armas de mano, con tamaño máximo de espada corta. Esto le proporciona 1 dado extra de ataque, pero todos los golpes de cada turno tendrán que alternarse entre un arma y la otra.",
        "Embestir": "Si el pesonaje corre hasta el enemigo, puede hacerle 1 ataque de 1 solo dado, que el enemigo podrá tratar de esquivar. Si el ataque tiene éxito, tendra derecho a un intento de derribo enfrentando su FU contra COR/DES del rival.",
        "En pie": "El personaje se pone en pie sin necesitar de obtener un éxito.",
        "Enardecido": "El personaje nunca huye. Ni siquiera es una opción.",
        "Esquivar proyectiles +1d": "Cuando el personaje esquiva un proyectil, obtiene 1 dado más de esquivar.",
        "Fabricar objeto mágico": "El personaje puede fabricar un objeto con un poder de nv1, siempre que obtenga ayuda de alguien con herrería, carpintería... según la naturaleza del objeto.",
        "Familiar": "El personaje tiene un animal familiar que nunca se separa de él. Un gato, un perro, una araña, un murciélago... con quien puede hablar. El familiar nunca entabla combate.",
        "Furia": "Si un personaje decide entrar en furia suma sus todos dados de defensa a dados de ataque, hasta el final del combate Es útil en multicombate dado que el máximo son 3 ataques contra cada enemigo. Cuando se esté usando furia, el talento crítico audaz deja de tener efecto.",
        "Golpear con escudo": "El personaje puede pasar 1 dado de su defensa (el que suma con el escudo) al ataque. Si este impacta, hará 1d6PV. Recuerda que hay que decidir cuántos dados vas a tirar a la vez.",
        "Hablar con los animales": "El personaje puede hablar con los animales... aunque eso no significa que les caiga bien, o que lo quieran ayudar.",
        "Hábil": "El personaje obtiene 1 punto de atributo que no sobrepase los límites máximos.",
        "Habilidad ambigua": "Permite desarrollar una habilidad prohibida como si fuese una habilidad no afín.",
        "Hipnosis": "Necesita 10 minutos y el objetivo se presta a ello; lo puede hipnotizar. El objetivo no entrará en combate y cualquier grito o movimiento lo despertará.",
        "Invulnerable a venenos": "El personaje es inmune a todo tipo de venenos naturales.",
        "Labia": "El personaje suma +10EXT a mentir, seducir, convencer, persuadir y charlatanería.",
        "Lanzar enemigo": "Si el personaje consigue realizar un ataque especial con éxito, puede agarrar al enemigo y lanzarlo a 3 metros. Para ellos tirará FU enfrentado a COR. La caída normal hace 1d4PV y cae derribado.",
        "Leer los labios": "El personaje puede leer los labios con tanta soltura como quien escucha a alguien que le esté hablando.",
        "Levantar 1 muerto": "El personaje puede levantar un zombie que aparece inmediatamente de las entrañas de la tierra para servirlo fielmente.",
        "Liderazgo": "El personaje obtiene un +20 en sus tiradas de liderazgo.",
        "Luchar desnudo": "El personaje lucha sin armadura pero su propia constitución hace que su cuerpo le proporcione 2P.Arm.",
        "Luchar sin armas": "El personaje lucha sin armas pero su marcialidad le permite bloquear golpes, por lo que puede bloquear como si estuviese armado.",
        "Mantener concentración": "Cuando el personaje esta concentrado dominando un hechizo y sufre daño, puede realizar una tirada de liderazgo para mantener la concentración.",
        "Maximizar conjuro": "Solo una vez por sesión. El conjuro tiene el doble de alcance, de área o de tiempo de duración.",
        "Memoria fotográfica": "El personaje recuerda a la perfección todos los detalles. Incluso puede hacer tiradas de percepción a posteriori.",
        "Percibir peligro": "El personaje puede tirar percepción para intuir emboscadas o trampas en un área de 15 metros.",
        "Poder adicional nv1": "El personaje obtiene sin gastar puntos, un hechizo de nv1 de cualquier saber, que no le cuenta para los máximos de memoria.",
        "Poder aumentado": "El personaje obtiene 3 PM adicionales.",
        "Primero en apuntar": "El personaje puede disparar su arma a distancia antes incluso que la fase de magia del turno.",
        "Puñetazo aturdidor": "Esta habilidad solo puede declararse 1 vez por combate. Si el personaje obtiene 1 ataque exitoso que no es defendido, ignorar el resto de éxitos pero conseguir 1 solo golpe que aturde a su rival durante 4 turnos.",
        "Reacción rápida": "El personaje siempre tiene un arma a mano (aunque esté dormido) y siempre tendrá derecho a una tirada de percepción enfrentada a esconderse de cualquiera que quiera atacarle en sigilo.",
        "Recarga rápida": "El personaje no pierde 1dado de ataque a distancia por disparar proyectiles en cada turno de forma consecutiva.",
        "Robusto": "El personaje obtiene 5 PV adicionales.",
        "Saber de": "El personaje tiene acceso a las listas de hechizo del saber indicado.",
        "Seductor": "El personaje obtiene +25 EXT en la habilidad de seducir, además de un +1 en aspecto; y mínimo aspecto 5 si su atributo es menor.",
        "Sentido del ritmo": "El personaje tiene un don natural para la música, lo que le otorga un +50 a su habilidad para Tocar Instrumentos.",
        "Separarse": "El personaje no necesita de un ataque exitoso no bloqueado para destrabarse del combate. Esto no genera un golpe fortuito.",
        "Sin inconsciencia": "El personaje no entra en estado de inconsciencia cuando le quedan menos de 5PV.",
        "Sombra": "El personaje no necesita un entorno propicio para esconderse. Puede hacerlo a la luz del día y al descubierto.",
        "Táctico": "El personaje puede retrasar su turno exactamente al momento que decida.",
        "Visión infrarroja élfica": "Esta visión infrarroja permite actuar en la oscuridad con un -20Hab. contra cualquier fuente de calor. Con el resto de objetos a -60.",
        "Visión infrarroja enana": "Esta visión infrarroja permite actuar en la oscuridad con un -35 ignorando si emite calor o no."
    }
    
    ATRIBUTOS_FISICOS = ["FUERZA", "CORPULENCIA", "DESTREZA", "RAPIDEZ"]
    ATRIBUTOS_MENTALES = ["RAZONAMIENTO", "MEMORIA", "PODER"]
    ATRIBUTOS_SOCIALES = ["PERCEPCIÓN", "CARISMA"]

    TABLA_BONIFICADORES = {
        "FUERZA": {
            "Bonif. daño": ["-(1d4+2)", "-1d4", "0", "0", "0", "0", "+1d4", "+1d4", "+1d6", "+1d4+2"], 
            "Bonif. ataque": [-15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
        },
        "CORPULENCIA": {
            "Puntos de vida": [5, 6, 8, 10, 12, 14, 16, 18, 20, 22]
        },
        "DESTREZA": {
            "Dados defensa": [0, 1, 1, 2, 2, 2, 2, 2, 2, 3], 
            "Bonif. ataque técnico": [-15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
        },
        "RAPIDEZ": {
            "Iniciativa": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
            "Dados ataque": [1, 1, 1, 2, 2, 2, 2, 2, 3, 3], 
            "Dados esquiva": [1, 1, 1, 2, 2, 2, 2, 2, 3, 3], 
            "Bonif. esquivar": [-15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
        },
        "RAZONAMIENTO": {
            "Índice éxito hechizo": ["0", "0", "5%", "20%", "40%", "55%", "70%", "80%", "85%", "90%"], 
            "Ayudas": ["0", "0", "1/30%", "1/40%", "1/50%", "2/50%", "2/50%", "2/60%", "3/60%", "3/65%"]
        },
        "MEMORIA": {
            "Nº hechizos": [1, 2, 3, 5, 6, 8, 9, 10, 11, 13], 
            "Bonif. experiencia": ["+1", "+1", "+2", "+2", "+3", "+3", "+4", "+4", "+5", "+5"]
        },
        "PODER": {
            "Índice éxito plegaria": ["0", "0", "5%", "20%", "40%", "55%", "70%", "80%", "85%", "90%"], 
            "Puntos de magia": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
            "Valentía": ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "95%"]
        },
        "PERCEPCIÓN": {
            "Percepción": ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "95%"], 
            "Bonif. ataque distancia": [-15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
        }
    }
    
    LISTAS_SABERES = {
        "Saber de la oscuridad": ["Oscuridad", "Aturdir", "Horror", "Vampiro", "Horror en masa", "Levantar muertos", "Marchitar", "Invocar demonio", "Portal dimensional", "Devorar almas"],
        "Saber de la destrucción": ["Rayo", "Entumecer extremidad", "Explosión", "Cegar", "Mutilación", "Convocación múltiple", "Congelar área", "Invocar wyrm", "Muerte", "Cataclismo"],
        "Saber de la protección": ["Escudo", "Alivio", "Curación", "Purificar", "Acelerar", "Regeneración", "Curación en masa", "Área escudo", "Detener el tiempo", "Viaje temporal"],
        "Saber de la canalización": ["Modificar clima", "Armas espirituales", "Proyectil múltiple", "Valentía de grupo", "Calmar en masa", "Muro de piedra", "Terremoto", "Convocar gran águila", "Lluvia de fuego", "Devolver el alma"],
        "Saber de encantamientos": ["Imagen desdoblada", "Detectar mecanismo", "Invisibilidad", "Potenciar armas", "Coraza de estrellas", "Transporte de grupo", "Visión verdadera", "Invocar elemental", "Proyectar enemigos", "Invulnerabilidad"],
        "Saber de lo arcano": ["Proyectil", "Áura en llamas", "Bóla de fuego", "Comunicación astral", "Presagio en las llamas", "Derretir la piedra", "Desintegración selectiva", "Convocar dragón menor", "Implosión", "Tormenta de masacre"],
        "Saber de la alquimia": ["Abrir cerraduras", "Telekinesis", "Devolver el daño", "Dormir", "Telaraña", "Metal a agua", "Clonación", "Convocar golem", "Derretir los huesos", "Lluvia de ácido"],
        "Saber de la transmutación": ["Jaula mágica", "Alterar atributo", "Licantropía", "Niebla consumidora", "Respirar", "Armadura de sangre de Dragón", "Cuerpo gigante", "Convocar mantícora", "Ilusión verdadera", "Nube de inestabilidad de la naturaleza"],
        "Saber del control": ["Ilusión objeto", "Convencer", "Alucinación", "Hipnosis", "Dominio"],
        "Saber de las sombras": ["Silencio", "Sombra Pegajosa", "Rostro Robado", "Duplicado Umbrío", "Visión del pasado"],
        "Saber de la armonía": ["Valentía", "Miedo", "Danza Irresistible", "Grito de la Discordia", "Silencio de Batalla"],
        "Saber de la naturaleza": ["Hablar con los animales", "Rastreo verdadero", "Control de animales", "Correr sobre elementos", "Convocar jauría"],
        "Saber de luz": ["Orbe de luz", "Aura de pureza", "Espada de luz", "Espíritu radiante", "Exorcismo"]
    }

    ARMADURAS = {
        "Nivel 1": {
            "piezas": [("Botas de cuero", 0.4), ("Chaleco cuero", 0.8), ("Guantes de cuero", 0.4), ("Capucha de cuero", 0.4)]
        },
        "Nivel 2": {
            "piezas": [("Botas de cuero duro", 0.6), ("Torso de cuero duro", 1.2), ("Antebrazos de cuero duro", 0.6), ("Casco de cuero", 0.6)]
        },
        "Nivel 3": {
            "Bezantada": {
                "piezas": [("Grebas bezanteadas", 0.8), ("Torso bezanteada", 1.6), ("Protección de brazo reforzado", 0.8), ("Casco cuero y hierro", 0.8)]
            },
            "Malla": {
                "piezas": [("Grebas metálicas", 1.0), ("Cota de malla", 2.0), ("Brazaletes metálicos", 1.0), ("Casco metálico", 1.0)]
            }
        },
        "Nivel 4": {
            "Coraza": {
                "piezas": [("Grebas reforzadas", 1.2), ("Coraza", 2.4), ("Antebrazo con puño metálico", 1.2), ("Yelmo metálico cerrado", 1.2)]
            },
            "Placas": {
                "piezas": [("Botas acorazadas", 1.4), ("Torso de placas", 2.8), ("Brazo acorazado", 1.4), ("Yelmo cerrado y reforzado", 1.4)]
            }
        }
    }
    
    ARMAS = [
        {"nombre": "Alfanje", "categoria": "1 mano", "fuerza": 5, "at": True, "daño": "1d6+2", "critico": "corte", "alcance": None},
        {"nombre": "Bola y cadena", "categoria": "1 mano", "fuerza": 4, "at": False, "daño": "1d6+1", "critico": "aplastamiento", "alcance": None},
        {"nombre": "Cimitarra", "categoria": "1 mano", "fuerza": 4, "at": True, "daño": "1d8", "critico": "corte", "alcance": None},
        {"nombre": "Cuchillo", "categoria": "1 mano", "fuerza": 1, "at": True, "daño": "1d3", "critico": "corte", "alcance": None},
        {"nombre": "Daga", "categoria": "1 mano", "fuerza": 2, "at": True, "daño": "1d4+1", "critico": "corte", "alcance": None},
        {"nombre": "Espada ancha", "categoria": "1 mano", "fuerza": 5, "at": False, "daño": "1d8", "critico": "corte", "alcance": None},
        {"nombre": "Espada corta", "categoria": "1 mano", "fuerza": 3, "at": True, "daño": "1d6", "critico": "corte", "alcance": None},
        {"nombre": "Espada larga", "categoria": "1 mano", "fuerza": 5, "at": False, "daño": "1d8", "critico": "corte", "alcance": None},
        {"nombre": "Espada ropera", "categoria": "1 mano", "fuerza": 5, "at": False, "daño": "1d8", "critico": "corte", "alcance": None},
        {"nombre": "Garrote", "categoria": "1 mano", "fuerza": 3, "at": False, "daño": "1d6", "critico": "aplastamiento", "alcance": None},
        {"nombre": "Hacha de batalla", "categoria": "1 mano", "fuerza": 4, "at": False, "daño": "1d6+1", "critico": "corte", "alcance": None},
        {"nombre": "Hacha de mano", "categoria": "1 mano", "fuerza": 3, "at": False, "daño": "1d6", "critico": "corte", "alcance": None},
        {"nombre": "Lanza corta", "categoria": "1 mano", "fuerza": 5, "at": True, "daño": "1d8+1", "critico": "penetración", "alcance": None},
        {"nombre": "Lanza de jinete", "categoria": "1 mano", "fuerza": 7, "at": True, "daño": "1d10+2", "critico": "penetración", "alcance": None},
        {"nombre": "Main gauche", "categoria": "1 mano", "fuerza": 2, "at": True, "daño": "1d4", "critico": "penetración", "alcance": None},
        {"nombre": "Mangual", "categoria": "1 mano", "fuerza": 3, "at": False, "daño": "1d6", "critico": "aplastamiento", "alcance": None},
        {"nombre": "Maza", "categoria": "1 mano", "fuerza": 5, "at": False, "daño": "1d8", "critico": "aplastamiento", "alcance": None},
        {"nombre": "Pico militar", "categoria": "1 mano", "fuerza": 4, "at": False, "daño": "1d6+1", "critico": "penetración", "alcance": None},
        {"nombre": "Sable", "categoria": "1 mano", "fuerza": 4, "at": True, "daño": "1d6+1", "critico": "corte", "alcance": None},
        {"nombre": "Tridente", "categoria": "1 mano", "fuerza": 5, "at": True, "daño": "1d8", "critico": "penetración", "alcance": None},
        {"nombre": "Alabarda", "categoria": "2 manos", "fuerza": 8, "at": True, "daño": "1d8+2", "critico": "corte/penetración", "alcance": None},
        {"nombre": "Espada larga", "categoria": "2 manos", "fuerza": 5, "at": True, "daño": "1d10", "critico": "corte", "alcance": None},
        {"nombre": "Gran clava", "categoria": "2 manos", "fuerza": 5, "at": False, "daño": "2d6", "critico": "aplastamiento", "alcance": None},
        {"nombre": "Gran hacha", "categoria": "2 manos", "fuerza": 8, "at": False, "daño": "2d6+2", "critico": "corte", "alcance": None},
        {"nombre": "Gran martillo", "categoria": "2 manos", "fuerza": 7, "at": False, "daño": "1d10+3", "critico": "aplastamiento", "alcance": None},
        {"nombre": "Guja", "categoria": "2 manos", "fuerza": 7, "at": True, "daño": "1d10+2", "critico": "corte", "alcance": None},
        {"nombre": "Hacha de batalla", "categoria": "2 manos", "fuerza": 4, "at": False, "daño": "1d8+1", "critico": "corte", "alcance": None},
        {"nombre": "Lanza larga", "categoria": "2 manos", "fuerza": 6, "at": True, "daño": "1d10+1", "critico": "penetración", "alcance": None},
        {"nombre": "Arco corto", "categoria": "arco", "fuerza": 3, "at": True, "daño": "1d6", "critico": "penetración", "alcance": "50m"},
        {"nombre": "Arco largo", "categoria": "arco", "fuerza": 4, "at": True, "daño": "1d8+1", "critico": "penetración", "alcance": "100m"},
        {"nombre": "Ballesta ligera", "categoria": "ballesta", "fuerza": 2, "at": False, "daño": "1d8", "critico": "penetración", "alcance": "60m"},
        {"nombre": "Ballesta pesada", "categoria": "ballesta", "fuerza": 4, "at": False, "daño": "1d10+1", "critico": "penetración", "alcance": "120m"},
        {"nombre": "Katana", "categoria": "exótica", "fuerza": 6, "at": True, "daño": "1d10+2", "critico": "corte", "alcance": None},
        {"nombre": "Látigo", "categoria": "exótica", "fuerza": 3, "at": True, "daño": "1d4", "critico": "corte", "alcance": None},
        {"nombre": "Chakram", "categoria": "exótica", "fuerza": 4, "at": True, "daño": "1d6", "critico": "corte", "alcance": "20m"},
        {"nombre": "Nunchaku", "categoria": "exótica", "fuerza": 4, "at": True, "daño": "1d6+1", "critico": "aplastamiento", "alcance": None},
    ]

    TALENTOS_RAZAS = {
        "Humano": [], 
        "Elfo": ["Visión infrarroja élfica", "Invulnerable a venenos"], 
        "Enano": ["Visión infrarroja enana", "Resistencia a venenos"], 
        "Semiorco": ["Sin inconsciencia"], 
        "Semielfo": ["Visión infrarroja élfica", "Resistencia a venenos"], 
        "Mediano": []
    }
    
    TALENTOS_SENDAS = {
        "Senda de los Guerreros": ["Dominio armaduras nv2", "Dominio armas 1M y 2M", "Dominio escudo", "Dominio de arco o ballesta", "Dominio 2 armas de mano"], 
        "Senda de los Bribones": ["Dominio armaduras nv1", "Dominio armas 1M", "Dominio arco corto"], 
        "Senda de los Diplomáticos": ["Dominio armadura nv1", "Dominio armas 1M"], 
        "Senda de los Magos": ["Dominio dagas"]
    }
    
    TALENTOS_PROFESIONES = {
        "Bárbaro": [], 
        "Paladín": ["Dominio armadura nv4", "Saber de luz"], 
        "Luchador": ["Dominio armadura nv4"], 
        "Ranger": ["Dominio armaduras nv3", "Afín a Rastrear", "Afín a Trampear"], 
        "Asesino": ["Dominio 2 armas de mano"], 
        "Timador": ["Afín a Mentir", "Afín a Perspicacia", "Afín a Disfrazarse"], 
        "Explorador": ["Afín con arco largo o ballesta", "Saber de la naturaleza"], 
        "Ladrón": [], 
        "Mentalista": ["Saber del control"], 
        "Agente": ["Dominio armadura nv2", "Afín a Esconderse"], 
        "Bardo": ["Saber de la armonía", "Sentido del ritmo"], 
        "Noble": ["Dominio armadura nv4"], 
        "Nigromante": ["Saber de la oscuridad", "Saber de la destrucción"], 
        "Sacerdote": ["Saber de la protección", "Saber de la canalización"], 
        "Ilusionista": ["Saber de lo arcano", "Saber de encantamientos"], 
        "Hechicero": ["Saber de la alquimia", "Saber de la transmutación"]
    }
    
    LIMITES_POR_RAZA = {
        "Humano": {"FUERZA": 8, "CORPULENCIA": 8, "DESTREZA": 8, "RAPIDEZ": 8, "RAZONAMIENTO": 9, "MEMORIA": 8, "PODER": 8, "PERCEPCIÓN": 8, "CARISMA": 9}, 
        "Elfo": {"FUERZA": 7, "CORPULENCIA": 6, "DESTREZA": 9, "RAPIDEZ": 10, "RAZONAMIENTO": 9, "MEMORIA": 9, "PODER": 8, "PERCEPCIÓN": 9, "CARISMA": 8}, 
        "Enano": {"FUERZA": 9, "CORPULENCIA": 10, "DESTREZA": 8, "RAPIDEZ": 7, "RAZONAMIENTO": 8, "MEMORIA": 8, "PODER": 8, "PERCEPCIÓN": 6, "CARISMA": 8}, 
        "Semiorco": {"FUERZA": 10, "CORPULENCIA": 9, "DESTREZA": 7, "RAPIDEZ": 8, "RAZONAMIENTO": 7, "MEMORIA": 8, "PODER": 8, "PERCEPCIÓN": 8, "CARISMA": 6}, 
        "Semielfo": {"FUERZA": 8, "CORPULENCIA": 8, "DESTREZA": 8, "RAPIDEZ": 8, "RAZONAMIENTO": 9, "MEMORIA": 8, "PODER": 8, "PERCEPCIÓN": 8, "CARISMA": 10}, 
        "Mediano": {"FUERZA": 5, "CORPULENCIA": 5, "DESTREZA": 10, "RAPIDEZ": 9, "RAZONAMIENTO": 8, "MEMORIA": 8, "PODER": 8, "PERCEPCIÓN": 9, "CARISMA": 8}
    }
    
    PUNTOS_POR_SENDA = {
        "Senda de los Guerreros": (27, 13, 10), 
        "Senda de los Bribones": (25, 16, 10), 
        "Senda de los Diplomáticos": (21, 19, 14), 
        "Senda de los Magos": (17, 22, 8)
    }
    
    TALENTOS_LISTA = {
        "Humano": ["Hábil", "Recarga rápida", "Primero en apuntar", "Desenfundar", "Táctico", "Labia", "Arma exótica", "Ambidiestro", "Cabalgar"], 
        "Elfo": ["Ambidiestro", "Cabalgar", "Correr y disparar", "Sombra", "Recarga rápida", "Primero en apuntar", "Poder adicional nv1", "Arma exótica", "Esquivar proyectiles +1d."], 
        "Enano": ["Ambidiestro", "Enardecido", "Aguante", "Robusto", "Embestir", "Puñetazo aturdidor"], 
        "Semiorco": ["Aterrar", "Aguante", "Embestir", "Puñetazo aturdidor", "Lanzar enemigo"], 
        "Semielfo": [], 
        "Mediano": ["Ambidiestro", "Afortunado", "Sombra", "Alerta", "Memoria fotográfica", "Separarse", "Esquivar proyectiles +1d", "Sombra"], 
        "Senda de los Guerreros": ["Crítico audaz", "Embestir", "Luchar sin armas", "Golpear con escudo", "Ataque desde el suelo", "Seductor", "Habilidad ambigua"], 
        "Bárbaro": ["Luchar desnudo", "Furia", "Robusto"], 
        "Paladín": ["Liderazgo"], 
        "Luchador": ["Robusto", "Dominio 2 armas de mano", "Luchar con cualquier arma"], 
        "Ranger": ["Dominio 2 armas de mano", "Percibir peligro", "Disparo preciso"], 
        "Senda de los Bribones": ["Crítico audaz", "Reflejos de gato", "Separarse", "Atacar desde el suelo", "Luchar con 2 armas cortas", "Correr y disparar", "Habilidad ambigua", "Disparo incapacitante"], 
        "Asesino": ["Atacar y desvanecerse", "Crítico atroz", "En pie"], 
        "Timador": ["Leer los labios"], 
        "Explorador": ["Hablar con los animales", "Disparo preciso", "Disparo a la garganta", "Dominio 2 armas de mano"], 
        "Ladrón": ["Atacar y desvanecerse", "Percibir peligro", "Disparo a bocajarro", "En pie"], 
        "Senda de los Diplomáticos": ["Afín a Intimidar", "Afín a Ciencias", "Dominio escudo", "Dominio armas largas", "Habilidad ambigua", "Gremio"], 
        "Mentalista": ["Afín a 1 habilidad de estudio", "Dominio armaduras nv2"], 
        "Agente": ["Dominio 2 armas de mano", "Dominio arco largo"], 
        "Bardo": ["Seductor", "Dominio arco largo"], 
        "Noble": ["Dominio armas 2M", "Poder"], 
        "Senda de los Magos": ["Poder aumentado", "Fabricar objeto mágico", "Maximizar conjuro", "Habilidad ambigua", "Reacción rápida"], 
        "Nigromante": ["Levantar 1 muerto", "Hablar con espíritu"], 
        "Sacerdote": ["Hablar con los animales", "Ayuda del dios", "Dominio armadura nv3"], 
        "Ilusionista": ["Familiar", "Mantener concentración"], 
        "Hechicero": ["Hipnosis", "Crear pócimas"]
    }
    
    TALENTOS_NUEVOS_POR_RAZA = {
        "Humano": 2, 
        "Elfo": 0, 
        "Enano": 1, 
        "Semiorco": 1, 
        "Semielfo": 1, 
        "Mediano": 3
    }
    
    HABILIDADES = {
        "Físicas": ["Intimidar", "Herrería", "Carpintería", "Curtir", "Saltar", "Trepar", "Nadar", "Construcción", "Resistir", "Arma 1", "Arma 2", "Arma 3", "Arma 4", "Luchar sin armas"], 
        "Subterfugio": ["Esconderse", "Cerrajería", "Trampear", "Robar", "Rastrear", "Falsificar", "Insultar", "Tratar animal", "Cuerdas", "Desactivar"], 
        "Generales": ["Valentía", "Profesional", "Riqueza", "Esquivar"], 
        "Diplomáticas": ["Idioma nuevo", "Perspicacia", "Mentir", "Persuadir", "Negociar", "Derecho", "Disfrazarse", "Tocar Instrumento", "Convencer", "Seducir", "Interrogar", "Charlatanería"], 
        "Estudio": ["Primeros Aux", "Medicina", "Buscar en libros", "Ciencias", "Crear Pócimas", "Investigar", "Tasar", "Ritual", "Orfebrería", "Localizar Documento", "Conocimientos"]
    }
    
    HABILIDADES_BASE_X = {
        "Intimidar": 3, "Herrería": 0, "Carpintería": 0, "Curtir": 0, "Saltar": 4, "Trepar": 4, "Nadar": 4, "Construcción": 0, "Resistir": 2, "Arma 1": 2, "Arma 2": 0, "Arma 3": 0, "Arma 4": 0, "Luchar sin armas": 4, "Esconderse": 2, "Cerrajería": 2, "Trampear": 2, "Robar": 2, "Rastrear": 2, "Falsificar": 0, "Insultar": 3, "Tratar animal": 2, "Cuerdas": 2, "Desactivar": 2, "Valentía": 0, "Profesional": 0, "Riqueza": 1, "Esquivar": 2, "Idioma nuevo": 0, "Perspicacia": 2, "Mentir": 2, "Persuadir": 2, "Negociar": 2, "Derecho": 1, "Disfrazarse": 1, "Tocar Instrumento": 0, "Convencer": 2, "Seducir": 2, "Interrogar": 2, "Charlatanería": 2, "Primeros Aux": 4, "Medicina": 0, "Buscar en libros": 8, "Ciencias": 0, "Crear Pócimas": 0, "Investigar": 0, "Tasar": 2, "Ritual": 0, "Orfebrería": 0, "Localizar Documento": 4, "Conocimientos": 2
    }
    
    HABILIDAD_ATRIBUTO_MAP = {
        "Intimidar": "CORPULENCIA", "Herrería": "FUERZA", "Carpintería": "RAZONAMIENTO", "Curtir": "DESTREZA", "Saltar": "RAPIDEZ", "Trepar": "RAPIDEZ", "Nadar": "DESTREZA", "Construcción": "RAZONAMIENTO", "Resistir": "CORPULENCIA", "Luchar sin armas": "FUERZA", "Esconderse": "RAZONAMIENTO", "Cerrajería": "DESTREZA", "Trampear": "DESTREZA", "Robar": "DESTREZA", "Rastrear": "PERCEPCIÓN", "Falsificar": "PERCEPCIÓN", "Insultar": "RAZONAMIENTO", "Tratar animal": "CARISMA", "Cuerdas": "DESTREZA", "Desactivar": "RAZONAMIENTO", "Valentía": "PODER", "Profesional": "RAZONAMIENTO", "Riqueza": "RAZONAMIENTO", "Esquivar": "RAPIDEZ", "Idioma nuevo": "MEMORIA", "Perspicacia": "PERCEPCIÓN", "Mentir": "CARISMA", "Persuadir": "ASPECTO", "Negociar": "CARISMA", "Derecho": "MEMORIA", "Disfrazarse": "RAZONAMIENTO", "Tocar Instrumento": "DESTREZA", "Convencer": "RAZONAMIENTO", "Seducir": "ASPECTO", "Interrogar": "PODER", "Charlatanería": "CARISMA", "Primeros Aux": "RAZONAMIENTO", "Medicina": "MEMORIA", "Buscar en libros": "RAZONAMIENTO", "Ciencias": "MEMORIA", "Crear Pócimas": "MEMORIA", "Investigar": "RAZONAMIENTO", "Tasar": "PERCEPCIÓN", "Ritual": "PODER", "Orfebrería": "DESTREZA", "Localizar Documento": "MEMORIA", "Conocimientos": "MEMORIA", "Arma 1": "FUERZA", "Arma 2": "FUERZA", "Arma 3": "FUERZA", "Arma 4": "FUERZA"
    }
    
    BONO_POR_VALOR_ATRIBUTO = [-15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
    
    HABILIDAD_COLORES = {
        "Físicas": "#FFD700", 
        "Subterfugio": "#FF5555", 
        "Generales": "#CCCCCC", 
        "Diplomáticas": "#55A8FF", 
        "Estudio": "#66DD77"
    }
    
    SendaRestricciones = {
        "Senda de los Guerreros": {"Físicas": 6, "Subterfugio": 4, "Diplomáticas": 4, "Generales": 4, "Estudio": 0}, 
        "Senda de los Diplomáticos": {"Físicas": 4, "Subterfugio": 0, "Diplomáticas": 6, "Generales": 4, "Estudio": 4}, 
        "Senda de los Bribones": {"Físicas": 4, "Subterfugio": 6, "Diplomáticas": 0, "Generales": 4, "Estudio": 4}, 
        "Senda de los Magos": {"Físicas": 0, "Subterfugio": 4, "Diplomáticas": 4, "Generales": 4, "Estudio": 6}
    }
    
    TAC_TABLE = {
        0: "20 (crítico)", 5: "20+", 10: "19+", 15: "18+", 20: "17+", 25: "16+", 30: "15+", 35: "14+", 40: "13+",
        45: "12+", 50: "11+", 55: "10+", 60: "09+", 65: "08+", 70: "07+", 75: "06+", 80: "05+", 85: "04+",
        90: "04+ (-1)", 95: "04+ (-2)", 100: "04+ (-3)", 105: "04+ (-4)", 110: "04+ (-5)"
    }

    RASGOS_ESPECIALES = {
        1: "Licantropía: El personaje se transforma en una bestia bajo la luna llena, ganando fuerza y ferocidad, pero perdiendo control. No heriría a ningún amigo por el que tenga afecto.",
        2: "Detectar Mentiras: Percibe cuando alguien miente con un 80% de precisión sin necesidad de tirar perspicacia.",
        3: "Flotar: Puede levitar unos centímetros del suelo, ignorando terrenos peligrosos.",
        4: "Piel de Piedra: +2 de armadura natural. Su piel es grisácea. Pierde su efecto si usa cualquier otro tipo de armadura.",
        5: "Medium: Tiene la capacidad de concentrarse y hablar con los muertos una vez al día.",
        6: "Invisibilidad Momentánea: Puede volverse invisible durante 2 minutos. Requiere estar desnudo. No se puede atacar ni lanzar hechizos en este estado.",
        7: "Regeneración: Recupera 1 PV por cada hora fuera de combate.",
        8: "Telepatía: Lee mentes superficiales (emociones, intenciones básicas).",
        9: "Control de Sombras: Manipula las sombras para crear ilusiones menores.",
        10: "Inmunidad al Veneno: No sufre efectos de venenos o toxinas. Si eres un elfo, tira de nuevo.",
        11: "Manos Ardientes: Su contacto quita 1d4 PV y puede encender fuego. Las palmas de sus manos se vuelven rojas.",
        12: "Salto Sobrenatural: Salta hasta 10 metros en cualquier dirección.",
        13: "Voz Hipnótica: Puede persuadir o sugestionar con +20% en habilidades sociales.",
        14: "Visión Nocturna Mejorada: Ve en la oscuridad total como si fuera de día.",
        15: "Piel Cambiante: Cambia el color de su piel para camuflarse (+30% esconderse con ropa, o +80 desnudo).",
        16: "Alquimia Innata: El personaje tendrá una colección de ingredientes con los que se pueden hacer todo tipo de pócimas menores.",
        17: "Afinidad con Animales: Los animales no lo atacan a menos que sean provocados.",
        18: "Doble Corazón: Sufre la mitad de asaltos de aturdimiento (redondeando hacia abajo), pero en cada hemorragia tendrá un +1PV por turno.",
        19: "Sangre Ácida: Al recibir daño crítico, salpica sangre que quema (1d4 daño que ignora armadura).",
        20: "Olfato de lobo: +20 a las tiradas de percepción en las que intervenga el olfato.",
        21: "Inmunidad al Miedo: +20 a cualquier tirada de valentía.",
        22: "Toque Curativo: Cura 1d6 PV a un aliado 1 vez al día.",
        23: "Reflejos Felinos: +5 a esquivar.",
        24: "Susurros del Viento: Escucha conversaciones a larga distancia si el viento lo permite.",
        25: "Pesadilla Viva: +10 a intimidar.",
        26: "Piel Elástica: Puede usar armaduras de talla +1 ó -1 corpulencia.",
        27: "Invocar Filo de fuego: Si el personaje gasta 1 acción, su arma se rodea de llamas y suma 2 puntos de daño.",
        28: "Respiración Bajo el Agua: No necesita aire para respirar en ambientes acuáticos.",
        29: "Ojos de Águila: Ve detalles a 1 kilómetro de distancia. +50 a percepción para ver algo a la lejanía.",
        30: "Robo de Energía: Al golpear, roba 1 PV al enemigo y lo cura.",
        31: "Inmunidad al Fuego: No sufre daño por llamas o calor extremo.",
        32: "Caminar sobre Agua: Puede cruzar líquidos como si fueran sólidos.",
        33: "Grito Atronador: Una vez al día, emite un grito que aturde 1 ronda a todos en 5 metros.",
        34: "Manipular Plantas: Hace que las plantas crezcan o se enreden a voluntad.",
        35: "Sueño Profético: Tiene visiones del futuro mientras duerme (vagas pero útiles).",
        36: "Pies Silenciosos: +40 a esconderse cuando la intención sea moverse en silencio.",
        37: "Afinidad Elemental (Fuego/Hielo/Rayo): Puede lanzar un hechizo de proyectil básico 1 vez al día.",
        38: "Mimetismo de Voz: Imita cualquier voz escuchada con perfección.",
        39: "Huesos Indestructibles: No puede sufrir fracturas o roturas óseas.",
        40: "Aura de Paz: 30% de posibilidades de que su grupo no sea atacado por enemigos hostiles.",
        41: "Control de Gravedad: Puede reducir su peso a la mitad o doblarlo.",
        42: "Doble Personalidad: Bajo estrés, adopta otra personalidad con habilidades sociales distintas.",
        43: "Piel de Camaleón: Se camufla automáticamente en entornos naturales (+60 a esconderse) si no se mueve y va desnudo.",
        44: "Sombra Viviente: Su sombra puede actuar independientemente (espiar, distraer) en un rango de 50m. Si se le dispara un foco de luz, vuelve a su portador.",
        45: "Sangre Regenerativa: Con unas gotas de su sangre y agua se pueden hacer pócimas que curen 1d4 PV.",
        46: "Invocar Niebla: Crea una neblina densa en 10 metros (1 vez/día).",
        47: "Dedos de Ladrón: +30% en habilidades de robo y cerrajería.",
        48: "Resistencia al Frío: No sufre daño por congelación o climas gélidos.",
        49: "Alma Gemela: Elige un compañero para tener una afinidad sensorial y sentimental absoluta con él.",
        50: "Inmunidad a la Magia: +2 a todas las tiradas enfrentadas para resistirse a los hechizos.",
        51: "Telekinesis Básica: Mueve objetos pequeños (hasta 1 kg) con la mente a un ritmo muy lento.",
        52: "Pacto con un Espíritu: Un espíritu menor lo asesora en sueños.",
        53: "Reconexión: Se recupera del aturdimiento dos rondas antes.",
        54: "Manos Pegajosas: Puede escalar superficies verticales sin equipo.",
        55: "Ventrílocuo: Puede lanzar su voz hasta 20 metros de distancia.",
        56: "Compartir daño: Puede darle puntos de vida a cualquier compañero solo con tocarlo.",
        57: "Golpes devastadores: El modificador de daño por fuerza aumenta una categoría.",
        58: "Susurro de las Hojas: Entiende el lenguaje de las plantas (mensajes simples).",
        59: "Ilusión Doppelganger: Crea una copia ilusoria de sí mismo durante 10 minutos que no se puede mover.",
        60: "Paladar perfecto: Identifica cualquier pócima, veneno o sustancia al probar una cantidad mínima.",
        61: "Marca de la Muerte: Marca a un enemigo y cualquiera que le ataque recibirá +1 al TAC.",
        62: "Afinidad con los Muertos: Los no muertos lo ignoran a menos que los ataque.",
        63: "Doble Salto: Puede saltar dos veces en el aire antes de caer.",
        64: "Ceguera Temporal: Una vez al día, surge un destello radiante que puede aturdir a enemigos cercanos por 2 turnos.",
        65: "Invocar Alimento: Crea comida y agua suficiente para una persona 1 vez al día.",
        66: "Sexto Sentido: Con una tirada de percepción, siente peligros inminentes (trampas, emboscadas).",
        67: "Control de Insectos: Atrae o repele insectos a voluntad.",
        68: "Sin Huellas: No deja rastros físicos al moverse (esto incluye olores).",
        69: "Lenguaje Universal: Entiende y habla todos los idiomas básicos.",
        70: "Inmunidad a la Electricidad: No sufre daño por rayos o descargas.",
        71: "Fuerza de Voluntad: +30 a resistir.",
        72: "Manos de Curador: Cura enfermedades menores con contacto.",
        73: "Afinidad con el Caos: Tiene un 10% de probabilidad de evitar cualquier daño mágico.",
        74: "Voz de Mando: Puede dar órdenes a criaturas pequeñas de mentalidad débil.",
        75: "Piel de Hielo: Resistencia al frío y puede congelar agua al tocarla.",
        76: "Sin Necesidad de Dormir: No necesita descansar, pero sufre -5 en habilidades (-1 al TAC) si no lo hace.",
        77: "Ojo clínico: Sabe los puntos de vida, atributos y rasgos de una criatura con sólo verla.",
        78: "Control de la Luz: Crea pequeñas fuentes de luz o sombras.",
        79: "Zancada veloz: +2 al movimiento.",
        80: "Sin Necesidad de Comer: No necesita alimento, pero disfruta al comer.",
        81: "Manipular el destino: Puede repetir una tirada (incluso de combate) una vez al día.",
        82: "Fase etérea: Una vez al día puede atravesar una pared.",
        83: "Lágrimas curativas: Sus lágrimas pueden detener cualquier hemorragia.",
        84: "Invocar Lluvia: Cambia el clima local a lluvia suave por 1 hora (1 vez/día).",
        85: "Nudo mágico: Puede hacer nudos imposibles de soltar que solo él puede desatar.",
        86: "Manos de Artesano: +20% en habilidades de fabricación.",
        87: "Sin Edad: No envejece físicamente.",
        88: "Control de Sonido: Puede silenciar o amplificar sonidos cercanos.",
        89: "Umbral de dolor: Ignora el primer daño de golpe simple que reciba en un combate.",
        90: "Sin Necesidad de Respirar: Puede contener la respiración durante 15 minutos.",
        91: "Wyrding: A su mente vienen a veces palabras proféticas que ni siquiera él sabe bien qué quieren decir.",
        92: "Puños de hierro: Cuando lucha sin armas hace 1d6 de daño y puede defender sin armas o escudo.",
        93: "Familiar: Tiene un familiar animal con el que se puede comunicar.",
        94: "Interrogación maldita: Permite interrogar al espíritu de alguien que acabe de morir en combate.",
        95: "Quiroptofilia: Puede hablar con los murciélagos (y llamarlos si hay alguno cerca).",
        96: "Tatuajes mágicos: Sus tatuajes pueden almacenar un hechizo de nivel 1 de cualquier saber que no tenga.",
        97: "Sin Rostro: Puede borrar su rostro de la memoria de otros, siendo irreconocible.",
        98: "Control del Tiempo: Puede detener el tiempo durante 60 segundos fuera de combate.",
        99: "Afinidad con los Dioses: Recibe señales divinas en momentos clave.",
        100: "Aura gravítica: Permite a voluntad que los proyectiles no mágicos dirigidos a 2 metros caigan al suelo."
    }

    EVENTOS_JUVENTUD = {
        1: "Huérfano de guerra, criado por lobos en un bosque maldito. Aún lleva una cicatriz con el símbolo de un rey olvidado.",
        2: "Hijo de nobles que huyó para ser mercenario. Su familia ofrece una recompensa por su “secuestro”.",
        3: "Nació en una prisión y nunca conoció la libertad hasta que un motín le dio la oportunidad de escapar.",
        4: "Fue sacrificado a un dios antiguo de niño, pero sobrevivió. Ahora lleva su marca y los sacerdotes lo persiguen.",
        5: "Es el séptimo hijo de un séptimo hijo, y los aldeanos susurran que eso lo hace capaz de ver fantasmas.",
        6: "Su aldea fue arrasada por un dragón. Solo él sobrevivió, escondido bajo los huesos de su familia.",
        7: "Era un sabio erudito hasta que una maldición lo dejó sin memoria. Ahora solo recuerda fragmentos de libros.",
        8: "Fue vendido como esclavo a un circo de monstruos, donde aprendió a luchar para entretener a la nobleza.",
        9: "Creció en un burdel y sabe más secretos de los poderosos que cualquier espía.",
        10: "Es el bastardo de un rey, pero su existencia es un secreto que muchos quieren borrar.",
        11: "Nació con un gemelo idéntico que murió al nacer. A veces sueña con su vida alternativa.",
        12: "Fue criado por un fantasma que lo enseñó a hablar en lenguas muertas.",
        13: "Su madre era una bruja que lo encerró en una jaula de hierro para “protegerlo del mundo”.",
        14: "Era un niño prodigio en la magia, hasta que un hechizo fallido le dejó sin poder pero con visiones proféticas.",
        15: "Sobrevivió a un naufragio y fue criado por tritones, que le enseñaron a respirar bajo el agua.",
        16: "Su pueblo lo exilió por romper un tabú ancestral. Aún no sabe cuál fue su error.",
        17: "Era el bufón de un tirano, hasta que un chiste sobre su crueldad lo obligó a huir.",
        18: "Creció en un monasterio donde le enseñaron que la realidad es una ilusión. A veces duda de su propia existencia.",
        19: "Fue enterrado vivo por una secta y rescatado por ladrones de tumbas. Ahora teme los espacios cerrados.",
        20: "Es el último descendiente de un linaje de verdugos reales. Su hacha familiar aún tiene muescas de ejecuciones.",
        21: "Nació en un campo de batalla y fue adoptado por un soldado moribundo que le dio su espada.",
        22: "Su mejor amigo era un gólem de barro que un día se derritió bajo la lluvia. Aún guarda un puñado de su arcilla.",
        23: "Fue pastor hasta que un rebaño de ovejas negras lo guió a un portal a otro plano. Nadie le cree.",
        24: "Era un cadáver resucitado por error. El sacerdote que lo devolvió a la vida ahora lo caza para “corregir su pecado”.",
        25: "Creció en una taberna y aprendió a pelear rompiendo botellas en las borracheras.",
        26: "Su sombra tiene vida propia y le susurra consejos siniestros.",
        27: "Fue criado por bandidos, pero los traicionó para salvar a un niño. Ahora la guardia y los bandidos lo quieren muerto.",
        28: "Es el único que sobrevivió a una plaga que convirtió a su pueblo en estatuas de sal.",
        29: "Era un príncipe en un reino de sueños, hasta que despertó y descubrió que era un mendigo.",
        30: "Su corazón fue robado por un hada y reemplazado por un reloj. Si se detiene, morirá.",
        31: "Nació en un ataúd y fue encontrado por un sepulturero que lo crió entre lápidas.",
        32: "Era un ídolo de gladiador hasta que mató a su oponente favorito. Abandonó la arena por remordimiento.",
        33: "Fue aprendiz de un inventor loco cuyos artefactos siempre explotaban. Tiene cicatrices de metralla.",
        34: "Creció en una biblioteca maldita donde los libros le mordían los dedos.",
        35: "Su aldea lo sacrificó a un dios antiguo, pero este lo escupió diciendo que “no valía la pena”.",
        36: "Era un cazador de brujas hasta que descubrió que él mismo tenía magia en la sangre.",
        37: "Nació con los ojos sin pupila. Un vidente le dijo que estaba destinado a matar a un dios.",
        38: "Fue marinero en un barco fantasma que navegaba entre mundos. Un día despertó en tierra firme sin explicación.",
        39: "Su reflejo en los espejos envejece más rápido que él. Ya no se reconoce.",
        40: "Era un espía que fingió su muerte tan bien que hasta él se lo cree a veces.",
        41: "Creció en un pantano donde los muertos caminaban. Pensó que era normal hasta que conoció a otras personas.",
        42: "Su familia era una secta que adoraba a un demonio. Él lo mató con su propia daga ritual.",
        43: "Fue trovador hasta que una canción suya provocó una revolución. Ahora es un fugitivo político.",
        44: "Nació en un día sin sombras. Los sacerdotes dicen que no tiene alma.",
        45: "Era un mendigo hasta que encontró una moneda que concede un deseo... pero cada vez pesa más.",
        46: "Su pueblo lo eligió como chivo expiatorio para calmar a un monstruo. Regresó para demostrar que no era necesario.",
        47: "Fue esclavo en una mina de cristales mágicos. Uno se incrustó en su piel y ahora brilla en la oscuridad.",
        48: "Creció en un burdel flotante sobre un río de lava. Sabe bailar sobre cuchillos.",
        49: "Su gemelo murió al nacer, pero él sigue hablando con él en sueños.",
        50: "Era un caballero hasta que descubrió que su orden era un culto a un vampiro.",
        51: "Fue un juguete viviente de un brujo que coleccionaba “humanos curiosos”. Escapó, pero le quedan costuras invisibles.",
        52: "Creció en un faro donde su padre encendía fuegos con huesos de náufragos para alejar a “algo” que acechaba en la niebla.",
        53: "Es la reencarnación de un héroe antiguo, pero solo lo sabe por las pesadillas que lo muestran fallando en su misión original.",
        54: "Fue vendido a un alquimista que lo usó para probar elixires. Ahora su sangre cambia de color bajo la luna llena.",
        55: "Su aldea era flotante, atada a globos gigantes. Un día las cuerdas se cortaron y solo él sobrevivió.",
        56: "Era un espantapájaros viviente en campos encantados. Los cuervos le enseñaron los secretos que robaban a los muertos.",
        57: "Nació en un año sin verano. Los ancianos dicen que su llegada robó el calor del mundo.",
        58: "Fue enterrado como tesoro por un dragón que lo confundió con una joya. Pasó años en la oscuridad hasta que un ladrón lo rescató.",
        59: "Su sombra no coincide con su cuerpo. A veces se mueve antes que él o señala peligros.",
        60: "Es el último paciente de un sanatorio abandonado. Los doctores desaparecieron, pero las voces en las paredes aún le dan “instrucciones”.",
        61: "Crió a un basilisco pensando que era un polluelo. Cuando abrió los ojos, su aldea era piedra.",
        62: "Fue marinero en un barco que navegó al fin del mundo. Vio el borde del abismo y ahora tiene miedo del horizonte.",
        63: "Su corazón fue reemplazado por un fruto mágico. Si no lo riega con lágrimas una vez al mes, empieza a pudrirse.",
        64: "Era un relojero hasta que descubrió que sus creaciones marcaban la hora de la muerte de sus dueños.",
        65: "Nació en un día con dos soles. Los astrólogos predicen que morirá cuando vuelvan a alinearse.",
        66: "Fue pastor de cabras voladoras en las montañas nubladas. Una se lo llevó a otro reino y nunca pudo regresar.",
        67: "Su sangre es tinta. Puede escribir con ella, pero cada palabra que plasma le acorta la vida.",
        68: "Es el doble perfecto de un rey loco, entrenado para morir en su lugar. Huyó antes de la ceremonia.",
        69: "Creció en un jardín de estatuas vivientes. Un día se dio cuenta de que eran personas petrificadas y reconocía sus caras.",
        70: "Fue trovador de una corte de hadas. Cuando regresó, habían pasado 100 años y su nombre era solo una leyenda.",
        71: "Su reflejo en el agua muestra un cadáver. Los ríos y lagos le susurran que “pronto estarán juntos”.",
        72: "El Huérfano del tiempo. Apareció en un pueblo sin recuerdos. Cada luna llena, envejece 10 años y luego rejuvenece.",
        73: "Nació con un puño cerrado. Cuando lo abrió a los 10 años, dentro había un diente de dragón.",
        74: "Fue mensajero de una ciudad subterránea. Escucha y entiende los ecos de las cavernas.",
        75: "Su cuna era un barco diminuto que flotó hasta la orilla. El timón tenía grabado un nombre que no es el suyo.",
        76: "Es el resultado de un hechizo fallido para resucitar a otro. A veces recuerda “su” vida pasada.",
        77: "Crió a un bebé vampiro como hermano. Lo dejó ir antes de que descubriera qué era, pero sabe que volverá.",
        78: "Fue esclavo en una biblioteca infernal donde los libros se alimentaban de recuerdos. Olvidó su infancia, pero sabe idiomas prohibidos.",
        79: "Su aldea lo ofreció a los lobos en invierno. Estos lo criaron, pero siempre nota cómo los otros humanos huelen... deliciosos.",
        80: "Es el único que recuerda un evento catastrófico que nunca ocurrió. Viene de una línea temporal borrada.",
        81: "El Pintor de Pesadillas. Sus cuadros se vuelven realidad al quemarlos. Ya no pinta desde el incidente.",
        82: "El Espectador. Vivió 20 años en un teatro maldito donde las obras eran ejecuciones reales. Aplaude sin querer al ver sangre.",
        83: "Su familia era una dinastía de verdugos poéticos. Cada ejecución terminaba con un haiku escrito en sangre.",
        84: "El Cantor de las Ratas. Las ratas le obedecen. Él dice que le cuentan historias de ciudades devoradas bajo tierra.",
        85: "Creció en un bosque donde los árboles susurraban mentiras. Aún no sabe cuántas de sus memorias son reales.",
        86: "Fue pintado en un cuadro por un artista que capturaba almas. Escapó, pero a veces se siente plano, como de dos dimensiones.",
        87: "Su primer amor fue un espectro. Cada noche de luna llena, su nombre aparece escrito en el rocío.",
        88: "Es el 13er hijo de una familia maldita. Sus 12 hermanos mayores desaparecieron uno por uno en su cumpleaños.",
        89: "Fue vendido a un museo de rarezas como “el último humano auténtico”. Se escapó, pero no está seguro de si era mentira.",
        90: "Nació con una cicatriz que forma runas antiguas. Cuando llueve, arden como hierro al rojo vivo.",
        91: "Era un actor tan convincente que interpretó a un dios... y empezó a manifestar sus poderes.",
        92: "Su pueblo lo abandonó en un laberinto. Caminó hasta encontrar la salida, pero el mundo fuera ya no era el mismo.",
        93: "El Guardián de la última palabra. Sabe qué dirá cada persona antes de morir. Nunca lo revela.",
        94: "Creyó que era inmortal hasta que un día se cortó y sangró. Ahora teme que su muerte lo esté alcanzando.",
        95: "El Niño de la luna roja. Nació durante un eclipse sangriento. Las bestias entienden lo que dice.",
        96: "Es el juguete roto de un niño divino. Todavía lleva la marca de “DESCARTADO” en la nuca.",
        97: "El mensajero de las raíces. Las plantas le susurran mensajes de lugares lejanos. Sus uñas son de corteza.",
        98: "El cazador de susurros. Persigue voces que solo él oye. Una de ellas es la suya... pero de otro tiempo.",
        99: "El guardián del último secreto. Sabe algo que haría que el mundo entero lo cazara. Incluso él desea olvidarlo.",
        100: "El espejo roto. Es una de las 7 copias imperfectas de un héroe legendario. Los otros 6 están muertos (¿o él es el falso?)."
    }
    
    X_A_VALOR_HABILIDAD = {
        10: 50, 12: 55, 14: 60, 16: 65, 18: 70, 20: 75, 23: 80, 26: 85,
        30: 90, 34: 95, 39: 100
    }
    UMBRALES_X = sorted(X_A_VALOR_HABILIDAD.keys())

    NIVELES_TALENTO = {3, 5, 7, 9, 11, 13, 15, 17}
    NIVELES_ATRIBUTO = {4, 7, 10, 13, 16, 19}

    def __init__(self):
        self.raza, self.senda, self.profesion = None, None, None
        self.nombre_personaje, self.sexo, self.ciudad_origen, self.historia = "", "", "", ""
        self.rasgo_especial = None
        self.evento_juventud = None
        self.aspecto = None
        self.atributos, self.puntos = {}, {}
        self.talentos_nuevos = []
        self.habilidades_bloques = self.inicializar_habilidades()
        self.hechizos_aprendidos = {}
        self.armadura_equipada = {}
        self.armas_equipadas = []
        self.nivel = 1
        self.torso_portrait_path = None
        self.face_portrait_path = None

    def inicializar_habilidades(self):
        return {nombre: 0 for lista in self.HABILIDADES.values() for nombre in lista}

    def reset_habilidades_y_hechizos(self):
        self.habilidades_bloques = self.inicializar_habilidades()
        self.hechizos_aprendidos = {}

    def set_raza(self, raza):
        self.raza = raza
        for atr in self.ATRIBUTOS_FISICOS + self.ATRIBUTOS_MENTALES + self.ATRIBUTOS_SOCIALES:
            self.atributos[atr] = {"valor": 3, "max_racial": self.LIMITES_POR_RAZA[raza][atr]}

    def set_senda(self, senda):
        self.senda = senda
        pf, pm, ps = self.PUNTOS_POR_SENDA[senda]
        self.puntos["fisicos"] = pf - 3 * len(self.ATRIBUTOS_FISICOS)
        self.puntos["mentales"] = pm - 3 * len(self.ATRIBUTOS_MENTALES)
        self.puntos["sociales"] = ps - 3 * len(self.ATRIBUTOS_SOCIALES)
        for atr in self.ATRIBUTOS_FISICOS + self.ATRIBUTOS_MENTALES + self.ATRIBUTOS_SOCIALES:
            self.atributos[atr]["valor"] = 3

    def set_profesion(self, profesion):
        self.profesion = profesion

    def get_atributo_cap(self, atributo):
        if not self.raza: 
            return 10
        return min(10, self.atributos[atributo]["max_racial"] + 1)

    def incrementar(self, grupo, atributo):
        if self.atributos[atributo]["valor"] < self.atributos[atributo]["max_racial"] and self.puntos[grupo] > 0:
            self.atributos[atributo]["valor"] += 1
            self.puntos[grupo] -= 1

    def decrementar(self, grupo, atributo):
        if self.atributos[atributo]["valor"] > 3:
            self.atributos[atributo]["valor"] -= 1
            self.puntos[grupo] += 1

    def tirar_aspecto(self):
        total = sum(random.choice([0, 1]) for _ in range(10))
        self.aspecto = min(total, 6) if self.raza == "Semiorco" else total
        return self.aspecto

    def talentos(self):
        return {
            "raza": self.TALENTOS_RAZAS.get(self.raza, []), 
            "senda": self.TALENTOS_SENDAS.get(self.senda, []), 
            "profesion": self.TALENTOS_PROFESIONES.get(self.profesion, [])
        }

    def get_bono_habilidad_por_atributo(self, nombre_habilidad):
        atributo_nombre = self.HABILIDAD_ATRIBUTO_MAP.get(nombre_habilidad)
        if not atributo_nombre: 
            return 0
        valor_atr = self.aspecto if atributo_nombre == "ASPECTO" else self.atributos.get(atributo_nombre, {}).get("valor")
        if valor_atr is None or not (1 <= valor_atr <= 10): 
            return 0
        return self.BONO_POR_VALOR_ATRIBUTO[valor_atr - 1]

    def get_valor_base_from_x(self, total_x):
        if total_x <= 0: 
            return 0
        if total_x < 10: 
            return total_x * 5
        
        umbral_aplicable = 0
        for umbral in self.UMBRALES_X:
            if total_x >= umbral:
                umbral_aplicable = umbral
            else:
                break
        
        return self.X_A_VALOR_HABILIDAD.get(umbral_aplicable, 0)

    def calcular_habilidades_finales(self):
        habilidades_finales = {}
        todos_talentos = self.talentos()["raza"] + self.talentos()["senda"] + self.talentos()["profesion"] + self.talentos_nuevos
        
        tiene_labia = any("labia" in t.lower() for t in todos_talentos)
        tiene_liderazgo = any("liderazgo" in t.lower() for t in todos_talentos)
        tiene_seductor = any("seductor" in t.lower() for t in todos_talentos)
        tiene_ritmo = any("sentido del ritmo" in t.lower() for t in todos_talentos)
        habilidades_labia = ["Mentir", "Seducir", "Convencer", "Persuadir", "Charlatanería"]

        for nombre, bloques_add in self.habilidades_bloques.items():
            total_x = self.get_base_x(nombre) + bloques_add
            valor_base = self.get_valor_base_from_x(total_x)
            
            bono_atr = 0
            if nombre == "Valentía":
                poder_valor = self.atributos.get("PODER", {}).get("valor")
                if poder_valor and (1 <= poder_valor <= 10):
                    bono_str = self.TABLA_BONIFICADORES["PODER"]["Valentía"][poder_valor - 1]
                    try: 
                        bono_atr = int(str(bono_str).replace('%', ''))
                    except (ValueError, TypeError): 
                        bono_atr = 0
            else:
                bono_atr = self.get_bono_habilidad_por_atributo(nombre)
            
            bono_extra = 0
            if tiene_labia and nombre in habilidades_labia: 
                bono_extra += 10
            if tiene_liderazgo and nombre == "Valentía": 
                bono_extra += 20
            if tiene_seductor and nombre == "Seducir": 
                bono_extra += 25
            if tiene_ritmo and nombre == "Tocar Instrumento":
                bono_extra += 50
            
            if valor_base > 0 or bono_atr != 0 or bono_extra != 0:
                habilidades_finales[nombre] = {
                    "base": valor_base, 
                    "bono_atr": bono_atr, 
                    "bono_extra": bono_extra, 
                    "total": valor_base + bono_atr + bono_extra
                }
        return habilidades_finales
    
    def como_dict(self):
        return {
            "nombre_personaje": self.nombre_personaje, 
            "sexo": self.sexo, 
            "ciudad_origen": self.ciudad_origen, 
            "historia": self.historia,
            "rasgo_especial": self.rasgo_especial,
            "evento_juventud": self.evento_juventud,
            "raza": self.raza, 
            "senda": self.senda, 
            "profesion": self.profesion, 
            "aspecto": self.aspecto, 
            "atributos": {k: v["valor"] for k, v in self.atributos.items()},
            "talentos": self.talentos(), 
            "talentos_nuevos": self.talentos_nuevos, 
            "habilidades_bloques": self.habilidades_bloques, 
            "hechizos_aprendidos": self.hechizos_aprendidos, 
            "armadura_equipada": self.armadura_equipada,
            "armas_equipadas": self.armas_equipadas,
            "nivel": self.nivel,
            "torso_portrait_path": self.torso_portrait_path,
            "face_portrait_path": self.face_portrait_path
        }

    def get_maximo_por_habilidad(self, tipo, nombre_habilidad, ignorar_ambigua=False):
        todos_talentos = self.talentos()["raza"] + self.talentos()["senda"] + self.talentos()["profesion"] + self.talentos_nuevos
        
        if not ignorar_ambigua:
            es_ambigua = any(f"Habilidad ambigua ({nombre_habilidad})" in talento for talento in todos_talentos)
            if es_ambigua: 
                return 4

        es_afin = any(f"Afín a {nombre_habilidad}" in talento for talento in todos_talentos)
        if es_afin: 
            return 6
            
        return self.SendaRestricciones.get(self.senda, {}).get(tipo, 0)

    def get_maximo_bloques_por_subida(self, tipo, nombre_habilidad):
        max_total = self.get_maximo_por_habilidad(tipo, nombre_habilidad)
        if max_total >= 6: 
            return 2
        elif max_total >= 4: 
            return 1
        else: 
            return 0
        
    def get_habilidades_prohibidas(self):
        prohibidas = []
        for tipo, lista in self.HABILIDADES.items():
            for hab in lista:
                if self.get_maximo_por_habilidad(tipo, hab, ignorar_ambigua=True) == 0:
                    prohibidas.append(hab)
        return prohibidas

    def puede_incrementar_habilidad(self, tipo, nombre, bloques_restantes):
        max_bloques_add = self.get_maximo_por_habilidad(tipo, nombre)
        if self.habilidades_bloques[nombre] >= max_bloques_add or bloques_restantes <= 0:
            return False
        return True

    def puede_decrementar_habilidad(self, nombre):
        return self.habilidades_bloques[nombre] > 0

    def get_talentos_disponibles_nuevos(self):
        talentos_raza = self.TALENTOS_LISTA.get(self.raza, [])
        if self.raza == "Semielfo": 
            talentos_raza = list(set(self.TALENTOS_LISTA["Humano"] + self.TALENTOS_LISTA["Elfo"]))
        talentos_senda = self.TALENTOS_LISTA.get(self.senda, [])
        talentos_prof = self.TALENTOS_LISTA.get(self.profesion, [])
        return sorted(list(set(talentos_raza + talentos_senda + talentos_prof)))

    def get_num_talentos_nuevos(self):
        return self.TALENTOS_NUEVOS_POR_RAZA.get(self.raza, 0)

    def get_bonificadores(self):
        bonos = {}
        for atr, tabla in self.TABLA_BONIFICADORES.items():
            valor = self.atributos.get(atr, {}).get("valor", 3)
            for nombre_bono, lista_valores in tabla.items():
                bonos[nombre_bono] = lista_valores[valor - 1]
        
        # Bonificadores de dados por nivel del personaje
        if self.nivel >= 6:
            bonos["Dados defensa"] += 1
        if self.nivel >= 8:
            bonos["Dados ataque"] += 1
        if self.nivel >= 10:
            bonos["Dados esquiva"] += 1
        if self.nivel >= 12:
            bonos["Dados defensa"] += 1  # Total +2
        if self.nivel >= 14:
            bonos["Dados ataque"] += 1  # Total +2
        if self.nivel >= 16:
            bonos["Dados esquiva"] += 1  # Total +2

        todos_talentos = self.talentos()["raza"] + self.talentos()["senda"] + self.talentos()["profesion"] + self.talentos_nuevos
        if any("poder aumentado" in t.lower() for t in todos_talentos):
            if "Puntos de magia" in bonos: 
                bonos["Puntos de magia"] += 3
        if any("robusto" in t.lower() for t in todos_talentos):
            if "Puntos de vida" in bonos: 
                bonos["Puntos de vida"] += 5
        return bonos

    def get_total_bloques_habilidades(self):
        boni = self.get_bonificadores().get("Bonif. experiencia", "+0")
        try: 
            return 30 + int(str(boni).replace("+", ""))
        except: 
            return 30

    def get_base_x(self, nombre):
        return self.HABILIDADES_BASE_X.get(nombre, 0)

    def get_saberes_disponibles(self):
        todos_talentos = self.talentos()["raza"] + self.talentos()["senda"] + self.talentos()["profesion"] + self.talentos_nuevos
        return [t for t in todos_talentos if t.startswith("Saber")]

    def puede_aprender_hechizo_nuevo(self, costo_bloques=6, bloques_disponibles=None):
        if bloques_disponibles is not None:
            if bloques_disponibles < costo_bloques: 
                return False
        else:
            total_bloques = self.get_total_bloques_habilidades()
            bloques_usados = sum(self.habilidades_bloques.values())
            if total_bloques - bloques_usados < costo_bloques: 
                return False
        
        max_hechizos = self.get_bonificadores().get("Nº hechizos", 0)
        num_hechizos_actual = sum(len(lista) for lista in self.hechizos_aprendidos.values())
        if num_hechizos_actual >= max_hechizos: 
            return False
        
        saberes = self.get_saberes_disponibles()
        poder_pj = self.atributos.get("PODER", {}).get("valor", 0)
        for saber in saberes:
            lista_completa = self.LISTAS_SABERES.get(saber, [])
            aprendidos_en_saber = self.hechizos_aprendidos.get(saber, [])
            if len(aprendidos_en_saber) < len(lista_completa):
                nivel_siguiente_hechizo = len(aprendidos_en_saber) + 1
                if nivel_siguiente_hechizo <= poder_pj: 
                    return True 
        return False
    
    def get_max_nivel_armadura(self):
        todos_talentos = self.talentos()["raza"] + self.talentos()["senda"] + self.talentos()["profesion"] + self.talentos_nuevos
        max_nivel = 0
        for talento in todos_talentos:
            match = re.search(r'nv(\d+)', talento.lower())
            if match and "armadura" in talento.lower():
                nivel = int(match.group(1))
                if nivel > max_nivel: 
                    max_nivel = nivel
        return max_nivel

    def equipar_armadura(self, nivel, subtipo=None):
        key = f"Nivel {nivel}"
        if key not in self.ARMADURAS: 
            return
        
        piezas = self.ARMADURAS[key][subtipo]["piezas"] if subtipo else self.ARMADURAS[key]["piezas"]
        total_proteccion = sum(p[1] for p in piezas)
        self.armadura_equipada = {
            "nivel": nivel, 
            "subtipo": subtipo, 
            "piezas": piezas, 
            "total": math.floor(total_proteccion)
        }
    
    def equipar_sin_armadura(self):
        self.armadura_equipada = {
            "nivel": 0, 
            "subtipo": "Sin armadura", 
            "piezas": [], 
            "total": 0
        }
    
    def aplicar_luchar_desnudo(self):
        """Aplica el efecto del talento 'Luchar desnudo' si corresponde"""
        todos_talentos = self.talentos()["raza"] + self.talentos()["senda"] + self.talentos()["profesion"] + self.talentos_nuevos
        tiene_luchar_desnudo = any("luchar desnudo" in t.lower() for t in todos_talentos)
        
        if tiene_luchar_desnudo and self.armadura_equipada.get("total", 0) == 0:
            # Modificar la armadura equipada para reflejar los 2 puntos del talento
            if not self.armadura_equipada:
                self.armadura_equipada = {
                    "nivel": 0, 
                    "subtipo": "Luchar desnudo", 
                    "piezas": [("Constitución natural", 2)], 
                    "total": 2
                }
            else:
                self.armadura_equipada["total"] = 2
                self.armadura_equipada["piezas"] = [("Constitución natural", 2)]
                if "subtipo" not in self.armadura_equipada or self.armadura_equipada["subtipo"] == "Sin armadura":
                    self.armadura_equipada["subtipo"] = "Luchar desnudo"
    
    def get_estilos_combate_disponibles(self):
        estilos = []
        todos_talentos = self.talentos()["raza"] + self.talentos()["senda"] + self.talentos()["profesion"] + self.talentos_nuevos
        tiene_talento = lambda patron: any(patron.lower() in talento.lower() for talento in todos_talentos)
        
        if tiene_talento("dominio dagas"): 
            estilos.append("Daga")
            return estilos
        if tiene_talento("armas 1m") or tiene_talento("arma 1m"):
            estilos.append("Arma a 1 mano")
            if tiene_talento("escudo"): 
                estilos.append("Arma a 1 mano y escudo")
        if tiene_talento("armas 2m") or tiene_talento("arma 2m"): 
            estilos.append("Arma a 2 manos")
        if tiene_talento("2 armas de mano"): 
            estilos.append("2 armas de mano")
        if tiene_talento("arco corto"): 
            estilos.append("Arco corto")
        if tiene_talento("arco largo"): 
            estilos.append("Arco largo")
        if tiene_talento("arco o ballesta") or tiene_talento("de arco"):
            if not tiene_talento("arco corto"): 
                estilos.append("Arco corto")
            if not tiene_talento("arco largo"): 
                estilos.append("Arco largo")
            estilos.append("Ballesta ligera")
            estilos.append("Ballesta pesada")
        if tiene_talento("exótica") or tiene_talento("exotica"): 
            estilos.append("Arma exótica")
        return list(set(estilos))
    
    def get_num_estilos_combate_disponibles(self):
        count = 1
        if self.habilidades_bloques.get("Arma 2", 0) > 0: 
            count += 1
        if self.habilidades_bloques.get("Arma 3", 0) > 0: 
            count += 1
        if self.habilidades_bloques.get("Arma 4", 0) > 0: 
            count += 1
        return count
    
    def get_armas_disponibles_por_estilo(self, estilo, mano_no_habil=False):
        todos_talentos = self.talentos()["raza"] + self.talentos()["senda"] + self.talentos()["profesion"] + self.talentos_nuevos
        es_ambidiestro = any("ambidiestro" in t.lower() for t in todos_talentos)
        fuerza = self.atributos.get("FUERZA", {}).get("valor", 0)
        armas_disponibles = []
        fuerza_req_multiplicador = 1 if es_ambidiestro else (2 if mano_no_habil else 1)
        
        if estilo == "Daga":
            return [arma for arma in self.ARMAS if arma["nombre"] == "Daga" and arma["fuerza"] * fuerza_req_multiplicador <= fuerza]

        if estilo == "Arma exótica":
            # Incluye armas de categoría 'exótica' O armas a distancia que no sean arcos/ballestas
            return [arma for arma in self.ARMAS if arma["fuerza"] * fuerza_req_multiplicador <= fuerza and (
                    arma["categoria"] == "exótica" or (arma.get("alcance") and arma["categoria"] not in ["arco", "ballesta"]))]
        
        categorias_map = {
            "Arma a 1 mano": "1 mano", 
            "Arma a 1 mano y escudo": "1 mano", 
            "2 armas de mano": "1 mano",
            "Arma a 2 manos": "2 manos", 
            "Arco corto": "arco", 
            "Arco largo": "arco",
            "Ballesta ligera": "ballesta", 
            "Ballesta pesada": "ballesta"
        }
        categoria_buscada = categorias_map.get(estilo)
        
        for arma in self.ARMAS:
            if arma["fuerza"] * fuerza_req_multiplicador > fuerza: 
                continue
            if estilo in ["Arco corto", "Arco largo", "Ballesta ligera", "Ballesta pesada"]:
                if arma["nombre"] == estilo: 
                    armas_disponibles.append(arma)
            elif categoria_buscada and arma["categoria"] == categoria_buscada:
                 armas_disponibles.append(arma)
        return armas_disponibles
    
    def equipar_arma(self, arma_info, estilo_combate, mano=None):
        nueva_arma = arma_info.copy()
        nueva_arma["estilo_combate"] = estilo_combate
        if mano is not None: 
            nueva_arma["mano"] = mano
        self.armas_equipadas.append(nueva_arma)
        return nueva_arma

    def get_combat_stats(self):
        stats = []
        bonos = self.get_bonificadores()
        estilos_usados = {}
        for arma in self.armas_equipadas:
            estilo = arma['estilo_combate']
            if estilo not in estilos_usados: 
                estilos_usados[estilo] = []
            estilos_usados[estilo].append(arma)

        slot_map = {}
        for i, estilo_combate in enumerate(estilos_usados.keys()):
            slot_map[estilo_combate] = f"Arma {i+1}"

        for estilo_combate, armas in estilos_usados.items():
            habilidad_arma_nombre = slot_map.get(estilo_combate)
            if not habilidad_arma_nombre: 
                continue

            habilidad_base = self.get_valor_base_from_x(self.get_base_x(habilidad_arma_nombre) + self.habilidades_bloques.get(habilidad_arma_nombre, 0))
            
            bono_atr = 0
            if armas[0]['categoria'] in ['arco', 'ballesta']:
                bono_atr = bonos.get('Bonif. ataque distancia', 0)
            else:
                bono_fuerza = bonos.get('Bonif. ataque', 0)
                if armas[0]['at']:
                    bono_destreza = bonos.get('Bonif. ataque técnico', 0)
                    bono_atr = max(bono_fuerza, bono_destreza)
                else:
                    bono_atr = bono_fuerza
            
            habilidad_total = habilidad_base + bono_atr
            tac_val = max(0, (habilidad_total // 5) * 5)
            tac_keys = sorted(self.TAC_TABLE.keys())
            
            final_tac_key = tac_keys[0]
            for key in tac_keys:
                if tac_val >= key: 
                    final_tac_key = key
                else: 
                    break
            tac = self.TAC_TABLE.get(final_tac_key)

            dados_ataque = bonos.get('Dados ataque', 1)
            dados_defensa = bonos.get('Dados defensa', 0)
            if estilo_combate == "2 armas de mano": 
                dados_ataque += 1
            if estilo_combate == "Arma a 1 mano y escudo": 
                dados_defensa += 1

            bono_daño_str = bonos.get('Bonif. daño', '0')
            if bono_daño_str == '0': 
                bono_daño_str = ""
            
            daño_final = ""
            if len(armas) > 1:
                arma_habil = next((a for a in armas if a.get('mano') == 'hábil'), armas[0])
                arma_no_habil = next((a for a in armas if a.get('mano') == 'no hábil'), armas[1])
                daño_habil = f"{arma_habil['daño']}{bono_daño_str}" if armas[0]['categoria'] not in ['arco', 'ballesta'] else arma_habil['daño']
                daño_no_habil = f"{arma_no_habil['daño']}{bono_daño_str}" if armas[0]['categoria'] not in ['arco', 'ballesta'] else arma_no_habil['daño']
                daño_final = f"{daño_habil} ({daño_no_habil})"
            else:
                if armas[0]['categoria'] in ['arco', 'ballesta']: 
                    daño_final = armas[0]['daño']
                else: 
                    daño_final = f"{armas[0]['daño']}{bono_daño_str}"
            
            stats.append({
                "estilo": estilo_combate, 
                "arma_nombre": " y ".join(a['nombre'] for a in armas),
                "critico": "/".join(set(a['critico'] for a in armas)), 
                "dados_atq_def": f"{dados_ataque}/{dados_defensa}",
                "tac": tac, 
                "alcance": armas[0].get('alcance') or "---", 
                "at": "Sí" if armas[0]['at'] else "No", 
                "daño": daño_final
            })
        return stats