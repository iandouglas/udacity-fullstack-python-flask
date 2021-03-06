import sys

from flask import render_template, flash, request, redirect, url_for, abort, jsonify
from forms import *
from sqlalchemy.sql import func
import bleach

from .utils import entity_search, add_or_get_genre_objects


def make_routes(app, db, models):

    @app.route('/venues')
    def venues():
        """
        venue "index" page data
        this method is much bigger than I'd otherwise like; given the freedom to do so, I'd probably
        look for a way to reduce the dictionary that gets built at the end
        """
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
                venue_model.name,
            ).all()

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
        """
        venue search implementation
        """
        response = entity_search(
            db.session,
            models['venue'],
            models['show'],
            bleach.clean(request.form['search_term'])
        )

        return render_template('pages/search_venues.html', results=response,
                               search_term=request.form.get('search_term', ''))

    @app.route('/venues/<int:venue_id>')
    def show_venue(venue_id):
        """
        venue "show" page
        """
        data = db.session.query(models['venue']).get(venue_id).info()
        return render_template('pages/show_venue.html', venue=data)

    @app.route('/venues/create', methods=['GET'])
    def create_venue_form():
        """
        set up the form for creating a new venue
        """
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)

    @app.route('/venues/create', methods=['POST'])
    def create_venue_submission():
        """
        process form submission for creating a new venue
        """
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

            genre_list = add_or_get_genre_objects(
                db.session,
                models['genre'],
                request.form.getlist('genres')
            )
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
            return redirect(url_for('venues'))

    @app.route('/venues/<venue_id>', methods=['DELETE'])
    def delete_venue(venue_id):
        """
        this was fun to build; I used a bit of JavaScript to do a delete fetch
        call to this endpoint and send back a true/false for success
        """
        venue = None
        try:
            venue = db.session.query(models['venue']).get(venue_id)
            venue.genres = []
            db.session.commit()
            models['venue'].query.filter_by(id=venue_id).delete()
            db.session.commit()
            flash('Venue successfully deleted.')
        except:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Venue not deleted.')
            if venue:
                return jsonify({'success': False})
        finally:
            db.session.close()
        return jsonify({'success': True})


    @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
    def edit_venue(venue_id):
        """
        set up the form to prepare to edit a venue
        """
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
        """
        process the form submission for editing a venue
        """
        data = request.form
        try:
            venue = models['venue'].query.get(venue_id)
            venue.name = bleach.clean(data['name'])
            venue.address = bleach.clean(data['address'])
            venue.city = bleach.clean(data['city'])
            venue.state = bleach.clean(data['state'])
            venue.phone = bleach.clean(data['phone'])
            venue.facebook_link = bleach.clean(data['facebook_link'])

            # reset genres here
            venue.genres = [] # delete all previous genres
            db.session.commit()
            venue.genres = add_or_get_genre_objects(
                db.session,
                models['genre'],
                request.form.getlist('genres')
            ) # and rebuild a new list of genres
            db.session.commit()
        except:
            db.session.rollback()
            flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
            print(sys.exc_info())
            return redirect(url_for('edit_venue', venue_id=venue_id))
        finally:
            db.session.close()
        flash('Venue successfully updated.')
        return redirect(url_for('show_venue', venue_id=venue_id))
