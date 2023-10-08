import base64

from flask import request, jsonify
from flask.views import MethodView
from ..database.db import execute_insert_query, email_exists, execute_select_query, execute_update_query, execute_delete_query


class UserAPI(MethodView):
    def post(self):
        """
        Create a new user.

        URL: /user/create
        Method: POST
        Description: Create a new user in the system.
        Request Body:
            - name (str): The user's name.
            - phoneNo (str): The user's phone number.
            - address (str): The user's address.
            - email (str): The user's email address.
            - idProof (str): The user's ID proof (base64-encoded).
            - drivingLicenceNo (str): The user's driving license number.
        Returns:
            JSON: A message indicating the success or failure of the operation.
        """
        # Retrieve user data from the request
        data = request.get_json()
        name = data.get('name')
        phone_no = data.get('phoneNo')
        address = data.get('address')
        email = data.get('email')
        id_proof = data.get('idProof')
        driving_licence_no = data.get('drivingLicenceNo')
        if email_exists(email):
            return {"Message": "Email Id already exists!"}, 500
        insert_query = "INSERT INTO User (name, phoneNo, address, email," \
                       "idProof, drivingLicenceNo)VALUES (%s, %s, %s, %s, %s,%s)"

        execute_insert_query(insert_query, (name, phone_no, address, email, id_proof, driving_licence_no))
        return {"Message": "User Created Successfully!"}, 200

    def get(self, user_id):
        """
               Retrieve user data by user ID.

               URL: /user/get/<user_id>
               Method: GET
               Description: Retrieve user information by user ID.
               URL Parameters:
                   - user_id (int): The ID of the user to retrieve.
               Returns:
                   JSON: User data including ID, name, phone number, address, email, ID proof, and driving license number.
        """
        try:
            # Define the SQL query to fetch user data by user_id
            query = f"SELECT * FROM User WHERE Id = {user_id}"

            # Execute the SQL query to fetch the user data
            result = execute_select_query(query)

            # Check if a user was found
            if result:
                # Assuming the query returns a single user, unpack the result
                result = result[0]

                user_data = {
                    'id': result[0],
                    'name': result[1],
                    'phoneNo': result[2],
                    'address': result[3],
                    'email': result[4],
                    'idProof':  base64.b64encode(result[5]).decode('utf-8'),
                    'drivingLicenceNo': result[6]
                }
                return jsonify(user_data), 200
            else:
                return jsonify({'message': 'User not found'}), 404
        except Exception as e:
            return jsonify({'message': 'Failed to retrieve user', 'error': str(e)}), 500
