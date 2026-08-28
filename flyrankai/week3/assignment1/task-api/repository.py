import os
import psycopg2
from psycopg2.extras import RealDictCursor


class TaskRepository:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")

        if not self.database_url:
            raise RuntimeError("DATABASE_URL is not set")

    def get_connection(self):
        return psycopg2.connect(self.database_url)

    def get_all(self):
        connection = self.get_connection()

        try:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT id, title, done FROM tasks ORDER BY id"
                )
                return cursor.fetchall()
        finally:
            connection.close()

    def get_by_id(self, task_id):
        connection = self.get_connection()

        try:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT id, title, done FROM tasks WHERE id = %s",
                    (task_id,)
                )
                return cursor.fetchone()
        finally:
            connection.close()

    def create(self, title):
        connection = self.get_connection()

        try:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (title, done)
                    VALUES (%s, FALSE)
                    RETURNING id, title, done
                    """,
                    (title,)
                )
                task = cursor.fetchone()
                connection.commit()
                return task
        finally:
            connection.close()

    def update(self, task_id, title, done):
        connection = self.get_connection()

        try:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET title = %s, done = %s
                    WHERE id = %s
                    RETURNING id, title, done
                    """,
                    (title, done, task_id)
                )
                task = cursor.fetchone()
                connection.commit()
                return task
        finally:
            connection.close()

    def delete(self, task_id):
        connection = self.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM tasks WHERE id = %s",
                    (task_id,)
                )

                deleted = cursor.rowcount > 0
                connection.commit()

                return deleted
        finally:
            connection.close()