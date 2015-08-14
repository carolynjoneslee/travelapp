from model import *
from server import app
import geocoder
from datetime import datetime
from json import loads


def load_users():
	"""Load carolyn & balloonicorn into database"""

	file = open('static/data/users.txt')

	for line in file:
		fname, lname, email, password, img_url = line.rstrip().split(",")

		user = User(fname=fname,
				   lname=lname,
				   email=email,
				   password=password,
				   img_url = img_url
				   )
		db.session.add(user)



def load_trips():
	"""Load carolyn's vacation into database"""

	file = open('static/data/trips.txt')

	for line in file:
		admin_id, title, start, end, destination = line.rstrip().split("|")

		admin_id = int(admin_id)
		start = datetime.strptime(start, "%Y, %m, %d")
		end = datetime.strptime(end, "%Y, %m, %d")

		destination = geocoder.google(destination)
		address = destination.address
		lat = destination.lat
		lng = destination.lng
		city = destination.city
		country_code = destination.country

		trip = Trip(admin_id=admin_id,
					title=title,
					start=start,
					end=end,
					latitude=lat,
					longitude=lng,
					address=address,
					city=city,
					country_code=country_code
					)
		db.session.add(trip)
		db.session.commit()

		# Create admin permission
		perm = Permission(trip_id=trip.trip_id,
				  user_id=admin_id,
				  can_edit=True
				  )
		db.session.add(perm)
		trip.create_days()




def load_permissions():
	"""Load permissions for Carolyn & Balloonicorn on carolyn's vacation"""

	file = open("static/data/permissions.txt")

	for line in file:
		trip_id, user_id, can_view, can_edit = line.rstrip().split(",")

		can_edit = loads(can_edit.lower())

		perm = Permission(trip_id=trip_id,
					  user_id=user_id,
					  can_edit=can_edit
					  )
		db.session.add(perm)

def load_events():
	"""Load one event for Carolyn's trip"""

	file = open('static/data/events.txt')

	for line in file:
		day_id, user_id, title, start, end, city = line.rstrip().split("|")

		start = datetime.strptime(start, "datetime(%Y, %m, %d)")
		end = datetime.strptime(end, "datetime(%Y, %m, %d)")
		
		event = Event(day_id=day_id,
					  user_id=user_id,
					  title=title,
					  start=start,
					  end=end,
					  city=city,
					)

		db.session.add(event)


def load_friendships():
	"""Load the friendships between Balloonicorn & Carolyn"""

	file = open('static/data/friendships.txt')

	for line in file:
		admin_id, friend_id = line.rstrip().split(",")

		friendship = Friendship(admin_id=admin_id,
								friend_id=friend_id
								)

		db.session.add(friendship)

#####################################################################
# Main Block

if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_trips()
    load_permissions()
    load_events()
    load_friendships()
    db.session.commit()
    print "Database is populated."