import random
import oracledb
from datetime import datetime

DB_USER = "SYSTEM"
DB_PASSWORD = "oracle"
DB_HOST = "localhost"
DB_PORT = 1522
DB_SERVICE = "XE"

# Données Sénégal
UNIVERSITIES = {
    "Public": [
        {"name": "UCAD-Dakar", "region": "Dakar", "des": True},
        {"name": "UIB-Thies", "region": "Thiès", "des": True},
        {"name": "UAS-Ziguinchor", "region": "Ziguinchor", "des": True},
        {"name": "UGB-Saint-Louis", "region": "Saint-Louis", "des": False},
        {"name": "UAD-Bambey", "region": "Bambey", "des": False},
        {"name": "UADB-Kaolack", "region": "Kaolack", "des": False},
        {"name": "UASZ-Kolda", "region": "Kolda", "des": False},
    ],
    "Private": [
        {"name": "EINS-Dakar", "region": "Dakar", "des": False},
        {"name": "EU-Dakar", "region": "Dakar", "des": False},
        {"name": "IPFORMED-Dakar", "region": "Dakar", "des": False},
        {"name": "USSD-Dakar", "region": "Dakar", "des": False},
        {"name": "HmpthB-Dakar", "region": "Dakar", "des": False},
    ]
}

STRUCTURES = {
    "Public": {
        "Dakar": ["HEAR", "HOGIP", "Fann", "HPD", "HMO", "IHS", "DllJm", "SmMncpal", "Pkn", "GsprdCmr", "RBdn", "Wkm", "KrMssr", "aBssNDw", "PMSghr", "CMIA", "Rfsqe", "HED"],
        "Regions": ["HRThs", "HMT", "Mbr", "Twwn", "MlBfzwn", "KMRSSL", "Ndmt", "Drbl", "Ftck", "Klck", "Kffrn", "Tmb", "Lg", "Lngr", "St-Ls", "RchrdTll", "Ndm", "aGNM", "Wrssg", "Mtm", "HRZchr", "HPxZchr", "Sdh", "Kld", "Bgnn"]
    },
    "Private": {
        "Dakar": ["ClnqCp", "ClnqMdln", "Ath", "NAT", "YnssLrq", "NdmYctm", "EMD", "NdngPlr", "MDng", "Mygu", "Aldo"],
        "Regions": ["Ths", "BlBssiMbr"]
    }
}

def create_tables(conn):
    """Crée les tables"""
    cursor = conn.cursor()
    
    # Drop tables if exist
    for table in ["ORL_PRACTITIONERS", "ORL_STUDENTS", "ORL_STRUCTURES", "ORL_UNIVERSITIES"]:
        cursor.execute(f"BEGIN EXECUTE IMMEDIATE 'DROP TABLE {table}'; EXCEPTION WHEN OTHERS THEN NULL; END;")
    
    # Universities
    cursor.execute("""
        CREATE TABLE ORL_UNIVERSITIES (
            UNIVERSITY_ID NUMBER PRIMARY KEY,
            NAME VARCHAR2(100),
            REGION VARCHAR2(50),
            SECTOR VARCHAR2(20),
            HAS_DES NUMBER,
            CREATED_AT TIMESTAMP DEFAULT SYSDATE
        )
    """)
    
    # Structures
    cursor.execute("""
        CREATE TABLE ORL_STRUCTURES (
            STRUCTURE_ID NUMBER PRIMARY KEY,
            NAME VARCHAR2(100),
            REGION VARCHAR2(50),
            SECTOR VARCHAR2(20),
            TYPE VARCHAR2(50),
            CREATED_AT TIMESTAMP DEFAULT SYSDATE
        )
    """)
    
    # Practitioners
    cursor.execute("""
        CREATE TABLE ORL_PRACTITIONERS (
            PRACTITIONER_ID NUMBER PRIMARY KEY,
            NAME VARCHAR2(100),
            SPECIALIZATION VARCHAR2(50),
            EXPERIENCE_YEARS NUMBER,
            STRUCTURE_ID NUMBER,
            UNIVERSITY_ID NUMBER,
            SECTOR VARCHAR2(20),
            REGION VARCHAR2(50),
            CREATED_AT TIMESTAMP DEFAULT SYSDATE,
            FOREIGN KEY (STRUCTURE_ID) REFERENCES ORL_STRUCTURES(STRUCTURE_ID),
            FOREIGN KEY (UNIVERSITY_ID) REFERENCES ORL_UNIVERSITIES(UNIVERSITY_ID)
        )
    """)
    
    # Students (DES)
    cursor.execute("""
        CREATE TABLE ORL_STUDENTS (
            STUDENT_ID NUMBER PRIMARY KEY,
            NAME VARCHAR2(100),
            DES_YEAR NUMBER,
            UNIVERSITY_ID NUMBER,
            STRUCTURE_ID NUMBER,
            REGION VARCHAR2(50),
            CREATED_AT TIMESTAMP DEFAULT SYSDATE,
            FOREIGN KEY (UNIVERSITY_ID) REFERENCES ORL_UNIVERSITIES(UNIVERSITY_ID),
            FOREIGN KEY (STRUCTURE_ID) REFERENCES ORL_STRUCTURES(STRUCTURE_ID)
        )
    """)
    
    conn.commit()
    cursor.close()

