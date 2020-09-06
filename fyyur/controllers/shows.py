import sys

import bleach
from flask import render_template, flash, request, url_for, redirect
from sqlalchemy import String, cast

from forms import *
from sqlalchemy.sql import func


def make_routes(app, db, models):
    @app.route('/shows')
    def shows():
        show_model = models['show']
        venue_model = models['venue']
        artist_model = models['artist']
        data = db.session.query(
                func.to_char(show_model.start_time, 'YYYY-MM-DD HH24:MI:SS').label('start_time'),
                venue_model.id.label('venue_id'),
                venue_model.name.label('venue_name'),
                artist_model.id.label('artist_id'),
                artist_model.name.label('artist_name'),
                artist_model.image_link.label('artist_image_link')
            ).filter(
                show_model.artist_id == artist_model.id,
                show_model.venue_id == venue_model.id
            ).order_by(show_model.start_time).all()
        return render_template('pages/shows.html', shows=data)

    @app.route('/shows/search', methods=['POST'])
    def search_shows():
        search_term = bleach.clean(request.form['search_term'])

        show_model = models['show']
        artist_model = models['artist']
        venue_model = models['venue']

        shows = db.session.query(
            artist_model.id.label('artist_id'),
            artist_model.name.label('artist_name'),
            artist_model.image_link.label('artist_image_link'),
            venue_model.id.label('venue_id'),
            venue_model.name.label('venue_name'),
            show_model.start_time.label('start_time'),
        ).filter(
            cast(show_model.start_time, String).ilike("%" + search_term + "%")
        ).join(
            artist_model,
            artist_model.id == show_model.artist_id
        ).join(
            venue_model,
            venue_model.id == show_model.artist_id
        ).order_by(
            show_model.start_time,
        ).all()

        results = {
            "count": len(shows),
            "data": shows
        }

        return render_template('pages/search_shows.html', results=results,
                               search_term=request.form.get('search_term', ''))

    @app.route('/shows/create')
    def create_shows():
        # renders form. do not touch.
        artist_model = models['artist']
        venue_model = models['venue']
        form = ShowForm()
        form.artist.choices = [(a.id, a.name) for a in artist_model.query.order_by(artist_model.name)]
        form.venue.choices = [(v.id, v.name) for v in venue_model.query.order_by(venue_model.name)]
        return render_template('forms/new_show.html', form=form)

    @app.route('/shows/create', methods=['POST'])
    def create_show_submission():
        try:
            artist = db.session.query(models['artist']).get(bleach.clean(request.form['artist']))
            venue = db.session.query(models['venue']).get(bleach.clean(request.form['venue']))
            show = models['show'](
                start_time=bleach.clean(request.form['start_time']),
                venue_id=venue.id,
                artist_id=artist.id
            )
            db.session.add(show)
            db.session.commit()
            flash('Show was successfully listed!')
        except:
            db.session.rollback()
            flash('An error occurred. Show could not be listed.')
            print(sys.exc_info())
            return redirect(url_for('create_shows'))
        finally:
            db.session.close()
        return redirect(url_for('shows'))

