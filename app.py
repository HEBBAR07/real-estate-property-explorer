from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# =========================
# MONGODB CONNECTION
# =========================

client = MongoClient("mongodb://localhost:27017/")

db = client["real_estate"]

properties = db["properties"]
users = db["users"]
favorites = db["favorites"]


# =========================
# ADD SAMPLE PROPERTIES
# =========================

def add_sample_properties():

    # Check whether Mysore properties already exist
    mysore_exists = properties.find_one({
        "location": {
            "$regex": "^Mysore$",
            "$options": "i"
        }
    })

    # Check whether Mangalore properties already exist
    mangalore_exists = properties.find_one({
        "location": {
            "$regex": "^Mangalore$",
            "$options": "i"
        }
    })

    # Add Mysore properties
    if not mysore_exists:

        properties.insert_many([
            {
                "title": "Beautiful Mysore House",
                "location": "Mysore",
                "type": "House",
                "price": 4500000,
                "image": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=900&q=80"
            },
            {
                "title": "Modern Mysore Villa",
                "location": "Mysore",
                "type": "Villa",
                "price": 8500000,
                "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=900&q=80"
            }
        ])

    # Add Mangalore properties
    if not mangalore_exists:

        properties.insert_many([
            {
                "title": "Mangalore Beach House",
                "location": "Mangalore",
                "type": "House",
                "price": 5500000,
                "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=900&q=80"
            },
            {
                "title": "Mangalore Modern Apartment",
                "location": "Mangalore",
                "type": "Apartment",
                "price": 6500000,
                "image": "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=900&q=80"
            }
        ])


# Run sample data function
add_sample_properties()


# =========================
# HOME PAGE + SEARCH
# =========================

@app.route("/")
def home():

    location = request.args.get("location", "").strip()
    property_type = request.args.get("type", "").strip()
    max_price = request.args.get("price", "").strip()

    query = {}

    # LOCATION
    if location:
        query["location"] = {
            "$regex": f"^{location}$",
            "$options": "i"
        }

    # PROPERTY TYPE
    if property_type:
        query["type"] = {
            "$regex": f"^{property_type}$",
            "$options": "i"
        }

    # PRICE
    if max_price:
        try:
            query["price"] = {
                "$lte": float(max_price)
            }
        except ValueError:
            pass

    # GET PROPERTIES
    properties_list = list(properties.find(query))

    return render_template(
        "index.html",
        properties=properties_list
    )


# =========================
# ADD PROPERTY
# =========================

@app.route("/add-property", methods=["GET", "POST"])
def add_property():

    if request.method == "POST":

        title = request.form.get("title")
        location = request.form.get("location")
        property_type = request.form.get("type")
        price = request.form.get("price")
        image = request.form.get("image")

        try:
            price = float(price)
        except:
            price = 0

        properties.insert_one({
            "title": title,
            "location": location,
            "type": property_type,
            "price": price,
            "image": image
        })

        return redirect(url_for("home"))

    return render_template("add_property.html")


# =========================
# VIEW PROPERTY
# =========================

@app.route("/property/<property_id>")
def view_property(property_id):

    property_data = properties.find_one({
        "_id": ObjectId(property_id)
    })

    if not property_data:
        return "Property not found"

    return render_template(
        "property.html",
        property=property_data
    )


# =========================
# EDIT PROPERTY
# =========================

@app.route("/edit-property/<property_id>", methods=["GET", "POST"])
def edit_property(property_id):

    property_data = properties.find_one({
        "_id": ObjectId(property_id)
    })

    if not property_data:
        return "Property not found"

    if request.method == "POST":

        title = request.form.get("title")
        location = request.form.get("location")
        property_type = request.form.get("type")
        price = request.form.get("price")
        image = request.form.get("image")

        try:
            price = float(price)
        except:
            price = 0

        properties.update_one(
            {"_id": ObjectId(property_id)},
            {
                "$set": {
                    "title": title,
                    "location": location,
                    "type": property_type,
                    "price": price,
                    "image": image
                }
            }
        )

        return redirect(url_for("home"))

    return render_template(
        "edit_property.html",
        property=property_data
    )


# =========================
# DELETE PROPERTY
# =========================

@app.route("/delete-property/<property_id>")
def delete_property(property_id):

    properties.delete_one({
        "_id": ObjectId(property_id)
    })

    return redirect(url_for("home"))


# =========================
# FAVORITE PROPERTY
# =========================

@app.route("/favorite/<property_id>")
def favorite_property(property_id):

    property_data = properties.find_one({
        "_id": ObjectId(property_id)
    })

    if property_data:

        favorites.insert_one({
            "property_id": property_data["_id"],
            "title": property_data.get("title"),
            "location": property_data.get("location"),
            "price": property_data.get("price"),
            "image": property_data.get("image")
        })

    return redirect(url_for("home"))


# =========================
# FAVORITES
# =========================

@app.route("/favorites")
def favorites_page():

    favorite_list = list(favorites.find())

    return render_template(
        "favorites.html",
        favorites=favorite_list
    )


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = users.find_one({
            "email": email,
            "password": password
        })

        if user:
            return redirect(url_for("home"))

        return "Invalid email or password"

    return render_template("login.html")


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = users.find_one({
            "email": email
        })

        if existing_user:
            return "User already exists"

        users.insert_one({
            "name": name,
            "email": email,
            "password": password
        })

        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":
    app.run(debug=True)