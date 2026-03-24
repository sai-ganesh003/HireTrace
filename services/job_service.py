from app import get_db

class JobService:
    
    @staticmethod
    def add_job(user_id, company, position, status, applied_date, follow_up_date, notes):
        """Add a new job"""
        conn = get_db()
        cursor = conn.cursor()
        sql = """INSERT INTO jobs (user_id, company, position, status, applied_date, follow_up_date, notes)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (user_id, company, position, status, applied_date, follow_up_date, notes))
        conn.commit()
        job_id = cursor.lastrowid
        conn.close()
        return job_id
    
    @staticmethod
    def get_job(job_id, user_id):
        """Get a single job"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE id = %s AND user_id = %s", (job_id, user_id))
        job = cursor.fetchone()
        conn.close()
        return job
    
    @staticmethod
    def get_all_jobs(user_id):
        """Get all jobs for a user"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE user_id = %s ORDER BY applied_date DESC", (user_id,))
        jobs = cursor.fetchall()
        conn.close()
        return jobs
    
    @staticmethod
    def update_job(job_id, user_id, company, position, status, applied_date, follow_up_date, notes):
        """Update a job"""
        conn = get_db()
        cursor = conn.cursor()
        sql = """UPDATE jobs SET company=%s, position=%s, status=%s, applied_date=%s, follow_up_date=%s, notes=%s 
                 WHERE id=%s AND user_id=%s"""
        cursor.execute(sql, (company, position, status, applied_date, follow_up_date, notes, job_id, user_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete_job(job_id, user_id):
        """Delete a job"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs WHERE id = %s AND user_id = %s", (job_id, user_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def change_status(job_id, user_id, status):
        """Change job status"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE jobs SET status = %s WHERE id = %s AND user_id = %s", (status, job_id, user_id))
        conn.commit()
        conn.close()