from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# DATABASE CONNECTION
conn = psycopg2.connect(
    host="localhost",
    database="online_bike_portal",
    user="postgres",
    password="root"
)

# ================= HOME + SEARCH =================
# @app.route("/")
# def home():

#     search = request.args.get("search")

#     cur = conn.cursor()

#     # SEARCH LOGIC
#     if search:
#         cur.execute(
#             "SELECT * FROM bikes WHERE LOWER(name) LIKE LOWER(%s)",
#             ('%' + search + '%',)
#         )
#     else:
#         cur.execute("SELECT * FROM bikes")

#     bikes = cur.fetchall()
#     cur.close()

#     return render_template("index.html", bikes=bikes)


@app.route("/")
def home():

    search = request.args.get("search")

    cur = conn.cursor()

    try:

        if search:
            cur.execute(
                "SELECT * FROM bikes WHERE bike_name ILIKE %s",
                ('%' + search + '%',)
            )
        else:
            cur.execute("SELECT * FROM bikes")

        bikes = cur.fetchall()
        cur.close()

        return render_template("index.html", bikes=bikes)

    except Exception as e:
        conn.rollback()
        print("Database Error:", e)
        bikes = []

    cur.close()

    return render_template("index.html", bikes=bikes)


# ================= REGISTER =================
@app.route("/register", methods=["POST"])
def register():

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",
        (username, email, password)
    )
    conn.commit()
    cur.close()

    return redirect("/")


# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    user = cur.fetchone()
    cur.close()

    if user:
        print("Login Successful")
    else:
        print("Invalid Login")

    return redirect("/")


# ================= OFFER PAGE =================
@app.route("/offer/<int:bike_id>")
def offer_page(bike_id):

    cur = conn.cursor()
    cur.execute("SELECT * FROM bikes WHERE id=%s", (bike_id,))
    bike = cur.fetchone()
    cur.close()

    return render_template("offer.html", bike=bike)


# ================= SUBMIT OFFER =================
@app.route("/submit_offer", methods=["POST"])
def submit_offer():

    name = request.form["name"]
    phone = request.form["phone"]
    bike_id = request.form["bike_id"]

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO offers(name,phone,bike_id) VALUES(%s,%s,%s)",
        (name, phone, bike_id)
    )
    conn.commit()
    cur.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)



try:
    cur.execute("SELECT * FROM bikes")
    bikes = cur.fetchall()

except Exception as e:
    conn.rollback()
    print(e)