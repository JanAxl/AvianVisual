import os
import random
import sqlite3
import flet as ft

# ==========================================
# CONFIGURACIÓN DE RUTAS Y BASE DE DATOS
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "avianvisual.db")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "aves")

# Crear automáticamente las carpetas assets/aves si no existen
os.makedirs(IMAGES_DIR, exist_ok=True)


def inicializar_bd():
    """Crea la base de datos SQLite y carga 15 especies, 30 quizzes únicos y 10 ejercicios de emparejamiento."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_comun TEXT NOT NULL,
            nombre_cientifico TEXT NOT NULL,
            orden_taxonomico TEXT NOT NULL,
            familia TEXT NOT NULL,
            estado_conservacion TEXT NOT NULL,
            rareza TEXT NOT NULL,
            dieta TEXT NOT NULL,
            envergadura_peso TEXT NOT NULL,
            habitat TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            imagen TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT NOT NULL,
            opcion_a TEXT NOT NULL,
            opcion_b TEXT NOT NULL,
            opcion_c TEXT NOT NULL,
            opcion_d TEXT NOT NULL,
            respuesta_correcta TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matching_quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            instruccion TEXT NOT NULL,
            pares_json TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM aves")
    if cursor.fetchone()[0] == 0:
        aves_semilla = [
            (
                "Tucán Pico Iris", "Ramphastos sulfuratus", "Piciformes", "Ramphastidae",
                "Preocupación Menor (LC)", "Común en selvas conservadas",
                "Frugívoro (frutos tropicales, insectos y pequeños reptiles)",
                "Longitud: 42–55 cm | Peso: 380–500 g",
                "Selvas tropicales húmedas y bordes de bosque del sureste",
                "Ave arborícola reconocible por su enorme pico ligero multicolor y plumaje negro intenso con garganta amarilla brillante.",
                "aves/tucan_pico_iris.jpg"
            ),
            (
                "Quetzal Mesoamericano", "Pharomachrus mocinno", "Trogoniformes", "Trogonidae",
                "Casi Amenazado (NT)", "Raro / Indicador de bosque sano",
                "Frugívoro especializado (aguacatillos silvestres) e insectos",
                "Longitud: 36–40 cm (+65 cm cola en machos) | Peso: 210 g",
                "Bosques mesófilos de montaña y selvas nubosas",
                "Considerada ave sagrada por culturas prehispánicas; presenta plumaje verde esmeralda iridiscente y pecho carmesí.",
                "aves/quetzal.jpg"
            ),
            (
                "Colibrí Garganta Rubí", "Archilochus colubris", "Apodiformes", "Trochilidae",
                "Preocupación Menor (LC)", "Migratorio estacional común",
                "Nectarívoro e insectívoro (néctar floral y pequeños artrópodos)",
                "Longitud: 7–9 cm | Envergadura: 8–11 cm | Peso: 2.5–3.8 g",
                "Jardines, claros de bosque y matorrales floridos",
                "Pequeño polinizador capaz de batir sus alas más de 50 veces por segundo y cruzar el Golfo de México sin escalas.",
                "aves/colibri_rubi.jpg"
            ),
            (
                "Momoto Cejas Turquesa", "Eumomota superciliosa", "Coraciiformes", "Momotidae",
                "Preocupación Menor (LC)", "Común en zonas tropicales",
                "Insectívoro y pequeños vertebrados (lagartijas y arañas)",
                "Longitud: 34 cm | Peso: 60–65 g",
                "Selvas bajas caducifolias, bordes de ríos y arboledas",
                "Posee una ceja azul turquesa brillante y dos plumas centrales de la cola con puntas en forma de raqueta que balancea como péndulo.",
                "aves/momoto.jpg"
            ),
            (
                "Garza Tigre Mexicana", "Tigrisoma mexicanum", "Pelecaniformes", "Ardeidae",
                "Preocupación Menor (LC)", "Poco común / Sigilosa",
                "Piscívoro y carnívoro (peces, ranas, cangrejos e insectos acuáticos)",
                "Longitud: 70–80 cm | Envergadura: 115 cm | Peso: 1,100–1,200 g",
                "Humedales, manglares, esteros y riberas sombreadas",
                "Garza robusta con garganta desnuda amarillo-verdosa y plumaje finamente barrado que le otorga excelente camuflaje entre juncos.",
                "aves/garza_tigre.jpg"
            ),
            (
                "Guacamaya Roja", "Ara macao", "Psittaciformes", "Psittacidae",
                "Preocupación Menor (LC) / En Peligro en México", "Muy Rara en estado silvestre",
                "Frugívoro y granívoro (semillas duras, nueces y frutos)",
                "Longitud: 81–96 cm | Envergadura: 100–110 cm | Peso: 900–1,100 g",
                "Selvas altas perennifolias y bosques ribereños",
                "Psitácido de gran tamaño con plumaje escarlata intenso, franjas amarillas y azules en las alas y rostro desnudo blanco.",
                "aves/guacamaya_roja.jpg"
            ),
            (
                "Águila Arpía", "Harpia harpyja", "Accipitriformes", "Accipitridae",
                "Vulnerable (VU)", "Extremadamente Rara",
                "Carnívoro apex (mamíferos arborícolas como monos y perezosos)",
                "Longitud: 89–105 cm | Envergadura: 176–224 cm | Peso: 4.5–9 kg",
                "Dosel de selvas tropicales primarias extensas",
                "Una de las rapaces más poderosas del mundo; posee una cresta doble eréctil y garras de hasta 13 cm de longitud.",
                "aves/aguila_arpia.jpg"
            ),
            (
                "Jabirú", "Jabiru mycteria", "Ciconiiformes", "Ciconiidae",
                "Preocupación Menor (LC) / En Peligro en México", "Rara / Especialista de humedal",
                "Carnívoro acuático (peces grandes, anfibios y reptiles pequeños)",
                "Altura: 120–140 cm | Envergadura: 230–280 cm | Peso: 4.3–8 kg",
                "Pantanos extensos, sabanas inundables y lagunas costeras",
                "Es el ave voladora más alta de América Central y del Sur; destaca por su plumaje blanco y cuello negro con base roja.",
                "aves/jabiru.jpg"
            ),
            (
                "Hocofaisán", "Crax rubra", "Galliformes", "Cracidae",
                "Vulnerable (VU)", "Poco común / Sensible a cacería",
                "Frugívoro y folívoro (frutos caídos, brotes tiernos e insectos)",
                "Longitud: 78–92 cm | Peso: 3.1–4.8 kg",
                "Selvas húmedas maduras con sotobosque denso",
                "Ave terrestre de gran porte con cresta de plumas rizadas; presenta marcado dimorfismo sexual entre machos negros y hembras barradas.",
                "aves/hocofaisan.jpg"
            ),
            (
                "Búho Cornudo", "Bubo virginianus", "Strigiformes", "Strigidae",
                "Preocupación Menor (LC)", "Común pero nocturno",
                "Carnívoro nocturno (roedores, aves, reptiles e insectos grandes)",
                "Longitud: 46–63 cm | Envergadura: 101–145 cm | Peso: 1.2–1.6 kg",
                "Bosques diversos, bordes agrícolas y zonas semiabiertas",
                "Rapaz nocturna adaptable con penachos auriculares prominentes, ojos amarillo intenso y vuelo completamente silencioso.",
                "aves/buho_cornudo.jpg"
            ),
            (
                "Carpintero Lineado", "Dryocopus lineatus", "Piciformes", "Picidae",
                "Preocupación Menor (LC)", "Común en arboledas",
                "Insectívoro (larvas perforadoras de madera, hormigas y frutos)",
                "Longitud: 31–36 cm | Peso: 180–225 g",
                "Selvas secundarias, plantaciones de cacao y bosques abiertos",
                "Carpintero grande con cresta roja llamativa y líneas faciales blancas que excava cavidades profundas en troncos muertos.",
                "aves/carpintero_lineado.jpg"
            ),
            (
                "Chara Verde", "Cyanocorax yncas", "Passeriformes", "Corvidae",
                "Preocupación Menor (LC)", "Común en grupos familiares",
                "Omnívoro (insectos, semillas, frutos y pequeños vertebrados)",
                "Longitud: 25–29 cm | Peso: 65–92 g",
                "Selvas bajas, matorrales densos y bosques ribereños",
                "Córvido muy social y ruidoso de plumaje verde brillante, pecho amarillo y cabeza azul cobalto con cresta frontal.",
                "aves/chara_verde.jpg"
            ),
            (
                "Martín Pescador Amazónico", "Chloroceryle amazona", "Coraciiformes", "Alcedinidae",
                "Preocupación Menor (LC)", "Común en cuerpos de agua",
                "Piscívoro (peces pequeños capturados mediante zambullida)",
                "Longitud: 29–30 cm | Peso: 110–140 g",
                "Ríos tranquilos, arroyos, lagunas y canales de manglar",
                "Presenta dorso verde metálico oscuro, collar blanco y un pico largo y robusto adaptado para atrapar presas bajo el agua.",
                "aves/martin_pescador.jpg"
            ),
            (
                "Oropéndola de Moctezuma", "Psarocolius montezuma", "Passeriformes", "Icteridae",
                "Preocupación Menor (LC)", "Común en colonias arbóreas",
                "Omnívoro (frutos, néctar, insectos y pequeños vertebrados)",
                "Longitud: 38–50 cm | Peso: 230–520 g",
                "Dosel de selvas húmedas y claros con árboles altos",
                "Famosa por construir nidos colgantes tejidos en forma de bolsa de hasta un metro de largo y emitir cantos líquidos complejos.",
                "aves/oropendola.jpg"
            ),
            (
                "Espátula Rosada", "Platalea ajaja", "Pelecaniformes", "Threskiornithidae",
                "Preocupación Menor (LC)", "Poco común / Estacional en costas",
                "Carnívoro filtrador (crustáceos, peces pequeños e insectos acuáticos)",
                "Longitud: 71–86 cm | Envergadura: 120–133 cm | Peso: 1.2–1.8 kg",
                "Lagunas costeras, manglares, marismas y pantanos",
                "Inconfundible por su plumaje rosado intenso y su pico largo aplanado en forma de cuchara con el que barre el agua de lado a lado.",
                "aves/espatula_rosada.jpg"
            )
        ]
        cursor.executemany("""
            INSERT INTO aves (
                nombre_comun, nombre_cientifico, orden_taxonomico, familia,
                estado_conservacion, rareza, dieta, envergadura_peso,
                habitat, descripcion, imagen
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, aves_semilla)

    # ---------------------------------------------------------
    # 30 QUIZZES ÚNICOS (2 preguntas distintas por cada ave)
    # ---------------------------------------------------------
    cursor.execute("SELECT COUNT(*) FROM quizzes")
    if cursor.fetchone()[0] < 30:
        cursor.execute("DELETE FROM quizzes")
        quizzes_30 = [
            ("1. ¿A qué familia taxonómica pertenece el Tucán Pico Iris (Ramphastos sulfuratus)?", "Ramphastidae", "Trogonidae", "Psittacidae", "Picidae", "Ramphastidae"),
            ("2. ¿De qué color es la garganta que contrasta con el plumaje negro del Tucán Pico Iris?", "Amarillo brillante", "Rojo carmesí", "Azul cobalto", "Blanco puro", "Amarillo brillante"),
            ("3. ¿Cuál es el fruto silvestre clave en la dieta especializada del Quetzal Mesoamericano?", "Aguacatillos silvestres", "Semillas de pino", "Bellotas de encino", "Néctar de bromelia", "Aguacatillos silvestres"),
            ("4. ¿Qué longitud adicional pueden alcanzar las plumas supracaudales (cola) del Quetzal macho?", "Hasta 65 cm", "Apenas 10 cm", "Más de 150 cm", "No tiene cola larga", "Hasta 65 cm"),
            ("5. ¿Cuántas veces por segundo puede batir sus alas el Colibrí Garganta Rubí?", "Más de 50 veces", "Entre 5 y 8 veces", "Exactamente 15 veces", "Menos de 20 veces", "Más de 50 veces"),
            ("6. ¿Qué hazaña migratoria realiza Archilochus colubris a pesar de pesar apenas 3 gramos?", "Cruza el Golfo de México sin escalas", "Hiberna bajo tierra en invierno", "Migra caminando por selvas", "Vuela hacia la Antártida", "Cruza el Golfo de México sin escalas"),
            ("7. ¿Qué forma distintiva tienen las puntas de las dos plumas centrales de la cola del Momoto?", "Forma de raqueta", "Forma de espiral", "Forma de abanico", "Puntas bifurcadas", "Forma de raqueta"),
            ("8. ¿A qué orden taxonómico pertenece el Momoto Cejas Turquesa (Eumomota superciliosa)?", "Coraciiformes", "Passeriformes", "Strigiformes", "Galliformes", "Coraciiformes"),
            ("9. ¿Qué rasgo físico en su garganta distingue a la Garza Tigre Mexicana (Tigrisoma mexicanum)?", "Garganta desnuda amarillo-verdosa", "Bolsa gular azul brillante", "Barba de plumas blancas", "Cresta doble naranja", "Garganta desnuda amarillo-verdosa"),
            ("10. ¿Qué función cumple el plumaje finamente barrado de la Garza Tigre Mexicana?", "Camuflaje entre juncos y riberas", "Atracción en vuelo oceánico", "Regulación térmica en nieve", "Señalización nocturna", "Camuflaje entre juncos y riberas"),
            ("11. ¿Cuál es el estado legal de conservación de la Guacamaya Roja (Ara macao) en México?", "En Peligro de Extinción", "Especie invasora", "Fuera de peligro nacional", "Extinta en América", "En Peligro de Extinción"),
            ("12. ¿Qué colores acompañan al rojo escarlata en las alas de la Guacamaya Roja?", "Franjas amarillas y azules", "Manchas negras y grises", "Bandas moradas y rosas", "Puntas totalmente blancas", "Franjas amarillas y azules"),
            ("13. ¿Cuál es la presa principal de la Águila Arpía (Harpia harpyja) en el dosel selvático?", "Mamíferos arborícolas como monos y perezosos", "Peces de arrecife", "Néctar y polen nocturno", "Crustáceos de manglar", "Mamíferos arborícolas como monos y perezosos"),
            ("14. ¿Qué longitud pueden alcanzar las garras posteriores de una Águila Arpía adulta?", "Hasta 13 cm", "Solo 2 cm", "Unos 30 cm", "Menos de 1 cm", "Hasta 13 cm"),
            ("15. ¿Qué récord de tamaño ostenta el Jabirú (Jabiru mycteria) en América Central y del Sur?", "Es el ave voladora más alta", "Es el ave más pequeña", "Tiene el pico más corto", "Es el ave más veloz en picada", "Es el ave voladora más alta"),
            ("16. ¿Qué coloración presenta la base del cuello desnudo del Jabirú?", "Rojo intenso", "Verde esmeralda", "Amarillo limón", "Azul turquesa", "Rojo intenso"),
            ("17. ¿Cómo se distingue visualmente un Hocofaisán (Crax rubra) macho adulto?", "Plumaje negro con cresta rizada y protuberancia amarilla en el pico", "Plumaje completamente rosado", "Alas azules y vientre blanco", "Sin cresta y cola blanca", "Plumaje negro con cresta rizada y protuberancia amarilla en el pico"),
            ("18. ¿Qué estrato de la selva habita principalmente el Hocofaisán?", "El suelo del sotobosque denso", "Las copas emergentes a 50 m", "Acantilados marinos", "Cuevas subterráneas", "El suelo del sotobosque denso"),
            ("19. ¿Qué característica de vuelo permite al Búho Cornudo (Bubo virginianus) cazar de noche sin ser detectado?", "Plumas con bordes aterciopelados que silencian el aleteo", "Planeo supersónico", "Aleteo ultrasónico", "Vuelo rasante sobre el mar", "Plumas con bordes aterciopelados que silencian el aleteo"),
            ("20. ¿Qué estructura cefálica da nombre común al Búho Cornudo?", "Penachos de plumas auriculares", "Cuernos óseos reales", "Cresta de piel roja", "Pico curvo hacia arriba", "Penachos de plumas auriculares"),
            ("21. ¿Cuál es el alimento principal del Carpintero Lineado (Dryocopus lineatus)?", "Larvas perforadoras de madera y hormigas", "Peces de río", "Frutos secos de palmera", "Pequeños roedores", "Larvas perforadoras de madera y hormigas"),
            ("22. ¿Qué función ecológica cumplen las cavidades excavadas por el Carpintero Lineado?", "Sirven de refugio posterior a otras aves y mamíferos", "Almacenan agua de lluvia", "Atraen peces", "Evitan incendios forestales", "Sirven de refugio posterior a otras aves y mamíferos"),
            ("23. ¿A qué familia de aves inteligentes pertenece la Chara Verde (Cyanocorax yncas)?", "Corvidae", "Trochilidae", "Ardeidae", "Ciconiidae", "Corvidae"),
            ("24. ¿Qué combinación de colores caracteriza el plumaje de la Chara Verde?", "Cuerpo verde, pecho amarillo y cabeza azul cobalto", "Totalmente negro brillante", "Gris pizarra con pecho rojo", "Blanco con alas negras", "Cuerpo verde, pecho amarillo y cabeza azul cobalto"),
            ("25. ¿Qué técnica de caza emplea el Martín Pescador Amazónico (Chloroceryle amazona)?", "Zambullida vertical desde una percha sobre el agua", "Persecución nocturna en bosque", "Filtrado de lodo en pantanos", "Captura de insectos en vuelo alto", "Zambullida vertical desde una percha sobre el agua"),
            ("26. ¿Qué peso aproximado tiene un Martín Pescador Amazónico adulto?", "110 a 140 gramos", "4.5 a 8 kilogramos", "3 a 4 gramos", "1.5 a 2 kilogramos", "110 a 140 gramos"),
            ("27. ¿Cómo son los nidos que construye la Oropéndola de Moctezuma (Psarocolius montezuma)?", "Bolsas colgantes tejidas de hasta 1 metro de largo", "Madrigueras excavadas en arena", "Plataformas de lodo en rocas", "No construye nido", "Bolsas colgantes tejidas de hasta 1 metro de largo"),
            ("28. ¿En qué tipo de organización social suele anidar la Oropéndola de Moctezuma?", "En colonias arbóreas numerosas", "De forma estrictamente solitaria", "En parejas bajo tierra", "En bandadas pelágicas", "En colonias arbóreas numerosas"),
            ("29. ¿Cómo obtiene su alimento la Espátula Rosada (Platalea ajaja) en aguas someras?", "Barriendo el agua de lado a lado con su pico en cuchara", "Buceando a 20 metros de profundidad", "Perforando cortezas de árboles", "Cazando desde las copas", "Barriendo el agua de lado a lado con su pico en cuchara"),
            ("30. ¿A qué se debe principalmente la intensa coloración rosada del plumaje de la Espátula Rosada?", "A los carotenoides presentes en los crustáceos de su dieta", "A la exposición directa al sol", "A un parásito benigno de humedal", "A su edad juvenil", "A los carotenoides presentes en los crustáceos de su dieta")
        ]
        cursor.executemany("""
            INSERT INTO quizzes (pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta)
            VALUES (?, ?, ?, ?, ?, ?)
        """, quizzes_30)

    # ---------------------------------------------------------
    # 10 EJERCICIOS DE EMPAREJAMIENTO / MATCHING (4 pares c/u)
    # ---------------------------------------------------------
    cursor.execute("SELECT COUNT(*) FROM matching_quizzes")
    if cursor.fetchone()[0] < 10:
        cursor.execute("DELETE FROM matching_quizzes")
        matching_10 = [
            (
                "Reto de Emparejamiento 1: Especie y Nombre Científico (Selva Alta)",
                "Conecta cada ave con su nomenclatura binominal correcta:",
                "Tucán Pico Iris::Ramphastos sulfuratus||Quetzal Mesoamericano::Pharomachrus mocinno||Guacamaya Roja::Ara macao||Águila Arpía::Harpia harpyja"
            ),
            (
                "Reto de Emparejamiento 2: Especie y Nombre Científico (Humedales y Bosques)",
                "Conecta cada especie con su nombre científico:",
                "Jabirú::Jabiru mycteria||Garza Tigre Mexicana::Tigrisoma mexicanum||Espátula Rosada::Platalea ajaja||Martín Pescador Amazónico::Chloroceryle amazona"
            ),
            (
                "Reto de Emparejamiento 3: Especie y Familia Taxonómica",
                "Une cada ave con la familia taxonómica a la que pertenece:",
                "Colibrí Garganta Rubí::Trochilidae||Momoto Cejas Turquesa::Momotidae||Hocofaisán::Cracidae||Búho Cornudo::Strigidae"
            ),
            (
                "Reto de Emparejamiento 4: Especie y Familia Taxonómica (Passeriformes y Piciformes)",
                "Relaciona cada ave con su familia correspondiente:",
                "Carpintero Lineado::Picidae||Chara Verde::Corvidae||Oropéndola de Moctezuma::Icteridae||Tucán Pico Iris::Ramphastidae"
            ),
            (
                "Reto de Emparejamiento 5: Rasgo Morfológico Distintivo",
                "Conecta cada especie con su característica física única:",
                "Momoto Cejas Turquesa::Plumas centrales en forma de raqueta||Espátula Rosada::Pico largo aplanado en forma de cuchara||Oropéndola de Moctezuma::Nidos colgantes tejidos de hasta 1 metro||Águila Arpía::Cresta doble eréctil y garras de 13 cm"
            ),
            (
                "Reto de Emparejamiento 6: Gremio Trófico y Dieta Especializada",
                "Une cada ave con su alimentación principal:",
                "Quetzal Mesoamericano::Aguacatillos silvestres||Colibrí Garganta Rubí::Néctar floral y pequeños artrópodos||Carpintero Lineado::Larvas perforadoras de madera||Martín Pescador Amazónico::Peces pequeños mediante zambullida"
            ),
            (
                "Reto de Emparejamiento 7: Hábitat Ecológico Principal",
                "Relaciona cada especie con su ecosistema característico:",
                "Quetzal Mesoamericano::Bosques mesófilos y selvas nubosas||Jabirú::Pantanos extensos y sabanas inundables||Hocofaisán::Sotobosque denso de selvas maduras||Espátula Rosada::Lagunas costeras y marismas"
            ),
            (
                "Reto de Emparejamiento 8: Envergadura y Peso",
                "Conecta cada especie con su rango morfométrico:",
                "Colibrí Garganta Rubí::Peso de 2.5 a 3.8 gramos||Águila Arpía::Envergadura de 176 a 224 cm||Jabirú::Altura de 120 a 140 cm||Momoto Cejas Turquesa::Peso de 60 a 65 gramos"
            ),
            (
                "Reto de Emparejamiento 9: Orden Taxonómico",
                "Une cada especie con su Orden taxonómico:",
                "Búho Cornudo::Strigiformes||Guacamaya Roja::Psittaciformes||Hocofaisán::Galliformes||Garza Tigre Mexicana::Pelecaniformes"
            ),
            (
                "Reto de Emparejamiento 10: Estado de Conservación y Rareza",
                "Relaciona cada ave con su situación ecológica:",
                "Águila Arpía::Vulnerable (VU) / Extremadamente rara||Quetzal Mesoamericano::Casi Amenazado (NT) / Indicador de bosque sano||Chara Verde::Preocupación Menor (LC) / Común en grupos familiares||Tucán Pico Iris::Preocupación Menor (LC) / Común en selvas conservadas"
            )
        ]
        cursor.executemany("""
            INSERT INTO matching_quizzes (titulo, instruccion, pares_json)
            VALUES (?, ?, ?)
        """, matching_10)

    conn.commit()
    conn.close()


