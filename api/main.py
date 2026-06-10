from fastapi import FastAPI
import os
import oracledb

app = FastAPI(
    title="ORL Sénégal API",
    version="1.0"
)

def get_connection():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dsn = f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_SERVICE')}"
    return oracledb.connect(user=user, password=password, dsn=dsn)

@app.get("/")
def home():
    return {"message": "ORL Sénégal API", "status": "running"}

@app.get("/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "ok"}
    except:
        return {"status": "error"}

@app.get("/statistics/summary")
def get_summary():
    """Résumé statistiques"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Compter les entités
        cursor.execute("SELECT COUNT(*) FROM ORL_UNIVERSITIES")
        unis = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ORL_STRUCTURES")
        structs = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ORL_PRACTITIONERS")
        practi = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ORL_STUDENTS")
        students = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "universities": unis,
            "structures": structs,
            "practitioners": practi,
            "students": students,
            "total": unis + structs + practi + students
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/statistics/universities")
def get_universities_stats():
    """Statistiques universités"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SECTOR, COUNT(*) as count, SUM(HAS_DES) as with_des
            FROM ORL_UNIVERSITIES
            GROUP BY SECTOR
        """)
        
        result = []
        for row in cursor.fetchall():
            result.append({
                "sector": row[0],
                "total": row[1],
                "with_des": row[2] or 0
            })
        
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/statistics/structures")
def get_structures_stats():
    """Statistiques structures"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SECTOR, REGION, COUNT(*) as count
            FROM ORL_STRUCTURES
            GROUP BY SECTOR, REGION
            ORDER BY SECTOR, REGION
        """)
        
        result = []
        for row in cursor.fetchall():
            result.append({
                "sector": row[0],
                "region": row[1],
                "count": row[2]
            })
        
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/statistics/practitioners")
def get_practitioners_stats():
    """Statistiques praticiens"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SECTOR, REGION, COUNT(*) as count, ROUND(AVG(EXPERIENCE_YEARS), 1) as avg_experience
            FROM ORL_PRACTITIONERS
            GROUP BY SECTOR, REGION
            ORDER BY SECTOR, REGION
        """)
        
        result = []
        for row in cursor.fetchall():
            result.append({
                "sector": row[0],
                "region": row[1],
                "count": row[2],
                "avg_experience": float(row[3]) if row[3] else 0
            })
        
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/statistics/students")
def get_students_stats():
    """Statistiques étudiants"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DES_YEAR, REGION, COUNT(*) as count
            FROM ORL_STUDENTS
            GROUP BY DES_YEAR, REGION
            ORDER BY DES_YEAR, REGION
        """)
        
        result = []
        for row in cursor.fetchall():
            result.append({
                "des_year": row[0],
                "region": row[1],
                "count": row[2]
            })
        
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/universities")
def get_all_universities():
    """Toutes les universités"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT UNIVERSITY_ID, NAME, REGION, SECTOR, HAS_DES
            FROM ORL_UNIVERSITIES
            ORDER BY SECTOR, NAME
        """)
        
        result = []
        for row in cursor.fetchall():
            result.append({
                "id": row[0],
                "name": row[1],
                "region": row[2],
                "sector": row[3],
                "has_des": bool(row[4])
            })
        
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/structures")
def get_all_structures():
    """Toutes les structures"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT STRUCTURE_ID, NAME, REGION, SECTOR, TYPE
            FROM ORL_STRUCTURES
            ORDER BY SECTOR, REGION, NAME
        """)
        
        result = []
        for row in cursor.fetchall():
            result.append({
                "id": row[0],
                "name": row[1],
                "region": row[2],
                "sector": row[3],
                "type": row[4]
            })
        
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}
