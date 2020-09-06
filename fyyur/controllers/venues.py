import sys

from flask import render_template, flash, request, redirect, url_for, abort
from forms import *
from datetime import datetime
from sqlalchemy.sql import func, ClauseElement
import bleach


def get_or_create_genre(db_session, genre_model, genre_name):
    instance = db_session.query(genre_model).filter_by(name=genre_name).first()
    if instance:
        return instance

    instance = genre_model(name=genre_name)
    db_session.add(instance)
    db_session.commit()
    return instance


def make_routes(app, db, models):

    @app.route('/venues')
    def venues():
        venue_model = models['venue']
        show_model = models['show']
        results = db.session.query(
                venue_model.state.label('state'),
                venue_model.city.label('city'),
                venue_model.name.label('name'),
                venue_model.id.label('id'),
                func.count(func.coalesce(show_model.id, 0)).label('upcoming_show_count')
            ).outerjoin(show_model, venue_model.id == show_model.venue_id
            ).group_by(
                venue_model.id
            ).order_by(
                venue_model.state,
                venue_model.city,
                venue_model.id,
            ).group_by(venue_model.id).all()

        last_city_state = ''
        data = []
        city_state = {}
        for venue in results:
            if '{}, {}'.format(venue.city, venue.state) != last_city_state:
                if 'venues' in city_state:
                    data.append(city_state)
                city_state = {
                    'city': venue.city,
                    'state': venue.state,
                    'venues': [],
                }
                last_city_state = '{}, {}'.format(venue.city, venue.state)

            city_state['venues'].append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': venue.upcoming_show_count,
            })
        if 'venues' in city_state:
            data.append(city_state)
        return render_template('pages/venues.html', areas=data)

    @app.route('/venues/search', methods=['POST'])
    def search_venues():
        # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
        # search for Hop should return "The Musical Hop".
        # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
        venue_model = models['venue']
        show_model = models['show']

        results = db.session.query(
            venue_model.name.label('name'),
            venue_model.id.label('id'),
            func.count(func.coalesce(show_model.id, 0)).label('upcoming_show_count')
        ).filter(
            venue_model.name.ilike("%" + bleach.clean(request.form['search_term']) + "%")
        ).outerjoin(show_model, venue_model.id == show_model.venue_id
                    ).group_by(
            venue_model.id
        ).order_by(
            venue_model.name,
        ).group_by(venue_model.id).all()

        response = {
            "count": len(results),
            "data": [{
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": venue.upcoming_show_count
            } for venue in results]
        }
        return render_template('pages/search_venues.html', results=response,
                               search_term=request.form.get('search_term', ''))

    @app.route('/venues/<int:venue_id>')
    def show_venue(venue_id):
        data = db.session.query(models['venue']).get(venue_id).info()
        return render_template('pages/show_venue.html', venue=data)

    #  Create Venue
    #  ----------------------------------------------------------------

    @app.route('/venues/create', methods=['GET'])
    def create_venue_form():
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)

    @app.route('/venues/create', methods=['POST'])
    def create_venue_submission():
        data = request.form
        error = False
        try:
            venue = models['venue'](
                name=bleach.clean(data['name']),
                address=bleach.clean(data['address']),
                city=bleach.clean(data['city']),
                state=bleach.clean(data['state']),
                phone=bleach.clean(data['phone']),
                facebook_link=bleach.clean(data['facebook_link'])
            )
            genres = request.form.getlist('genres')
            genre_list = []
            for genre in genres:
                db_genre = get_or_create_genre(db.session, models['genre'], genre)
                if db_genre is not None:
                    genre_list.append(db_genre)
            venue.genres = genre_list
            db.session.add(venue)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        finally:
            db.session.close()

        if error:
            return render_template('pages/home.html')
        else:
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
            return render_template('pages/venues.html')

    @app.route('/venues/<venue_id>', methods=['DELETE'])
    def delete_venue(venue_id):
        # TODO: Complete this endpoint for taking a venue_id, and using
        # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

        # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
        # clicking that button delete it from the db then redirect the user to the homepage
        return None

    @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
    def edit_venue(venue_id):
        form = VenueForm()
        venue = db.session.query(models['venue']).get(venue_id)
        if venue:
            form.name.data = venue.name
            form.city.data = venue.city
            form.state.data = venue.state
            form.address.data = venue.address
            form.phone.data = venue.phone
            form.genres.data = [genre.name for genre in venue.genres]
            form.facebook_link.data = venue.facebook_link
            return render_template('forms/edit_venue.html', form=form, venue=venue)
        return render_template('errors/404.html')

    @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
    def edit_venue_submission(venue_id):
        # TODO: take values from the form submitted, and update existing
        # venue record with ID <venue_id> using the new attributes
        return redirect(url_for('show_venue', venue_id=venue_id))


