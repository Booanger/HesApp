from . import db, User, Restaurant, UserRole
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta


class UserService:
    # Authorization
    def login(email, password):
        # Authenticate the user and return access tokens or manage sessions
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"msg": "User not found"}, 404
        if not check_password_hash(user.password, password):
            return {"msg": "Bad username or password"}, 401

        access_token = create_access_token(
            identity=user.id, expires_delta=timedelta(days=365 * 100)
        )
        return {"access_token": access_token}, 200

    def register_customer(username, email, password, phone):
        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()
        if existing_user:
            return {"error": "Username or email already registered"}, 409

        customer = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method="scrypt"),
            phone=phone,
            role=UserRole.CUSTOMER,
        )
        db.session.add(customer)
        db.session.commit()

        access_token = create_access_token(identity=customer.id)

        return {
            "message": f"User {customer.username} registered successfully",
            "access_token": access_token,
        }, 200

    def register_staff(
        username,
        email,
        password,
        phone,
        restaurant_name,
        restaurant_description,
        restaurant_address,
        restaurant_phone,
        restaurant_logo,
    ):
        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()
        if existing_user:
            return {"error": "Username or email already registered"}, 409

        staff = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method="scrypt"),
            phone=phone,
            role=UserRole.STAFF,
        )
        db.session.add(staff)

        restaurant = Restaurant(
            staff_user_id=staff.id,
            name=restaurant_name,
            description=restaurant_description,
            address=restaurant_address,
            phone=restaurant_phone,
            logo=restaurant_logo,
        )
        db.session.add(restaurant)

        db.session.commit()

        access_token = create_access_token(identity=staff.id)
        return {
            "message": f"Staff {staff.username} and their restaurant {restaurant.name} registered successfully",
            "access_token": access_token,
        }, 200

    # Customer Related
    def get_customer(customer_id):
        # Retrieve customer user information
        customer = User.query.filter_by(id=customer_id, role=UserRole.CUSTOMER).first()
        if customer:
            return customer.to_dict(), 200
        return {"msg": "User not found"}, 404

    def update_customer(customer_id, data):
        # Update customer user information
        if "password" in data:
            hashed_password = generate_password_hash(data["password"], method="sha256")
            data["password"] = hashed_password

        if "username" in data:
            existing_user = User.query.filter(
                (User.username == data["username"]) & (User.id != customer_id)
            ).first()
            if existing_user:
                return {"error": "Username already exists"}, 409

        customer = User.query.filter_by(id=customer_id, role=UserRole.CUSTOMER).first()
        if customer:
            customer.username = data.get("username", customer.username)
            customer.password = data.get("password", customer.password)
            customer.phone = data.get("phone", customer.phone)
            db.session.commit()
            return {"msg": "User updated successfully"}, 200
        return {"msg": "User update failed"}, 500

    # Staff Related
    def get_staff(staff_id):
        # Retrieve staff user and related restaurant information
        staff = User.query.filter_by(id=staff_id, role=UserRole.STAFF).first()
        restaurant = Restaurant.query.filter_by(staff_user_id=staff.id).first()
        if staff and restaurant:
            staff = staff.to_dict()
            staff["restaurant_id"] = restaurant.id
            staff["restaurant_staff_user_id"] = restaurant.staff_user_id
            staff["restaurant_name"] = restaurant.name
            staff["restaurant_description"] = restaurant.description
            staff["restaurant_address"] = restaurant.address
            staff["restaurant_phone"] = restaurant.phone
            staff["restaurant_logo"] = restaurant.logo
            return staff, 200
        return {"msg": "Staff not found"}, 404

    def update_staff(staff_id, data):
        # Update staff user and related restaurant information
        if "password" in data:
            hashed_password = generate_password_hash(data["password"], method="sha256")
            data["password"] = hashed_password

        if "username" in data:
            existing_user = User.query.filter(
                (User.username == data["username"]) & (User.id != staff_id)
            ).first()
            if existing_user:
                return {"error": "Username already exists"}, 409

        staff = User.query.filter_by(id=staff_id, role=UserRole.STAFF).first()
        restaurant = Restaurant.query.filter_by(staff_user_id=staff.id).first()
        if staff and restaurant:
            staff.username = data.get("username", staff.username)
            staff.password = data.get("password", staff.password)
            staff.phone = data.get("phone", staff.phone)
            restaurant.name = data.get("restaurant_name", restaurant.name)
            restaurant.description = data.get(
                "restaurant_description", restaurant.description
            )
            restaurant.address = data.get("restaurant_address", restaurant.address)
            restaurant.phone = data.get("restaurant_phone", restaurant.phone)
            restaurant.logo = data.get("restaurant_logo", restaurant.logo)
            db.session.commit()
            return {"msg": "Staff updated successfully"}, 200
        return {"msg": "Staff update failed"}, 500

    def get_role(user_id):
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user.role
        return None
