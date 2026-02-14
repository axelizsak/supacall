"""
Script to display reservations in a formatted view.
"""
import asyncio
from datetime import datetime
from database import db


async def display_reservations():
    """Displays all reservations in a formatted layout"""

    # Initialize the database
    await db.init_db()

    # Retrieve all reservations
    reservations = await db.get_all_reservations()

    if not reservations:
        print("\n📅 No reservations yet.\n")
        return

    print("\n" + "="*80)
    print(f"📅 RESERVATIONS ({len(reservations)} total)")
    print("="*80 + "\n")

    # Group by date
    reservations_by_date = {}
    for res in reservations:
        date = res['date']
        if date not in reservations_by_date:
            reservations_by_date[date] = []
        reservations_by_date[date].append(res)

    # Display by date
    for date in sorted(reservations_by_date.keys(), reverse=True):
        date_reservations = reservations_by_date[date]

        # Format the date
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_formatted = date_obj.strftime('%A %d %B %Y')
        except:
            date_formatted = date

        print(f"📆 {date_formatted}")
        print("-" * 80)

        # Sort by time
        date_reservations.sort(key=lambda x: x['heure'])

        for res in date_reservations:
            status_emoji = "✅" if res['status'] == 'confirmed' else "❌"

            print(f"""
  {status_emoji} ID: {res['id']}
     👤 Name: {res['nom']}
     📞 Phone: {res['telephone']}
     🕐 Time: {res['heure']}
     👥 Guests: {res['nombre_personnes']}
     💬 Comments: {res['commentaires'] or 'None'}
     📅 Created at: {res['created_at']}
            """)

        total_personnes = sum(r['nombre_personnes'] for r in date_reservations)
        print(f"\n  📊 Total for this date: {len(date_reservations)} reservation(s) | {total_personnes} guest(s)")
        print("\n")

    print("="*80 + "\n")


async def display_statistics():
    """Displays reservation statistics"""

    reservations = await db.get_all_reservations()

    if not reservations:
        return

    print("📊 STATISTICS")
    print("="*80)

    total_reservations = len(reservations)
    total_personnes = sum(r['nombre_personnes'] for r in reservations)
    avg_personnes = total_personnes / total_reservations if total_reservations > 0 else 0

    # Find the largest reservation
    max_reservation = max(reservations, key=lambda x: x['nombre_personnes'])

    print(f"""
  📈 Total reservations: {total_reservations}
  👥 Total guests: {total_personnes}
  📊 Average per reservation: {avg_personnes:.1f} guests
  🏆 Largest reservation: {max_reservation['nombre_personnes']} guests ({max_reservation['nom']})
    """)

    # Reservations by date
    dates = {}
    for res in reservations:
        date = res['date']
        dates[date] = dates.get(date, 0) + 1

    print("  📅 Reservations by date:")
    for date, count in sorted(dates.items())[:5]:  # Top 5 dates
        print(f"     - {date}: {count} reservation(s)")

    print("\n" + "="*80 + "\n")


async def main():
    """Main function"""
    print("\n🍽️  RESERVATION MANAGEMENT SYSTEM")

    await display_reservations()
    await display_statistics()


if __name__ == "__main__":
    asyncio.run(main())
