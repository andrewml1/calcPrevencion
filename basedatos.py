import json
import psycopg2

def credenciales(usuario):
    # Specify the filename
    filename = "database_config.json"

    # Load the JSON data from the file
    with open(filename, "r") as json_file:
        data = json.load(json_file)

    # Choose a user (e.g., "Admin" or "SanPedro")
    chosen_user = usuario

    # Get the attributes for the chosen user
    user_attributes = data.get(chosen_user, None)
    return user_attributes

def crearTablasPostgres(credenciales):
    conn = psycopg2.connect(
        database=credenciales["database"],
        user=credenciales["user"],
        password=credenciales["password"],
        host=credenciales["host"],
        port=credenciales["port"]
    )

    cursor = conn.cursor()
    table_name = 'findrisc'

    # Verificar si la tabla ya existe
    cursor.execute(
        f"SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name='{table_name}'"
    )
    result = cursor.fetchone()

    # Crear la tabla si no existe
    if not result:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS findrisc (
                id SERIAL PRIMARY KEY,
                id_number TEXT NOT NULL,
                age INTEGER NOT NULL,
                height REAL NOT NULL,
                weight REAL NOT NULL,
                waist REAL NOT NULL,
                gender TEXT NOT NULL,
                physical_activity INTEGER NOT NULL,
                fruit_vegetables INTEGER NOT NULL,
                hypertension_meds INTEGER NOT NULL,
                high_glucose INTEGER NOT NULL,
                family_diabetes INTEGER NOT NULL,
                score INTEGER,
                risk TEXT,
                bmi REAL,
                bmi_score INTEGER,
                waist_score INTEGER,
                age_score INTEGER
            );
        ''')

    conn.commit()  # No olvides hacer commit de los cambios después de crear las tablas
    cursor.close()  # Cerrar el cursor
    conn.close()  # Cerrar la conexión

def guardar_datos(id_number, age, height, weight, waist, gender, bmi_score, waist_score,
                      physical_activity, fruit_vegetables, hypertension_meds, high_glucose,
                      family_diabetes, age_score, score, risk, bmi, credenciales):

        conn = psycopg2.connect(
            database=credenciales["database"],
            user=credenciales["user"],
            password=credenciales["password"],
            host=credenciales["host"],
            port=credenciales["port"]
        )

        cursor = conn.cursor()

        query = f"""
            INSERT INTO findrisc (
                id_number, age, height, weight, waist, gender, bmi_score, waist_score,
                physical_activity, fruit_vegetables, hypertension_meds, high_glucose,
                family_diabetes, age_score, score, risk, bmi
            )
            VALUES (
                '{id_number}', {age}, {height}, {weight}, {waist}, '{gender}', {bmi_score}, {waist_score},
                {physical_activity}, {fruit_vegetables}, {hypertension_meds}, {high_glucose},
                {family_diabetes}, {age_score}, {score}, '{risk}', {bmi}
            )
        """

        cursor.execute(query)

        conn.commit()
        conn.close()


# cred= credenciales("prosalco")
# crearTablasPostgres(cred)

