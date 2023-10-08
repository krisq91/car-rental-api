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

    def put(self, user_id):
        """
               Update user information by user ID.

               URL: /user/update/<user_id>
               Method: PUT
               Description: Update user information by user ID.
               URL Parameters:
                   - user_id (int): The ID of the user to update.
               Request Body:
                   - name (str): The updated user's name.
                   - phoneNo (str): The updated user's phone number.
                   - address (str): The updated user's address.
                   - email (str): The updated user's email address.
                   - idProof (str): The updated user's ID proof (base64-encoded).
                   - drivingLicenceNo (str): The updated user's driving license number.
               Returns:
                   JSON: A message indicating the success or failure of the operation.
        """
        try:
            # Retrieve user data from the request JSON
            data = request.get_json()
            updated_name = data.get('name')
            updated_phone_no = data.get('phoneNo')
            updated_address = data.get('address')
            updated_email = data.get('email')
            updated_id_proof = data.get('idProof')
            updated_driving_licence_no = data.get('drivingLicenceNo')

            # Check if the user with the specified user_id exists
            select_query = f"SELECT * FROM User WHERE Id = {user_id}"
            existing_user = execute_select_query(select_query)

            if not existing_user:
                return jsonify({'message': 'User not found'}), 404

            # Define the UPDATE query to update the user data
            update_query = """
                UPDATE User
                SET name = %s, phoneNo = %s, address = %s, email = %s,
                    idProof = %s, drivingLicenceNo = %s
                WHERE Id = %s
            """

            # Execute the UPDATE query with the updated user data and user_id
            execute_update_query(update_query, (
                updated_name, updated_phone_no, updated_address, updated_email,
                updated_id_proof, updated_driving_licence_no, user_id
            ))

            return jsonify({'message': 'User updated successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500

    def delete(self, user_id):
        """
                Delete a user by user ID.

                URL: /user/delete/<user_id>
                Method: DELETE
                Description: Delete a user by user ID.
                URL Parameters:
                    - user_id (int): The ID of the user to delete.
                Returns:
                    JSON: A message indicating the success or failure of the operation.
        """
        try:
            # Check if the user with the specified user_id exists
            select_query = f"SELECT * FROM User WHERE Id = {user_id}"
            existing_user = execute_select_query(select_query)

            if not existing_user:
                return jsonify({'message': 'User not found'}), 404

            # Define the DELETE query to delete the user by user_id
            delete_query = "DELETE FROM User WHERE Id = %s"

            # Execute the DELETE query with the user_id
            execute_delete_query(delete_query, (user_id,))

            return jsonify({'message': 'User deleted successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Failed to delete user', 'error': str(e)}), 500