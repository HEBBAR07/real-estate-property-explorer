from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["real_estate"]
properties = db["properties"]

# Remove old Mysore and Mangalore sample properties
properties.delete_many({
    "location": {
        "$regex": "Mysore|Mangalore",
        "$options": "i"
    }
})

property_list = [

    # MYSORE
    {
        "title": "Luxury Villa",
        "location": "Mysore",
        "price": 7500000,
        "type": "Villa",
        "bedrooms": 4,
        "bathrooms": 3,
        "area": 2400,
        "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Modern Apartment",
        "location": "Mysore",
        "price": 4200000,
        "type": "Apartment",
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 1200,
        "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Family House",
        "location": "Mysore",
        "price": 5800000,
        "type": "House",
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 1800,
        "image": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Premium Apartment",
        "location": "Mysore",
        "price": 5000000,
        "type": "Apartment",
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 1500,
        "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Green Villa",
        "location": "Mysore",
        "price": 6800000,
        "type": "Villa",
        "bedrooms": 3,
        "bathrooms": 3,
        "area": 2100,
        "image": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=800&q=80"
    },

    # MANGALORE
    {
        "title": "Sea View Apartment",
        "location": "Mangalore",
        "price": 5200000,
        "type": "Apartment",
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 1500,
        "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Luxury Villa",
        "location": "Mangalore",
        "price": 7800000,
        "type": "Villa",
        "bedrooms": 4,
        "bathrooms": 3,
        "area": 2500,
        "image": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Modern House",
        "location": "Mangalore",
        "price": 6200000,
        "type": "House",
        "bedrooms": 3,
        "bathrooms": 3,
        "area": 1900,
        "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Affordable Apartment",
        "location": "Mangalore",
        "price": 3800000,
        "type": "Apartment",
        "bedrooms": 2,
        "bathrooms": 2,
        "area": 1100,
        "image": "https://images.unsplash.com/photo-1554995207-c18c203602cb?auto=format&fit=crop&w=800&q=80"
    },
    {
        "title": "Beachside Villa",
        "location": "Mangalore",
        "price": 9000000,
        "type": "Villa",
        "bedrooms": 4,
        "bathrooms": 4,
        "area": 2800,
        "image": "https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=800&q=80"
    }
]

result = properties.insert_many(property_list)

print("================================")
print("Properties added successfully!")
print("Mysore properties: 5")
print("Mangalore properties: 5")
print("Total added:", len(result.inserted_ids))
print("================================")