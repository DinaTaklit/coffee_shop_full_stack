import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS


from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    @TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    #db_drop_and_create_all()

    ## ROUTES
    '''
    @Done implement endpoint
        GET /drinks
            it should be a public endpoint
            it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks')
    def get_drinks(): 
        data = Drink.query.all()  
        drinks = list(map(Drink.short, data))
        if drinks is None or len(drinks)==0: 
            abort(404)                 
        return jsonify({
            'success': True,
            'drinks':drinks 
        }) 

    '''
    @Done implement endpoint
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    ''' 
    @app.route('/drinks-detail')
    @requires_auth(permission='get:drinks-detail')#require the 'get:drinks-detail' permission
    def get_drinks_detail(payload):
        drinks_query = Drink.query.all()  
        drinks = list(map(Drink.long, drinks_query))
        if drinks is None or len(drinks)==0: 
            abort(404)                 
        return jsonify({
            'success': True,
            'drinks':drinks 
        }) 


    '''
    @TODO implement endpoint
        POST /drinks
            it should create a new row in the drinks table
            it should require the 'post:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
            or appropriate status code indicating reason for failure
    '''




    '''
    @TODO implement endpoint
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''


    '''
    @TODO implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''


    ## Error Handling
    '''
    @Done implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''

    '''
    @Done implement error handler for 404
        error handler should conform to general task above 
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success":False,
            "error":404,
            "message":"resource not found"
        }),404
        
    '''
    @Done implement error handler for 400
        error handler should conform to general task above 
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success":False,
            "error":400,
            "message": "bad request"
        }),400

    '''
    @Done implement error handler for 405
    '''
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success":False,
            "error":405,
            "message":"method not allowed"
        }),405

    '''
    @Done implement error handler for 422
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
        }), 422


    '''
    @Done implement error handler for AuthError
        error handler should conform to general task above 
    '''
    
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False, 
            "error": error.status_code,
            "code":error.error['code'],
            "message": error.error['description']
        }), error.status_code
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)   