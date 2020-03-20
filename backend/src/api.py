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
    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def post_drink(payload):
        body = request.get_json()
        if body is None: 
            abort(404)
        title = body.get('title', None)
        recipe = body.get('recipe', None)   
        
        duplicate = Drink.query.filter(Drink.title == title).one_or_none() # verify id there is no duplicate
        if duplicate != None:
            abort(400)
        if type(recipe) is not list: # if the reciepe has not been inputed as a list 
            recipe = [recipe]    
        try:
            new_drink = Drink(title=title, recipe=json.dumps(recipe))
            new_drink.insert()                                                
            return jsonify({
                'success': True,
                'drinks': [new_drink.long()]
            })
        except Exception as error: 
            abort(422)
        
        


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

    @app.route('/drinks/<int:drink_id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def update_drink(payload, drink_id):
        try: 
            drink = Drink.query.filter(Drink.id == drink_id).one_or_none() # get the element with given id
            if drink is None: 
                abort(404)
            body = request.get_json() # get the body
            
            if body is None: 
                abort(404) 
                
            updated_title = body.get('title', None)
            updated_recipe = body.get('recipe', None)   
                        
            if updated_title is not None:
                drink.title = updated_title
            
            if updated_recipe != None: 
                if type(updated_recipe) is not list: # if the recipe is not a list transform it as a list
                    updated_recipe = [updated_recipe] 
                     
                drink.recipe = json.dumps(updated_recipe) #update drink.recipe with given value

            drink.update() #update the record
            return jsonify({
                'success':True,
                'drinks':[drink.long()]
            })
        except:
            abort(422)
            

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