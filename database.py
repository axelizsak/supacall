"""
Database management for reservations.
"""
import aiosqlite
import asyncio
from datetime import datetime
from typing import List, Dict, Optional


class ReservationDB:
    def __init__(self, db_path: str = "reservations.db"):
        self.db_path = db_path

    async def init_db(self):
        """Initializes the database with the required tables"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    telephone TEXT NOT NULL,
                    date TEXT NOT NULL,
                    heure TEXT NOT NULL,
                    nombre_personnes INTEGER NOT NULL,
                    commentaires TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'confirmed'
                )
            """)
            await db.commit()

    async def create_reservation(
        self,
        nom: str,
        telephone: str,
        date: str,
        heure: str,
        nombre_personnes: int,
        commentaires: str = ""
    ) -> Dict:
        """Creates a new reservation"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO reservations
                (nom, telephone, date, heure, nombre_personnes, commentaires)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nom, telephone, date, heure, nombre_personnes, commentaires))
            await db.commit()

            return {
                "id": cursor.lastrowid,
                "nom": nom,
                "telephone": telephone,
                "date": date,
                "heure": heure,
                "nombre_personnes": nombre_personnes,
                "commentaires": commentaires,
                "status": "confirmed"
            }

    async def get_reservations_by_date(self, date: str) -> List[Dict]:
        """Retrieves all reservations for a given date"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM reservations WHERE date = ? ORDER BY heure",
                (date,)
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]

    async def check_availability(self, date: str, heure: str, nombre_personnes: int) -> bool:
        """Checks availability for a given date and time"""
        reservations = await self.get_reservations_by_date(date)

        # Count total guests within a 2-hour window around the requested time
        total_personnes = sum(
            r['nombre_personnes'] for r in reservations
            if abs(self._time_to_minutes(r['heure']) - self._time_to_minutes(heure)) < 120
        )

        # Maximum capacity (configurable)
        MAX_CAPACITY = 50

        return (total_personnes + nombre_personnes) <= MAX_CAPACITY

    def _time_to_minutes(self, time_str: str) -> int:
        """Converts a time string (HH:MM) to minutes since midnight"""
        try:
            h, m = map(int, time_str.split(':'))
            return h * 60 + m
        except:
            return 0

    async def get_all_reservations(self) -> List[Dict]:
        """Retrieves all reservations"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM reservations ORDER BY date DESC, heure DESC"
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]


# Global instance
db = ReservationDB()
