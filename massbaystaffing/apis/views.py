# massbaystaffing/apis/views.py
from flask import render_template, url_for, redirect, flash, jsonify, request, Blueprint
from massbaystaffing import db
from flask_login import current_user, login_user, logout_user, login_required

import requests
import time


@app.route('/api/retrieve', methods=['GET', 'POST'])
def retrieve():
    # try:
    jobtitle = request.headers.get('jobtitle')
    company = request.headers.get('company')
    city = request.headers.get('city')
    state = request.headers.get('state')
    zip = request.headers.get('zip')
    descr = request.headers.get('descr')
    jstatus = request.headers.get('jstatus')
    link = request.headers.get('link')
    duties = request.headers.get('duties')
    requi = request.headers.get('requi')
    post_date = request.headers.get('post_date')

    if jobtitle and company:
        results = Job.query.filter_by(jobtitle=jobtitle, company=company).all()
    elif not company and jobtitle:
        results = Job.query.filter_by(jobtitle=jobtitle).all()
    elif not jobtitle and company:
        results = Job.query.filter_by(company=company).all()
    elif not jobtitle and not company:
        results = Job.query.all()
    else:
        return jsonify({ 'error#304': 'Required params not included' })

    if not results:
        return jsonify({ 'success': 'No job matching that description.' })

    # remember that results is a list of db.Model objects
    parties = []

    for job in results:
        party = {
            'id': job.id,
            'jobtitle': job.jobtitle,
            'company': job.company,
            'city': job.city,
            'state': job.state,
            'zip': job.zip,
            'descr': job.descr,
            'jstatus': job.jstatus,
            'link': job.link,
            'duties': job.duties,
            'requi': job.requi,
            'post_date': job.post_date
        }

        parties.append(party)

    return jsonify(parties)

    # except:
    #     return jsonify({ 'error#305': 'something went wrong' })




# API call return posts for username
@app.route('/api/posts', methods=['GET', 'POST'])
def posts():
    username = request.headers.get('username')

    user  = User.query.filter_by(username=username).first()

    customers = [
        {
            'name': 'John',
            'age': 22
        },
        {
            'name': 'Alex',
            'age': 12
        },
        {
            'name': 'Annie',
            'age': 67
        },
        {
            'name': 'Jake',
            'age': 45
        },
        {
            'name': 'Bill',
            'age': 32
        },
    ]

    try:
        posts = []

        for post in posts:
            if customer['age'] < int(max) and customer['age'] > int(min):
                range.append(customer)

        if name:
            customers = []
            for customer in range:
                if customer['name'] == name:
                    customers.append(customer)
            return jsonify(customers)

        return jsonify(range)
    except:
        return jsonify({ 'error': 'Incompatible parameter values'})


    return jsonify({ 'error': 'Something went wrong' })