def insert_universities(conn):
    """Insère les universités"""
    cursor = conn.cursor()
    uni_id = 1
    
    for sector, unis in UNIVERSITIES.items():
        for uni in unis:
            cursor.execute("""
                INSERT INTO ORL_UNIVERSITIES (UNIVERSITY_ID, NAME, REGION, SECTOR, HAS_DES)
                VALUES (:1, :2, :3, :4, :5)
            """, (uni_id, uni["name"], uni["region"], sector, 1 if uni["des"] else 0))
            uni_id += 1
    
    conn.commit()
    print(f"✓ {uni_id-1} universités insérées")
    cursor.close()

def insert_structures(conn):
    """Insère les structures"""
    cursor = conn.cursor()
    struct_id = 1
    
    for sector, locations in STRUCTURES.items():
        for location, names in locations.items():
            region = "Dakar" if location == "Dakar" else "Régions"
            for name in names:
                cursor.execute("""
                    INSERT INTO ORL_STRUCTURES (STRUCTURE_ID, NAME, REGION, SECTOR, TYPE)
                    VALUES (:1, :2, :3, :4, :5)
                """, (struct_id, name, region, sector, "Hôpital" if sector == "Public" else "Clinique"))
                struct_id += 1
    
    conn.commit()
    print(f"✓ {struct_id-1} structures insérées")
    cursor.close()

def insert_practitioners(conn):
    """Insère les praticiens (108)"""
    cursor = conn.cursor()
    pract_id = 1
    
    cursor.execute("SELECT STRUCTURE_ID FROM ORL_STRUCTURES")
    structures = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT UNIVERSITY_ID FROM ORL_UNIVERSITIES")
    universities = [row[0] for row in cursor.fetchall()]
    
    for i in range(108):
        name = f"Dr. Praticien {i+1}"
        exp = random.randint(2, 35)
        struct = random.choice(structures)
        uni = random.choice(universities)
        sector = random.choice(["Public", "Private"])
        region = random.choice(["Dakar", "Thiès", "Saint-Louis", "Ziguinchor", "Kaolack", "Kolda"])
        
        cursor.execute("""
            INSERT INTO ORL_PRACTITIONERS (PRACTITIONER_ID, NAME, SPECIALIZATION, EXPERIENCE_YEARS, STRUCTURE_ID, UNIVERSITY_ID, SECTOR, REGION)
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
        """, (pract_id, name, "ORL", exp, struct, uni, sector, region))
        pract_id += 1
    
    conn.commit()
    print(f"✓ 108 praticiens insérés")
    cursor.close()

def insert_students(conn):
    """Insère les étudiants (185 DES)"""
    cursor = conn.cursor()
    student_id = 1
    
    cursor.execute("SELECT UNIVERSITY_ID FROM ORL_UNIVERSITIES WHERE HAS_DES = 1")
    des_universities = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT STRUCTURE_ID FROM ORL_STRUCTURES")
    structures = [row[0] for row in cursor.fetchall()]
    
    des_distribution = [65, 56, 48, 16]  # DES1, DES2, DES3, DES4
    
    for year, count in enumerate(des_distribution, 1):
        for i in range(count):
            name = f"Etudiant DES{year} {i+1}"
            uni = random.choice(des_universities)
            struct = random.choice(structures)
            region = random.choice(["Dakar", "Thiès", "Saint-Louis", "Ziguinchor"])
            
            cursor.execute("""
                INSERT INTO ORL_STUDENTS (STUDENT_ID, NAME, DES_YEAR, UNIVERSITY_ID, STRUCTURE_ID, REGION)
                VALUES (:1, :2, :3, :4, :5, :6)
            """, (student_id, name, year, uni, struct, region))
            student_id += 1
    
    conn.commit()
    print(f"✓ 185 étudiants (DES) insérés")
    cursor.close()

def main():
    try:
        print("Connexion à Oracle...")
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"
        )
        
        print("Création des tables...")
        create_tables(conn)
        
        print("Insertion des données...")
        insert_universities(conn)
        insert_structures(conn)
        insert_practitioners(conn)
        insert_students(conn)
        
        conn.close()
        
        print("\n✅ Dataset ORL Sénégal créé avec succès !")
        print(f"   • 12 universités")
        print(f"   • 56 structures")
        print(f"   • 108 praticiens")
        print(f"   • 185 étudiants (DES)")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    main()
