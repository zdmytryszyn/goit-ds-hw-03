import argparse

from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://zoreslavd:<my_password>@mycluster.bnmc1.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster",
    server_api=ServerApi('1')
)

db = client.test

parser = argparse.ArgumentParser("Cats DB management")
parser.add_argument("--action",
                    help="create, find_all, find_by_name, update_name, \
                    update_feature, delete_by_name, delete_all, new_feature"
                    )
parser.add_argument("--id")
parser.add_argument("--name")
parser.add_argument("--age")
parser.add_argument("--features", nargs="+")
parser.add_argument("--new_feature")

args = vars(parser.parse_args())

action = args.get("action")
pk = args.get("id")
name = args.get("name")
age = args.get("age")
features = args.get("features")
new_feature = args.get("new_feature")


def create(name, age, features):
    if not name or not age or not features:
        raise ValueError("Name, age, and features are required for creating a new cat.")
    return db.cats.insert_one(
        {
            "name": name,
            "age": age,
            "features": features,
        }
    )


def read_all():
    result = db.cats.find({})
    if not list(result):
        raise NameError(f"No cats found in database!")
    return result


def read_by_name(name):
    result = db.cats.find_one({"name": name})
    if not result:
        raise NameError(f"No cat with name {name} found")
    return result


def update_age_by_name(name, age):
    db.cats.update_one(read_by_name(name), {"$set": {"age": int(age)}})


def update_new_feature(name, new_feature):
    if not new_feature:
        raise NameError("No new feature provided!")
    db.cats.update_one(read_by_name(name), {"$push": {"features": new_feature}})


def delete_by_name(name):
    if not db.cats.find_one({"name": name}):
        raise NameError("Can't delete, no such cat in DB!")
    db.cats.delete_one({"name": name})


def delete_all():
    db.cats.delete_many({})


def main():
    match action:
        case "create":
            new_cat = create(name, age, features)
            print(f"New cat created: {new_cat}")
        case "find_all":
            all_cats = read_all()
            print(f"All cats in DB: {[cat for cat in all_cats]}")
        case "find_by_name":
            one_cat = read_by_name(name)
            print(f"Cat with name {name}: {one_cat}")
        case "update_name":
            update_age_by_name(name, age)
            print(f"Updated cat: {name}, with age {age}")
        case "update_feature":
            update_new_feature(name, new_feature)
            print(f"Updated cat: {name}, with added feature '{new_feature}'")
        case "delete_by_name":
            delete_by_name(name)
            print(f"Cat {name} was deleted")
        case "delete_all":
            delete_all()
            print("All cats were deleted")
        case _:
            print("Unknown command")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