def obtener_aves():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre_comun, nombre_cientifico, orden_taxonomico, familia,
               estado_conservacion, rareza, dieta, envergadura_peso,
               habitat, descripcion, imagen
        FROM aves
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def obtener_quizzes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta FROM quizzes ORDER BY id ASC")
    data = cursor.fetchall()
    conn.close()
    return data


def obtener_matching_quizzes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, instruccion, pares_json FROM matching_quizzes ORDER BY id ASC")
    data = cursor.fetchall()
    conn.close()
    return data


# ==========================================
# CAPA DE PRESENTACIÓN (Flet 1.0.0)
# ==========================================
def main(page: ft.Page):
    page.title = "AvianVisual — Enciclopedia & Evaluador Ornitológico"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.bgcolor = "grey50"

    inicializar_bd()

    puntaje = 0
    indice_global = 0  # Flujo único continuo: 0..29 = Quizzes | 30..39 = Retos de Emparejamiento

    content_area = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    txt_puntaje = ft.Text(f"Puntaje acumulado: {puntaje} pts", weight=ft.FontWeight.BOLD, color="deeppurple", size=14)

    def construir_widget_imagen(ruta_relativa: str, alto: int = 220):
        ruta_absoluta = os.path.join(ASSETS_DIR, ruta_relativa.replace("/", os.sep))
        if os.path.exists(ruta_absoluta):
            return ft.Container(
                content=ft.Image(
                    src=ruta_relativa,
                    height=alto,
                    fit=ft.BoxFit.CONTAIN,
                    border_radius=10
                ),
                alignment=ft.Alignment.CENTER,
                padding=5
            )
        else:
            return ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.IMAGE_OUTLINED, size=48, color="grey"),
                    ft.Text("Sin fotografía asignada", weight=ft.FontWeight.BOLD, color="grey700", size=13),
                    ft.Text(f"Coloca tu imagen en: assets/{ruta_relativa}", size=11, color="grey600", italic=True)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                height=alto,
                bgcolor="grey200",
                border_radius=10,
                alignment=ft.Alignment.CENTER,
                padding=10
            )

    def mostrar_detalle_ave(ave):
        content_area.controls.clear()

        (
            ave_id, nombre_comun, nombre_cientifico, orden_tax, familia,
            conservacion, rareza, dieta, medidas, habitat, descripcion, imagen
        ) = ave

        def crear_fila_dato(titulo: str, valor: str, color_valor: str = "black87"):
            return ft.Container(
                content=ft.Column([
                    ft.Text(titulo, size=12, weight=ft.FontWeight.BOLD, color="green900"),
                    ft.Text(valor, size=14, color=color_valor)
                ], spacing=2),
                padding=10,
                bgcolor="grey50",
                border_radius=8,
                border=ft.Border.all(1, "grey300")
            )

        boton_volver = ft.Button(
            "Volver al Catálogo de Aves",
            icon=ft.Icons.ARROW_BACK,
            on_click=mostrar_enciclopedia
        )

        ficha_individual = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    boton_volver,
                    ft.Divider(),
                    construir_widget_imagen(imagen, alto=240),
                    ft.Text(nombre_comun, size=24, weight=ft.FontWeight.BOLD, color="green900"),
                    ft.Text(f"Nombre científico: {nombre_cientifico}", size=16, italic=True, color="grey700"),
                    ft.Divider(),
                    crear_fila_dato("Clasificación Taxonómica", f"Orden: {orden_tax}  |  Familia: {familia}"),
                    crear_fila_dato("Estado de Conservación (UICN / NOM-059)", conservacion, "red800" if "Vulnerable" in conservacion or "Peligro" in conservacion else "green800"),
                    crear_fila_dato("Rareza y Avistamiento", rareza, "blue800"),
                    crear_fila_dato("Morfometría (Envergadura / Peso)", medidas),
                    crear_fila_dato("Dieta y Gremio Trófico", dieta),
                    crear_fila_dato("Hábitat y Distribución Ecológica", habitat),
                    crear_fila_dato("Descripción Científica", descripcion),
                ], spacing=10),
                padding=20,
                bgcolor="white",
                border_radius=12,
                width=760
            )
        )

        content_area.controls.append(ficha_individual)
        page.update()

    def mostrar_enciclopedia(e=None):
        content_area.controls.clear()
        aves = obtener_aves()

        content_area.controls.append(
            ft.Column([
                ft.Text(f"Catálogo Ornitológico ({len(aves)} especies)", size=20, weight=ft.FontWeight.BOLD, color="green900", text_align=ft.TextAlign.CENTER),
                ft.Text("Selecciona cualquier especie para abrir su pantalla individual con datos científicos completos.", size=12, color="grey700", text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2)
        )

        for ave in aves:
            ave_id, nombre_comun, nombre_cientifico, orden_tax, familia, conservacion, rareza, *_, imagen = ave

            ruta_abs = os.path.join(ASSETS_DIR, imagen.replace("/", os.sep))
            miniatura = (
                ft.Image(src=imagen, width=64, height=64, fit=ft.BoxFit.COVER, border_radius=8)
                if os.path.exists(ruta_abs)
                else ft.Container(
                    content=ft.Icon(ft.Icons.PHOTO_CAMERA, color="green700", size=28),
                    width=64, height=64, bgcolor="green50", border_radius=8,
                    alignment=ft.Alignment.CENTER
                )
            )

            tarjeta_lista = ft.Card(
                content=ft.Container(
                    content=ft.Row([
                        miniatura,
                        ft.Column([
                            ft.Text(nombre_comun, size=16, weight=ft.FontWeight.BOLD, color="green800"),
                            ft.Text(f"{nombre_cientifico} • {familia}", italic=True, size=12, color="grey700"),
                            ft.Text(f"Rareza: {rareza}", size=12, color="bluegrey700")
                        ], expand=True, spacing=2),
                        ft.Button(
                            "Ver ficha",
                            icon=ft.Icons.VISIBILITY,
                            on_click=lambda e, a=ave: mostrar_detalle_ave(a)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=12,
                    bgcolor="white",
                    border_radius=10,
                    width=760
                )
            )
            content_area.controls.append(tarjeta_lista)

        page.update()

    # =========================================================
    # MÓDULO ÚNICO CONTINUO: 30 QUIZZES + 10 RETOS DE EMPAREJAMIENTO
    # =========================================================
    def mostrar_evaluacion_unificada(e=None):
        nonlocal puntaje, indice_global
        content_area.controls.clear()

        quizzes = obtener_quizzes()
        matchings = obtener_matching_quizzes()
        total_pasos = len(quizzes) + len(matchings)  # 40 desafíos seguidos sin selección manual

        if total_pasos == 0:
            content_area.controls.append(ft.Text("No hay actividades disponibles en la base de datos."))
            page.update()
            return

        if indice_global >= total_pasos:
            def reiniciar_todo(e):
                nonlocal indice_global
                indice_global = 0
                mostrar_evaluacion_unificada()

            content_area.controls.append(
                ft.Container(
                    content=ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.EMOJI_EVENTS, size=68, color="amber"),
                                ft.Text(
                                    "¡Felicidades! Has completado todos los Quizzes y Retos",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color="deeporange",
                                    text_align=ft.TextAlign.CENTER
                                ),
                                txt_puntaje,
                                ft.Text(
                                    "Completaste las 30 preguntas y los 10 retos de emparejamiento en secuencia.",
                                    size=14,
                                    color="grey700",
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Button("Reiniciar Evaluación Completa", icon=ft.Icons.REFRESH, on_click=reiniciar_todo)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=14),
                            padding=28,
                            bgcolor="white",
                            border_radius=12,
                            width=700
                        )
                    ),
                    alignment=ft.Alignment.CENTER
                )
            )
            page.update()
            return

        # -----------------------------------------------------
        # PARTE A: QUIZZES DE OPCIÓN MÚLTIPLE (Índices 0 al 29)
        # -----------------------------------------------------
        if indice_global < len(quizzes):
            pregunta, op_a, op_b, op_c, op_d, correcta = quizzes[indice_global]
            respondido = False
            txt_resultado = ft.Text("", weight=ft.FontWeight.BOLD, size=14, text_align=ft.TextAlign.CENTER)

            btn_siguiente = ft.Button(
                "Siguiente desafío",
                icon=ft.Icons.NAVIGATE_NEXT,
                visible=False
            )

            def avanzar_quiz(e=None):
                nonlocal indice_global
                indice_global += 1
                mostrar_evaluacion_unificada()

            btn_siguiente.on_click = avanzar_quiz

            botones_opciones = []

            def verificar(opcion_elegida):
                nonlocal puntaje, respondido
                if respondido:
                    return
                respondido = True

                for b in botones_opciones:
                    b.disabled = True

                if opcion_elegida == correcta:
                    puntaje += 10
                    txt_puntaje.value = f"Puntaje acumulado: {puntaje} pts"
                    txt_resultado.value = "¡Respuesta Correcta! +10 puntos."
                    txt_resultado.color = "green700"
                else:
                    txt_resultado.value = f"Respuesta Incorrecta. La correcta era: {correcta}"
                    txt_resultado.color = "red700"

                btn_siguiente.visible = True
                page.update()

            opciones = [op_a, op_b, op_c, op_d]
            for op in opciones:
                botones_opciones.append(
                    ft.Button(op, on_click=lambda e, o=op: verificar(o), width=480)
                )

            caja_pregunta_llamativa = ft.Container(
                content=ft.Text(
                    pregunta,
                    size=17,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    text_align=ft.TextAlign.CENTER
                ),
                bgcolor="deeporange600",
                padding=16,
                border_radius=10,
                width=640,
                alignment=ft.Alignment.CENTER
            )

            tarjeta_quiz = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Evaluación Ornitológica Continua",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="deeppurple",
                            text_align=ft.TextAlign.CENTER
                        ),
                        txt_puntaje,
                        ft.Text(
                            f"Desafío {indice_global + 1} de {total_pasos}",
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color="grey700",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.ProgressBar(value=(indice_global + 1) / total_pasos, color="deeporange", bgcolor="orange100"),
                        ft.Divider(),
                        caja_pregunta_llamativa,
                        ft.Column(
                            botones_opciones,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        txt_resultado,
                        btn_siguiente
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                    padding=24,
                    bgcolor="white",
                    border_radius=12,
                    width=740
                )
            )

            content_area.controls.append(
                ft.Container(content=tarjeta_quiz, alignment=ft.Alignment.CENTER)
            )
            page.update()
            return

        # -----------------------------------------------------
        # PARTE B: RETOS DE EMPAREJAMIENTO (Índices 30 al 39)
        # -----------------------------------------------------
        idx_match = indice_global - len(quizzes)
        titulo, instruccion, pares_raw = matchings[idx_match]
        pares = [item.split("::") for item in pares_raw.split("||")]
        mapa_correcto = {ave: dato for ave, dato in pares}

        aves_izq = [ave for ave, _ in pares]
        datos_der = [dato for _, dato in pares]
        random.shuffle(datos_der)

        seleccion_ave = None
        seleccion_dato = None
        emparejados = set()

        txt_estado_match = ft.Text(
            "Selecciona un ave (izquierda) y luego su dato correspondiente (derecha).",
            size=13,
            color="bluegrey800",
            text_align=ft.TextAlign.CENTER
        )

        btn_siguiente_match = ft.Button(
            "Siguiente desafío",
            icon=ft.Icons.NAVIGATE_NEXT,
            visible=False
        )

        def avanzar_matching(e):
            nonlocal indice_global
            indice_global += 1
            mostrar_evaluacion_unificada()

        btn_siguiente_match.on_click = avanzar_matching

        botones_izq = {}
        botones_der = {}

        def evaluar_par():
            nonlocal seleccion_ave, seleccion_dato, puntaje
            if seleccion_ave is None or seleccion_dato is None:
                return

            if mapa_correcto[seleccion_ave] == seleccion_dato:
                emparejados.add(seleccion_ave)
                puntaje += 5
                txt_puntaje.value = f"Puntaje acumulado: {puntaje} pts"

                botones_izq[seleccion_ave].disabled = True
                botones_izq[seleccion_ave].icon = ft.Icons.CHECK_CIRCLE
                botones_der[seleccion_dato].disabled = True
                botones_der[seleccion_dato].icon = ft.Icons.CHECK_CIRCLE

                txt_estado_match.value = f"¡Correcto! {seleccion_ave} ↔ {seleccion_dato} (+5 pts)"
                txt_estado_match.color = "green700"
            else:
                txt_estado_match.value = f"No coincide: '{seleccion_ave}' con '{seleccion_dato}'. Intenta de nuevo."
                txt_estado_match.color = "red700"

            seleccion_ave = None
            seleccion_dato = None

            if len(emparejados) == len(pares):
                txt_estado_match.value = "¡Excelente! Emparejaste todos los puntos de este reto."
                btn_siguiente_match.visible = True

            page.update()

        def click_ave(ave_nombre):
            nonlocal seleccion_ave
            seleccion_ave = ave_nombre
            txt_estado_match.value = f"Ave seleccionada: {ave_nombre} → Ahora elige su dato a la derecha."
            txt_estado_match.color = "deeppurple"
            page.update()
            evaluar_par()

        def click_dato(dato_texto):
            nonlocal seleccion_dato
            seleccion_dato = dato_texto
            txt_estado_match.value = f"Dato seleccionado: {dato_texto} → Ahora elige el ave a la izquierda."
            txt_estado_match.color = "deeppurple"
            page.update()
            evaluar_par()

        col_izquierda = ft.Column(
            [ft.Text("Especies", weight=ft.FontWeight.BOLD, color="deeppurple", text_align=ft.TextAlign.CENTER)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
        )

        col_derecha = ft.Column(
            [ft.Text("Datos Científicos / Rasgos", weight=ft.FontWeight.BOLD, color="deeppurple", text_align=ft.TextAlign.CENTER)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
        )

        for ave_nom in aves_izq:
            b_izq = ft.Button(
                ave_nom,
                icon=ft.Icons.RADIO_BUTTON_UNCHECKED,
                on_click=lambda e, a=ave_nom: click_ave(a),
                width=260
            )
            botones_izq[ave_nom] = b_izq
            col_izquierda.controls.append(b_izq)

        for d_txt in datos_der:
            b_der = ft.Button(
                d_txt,
                icon=ft.Icons.RADIO_BUTTON_UNCHECKED,
                on_click=lambda e, d=d_txt: click_dato(d),
                width=350
            )
            botones_der[d_txt] = b_der
            col_derecha.controls.append(b_der)

        banner_reto_llamativo = ft.Container(
            content=ft.Column([
                ft.Text(
                    titulo,
                    size=17,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    instruccion,
                    size=13,
                    color="amber100",
                    text_align=ft.TextAlign.CENTER
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
            bgcolor="deeppurple700",
            padding=14,
            border_radius=10,
            width=640,
            alignment=ft.Alignment.CENTER
        )

        tarjeta_matching = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Evaluación Ornitológica Continua",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="deeppurple",
                        text_align=ft.TextAlign.CENTER
                    ),
                    txt_puntaje,
                    ft.Text(
                        f"Desafío {indice_global + 1} de {total_pasos}",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color="grey700",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.ProgressBar(value=(indice_global + 1) / total_pasos, color="deeppurple", bgcolor="purple100"),
                    ft.Divider(),
                    banner_reto_llamativo,
                    ft.Row(
                        [col_izquierda, col_derecha],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        spacing=20,
                        wrap=True
                    ),
                    ft.Divider(),
                    txt_estado_match,
                    btn_siguiente_match
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                padding=24,
                bgcolor="white",
                border_radius=12,
                width=740
            )
        )

        content_area.controls.append(
            ft.Container(content=tarjeta_matching, alignment=ft.Alignment.CENTER)
        )
        page.update()

    nav_bar = ft.Row([
        ft.Button("Enciclopedia (15 Aves)", icon=ft.Icons.BOOK, on_click=mostrar_enciclopedia),
        ft.Button("Quizzes y Retos (40)", icon=ft.Icons.QUIZ, on_click=mostrar_evaluacion_unificada),
    ], alignment=ft.MainAxisAlignment.CENTER, wrap=True)

    page.add(
        ft.Column([
            ft.Text("AvianVisual — Enciclopedia Ornitológica", size=22, weight=ft.FontWeight.BOLD, color="green900", text_align=ft.TextAlign.CENTER),
            nav_bar,
            ft.Divider(),
            content_area
        ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    mostrar_enciclopedia()


if __name__ == "__main__":
    ft.run(main, assets_dir=ASSETS_DIR)
