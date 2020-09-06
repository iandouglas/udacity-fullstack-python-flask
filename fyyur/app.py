# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from controllers import base, venues, artists, shows
from dateutil import tz
from datetime import datetime
from sqlalchemy.sql import func


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# connect to a local postgresql database
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

artist_genres = db.Table('artist_genres',
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
)

venue_genres = db.Table('venue_genres',
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    genres = db.relationship('Genre', secondary=venue_genres, backref=db.backref('venues', lazy=True))
    shows = db.relationship('Show', backref='venue', lazy='dynamic')

    def __repr__(self):
        return f'Venue: id:{self.id}, {self.name}'

    def info(self):
        past_shows = self.get_shows(Show.start_time <= datetime.now())
        upcoming_shows = self.get_shows(Show.start_time > datetime.now())

        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            'past_shows': past_shows,
            'upcoming_shows': upcoming_shows,
            'past_shows_count': len(past_shows),
            'upcoming_shows_count': len(upcoming_shows)
        }

    def get_shows(self, comparison):
        results = []

        for show in db.session.query(
                Show.artist_id.label('artist_id'),
                Artist.name.label('artist_name'),
                Artist.image_link.label('artist_image_link'),
                func.to_char(Show.start_time, 'YYYY-MM-DD HH24:MI:SS').label('start_time')
            ).filter(
                Show.artist_id == Artist.id,
                Show.venue_id == self.id
            ).filter(
                comparison
            ).all():

            results.append({
                'artist_id': show.artist_id,
                'artist_name': show.artist_name,
                'artist_image_link': show.artist_image_link,
                'start_time': show.start_time
            })
        return results


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    genres = db.relationship('Genre', secondary=artist_genres, backref=db.backref('genres', lazy=True))
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return f'Artist: id:{self.id}, {self.name}'

    def info(self):
        past_shows = self.get_shows(Show.start_time <= datetime.now())
        upcoming_shows = self.get_shows(Show.start_time > datetime.now())

        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            'past_shows': past_shows,
            'upcoming_shows': upcoming_shows,
            'past_shows_count': len(past_shows),
            'upcoming_shows_count': len(upcoming_shows)
        }

    def get_shows(self, comparison):
        results = []

        for show in db.session.query(
                Show.venue_id.label('venue_id'),
                Venue.name.label('venue_name'),
                Venue.image_link.label('venue_image_link'),
                func.to_char(Show.start_time, 'YYYY-MM-DD HH24:MI:SS').label('start_time')
            ).filter(
                Show.artist_id == self.id,
                Show.venue_id == Venue.id
            ).filter(
                comparison
            ).all():

            results.append({
                'venue_id': show.venue_id,
                'venue_name': show.venue_name,
                'venue_image_link': show.venue_image_link,
                'start_time': show.start_time
            })
        return results


# Implement Show and Genre models, and complete all model relationships and properties, as a database migration.
class Genre(db.Model):
    __tablename__ = 'Genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)

    def __repr__(self):
        return f'{self.name}'


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

    def __repr__(self):
        return f'Show: id:{self.id}, {self.start_time}, {self.venue.name}, {self.artist.name}'

    def venue_info(self):
        show_venue = self.venue
        return {
            'venue_id': show_venue.id,
            'venue_name': show_venue.name,
            'venue_image_link': show_venue.image_link,
            'start_time': self.start_time
        }
# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en_US')


app.jinja_env.filters['datetime'] = format_datetime

models = {
    'artist': Artist,
    'venue': Venue,
    'show': Show,
    'genre': Genre,
    'venue_genres': venue_genres
}
# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#
base.make_routes(app)

#  Venues
#  ----------------------------------------------------------------
venues.make_routes(app, db, models)

#  Artists
#  ----------------------------------------------------------------
artists.make_routes(app, db, models)

#  Shows
#  ----------------------------------------------------------------
shows.make_routes(app, db, models)


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
