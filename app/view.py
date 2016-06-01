'''
    Copyright (C) 2016 Lion Cui <lioncui@163.com>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

#!/usr/bin/python
#-*- coding:utf-8 -*-
from app import app
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from app import models, db
from werkzeug import secure_filename
import dbsync
from tqdm import *
import os

@app.route('/')
def index():
    try:
        redata = db.session.query(models.LOG.ip, 
                                    models.LOG.url,
                                    models.LOG.status, 
                                    models.LOG.num
                                ).all()
    except:
        redata = []
    try:
        status_code = db.session.execute("SELECT status,COUNT(status) FROM log GROUP BY status").fetchall()
        status_code = dict(status_code)
        for i in status_code:
            status_code[i.decode('utf-8')] = status_code[i]
    except:
        status_code = []
    try:
        top_access_url = []
        top_url = db.session.execute("SELECT COUNT(*), url FROM log GROUP BY url").fetchall()
        if top_url:
            top_url.sort()
            top_access_url = top_url[-5:]
    except:
        top_access_url = []

    try:
        ip_address_status = db.session.execute("SELECT status,address,COUNT(status) FROM log GROUP BY status,address").fetchall()
        address_map = {}
        if ip_address_status:
            for x in ip_address_status:
                if x[0] in address_map and x[1] != 'None':
                    address_map[x[0]][x[1]] = x[2]
                elif x[0] not in address_map and x[1] != "None":
                    address_map[x[0]] = { x[1]: x[2]}
    except:
        address_map = {}

    return render_template("index.html", 
                            redata = redata,
                            status_code = status_code, 
                            top_access_url = top_access_url,
                            address_map = address_map,
                            getsize = os.path.getsize
                            )


@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['upload']
        db.session.execute("DROP TABLE IF EXISTS log")
        db.session.commit()
        db.create_all()
        dbsync.exportmysql(f)
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404